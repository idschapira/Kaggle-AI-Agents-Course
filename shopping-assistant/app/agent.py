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

import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini

# Section 10 fix: load GOOGLE_API_KEY securely from a git-ignored .env file
# instead of hardcoding it in source. See app/.env (never committed) and
# app/.env.example (placeholder, safe to commit) for the expected format.
load_dotenv(Path(__file__).resolve().parent / ".env")

if not os.environ.get("GOOGLE_API_KEY"):
    raise RuntimeError(
        "GOOGLE_API_KEY is not set. Create shopping-assistant/app/.env "
        "(see app/.env.example) with a real key from https://aistudio.google.com/apikey."
    )

model = Gemini(model="gemini-3.1-flash-lite")

# In-memory discount redemption store (simulating database state).
DISCOUNT_STORE: Dict[str, bool] = {"WELCOME50": False, "SUMMER20": False}

# Threat model fix (Elevation of Privilege, see threat_model.md):
# `user_id` must never be trusted just because the LLM decided to pass it in
# the tool call — it must be checked against a known set of *registered*
# users. Rejecting only the "guest_" prefix let any other string (e.g.
# "admin_master") pass as if it were an authenticated user. In a real system
# this set would come from an authenticated session/database, not be
# hardcoded — but even this in-memory allow-list closes the gap where any
# arbitrary string was accepted as valid.
REGISTERED_USERS = {"user_alice", "user_bob"}


def redeem_discount(code: str, user_id: str) -> str:
    """Agent Tool: Redeem a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem (e.g. "WELCOME50").
        user_id: The ID of the user requesting redemption.

    Returns:
        A success or error message describing the outcome.
    """
    if code not in DISCOUNT_STORE:
        return "Error: Invalid discount code."
    if DISCOUNT_STORE[code]:
        return "Error: Discount code has already been redeemed."
    if not user_id or user_id not in REGISTERED_USERS:
        return "Error: Registered user account required to redeem discounts."

    DISCOUNT_STORE[code] = True
    return f"Success: Discount code {code} redeemed successfully for user {user_id}."


root_agent = Agent(
    name="ShoppingHelper",
    model=model,
    instruction=(
        "You are a helpful shopping assistant for a retail store. "
        "Use your tools to redeem discount codes for users."
    ),
    tools=[redeem_discount],
)

app = App(
    root_agent=root_agent,
    name="app",
)
