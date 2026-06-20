# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Custom trace generator for the expense-approval workflow.

Why not just `agents-cli eval generate`? That command drives a normal
chat agent: send a prompt, capture the single response, done. Our graph
is not a chat agent - `human_approval` deliberately pauses the run with a
`RequestInput` interrupt (see expense_agent/agent.py) and waits for a
second call carrying the human's decision. `eval generate` has no
built-in way to detect that pause and answer it, so this script drives
the graph directly with ADK's `Runner` and answers each pause itself,
using the `expected_outcome.human_decision` recorded in
`datasets/basic-dataset.json` to decide approve/reject - the same
"automated reviewer" idea used for the Pub/Sub tests in Section 8, just
wired into the eval loop instead of a terminal.

Output: `artifacts/traces/generated_traces.json`, in the multi-turn
`agent_data.turns` trace shape `agents-cli eval grade` expects (see
references/dataset_schema.md in the google-agents-cli-eval skill).
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# Lets this script import `expense_agent` when run directly
# (`uv run python tests/eval/generate_traces.py`) instead of via pytest,
# which already adds the project root via `pythonpath = "."` in
# pyproject.toml.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from google.adk.cli.utils.envs import load_dotenv_for_agent  # noqa: E402

# These three helpers live in ADK's private workflow-utils module, not in
# the public `google.adk.events` package - confirmed by grepping the
# installed library, since `from google.adk.events.request_input import
# create_request_input_response` raises ImportError (that module only
# defines the `RequestInput` *class*, not these HITL-response helpers).
from google.adk.workflow.utils._workflow_hitl_utils import (  # noqa: E402
    create_request_input_response,
    get_request_input_interrupt_ids,
    has_request_input_function_call,
)
from google.adk.runners import Runner  # noqa: E402
from google.adk.sessions import InMemorySessionService  # noqa: E402
from google.genai import types  # noqa: E402

# `adk web` / `adk run` load the agent's .env for you; a bare script
# doesn't get that for free, so we call ADK's own loader explicitly -
# same fix as the GOOGLE_API_KEY / Vertex auth note in agent.py.
load_dotenv_for_agent(agent_name="expense_agent", agent_parent_folder=str(PROJECT_ROOT))

from expense_agent.agent import app  # noqa: E402

DATASET_PATH = Path(__file__).resolve().parent / "datasets" / "basic-dataset.json"
OUTPUT_PATH = PROJECT_ROOT / "artifacts" / "traces" / "generated_traces.json"


def _event_author(event: Any) -> str:
    """Recovers the *real* node that produced an event.

    `event.author` is NOT reliable for this: ADK's `Workflow._run_impl`
    does `ctx.event_author = self.name` once, and every child `Context`
    (including plain `@node` functions like `parse_expense` and
    `security_screen`) inherits that value - so `event.author` collapses
    to the generic workflow name (`"expense_approval_workflow"`) for all
    of them, while only `LlmAgent`-backed nodes (`review_agent`) keep
    their own name. Confirmed by reading `_node_runner.py`'s
    `_enrich_event` and `agents/context.py`'s `event_author` property.

    `event.node_info.path`, however, is stamped unconditionally with the
    *real* node path (e.g. "expense_approval_workflow@1/security_screen@1"),
    regardless of any `event_author` override. We take the last segment
    and strip the "@run_id" suffix to get the clean node name.
    """
    node_info = getattr(event, "node_info", None)
    path = getattr(node_info, "path", None) if node_info is not None else None
    if path:
        return path.split("/")[-1].split("@")[0]
    return event.author or "expense_agent"


def _event_to_agent_event(event: Any) -> dict[str, Any]:
    """Converts one ADK `Event` into the trace schema's `AgentEvent` shape.

    Chat-model events already carry a `Content` (role + parts) we can
    reuse as-is. Our plain `@node` functions instead return
    `Event(output=...)` - a Python dict, not a `Content` - so for those
    we serialize `output` as text ourselves. Either way the grading LLM
    gets something readable in `agent_data`.
    """
    if event.content is not None:
        content = event.content.model_dump(exclude_none=True, mode="json")
    else:
        content = {
            "role": "model",
            "parts": [{"text": json.dumps(event.output, default=str, ensure_ascii=False)}],
        }
    return {"author": _event_author(event), "content": content}


async def _run_case(case: dict[str, Any]) -> dict[str, Any]:
    """Runs one dataset case through the real graph and records every turn."""
    case_id = case["eval_case_id"]
    user_text = case["prompt"]["parts"][0]["text"]
    human_decision = (case.get("expected_outcome") or {}).get("human_decision")

    # A fresh in-memory session per case keeps cases fully independent -
    # no state leaks between, say, the clean case and the injection case.
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=app.name, user_id=case_id, session_id=case_id)
    runner = Runner(app=app, session_service=session_service)

    turns: list[dict[str, Any]] = []

    # --- Turn 0: submit the expense ---------------------------------
    turn0_events = [{"author": "user", "content": {"role": "user", "parts": [{"text": user_text}]}}]
    interrupt_id: str | None = None
    async for event in runner.run_async(
        user_id=case_id,
        session_id=case_id,
        new_message=types.Content(role="user", parts=[types.Part(text=user_text)]),
    ):
        turn0_events.append(_event_to_agent_event(event))
        if has_request_input_function_call(event):
            ids = get_request_input_interrupt_ids(event)
            interrupt_id = ids[0] if ids else None
    turns.append({"turn_index": 0, "events": turn0_events})

    # --- Turn 1 (only if the graph paused for a human) --------------
    # Cases under the auto-approve threshold never reach human_approval,
    # so interrupt_id stays None and there's nothing to resume.
    if interrupt_id is not None:
        approved = human_decision == "approve"
        decision_response = {
            "approved": approved,
            "approver": "eval-harness (automated)",
            "comment": (
                f"Automated {'approval' if approved else 'rejection'} "
                f"for eval case '{case_id}'."
            ),
        }
        resume_part = create_request_input_response(interrupt_id, decision_response)
        turn1_events = [
            {
                "author": "user",
                "content": {
                    "role": "user",
                    "parts": [resume_part.model_dump(exclude_none=True, mode="json")],
                },
            }
        ]
        async for event in runner.run_async(
            user_id=case_id,
            session_id=case_id,
            new_message=types.Content(role="user", parts=[resume_part]),
        ):
            turn1_events.append(_event_to_agent_event(event))
        turns.append({"turn_index": 1, "events": turn1_events})

    return {
        "eval_case_id": case_id,
        "agent_data": {
            "agents": {
                "expense_agent": {
                    "agent_id": "expense_agent",
                    "agent_type": "Workflow",
                }
            },
            "turns": turns,
        },
    }


async def main() -> None:
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    traces = []
    for case in dataset["eval_cases"]:
        print(f"Generating trace for '{case['eval_case_id']}'...")
        traces.append(await _run_case(case))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps({"eval_cases": traces}, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(traces)} traces to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
