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

    START -> parse_expense --"auto_approve"--> auto_approve -------------+
                            \\                                            |
                             \\--"needs_review"--> security_screen        |
                                                    --"clean"--> review_agent
                                                    --"injection"---+      |
                                                                     \\     |
                                                    review_agent --> human_approval --> record_outcome
                                                                                          ^
                                                                     auto_approve --------+

- parse_expense reads the raw event, extracts the expense, and decides the
  route in plain Python (amount < AUTO_APPROVE_THRESHOLD_USD or not).
- auto_approve handles the cheap path. No LLM call.
- security_screen runs before the LLM ever sees a >= threshold expense: it
  redacts PII (SSNs / card numbers) in plain Python, and short-circuits
  anything that looks like a prompt-injection attempt straight to a human,
  bypassing the LLM entirely.
- review_agent (an LlmAgent) is the ONLY place the model is used: it judges
  risk factors on the already-redacted description and never decides
  approval itself.
- human_approval is a FunctionNode that yields RequestInput to pause the
  graph until a person approves or rejects.
- record_outcome is the convergence point for all paths.
"""

from __future__ import annotations

import base64
import binascii
import json
import logging
import os
import re
from typing import Any, Literal

from pydantic import BaseModel, Field

import google.genai as genai
from google.adk.agents.context import Context
from google.adk.apps import App, ResumabilityConfig
from google.adk.events import Event, RequestInput
from google.genai import types as genai_types
from google.adk.workflow import START, Workflow, node

from . import config

logger = logging.getLogger(__name__)

# NOTE: this project authenticates with a Google AI Studio API key (see
# .env -> GOOGLE_GENAI_USE_VERTEXAI=FALSE / GOOGLE_API_KEY=...), not Vertex
# AI. Earlier scaffolds hardcoded `google.auth.default()` +
# `GOOGLE_GENAI_USE_VERTEXAI=True` here, which forced Vertex mode and
# crashed without GCP ADC credentials - the same bug found in Dia 3's
# customer-support-agent. Deliberately left out so the .env setting wins.


# ---------------------------------------------------------------------------
# Schemas - the data passed between nodes via ctx.state
# ---------------------------------------------------------------------------


class Expense(BaseModel):
    """A parsed expense report.

    `amount_usd` accepts the alias "amount" too: the codelab's own test
    payload uses the shorter key ({"amount": 150.0, ...}), so without the
    alias Pydantic would reject it with "Field required" even though the
    value is right there under a different name.
    """

    model_config = {"populate_by_name": True}

    amount_usd: float = Field(alias="amount")
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


class SecurityScreenResult(BaseModel):
    """Audit trail of what the pre-LLM security checkpoint found.

    `screened=False` means the expense never went through security_screen at
    all (the auto-approve path skips it - amounts that small don't reach the
    LLM either, so there's nothing to screen before).
    """

    screened: bool = False
    redacted_categories: list[str] = Field(default_factory=list)
    injection_detected: bool = False


# ---------------------------------------------------------------------------
# Step 1 - parse the event + route by amount (plain Python, no LLM)
# ---------------------------------------------------------------------------


def _extract_expense_payload(node_input: Any) -> dict[str, Any]:
    """Normalizes `node_input` into a plain expense dict.

    `node_input` can arrive in several different shapes depending on who -
    or what - is calling the graph:

    - a `google.genai.types.Content` object - this is what the ADK
      Playground/dev-ui chat box sends, because it wraps anything you type
      the same way it would wrap a message to an LLM, even though this graph
      has no chat model at the entry point. We pull the typed text back out
      of `content.parts[*].text` before treating it as our payload.
    - the envelope `{"data": <expense dict>, "attributes": {...}}` - this is
      what our own ambient trigger endpoint (`fast_api_app.py`) sends after
      it has already base64-decoded the raw Pub/Sub message.
    - a dict (or JSON text) with a "data" key holding base64-encoded JSON -
      the shape a raw, un-decoded Pub/Sub push message would have.
    - already plain JSON text or a plain dict with the expense fields
      directly at the top level (how we feed it in local tests, or how the
      Playground sends a typed-in JSON object).

    Each `if` below only fires if the previous step left something that
    still needs unwrapping, so any of the shapes above fall through to the
    same final dict.
    """
    if isinstance(node_input, genai_types.Content):
        node_input = "".join(
            part.text for part in (node_input.parts or []) if part.text
        )

    if isinstance(node_input, str):
        try:
            node_input = json.loads(node_input)
        except json.JSONDecodeError:
            pass  # not JSON yet - might still be a bare base64 string

    if isinstance(node_input, dict) and "data" in node_input:
        node_input = node_input["data"]

    if isinstance(node_input, str):
        try:
            node_input = base64.b64decode(node_input, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            pass  # not base64 either - treat it as plain JSON text already
        node_input = json.loads(node_input)

    if not isinstance(node_input, dict):
        raise ValueError(f"Unrecognized expense event payload: {node_input!r}")

    return node_input


@node
def parse_expense(node_input: Any) -> Event:
    """Extracts the expense and routes it by dollar amount."""
    payload = _extract_expense_payload(node_input)
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
        state={
            "decision": decision.model_dump(),
            # record_outcome reads security_screen on every path; this one
            # never ran the checkpoint, so we log that explicitly instead of
            # leaving the key missing.
            "security_screen": SecurityScreenResult().model_dump(),
        },
    )


# ---------------------------------------------------------------------------
# Step 1.5 - pre-LLM security checkpoint: PII redaction + injection defense
# ---------------------------------------------------------------------------

# Catches runs of 9-19 digits (optionally separated by spaces/dashes), which
# covers both a 9-digit SSN and a 12-19 digit card number. This is a mock
# screen for the codelab - good enough to demo the pattern, not a production
# PII scanner.
_PII_NUMBER_PATTERN = re.compile(r"\b\d[\d\-\s]{7,17}\d\b")

# Phrases that try to talk the workflow into skipping its own rules. Matched
# case-insensitively so "Bypass all rules" and "bypass ALL rules" both trip it.
_INJECTION_PATTERN = re.compile(
    r"bypass\s+(all\s+)?rules"
    r"|ignore\s+(all\s+)?(previous\s+)?(instructions|rules)"
    r"|auto[-\s]?approve"
    r"|override\s+(the\s+)?(rules|approval|policy)"
    r"|disregard\s+(the\s+)?(rules|policy)",
    re.IGNORECASE,
)


def _redact_pii(text: str) -> tuple[str, list[str]]:
    """Replaces SSN/card-shaped numbers with a tag, returns (clean_text, categories)."""
    redacted_categories: list[str] = []

    def _replace(match: re.Match[str]) -> str:
        digit_count = len(re.sub(r"\D", "", match.group()))
        category = (
            "ssn"
            if digit_count == 9
            else "credit_card"
            if 12 <= digit_count <= 19
            else "pii_number"
        )
        if category not in redacted_categories:
            redacted_categories.append(category)
        return f"[REDACTED-{category.upper()}]"

    return _PII_NUMBER_PATTERN.sub(_replace, text), redacted_categories


@node
def security_screen(expense: dict) -> Event:
    """Runs before the LLM for every expense that didn't auto-approve.

    Two jobs, both plain Python - no model call involved:
      1. Redact PII (SSN/card-shaped numbers) from the description, so
         neither review_agent nor the logs ever see raw sensitive data.
      2. Detect prompt-injection attempts. If the description is trying to
         talk the system into auto-approving itself, skip review_agent
         completely and route straight to a human, flagged as a security
         event.
    Clean expenses continue on to review_agent with the redacted text.
    """
    clean_description, redacted_categories = _redact_pii(expense["description"])
    injection_detected = bool(_INJECTION_PATTERN.search(clean_description))

    cleaned_expense = {**expense, "description": clean_description}
    screen_result = SecurityScreenResult(
        screened=True,
        redacted_categories=redacted_categories,
        injection_detected=injection_detected,
    )

    state_update: dict[str, Any] = {
        "expense": cleaned_expense,
        "security_screen": screen_result.model_dump(),
    }

    if injection_detected:
        # review_agent never runs on this path, so human_approval still
        # needs a risk_assessment to show the reviewer - we synthesize it
        # here instead of asking the (bypassed) LLM for one.
        state_update["risk_assessment"] = RiskAssessment(
            risk_level="high",
            reasons=[
                "Prompt-injection attempt detected in the expense description.",
                *(
                    [f"PII redacted: {', '.join(redacted_categories)}"]
                    if redacted_categories
                    else []
                ),
            ],
            recommendation=(
                "Do not auto-approve. The LLM reviewer was bypassed for "
                "safety - a human must make this call."
            ),
        ).model_dump()

    return Event(
        output=cleaned_expense,
        state=state_update,
        route="injection" if injection_detected else "clean",
    )


# ---------------------------------------------------------------------------
# Step 2b - the only node that touches the LLM, and only for risk judgment
# ---------------------------------------------------------------------------

_REVIEW_INSTRUCTION = (
    "You are a financial-risk reviewer for employee expense reports. "
    "You will receive one expense report as JSON (amount_usd, submitter, "
    "category, description, date). Judge it for risk factors only - "
    "things like a vague description, a category/description mismatch, "
    "an amount suspiciously close to an approval limit, or an unusual "
    "date. You never approve or reject anything yourself; a human makes "
    "that call after reading your assessment."
)


@node
def review_agent(expense: dict) -> Event:
    # Uses the sync genai client (requests, not aiohttp) to avoid the
    # "Future attached to a different loop" crash that LlmAgent causes when
    # Agent Runtime runs stream_query in a new asyncio.run() thread.
    #
    # Client selection: Vertex AI in Agent Runtime (no API key present),
    # AI Studio locally (GOOGLE_API_KEY set in .env). Explicit project/location
    # avoids the Cloud Resource Manager API lookup that would fail if that API
    # is not enabled in the project.
    if os.environ.get("GOOGLE_API_KEY"):
        client = genai.Client()
    else:
        client = genai.Client(
            vertexai=True,
            project=os.environ.get("GOOGLE_CLOUD_PROJECT", "kaggle-dia5-agent-runtime"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-east1"),
        )
    response = client.models.generate_content(
        model=config.RISK_REVIEW_MODEL,
        contents=f"{_REVIEW_INSTRUCTION}\n\n{json.dumps(expense)}",
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RiskAssessment,
        ),
    )
    risk_data = json.loads(response.text)
    return Event(output=risk_data, state={"risk_assessment": risk_data})


# ---------------------------------------------------------------------------
# Step 3 - pause for a human (human-in-the-loop)
# ---------------------------------------------------------------------------


@node(rerun_on_resume=True)
def human_approval(
    ctx: Context, expense: dict, risk_assessment: dict, security_screen: dict
):
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
        security_banner = (
            "SECURITY EVENT: a prompt-injection attempt was detected and "
            "blocked before the LLM ever ran.\n"
            if security_screen.get("injection_detected")
            else ""
        )
        redacted_note = (
            "(PII redacted from description: "
            f"{', '.join(security_screen['redacted_categories'])})\n"
            if security_screen.get("redacted_categories")
            else ""
        )
        yield RequestInput(
            interrupt_id=interrupt_id,
            message=(
                f"{security_banner}"
                f"Expense alert ({risk_assessment['risk_level'].upper()} risk) - "
                f"{expense['submitter']} submitted ${expense['amount_usd']:.2f} "
                f"for {expense['category']}: {expense['description']}.\n"
                f"{redacted_note}"
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
def record_outcome(expense: dict, decision: dict, security_screen: dict) -> Event:
    """Logs the final outcome. Swap this for a DB write / Pub/Sub ack in prod."""
    logger.info(
        "Expense outcome | submitter=%s amount=%.2f approved=%s by=%s comment=%s "
        "redacted=%s injection_detected=%s",
        expense["submitter"],
        expense["amount_usd"],
        decision["approved"],
        decision["approver"],
        decision.get("comment", ""),
        ",".join(security_screen.get("redacted_categories", [])) or "none",
        security_screen.get("injection_detected", False),
    )
    return Event(
        output={"expense": expense, "decision": decision, "security_screen": security_screen}
    )


# ---------------------------------------------------------------------------
# The graph
# ---------------------------------------------------------------------------

root_agent = Workflow(
    name="expense_approval_workflow",
    edges=[
        (START, parse_expense),
        (parse_expense, {"auto_approve": auto_approve, "needs_review": security_screen}),
        (security_screen, {"clean": review_agent, "injection": human_approval}),
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
