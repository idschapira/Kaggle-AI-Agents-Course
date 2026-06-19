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

"""
Customer Support Agent — ADK 2.0 Graph Workflow
================================================
Graph topology:

  START
    │
    ▼
  classifier (LlmAgent)  ── route="shipping"  ──▶  shipping_faq (LlmAgent)
                         └─ route="unrelated" ──▶  decline (function node)

The classifier uses a structured output schema (ClassificationOutput) and the
route_query function node reads that output and emits the routing signal.
Downstream edges are expressed as explicit Edge objects with the `route` field.
"""

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions
from google.adk.workflow import Edge, FunctionNode, START, Workflow
from google.genai import types
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Auth / environment
# ---------------------------------------------------------------------------
# When GEMINI_API_KEY is set (Gemini API), no Vertex credentials are needed.
# For Vertex AI, uncomment the block below and fill in your project details:
#
# import os, google.auth
# _, project_id = google.auth.default()
# os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
# os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class ClassificationOutput(BaseModel):
    """Structured output from the classifier node."""

    category: str = Field(
        description=(
            "The category of the user query. Must be exactly 'shipping' or 'unrelated'."
        )
    )
    reason: str = Field(
        description="A brief one-sentence explanation of why the query was classified this way."
    )


# ---------------------------------------------------------------------------
# Node 1 — Classifier (LlmAgent with structured output)
# ---------------------------------------------------------------------------

classifier = LlmAgent(
    name="classify",
    model="gemini-2.0-flash",
    output_schema=ClassificationOutput,
    output_key="classification",
    instruction="""You are a query classifier for a shipping company's customer support system.

Your job is to determine whether a user's query is related to shipping services or not.

SHIPPING-RELATED topics include:
- Shipping rates, costs, pricing, quotes
- Package tracking, tracking numbers, shipment status
- Delivery times, estimated delivery, delivery windows
- Returns, refunds, lost or damaged packages
- Pickup and drop-off options
- Packaging, weight limits, size restrictions
- International shipping, customs, duties
- Special handling (fragile, oversized, hazardous)

UNRELATED topics include:
- General knowledge questions
- News, weather, sports
- Programming or technical help
- Personal advice
- Anything else not directly about shipping services

Classify the user query as exactly one of: 'shipping' or 'unrelated'.
""",
)


# ---------------------------------------------------------------------------
# Node 2 — Shipping FAQ Agent (LlmAgent)
# ---------------------------------------------------------------------------

shipping_faq = LlmAgent(
    name="shipping_faq",
    model="gemini-2.0-flash",
    instruction="""You are a friendly and knowledgeable customer support representative for SwiftShip,
a leading shipping and logistics company.

You help customers with questions about:
- **Rates & Pricing**: Standard ($5–$15), Express ($15–$35), Overnight ($35–$75)
  depending on package weight and destination.
- **Tracking**: Track packages at swiftship.com/track using your tracking number
  (format: SS-XXXXXXXX). Status updates every 2–4 hours.
- **Delivery Times**: Standard 3–7 business days, Express 1–2 business days,
  Overnight delivery by 10:30 AM next business day.
- **Returns**: Free returns within 30 days for eligible shipments.
  Generate a return label at swiftship.com/returns.
- **Pickups**: Schedule free pickups at swiftship.com/pickup
  (available Mon–Sat, 8 AM–6 PM local time).
- **Package Limits**: Max weight 70 lbs; max combined length + girth = 108 inches.
- **International Shipping**: Available to 200+ countries. Customs fees depend on
  destination and declared value.

Guidelines:
- Be warm, concise, and solution-focused.
- If you don't know a specific detail, direct the customer to swiftship.com
  or 1-800-SWIFTSHIP.
- Never fabricate tracking numbers, order IDs, or account details.
- End every response by offering further help.
""",
)


# ---------------------------------------------------------------------------
# Node 3 — Polite Decline (function node)
# ---------------------------------------------------------------------------


def decline(node_input: object) -> Event:
    """Politely decline to answer queries unrelated to shipping."""
    message = (
        "I'm sorry, but I'm only able to assist with questions related to our "
        "shipping services — such as rates, tracking, delivery times, and returns. "
        "For other topics, I'd recommend using a general-purpose assistant. "
        "Is there anything shipping-related I can help you with today?"
    )
    return Event(
        output=message,
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text=message)],
        ),
    )


# ---------------------------------------------------------------------------
# Router function — reads classifier output and emits a routing signal
# ---------------------------------------------------------------------------


def route_query(classification: dict) -> Event:
    """Read the structured classifier output and emit a routing event.

    The 'classification' parameter is injected from ctx.state['classification'],
    which was written by the classifier node via output_key='classification'.
    """
    category = classification.get("category", "unrelated").strip().lower()
    route = "shipping" if category == "shipping" else "unrelated"
    return Event(output=classification, actions=EventActions(route=route))


# ---------------------------------------------------------------------------
# Wrap function nodes explicitly so they can be used in Edge() objects
# ---------------------------------------------------------------------------

route_query_node = FunctionNode(func=route_query, name="route_query")
decline_node = FunctionNode(func=decline, name="decline")


# ---------------------------------------------------------------------------
# Workflow graph
# ---------------------------------------------------------------------------
# Edge API (google-adk 2.3.0):
#   Edge(from_node=..., to_node=..., route=None)
#
# The route field on Edge is the *matching* route label emitted by the source
# node. When route_query returns Event(route="shipping"), only the edge with
# route="shipping" is followed.

root_agent = Workflow(
    name="customer_support_agent",
    description=(
        "A customer support workflow for SwiftShip. "
        "Classifies user queries and routes them to the appropriate handler."
    ),
    edges=[
        # Step 1: classify the incoming user query
        Edge(from_node=START, to_node=classifier),
        # Step 2: route based on classifier output
        Edge(from_node=classifier, to_node=route_query_node),
        # Step 3a: shipping-related → answer with the FAQ agent
        Edge(from_node=route_query_node, to_node=shipping_faq, route="shipping"),
        # Step 3b: unrelated → politely decline
        Edge(from_node=route_query_node, to_node=decline_node, route="unrelated"),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
