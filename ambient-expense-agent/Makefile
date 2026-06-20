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

.PHONY: install playground run lint test

install:
	uv sync --all-extras

# Calls `adk web` directly instead of `agents-cli playground` / `agents-cli
# run`: on Windows that wrapper fails with "Got unexpected extra arguments"
# (a known bug catalogued in Dia 3) because it mis-expands the "." path
# argument. `adk web` also auto-disables --reload on Windows by itself, so
# no flag is needed for that either.
playground:
	uv run adk web expense_agent --host 127.0.0.1 --port 8080

# Runs the ambient FastAPI entrypoint (Pub/Sub trigger endpoint) on :8080.
run:
	uv run uvicorn expense_agent.fast_api_app:app --host 0.0.0.0 --port 8080

lint:
	uv run ruff check . && uv run ruff format --check . && uv run ty check . && uv run codespell

test:
	uv run pytest
