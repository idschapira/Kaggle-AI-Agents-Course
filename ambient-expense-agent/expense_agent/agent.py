# ruff: noqa
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

"""Ambient expense-approval agent (ADK 2.0 Workflow graph API).

Graph::

    START -> parse_expense --"auto_approve"--> auto_approve -----+
                            \\                                    |
                             \\--"needs_review"--> review_agent --+--> human_approval --> record_outcome
                                                                                            ^
                                                                   auto_approve ------------+

- parse_expense reads the raw event, extracts the expense, and decides the
  route in plain Python (amount < AUTO_APPROVE_THRESHOLD_USD or not).
- auto_approve handles the cheap path. No LLM call.
- review_agent (an LlmAgent) is the ONLY place the model is used: it judges
  risk factors and never decides approval itself.
- human_approval is a FunctionNode that yields RequestInput to pause the
  graph until a person approves or rejects.
- record_outcome is the convergence point for both paths.
"""

from __future__ import annotations

import base64
import binascii
import json
import logging
import os
from typing import Any, Literal

import google.auth
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App, ResumabilityConfig
from google.adk.events import Event, RequestInput
from google.adk.models import Gemini
from google.adk.workflow import START, Workflow, node

from . import config

logger = logging.getLogger(__name__)

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


# ---------------------------------------------------------------------------
# Schemas - the data passed between nodes via ctx.state
# ---------------------------------------------------------------------------


class Expense(BaseModel):
    """A parsed expense report."""

    amount_usd: float
    submitter: str
    category: str
    description: str
    date: str


class RiskAssessment(BaseModel):
    """The LLM's risk judgment. It informs the human - it does not decide."""

    risk_level: Literal["low", "medium", "high"]
    reasons: list[str] = Field(default_factory=list)
    recommendation: str


class ApprovalDecision(BaseModel):
    """What the human reviewer (or the auto-approve rule) decided."""

    approved: bool
    approver: str
    comment: str = ""


# ---------------------------------------------------------------------------
# Step 1 - parse the event + route by amount (plain Python, no LLM)
# ---------------------------------------------------------------------------


@node
def parse_expense(node_input: Any) -> Event:
    """Extracts the expense and routes it by dollar amount.

    `node_input` is whatever the workflow is started with: a dict with a
    "data" key that is either base64-encoded JSON (how Pub/Sub delivers
    messages in production) or already plain JSON (how we feed it in local
    tests).
    """
    raw = node_input.get("data", node_input) if isinstance(node_input, dict) else node_input

    if isinstance(raw, str):
        try:
            raw = base64.b64decode(raw, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            pass  # not base64 - treat it as plain JSON text already
        payload = json.loads(raw)
    elif isinstance(raw, dict):
        payload = raw
    else:
        raise ValueError(f"Unrecognized expense event payload: {raw!r}")

    expense = Expense.model_validate(payload)

    route: str = (
        "auto_approve"
        if expense.amount_usd < config.AUTO_APPROVE_THRESHOLD_USD
        else "needs_review"
    )

    return Event(
        output=expense.model_dump(),
        state={"expense": expense.model_dump()},
        route=route,
    )


# ---------------------------------------------------------------------------
# Step 2a - the cheap path
# ---------------------------------------------------------------------------


@node
def auto_approve(expense: dict) -> Event:
    """Approves instantly. Only reachable for amounts under the threshold."""
    decision = ApprovalDecision(
        approved=True,
        approver="system",
        comment=(
            f"Auto-approved: ${expense['amount_usd']:.2f} is under the "
            f"${config.AUTO_APPROVE_THRESHOLD_USD:.2f} threshold."
        ),
    )
    return Event(
        output=decision.model_dump(),
        state={"decision": decision.model_dump()},
    )


# ---------------------------------------------------------------------------
# Step 2b - the only node that touches the LLM, and only for risk judgment
# ---------------------------------------------------------------------------

review_agent = LlmAgent(
    name="review_agent",
    model=Gemini(model=config.RISK_REVIEW_MODEL),
    instruction=(
        "You are a financial-risk reviewer for employee expense reports. "
        "You will receive one expense report as JSON (amount_usd, submitter, "
        "category, description, date). Judge it for risk factors only - "
        "things like a vague description, a category/description mismatch, "
        "an amount suspiciously close to an approval limit, or an unusual "
        "date. You never approve or reject anything yourself; a human makes "
        "that call after reading your assessment."
    ),
    output_schema=RiskAssessment,
    output_key="risk_assessment",
)


# ---------------------------------------------------------------------------
# Step 3 - pause for a human (human-in-the-loop)
# ---------------------------------------------------------------------------


@node(rerun_on_resume=True)
def human_approval(ctx: Context, expense: dict, risk_assessment: dict):
    """Pauses the graph and asks a person to approve or reject.

    `rerun_on_resume=True` means this function runs again from the top once
    the human responds. The first time through, `ctx.resume_inputs` has no
    entry yet, so we `yield RequestInput(...)` and stop. On resume, the same
    `interrupt_id` now has the human's answer, so we skip straight to
    recording it.
    """
    interrupt_id = f"approval:{ctx.node_path}"
    decision = ctx.resume_inputs.get(interrupt_id)

    if decision is None:
        yield RequestInput(
            interrupt_id=interrupt_id,
            message=(
                f"Expense alert ({risk_assessment['risk_level'].upper()} risk) - "
                f"{expense['submitter']} submitted ${expense['amount_usd']:.2f} "
                f"for {expense['category']}: {expense['description']}.\n"
                f"Reasons: {', '.join(risk_assessment['reasons']) or 'n/a'}\n"
                f"Model recommendation: {risk_assessment['recommendation']}\n"
                "Approve or reject?"
            ),
            response_schema=ApprovalDecision,
        )
        return

    yield Event(output=decision, state={"decision": decision})


# ---------------------------------------------------------------------------
# Step 4 - both paths converge here
# ---------------------------------------------------------------------------


@node
def record_outcome(expense: dict, decision: dict) -> Event:
    """Logs the final outcome. Swap this for a DB write / Pub/Sub ack in prod."""
    logger.info(
        "Expense outcome | submitter=%s amount=%.2f approved=%s by=%s comment=%s",
        expense["submitter"],
        expense["amount_usd"],
        decision["approved"],
        decision["approver"],
        decision.get("comment", ""),
    )
    return Event(output={"expense": expense, "decision": decision})


# ---------------------------------------------------------------------------
# The graph
# ---------------------------------------------------------------------------

root_agent = Workflow(
    name="expense_approval_workflow",
    edges=[
        (START, parse_expense),
        (parse_expense, {"auto_approve": auto_approve, "needs_review": review_agent}),
        (review_agent, human_approval),
        (auto_approve, record_outcome),
        (human_approval, record_outcome),
    ],
)

# `is_resumable=True` is required so the human_approval pause (an interrupt
# created by RequestInput) survives across separate API calls - the person
# approving/rejecting will typically do so in a request that arrives long
# after the one that triggered the pause.
app = App(
    root_agent=root_agent,
    name="expense_agent",
    resumability_config=ResumabilityConfig(is_resumable=True),
)
