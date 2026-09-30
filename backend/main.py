"""FastAPI transport layer for streaming graph events."""
from __future__ import annotations

import asyncio
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from cache import cache
from database import save_run
from graph import AgentState, workflow

app = FastAPI(title="Multi-Agent Enterprise Orchestration Platform", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
checkpoints: dict[str, AgentState] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "orchestrator"}


async def send_event(websocket: WebSocket, event: dict[str, Any]) -> None:
    await websocket.send_json(event)


@app.websocket("/ws/orchestrate/{run_id}")
async def orchestrate(websocket: WebSocket, run_id: str) -> None:
    await websocket.accept()
    try:
        message = await websocket.receive_json()
        query = str(message.get("query", "")).strip()
        if not query:
            await send_event(websocket, {"agent": "system", "status": "error", "payload": "Query is required"})
            return
        cached = cache.get(query)
        if cached:
            await send_event(websocket, {"agent": "system", "status": "cached", "payload": cached})
            return

        state: AgentState = {"query": query, "status": "started", "paused": True}
        async for event in workflow.stream(state):
            await send_event(websocket, event)
            if event["status"] == "paused":
                checkpoints[run_id] = event["payload"]
                break

        while True:
            message = await websocket.receive_json()
            action = message.get("action")
            if action == "resume":
                state = checkpoints.get(run_id, state)
                state["override"] = message.get("override", {})
                state["paused"] = False
                result: dict[str, Any] = state
                async for event in workflow.stream(state, resume=True):
                    await send_event(websocket, event)
                    if event["status"] == "complete" and event["agent"] == "system":
                        result = event["payload"]
                cache.set(query, result)
                save_run(query, result)
                break
            if action == "cancel":
                await send_event(websocket, {"agent": "system", "status": "cancelled", "payload": "Run cancelled"})
                break
    except WebSocketDisconnect:
        checkpoints.pop(run_id, None)
    except Exception as exc:
        await send_event(websocket, {"agent": "system", "status": "error", "payload": str(exc)})
