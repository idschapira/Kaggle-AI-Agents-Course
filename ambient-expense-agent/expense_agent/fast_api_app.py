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
import json
import logging
import os

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from starlette.requests import Request

from expense_agent.app_utils.telemetry import setup_telemetry
from expense_agent.app_utils.typing import Feedback

setup_telemetry()
# Standard Python logging instead of a Cloud Logging client: this project
# runs on a Google AI Studio API key, not Vertex/GCP credentials, so a
# google.cloud.logging.Client() would hang/crash waiting for ADC - the same
# bug already fixed in Dia 3's customer-support-agent.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=False,
    # Makes this agent "ambient": registers ADK's built-in
    # /apps/{app_name}/trigger/pubsub endpoint, which decodes the base64
    # Pub/Sub payload and starts a fresh workflow session per event.
    trigger_sources=["pubsub"],
)
app.title = "ambient-expense-agent"
app.description = "API for interacting with the Agent ambient-expense-agent"


@app.middleware("http")
async def shorten_pubsub_subscription_name(request: Request, call_next):
    """Normalizes the Pub/Sub subscription name before ADK sees it.

    Real Pub/Sub push requests carry a fully-qualified subscription path
    (e.g. "projects/my-project/subscriptions/expense-agent-sub"). ADK's
    built-in trigger handler turns that into the session's userId by just
    swapping "/" for "--", which keeps the whole path
    ("projects--my-project--subscriptions--expense-agent-sub") - unreadable
    in the dev-ui session list. We intercept the request here and rewrite
    "subscription" down to its last path segment ("expense-agent-sub")
    before ADK's handler ever sees it, so session records stay readable.
    """
    if request.url.path.endswith("/trigger/pubsub") and request.method == "POST":
        body = await request.body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = None

        if isinstance(payload, dict) and isinstance(payload.get("subscription"), str):
            payload["subscription"] = payload["subscription"].rsplit("/", 1)[-1]
            body = json.dumps(payload).encode("utf-8")

        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        request._receive = receive  # noqa: SLF001 - Starlette's documented way to replay the body

    return await call_next(request)


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.info("Feedback received: %s", feedback.model_dump())
    return {"status": "success"}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
