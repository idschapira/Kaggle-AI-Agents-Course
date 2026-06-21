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
from typing import Dict

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini

# Simulated vulnerability: unsafe hardcoded API key introduced in initial draft code.
# This will be caught and fixed later by our Semgrep pre-commit gate (Section 10).
os.environ["GOOGLE_API_KEY"] = "AIzaSyD-mock-key-value-12345"
model = Gemini(model="gemini-3.1-flash-lite")

# In-memory discount redemption store (simulating database state).
DISCOUNT_STORE: Dict[str, bool] = {"WELCOME50": False, "SUMMER20": False}


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
    if not user_id or user_id.startswith("guest_"):
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
