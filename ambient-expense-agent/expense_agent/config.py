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

"""Tunable knobs for the expense-approval agent.

Kept separate from agent.py so the threshold and model can be changed
(or read from env vars later) without touching the graph logic.
"""

# Expense reports strictly under this amount (USD) are auto-approved by
# plain Python - no LLM call. At or above it, the LLM risk-review step runs
# and a human must approve or reject.
AUTO_APPROVE_THRESHOLD_USD: float = 100.0

# Model used ONLY for the risk-judgment step (review_agent). It never makes
# the routing/approval decision itself - that stays in Python and with the
# human reviewer.
RISK_REVIEW_MODEL: str = "gemini-2.5-flash-lite"
