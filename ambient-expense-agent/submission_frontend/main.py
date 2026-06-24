"""Expense Manager Dashboard — FastAPI service for reviewing paused Agent Runtime sessions."""

import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import vertexai
from vertexai.preview import reasoning_engines
from google.adk.sessions import VertexAiSessionService

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "kaggle-dia5-agent-runtime")
AGENT_RUNTIME_ID = os.environ.get(
    "AGENT_RUNTIME_ID",
    "projects/17805413958/locations/us-east1/reasoningEngines/1821600496155099136",
)
USER_ID = "default-user"


def _location_from_resource(name: str) -> str:
    parts = name.split("/")
    try:
        return parts[parts.index("locations") + 1]
    except (ValueError, IndexError):
        return "us-east1"


LOCATION = _location_from_resource(AGENT_RUNTIME_ID)
vertexai.init(project=PROJECT_ID, location=LOCATION)
_session_svc = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Expense Manager Dashboard", docs_url=None, redoc_url=None)


class ActionRequest(BaseModel):
    interrupt_id: str
    approved: bool


# ── Helpers ───────────────────────────────────────────────────────────────────
def _find_pending(session) -> dict | None:
    """Return the first unresolved adk_request_input interrupt from a session, or None."""
    calls: dict[str, dict] = {}  # call_id → args
    responses: set[str] = set()  # call_ids that already have a response

    for event in getattr(session, "events", []) or []:
        content = getattr(event, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            fc = getattr(part, "function_call", None)
            if fc and getattr(fc, "name", None) == "adk_request_input":
                calls[fc.id] = dict(getattr(fc, "args", {}) or {})
            fr = getattr(part, "function_response", None)
            if fr and getattr(fr, "name", None) == "adk_request_input":
                responses.add(fr.id)

    unresolved = {k: v for k, v in calls.items() if k not in responses}
    if not unresolved:
        return None
    interrupt_id, payload = next(iter(unresolved.items()))
    return {"session_id": session.id, "interrupt_id": interrupt_id, "payload": payload}


def _extract_text(events) -> str:
    """Collect all text parts from an agent stream response."""
    texts = []
    for ev in events or []:
        if isinstance(ev, dict):
            content = ev.get("content") or {}
            parts = content.get("parts", []) if isinstance(content, dict) else []
            for p in parts:
                if isinstance(p, dict) and p.get("text"):
                    texts.append(p["text"])
        else:
            content = getattr(ev, "content", None)
            for p in getattr(content, "parts", []) or []:
                t = getattr(p, "text", None)
                if t:
                    texts.append(t)
    return "\n".join(t for t in texts if t.strip()) or "Action processed successfully."


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/api/pending")
async def api_pending():
    try:
        resp = await _session_svc.list_sessions(
            app_name=AGENT_RUNTIME_ID, user_id=USER_ID
        )
    except Exception as exc:
        raise HTTPException(502, detail=f"Session service error: {exc}") from exc

    sessions = getattr(resp, "sessions", []) or []
    pending = []
    for s in sessions:
        try:
            full = await _session_svc.get_session(
                app_name=AGENT_RUNTIME_ID, user_id=USER_ID, session_id=s.id
            )
            hit = _find_pending(full)
            if hit:
                pending.append(hit)
        except Exception:
            continue
    return {"pending": pending}


@app.post("/api/action/{session_id}")
async def api_action(session_id: str, body: ActionRequest):
    resume_msg = {
        "role": "user",
        "parts": [
            {
                "function_response": {
                    "id": body.interrupt_id,
                    "name": "adk_request_input",
                    "response": {"approved": body.approved},
                }
            }
        ],
    }

    def _call():
        engine = reasoning_engines.ReasoningEngine(resource_name=AGENT_RUNTIME_ID)
        return list(
            engine.stream_query(
                message=resume_msg,
                user_id=USER_ID,
                session_id=session_id,
            )
        )

    try:
        events = await asyncio.to_thread(_call)
    except Exception as exc:
        raise HTTPException(502, detail=f"Resume failed: {exc}") from exc

    return {
        "status": "approved" if body.approved else "rejected",
        "agent_response": _extract_text(events),
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(DASHBOARD_HTML)


# ── Dashboard HTML ────────────────────────────────────────────────────────────
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Expense Approvals — Manager Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #07071a;
      --surface: rgba(255,255,255,0.035);
      --surface-hover: rgba(255,255,255,0.065);
      --border: rgba(255,255,255,0.07);
      --border-hover: rgba(255,255,255,0.14);
      --accent: #7c3aed;
      --accent-glow: rgba(124,58,237,0.3);
      --green: #22c55e;
      --green-dim: rgba(34,197,94,0.18);
      --green-glow: rgba(34,197,94,0.25);
      --red: #ef4444;
      --red-dim: rgba(239,68,68,0.12);
      --red-glow: rgba(239,68,68,0.25);
      --amber: #f59e0b;
      --text: #e2e8f0;
      --text-secondary: #94a3b8;
      --text-muted: #475569;
      --font: 'Outfit', system-ui, sans-serif;
      --radius: 16px;
      --radius-sm: 10px;
      --ease: cubic-bezier(0.4, 0, 0.2, 1);
    }

    body {
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Radial background glows */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background:
        radial-gradient(ellipse 700px 500px at 8% 25%, rgba(124,58,237,0.13) 0%, transparent 70%),
        radial-gradient(ellipse 600px 400px at 92% 12%, rgba(59,130,246,0.09) 0%, transparent 65%),
        radial-gradient(ellipse 900px 500px at 50% 105%, rgba(99,102,241,0.07) 0%, transparent 65%);
      pointer-events: none;
      z-index: 0;
    }

    .container {
      position: relative;
      z-index: 1;
      max-width: 1320px;
      margin: 0 auto;
      padding: 0 36px;
    }

    /* ── Header ── */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 28px 0 24px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 44px;
    }

    .logo { display: flex; align-items: center; gap: 14px; }

    .logo-mark {
      width: 44px; height: 44px;
      background: linear-gradient(135deg, #7c3aed, #6366f1);
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 24px var(--accent-glow), inset 0 1px 0 rgba(255,255,255,0.15);
      flex-shrink: 0;
    }

    .logo-text h1 {
      font-size: 21px; font-weight: 700; letter-spacing: -0.5px;
      background: linear-gradient(135deg, #e2e8f0 40%, #94a3b8);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .logo-text p { font-size: 13px; color: var(--text-muted); margin-top: 2px; }

    .header-right { display: flex; align-items: center; gap: 10px; }

    .live-badge {
      display: flex; align-items: center; gap: 7px;
      padding: 6px 12px;
      background: rgba(34,197,94,0.08);
      border: 1px solid rgba(34,197,94,0.18);
      border-radius: 30px;
      font-size: 12px; font-weight: 600; color: #4ade80;
      letter-spacing: 0.3px;
    }
    .live-dot {
      width: 6px; height: 6px; border-radius: 50%;
      background: #22c55e;
      animation: pulse 2s ease-in-out infinite;
    }

    .btn-ghost {
      display: flex; align-items: center; gap: 7px;
      padding: 8px 16px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text-secondary);
      font-family: var(--font); font-size: 13px; font-weight: 500;
      cursor: pointer;
      transition: all 0.2s var(--ease);
    }
    .btn-ghost:hover { background: var(--surface-hover); border-color: var(--border-hover); color: var(--text); }
    .btn-ghost.spinning svg { animation: spin 0.75s linear infinite; }

    /* ── Stats row ── */
    .stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 44px;
    }

    .stat-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 26px;
      backdrop-filter: blur(20px);
      transition: all 0.25s var(--ease);
    }
    .stat-card:hover {
      background: var(--surface-hover);
      border-color: var(--border-hover);
      transform: translateY(-2px);
    }

    .stat-label {
      font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.8px; color: var(--text-muted); margin-bottom: 10px;
    }
    .stat-value { font-size: 40px; font-weight: 800; letter-spacing: -2px; line-height: 1; }
    .stat-card.s-pending .stat-value { color: var(--amber); }
    .stat-card.s-approved .stat-value { color: var(--green); }
    .stat-card.s-rejected .stat-value { color: var(--red); }

    .stat-sub { font-size: 13px; color: var(--text-muted); margin-top: 6px; }

    /* ── Section header ── */
    .section-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 24px; }
    .section-title { font-size: 23px; font-weight: 700; letter-spacing: -0.6px; }
    .section-desc { font-size: 13px; color: var(--text-secondary); margin-top: 3px; }

    /* ── Cards grid ── */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 20px;
      padding-bottom: 60px;
    }

    /* ── Expense card ── */
    .expense-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 26px;
      backdrop-filter: blur(24px);
      transition: all 0.25s var(--ease);
      position: relative;
      overflow: hidden;
    }
    .expense-card::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(124,58,237,0.04) 0%, transparent 60%);
      pointer-events: none;
    }
    .expense-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, #7c3aed, #6366f1, #06b6d4);
      opacity: 0;
      transition: opacity 0.25s var(--ease);
    }
    .expense-card:hover {
      background: var(--surface-hover);
      border-color: var(--border-hover);
      transform: translateY(-4px);
      box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 0 0 1px rgba(124,58,237,0.1);
    }
    .expense-card:hover::before { opacity: 1; }

    .card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 22px; }

    .card-amount-block {}
    .card-amount {
      font-size: 36px; font-weight: 800; letter-spacing: -1.5px;
      background: linear-gradient(135deg, #f1f5f9, #cbd5e1);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .card-date { font-size: 12px; color: var(--text-muted); margin-top: 4px; font-weight: 500; }

    .pending-badge {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 5px 11px;
      background: rgba(245,158,11,0.1);
      border: 1px solid rgba(245,158,11,0.22);
      border-radius: 20px;
      font-size: 11px; font-weight: 700; color: var(--amber);
      letter-spacing: 0.4px; text-transform: uppercase;
      flex-shrink: 0;
    }
    .badge-pulse {
      width: 5px; height: 5px; border-radius: 50%;
      background: var(--amber);
      animation: pulse 1.8s ease-in-out infinite;
    }

    .card-fields { margin-bottom: 18px; display: flex; flex-direction: column; gap: 12px; }
    .card-field {}
    .field-label {
      font-size: 10px; text-transform: uppercase; letter-spacing: 1px;
      color: var(--text-muted); font-weight: 700; margin-bottom: 3px;
    }
    .field-value { font-size: 15px; font-weight: 500; }

    .card-desc {
      background: rgba(255,255,255,0.025);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 13px 15px;
      font-size: 13px; line-height: 1.6;
      color: var(--text-secondary);
      margin-bottom: 22px;
      font-style: italic;
    }

    /* ── Action buttons ── */
    .card-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

    .action-btn {
      display: flex; align-items: center; justify-content: center; gap: 7px;
      padding: 13px 0;
      border-radius: var(--radius-sm);
      border: none;
      font-family: var(--font); font-size: 14px; font-weight: 600;
      cursor: pointer;
      transition: all 0.2s var(--ease);
      position: relative;
    }
    .action-btn:active { transform: scale(0.97); }
    .action-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

    .action-btn.approve {
      background: var(--green-dim);
      border: 1px solid rgba(34,197,94,0.28);
      color: #4ade80;
    }
    .action-btn.approve:hover:not(:disabled) {
      background: rgba(34,197,94,0.28);
      border-color: rgba(34,197,94,0.5);
      box-shadow: 0 0 22px var(--green-glow);
      transform: translateY(-1px);
    }

    .action-btn.reject {
      background: var(--red-dim);
      border: 1px solid rgba(239,68,68,0.22);
      color: #f87171;
    }
    .action-btn.reject:hover:not(:disabled) {
      background: rgba(239,68,68,0.25);
      border-color: rgba(239,68,68,0.45);
      box-shadow: 0 0 22px var(--red-glow);
      transform: translateY(-1px);
    }

    .btn-spinner {
      width: 15px; height: 15px;
      border: 2px solid rgba(255,255,255,0.18);
      border-top-color: currentColor;
      border-radius: 50%;
      animation: spin 0.6s linear infinite;
      display: none;
    }
    .action-btn.loading .btn-spinner { display: block; }
    .action-btn.loading .btn-label { opacity: 0.6; }
    .action-btn.loading .btn-icon { display: none; }

    /* ── Empty / skeleton states ── */
    .empty-state {
      text-align: center; padding: 90px 24px;
      grid-column: 1 / -1;
    }
    .empty-icon { font-size: 52px; margin-bottom: 18px; opacity: 0.35; }
    .empty-title { font-size: 20px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; }
    .empty-sub { font-size: 14px; color: var(--text-muted); line-height: 1.6; }

    .skel {
      background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
      background-size: 400% 100%;
      animation: shimmer 1.4s ease infinite;
      border-radius: 8px;
    }
    @keyframes shimmer {
      0% { background-position: 100% 0; }
      100% { background-position: -100% 0; }
    }

    /* ── Modal ── */
    .modal-backdrop {
      position: fixed; inset: 0;
      background: rgba(7,7,26,0.72);
      backdrop-filter: blur(6px);
      z-index: 100;
      opacity: 0; pointer-events: none;
      transition: opacity 0.3s var(--ease);
    }
    .modal-backdrop.open { opacity: 1; pointer-events: all; }

    .modal-panel {
      position: fixed; top: 0; right: 0; bottom: 0;
      width: 500px; max-width: 100vw;
      background: linear-gradient(160deg, #0e0e24 0%, #0a0a1a 100%);
      border-left: 1px solid var(--border);
      z-index: 101;
      transform: translateX(100%);
      transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1);
      display: flex; flex-direction: column;
      box-shadow: -24px 0 80px rgba(0,0,0,0.6);
      overflow: hidden;
    }
    .modal-panel.open { transform: translateX(0); }

    .modal-glow {
      position: absolute; top: 0; right: 0;
      width: 300px; height: 300px;
      background: radial-gradient(ellipse at top right, rgba(124,58,237,0.12) 0%, transparent 65%);
      pointer-events: none;
    }

    .modal-header {
      padding: 32px 32px 0;
      display: flex; align-items: flex-start; justify-content: space-between;
      flex-shrink: 0;
    }
    .modal-title { font-size: 22px; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 4px; }
    .modal-sid { font-size: 12px; color: var(--text-muted); font-family: 'SF Mono', monospace; }

    .modal-close-btn {
      width: 38px; height: 38px;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 9px;
      color: var(--text-muted);
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: all 0.2s var(--ease); flex-shrink: 0;
    }
    .modal-close-btn:hover { background: var(--surface-hover); color: var(--text); }

    .modal-body { padding: 28px 32px 32px; overflow-y: auto; flex: 1; }

    .modal-status-pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 9px 18px;
      border-radius: 30px;
      font-size: 14px; font-weight: 700;
      margin-bottom: 28px;
      letter-spacing: 0.2px;
    }
    .modal-status-pill.approved {
      background: rgba(34,197,94,0.1);
      border: 1px solid rgba(34,197,94,0.25);
      color: #4ade80;
    }
    .modal-status-pill.rejected {
      background: rgba(239,68,68,0.1);
      border: 1px solid rgba(239,68,68,0.25);
      color: #f87171;
    }

    .modal-divider { height: 1px; background: var(--border); margin: 20px 0; }

    .modal-section-label {
      font-size: 11px; text-transform: uppercase; letter-spacing: 0.9px;
      color: var(--text-muted); font-weight: 700; margin-bottom: 12px;
    }

    .agent-response-box {
      background: rgba(255,255,255,0.025);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      font-size: 14px; line-height: 1.75;
      color: var(--text-secondary);
      white-space: pre-wrap;
    }

    .modal-detail-row {
      display: flex; justify-content: space-between; align-items: baseline;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      font-size: 14px;
    }
    .modal-detail-row:last-child { border-bottom: none; }
    .modal-detail-key { color: var(--text-muted); font-weight: 500; }
    .modal-detail-val { color: var(--text); font-weight: 600; text-align: right; max-width: 60%; }

    /* ── Toast ── */
    .toasts {
      position: fixed; bottom: 28px; left: 50%;
      transform: translateX(-50%);
      z-index: 200;
      display: flex; flex-direction: column; gap: 8px; align-items: center;
      pointer-events: none;
    }
    .toast {
      display: flex; align-items: center; gap: 10px;
      padding: 11px 20px;
      background: rgba(20,20,40,0.96);
      border: 1px solid var(--border);
      border-radius: 30px;
      font-size: 14px; font-weight: 500;
      backdrop-filter: blur(20px);
      box-shadow: 0 8px 36px rgba(0,0,0,0.4);
      pointer-events: all;
      animation: toast-in 0.3s cubic-bezier(0.34,1.56,0.64,1);
      transition: opacity 0.3s;
    }
    .toast.out { opacity: 0; }
    @keyframes toast-in {
      from { opacity: 0; transform: translateY(12px) scale(0.93); }
      to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* ── Animations ── */
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50%       { opacity: 0.55; transform: scale(0.75); }
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Responsive ── */
    @media (max-width: 768px) {
      .container { padding: 0 16px; }
      .stats { grid-template-columns: 1fr; }
      .cards-grid { grid-template-columns: 1fr; }
      .modal-panel { width: 100%; }
    }
  </style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <header>
    <div class="logo">
      <div class="logo-mark">💰</div>
      <div class="logo-text">
        <h1>Expense Approvals</h1>
        <p>AI-powered compliance review dashboard</p>
      </div>
    </div>
    <div class="header-right">
      <div class="live-badge"><span class="live-dot"></span>Live</div>
      <button class="btn-ghost" id="refreshBtn" onclick="loadPending()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <path d="M21 12a9 9 0 11-3.2-6.8M21 3v5h-5"/>
        </svg>
        Refresh
      </button>
    </div>
  </header>

  <!-- Stats -->
  <div class="stats">
    <div class="stat-card s-pending">
      <div class="stat-label">Pending Review</div>
      <div class="stat-value" id="statPending">—</div>
      <div class="stat-sub">awaiting decision</div>
    </div>
    <div class="stat-card s-approved">
      <div class="stat-label">Approved</div>
      <div class="stat-value" id="statApproved">0</div>
      <div class="stat-sub">this session</div>
    </div>
    <div class="stat-card s-rejected">
      <div class="stat-label">Rejected</div>
      <div class="stat-value" id="statRejected">0</div>
      <div class="stat-sub">this session</div>
    </div>
  </div>

  <!-- Section header -->
  <div class="section-header">
    <div>
      <div class="section-title">Pending Approvals</div>
      <div class="section-desc">Expenses flagged by the compliance agent — review and take action</div>
    </div>
  </div>

  <!-- Cards -->
  <div class="cards-grid" id="cardsGrid"></div>

</div>

<!-- Modal backdrop -->
<div class="modal-backdrop" id="modalBackdrop" onclick="closeModal()"></div>

<!-- Modal panel -->
<div class="modal-panel" id="modalPanel">
  <div class="modal-glow"></div>
  <div class="modal-header">
    <div>
      <div class="modal-title">Review Complete</div>
      <div class="modal-sid" id="modalSid"></div>
    </div>
    <button class="modal-close-btn" onclick="closeModal()">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <path d="M18 6L6 18M6 6l12 12"/>
      </svg>
    </button>
  </div>
  <div class="modal-body">
    <div id="modalStatusPill"></div>
    <div id="modalDetails"></div>
    <div class="modal-divider"></div>
    <div class="modal-section-label">Agent Compliance Review</div>
    <div class="agent-response-box" id="modalResponse"></div>
  </div>
</div>

<!-- Toasts -->
<div class="toasts" id="toasts"></div>

<script>
  const counts = { approved: 0, rejected: 0 };

  // ── Utilities ──────────────────────────────────────────────────────────────
  function toast(msg, type) {
    const icons = { info: 'ℹ️', success: '✅', error: '❌' };
    const el = document.createElement('div');
    el.className = 'toast';
    el.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${msg}</span>`;
    document.getElementById('toasts').appendChild(el);
    setTimeout(() => {
      el.classList.add('out');
      setTimeout(() => el.remove(), 320);
    }, 3800);
  }

  function fmt(val, curr) {
    if (val == null || val === '') return '—';
    try {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: curr || 'USD' }).format(parseFloat(val));
    } catch { return String(val); }
  }

  function pick(obj, ...keys) {
    for (const k of keys) if (obj[k] != null && obj[k] !== '') return obj[k];
    return null;
  }

  // ── Modal ──────────────────────────────────────────────────────────────────
  function openModal(status, sessionId, response, detailRows) {
    document.getElementById('modalSid').textContent = 'Session …' + sessionId.slice(-12);
    document.getElementById('modalStatusPill').innerHTML =
      `<div class="modal-status-pill ${status}">${status === 'approved' ? '✓ Approved' : '✕ Rejected'}</div>`;

    const rows = (detailRows || [])
      .map(([k, v]) => `<div class="modal-detail-row"><span class="modal-detail-key">${k}</span><span class="modal-detail-val">${v}</span></div>`)
      .join('');
    document.getElementById('modalDetails').innerHTML = rows
      ? `<div class="modal-section-label" style="margin-top:0">Expense Summary</div>${rows}<div class="modal-divider"></div>`
      : '';

    document.getElementById('modalResponse').textContent = response || 'The agent has processed this request.';
    document.getElementById('modalBackdrop').classList.add('open');
    document.getElementById('modalPanel').classList.add('open');
  }

  function closeModal() {
    document.getElementById('modalBackdrop').classList.remove('open');
    document.getElementById('modalPanel').classList.remove('open');
  }

  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  // ── Card rendering ─────────────────────────────────────────────────────────
  function renderCard(item) {
    const p = item.payload || {};
    const exp = (typeof p.expense === 'object' && p.expense) ? p.expense : p;

    const amount   = pick(exp, 'amount', 'total', 'cost') ?? pick(p, 'amount');
    const currency = pick(exp, 'currency') ?? 'USD';
    const merchant = pick(exp, 'merchant', 'vendor', 'payee') ?? pick(p, 'merchant', 'vendor') ?? 'Unknown Merchant';
    const category = pick(exp, 'category', 'type', 'expense_type') ?? pick(p, 'category') ?? 'General';
    const requester= pick(exp, 'requester', 'employee', 'submitted_by', 'name') ?? pick(p, 'requester', 'employee') ?? 'Unknown';
    const desc     = pick(exp, 'description', 'purpose', 'note', 'reason') ?? pick(p, 'description', 'message') ?? 'No description';
    const date     = pick(exp, 'date', 'created_at') ?? new Date().toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});

    const amtDisplay = amount != null ? fmt(amount, currency) : '—';

    // Store detail rows for modal
    const detailRows = JSON.stringify([
      ['Amount', amtDisplay],
      ['Merchant', merchant],
      ['Category', category],
      ['Requested by', requester],
      ['Date', date],
    ]);

    const sid = item.session_id;
    const iid = item.interrupt_id;

    return `
<div class="expense-card" id="card-${sid}" data-detail='${detailRows.replace(/'/g,"&apos;")}'>
  <div class="card-top">
    <div class="card-amount-block">
      <div class="card-amount">${amtDisplay}</div>
      <div class="card-date">${date}</div>
    </div>
    <div class="pending-badge"><span class="badge-pulse"></span>Pending</div>
  </div>

  <div class="card-fields">
    <div class="card-field">
      <div class="field-label">Merchant</div>
      <div class="field-value">${merchant}</div>
    </div>
    <div class="card-field">
      <div class="field-label">Category</div>
      <div class="field-value">${category}</div>
    </div>
    <div class="card-field">
      <div class="field-label">Requested by</div>
      <div class="field-value">${requester}</div>
    </div>
  </div>

  <div class="card-desc">${desc}</div>

  <div class="card-actions">
    <button class="action-btn approve" id="approve-${sid}"
      onclick="handleAction('${sid}','${iid}',true)">
      <span class="btn-icon">✓</span>
      <span class="btn-label">Approve</span>
      <div class="btn-spinner"></div>
    </button>
    <button class="action-btn reject" id="reject-${sid}"
      onclick="handleAction('${sid}','${iid}',false)">
      <span class="btn-icon">✕</span>
      <span class="btn-label">Reject</span>
      <div class="btn-spinner"></div>
    </button>
  </div>
</div>`;
  }

  // ── Load pending ───────────────────────────────────────────────────────────
  async function loadPending() {
    const btn  = document.getElementById('refreshBtn');
    const grid = document.getElementById('cardsGrid');
    btn.classList.add('spinning');

    grid.innerHTML = [1,2,3].map(() => `
      <div class="expense-card">
        <div class="skel" style="height:28px;width:50%;margin-bottom:18px"></div>
        <div class="skel" style="height:14px;width:80%;margin-bottom:10px"></div>
        <div class="skel" style="height:14px;width:65%;margin-bottom:10px"></div>
        <div class="skel" style="height:14px;width:70%;margin-bottom:18px"></div>
        <div class="skel" style="height:80px;margin-bottom:18px"></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div class="skel" style="height:46px"></div>
          <div class="skel" style="height:46px"></div>
        </div>
      </div>`).join('');

    try {
      const res = await fetch('/api/pending');
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      const pending = data.pending || [];

      document.getElementById('statPending').textContent  = pending.length;
      document.getElementById('statApproved').textContent = counts.approved;
      document.getElementById('statRejected').textContent = counts.rejected;

      if (pending.length === 0) {
        grid.innerHTML = `<div class="empty-state">
          <div class="empty-icon">🎉</div>
          <div class="empty-title">All caught up!</div>
          <div class="empty-sub">No expenses are waiting for your approval right now.<br>Check back shortly — new submissions will appear automatically.</div>
        </div>`;
      } else {
        grid.innerHTML = pending.map(renderCard).join('');
      }
    } catch (err) {
      grid.innerHTML = `<div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <div class="empty-title">Could not load approvals</div>
        <div class="empty-sub">${err.message}</div>
      </div>`;
      toast('Failed to load: ' + err.message, 'error');
    } finally {
      btn.classList.remove('spinning');
    }
  }

  // ── Handle action ──────────────────────────────────────────────────────────
  async function handleAction(sessionId, interruptId, approved) {
    const aBtn = document.getElementById('approve-' + sessionId);
    const rBtn = document.getElementById('reject-'  + sessionId);
    const active = approved ? aBtn : rBtn;

    aBtn.disabled = true;
    rBtn.disabled = true;
    active.classList.add('loading');

    try {
      const res = await fetch('/api/action/' + sessionId, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ interrupt_id: interruptId, approved }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'HTTP ' + res.status }));
        throw new Error(err.detail || 'HTTP ' + res.status);
      }

      const result = await res.json();
      if (approved) counts.approved++; else counts.rejected++;

      // Animate card out
      const card = document.getElementById('card-' + sessionId);
      let detailRows = [];
      try { detailRows = JSON.parse(card.dataset.detail); } catch {}

      if (card) {
        card.style.transition = 'all 0.38s cubic-bezier(0.4,0,0.2,1)';
        card.style.opacity    = '0';
        card.style.transform  = 'scale(0.94) translateY(-8px)';
        setTimeout(() => {
          card.remove();
          document.getElementById('statApproved').textContent = counts.approved;
          document.getElementById('statRejected').textContent = counts.rejected;
          const rem = document.querySelectorAll('.expense-card').length;
          document.getElementById('statPending').textContent  = rem;
          if (rem === 0) {
            document.getElementById('cardsGrid').innerHTML = `<div class="empty-state">
              <div class="empty-icon">🎉</div>
              <div class="empty-title">All caught up!</div>
              <div class="empty-sub">Queue is empty. Great work!</div>
            </div>`;
          }
        }, 380);
      }

      toast('Expense ' + (approved ? 'approved' : 'rejected') + ' successfully', 'success');
      openModal(result.status, sessionId, result.agent_response, detailRows);

    } catch (err) {
      toast('Action failed: ' + err.message, 'error');
      aBtn.disabled = false;
      rBtn.disabled = false;
      active.classList.remove('loading');
    }
  }

  // ── Init + auto-refresh every 30 s ────────────────────────────────────────
  loadPending();
  setInterval(loadPending, 30000);
</script>
</body>
</html>"""
