"""Typed LangGraph workflow for the two-agent pricing demo."""
from __future__ import annotations

import asyncio
import re
from typing import Any, AsyncIterator, TypedDict

try:
    from langgraph.graph import END, StateGraph
except ImportError:  # Keeps the demo importable before dependencies are installed.
    END = "__end__"
    StateGraph = None


class AgentState(TypedDict, total=False):
    query: str
    research: dict[str, Any]
    pricing: dict[str, Any]
    status: str
    paused: bool
    override: dict[str, Any]


class OrchestrationGraph:
    """Small deterministic graph that is easy to replace with an LLM node."""

    def __init__(self) -> None:
        self._graph = self._build_graph() if StateGraph else None

    def _build_graph(self) -> Any:
        workflow = StateGraph(AgentState)
        workflow.add_node("market_research", self.market_research)
        workflow.add_node("dynamic_pricing", self.dynamic_pricing)
        workflow.set_entry_point("market_research")
        workflow.add_edge("market_research", "dynamic_pricing")
        workflow.add_edge("dynamic_pricing", END)
        return workflow.compile()

    async def market_research(self, state: AgentState) -> AgentState:
        query = state["query"]
        await asyncio.sleep(0.08)
        normalized = re.sub(r"\s+", " ", query).strip()
        return {
            **state,
            "research": {
                "query": normalized,
                "competitors": [
                    {"name": "MetricFlow", "starting_price": 49, "strength": "fast setup"},
                    {"name": "Northstar BI", "starting_price": 89, "strength": "governance"},
                    {"name": "SignalDesk", "starting_price": 149, "strength": "enterprise scale"},
                ],
                "features": ["Real-time dashboards", "Role-based access", "Usage alerts"],
            },
            "status": "research_complete",
        }

    async def dynamic_pricing(self, state: AgentState) -> AgentState:
        research = state.get("research", {})
        competitors = research.get("competitors", [])
        average = round(sum(item["starting_price"] for item in competitors) / max(len(competitors), 1))
        override = state.get("override", {})
        anchor = int(override.get("anchor", average))
        return {
            **state,
            "pricing": {
                "currency": "USD/month",
                "recommended_anchor": anchor,
                "tiers": [
                    {"name": "Launch", "price": max(anchor - 40, 29), "seats": 10},
                    {"name": "Scale", "price": anchor, "seats": 50},
                    {"name": "Enterprise", "price": anchor + 110, "seats": "unlimited"},
                ],
                "rationale": "Position near the category midpoint while preserving a clear enterprise premium.",
            },
            "status": "pricing_complete",
        }

    async def run(self, state: AgentState) -> AgentState:
        if self._graph:
            result = await self._graph.ainvoke(state)
            return result
        state = await self.market_research(state)
        return await self.dynamic_pricing(state)

    async def stream(self, state: AgentState, resume: bool = False) -> AsyncIterator[dict[str, Any]]:
        yield {"agent": "system", "status": "started", "payload": "Graph checkpoint created"}
        yield {"agent": "market_research", "status": "running", "payload": "Scanning competitor signals..."}
        state = await self.market_research(state)
        yield {"agent": "market_research", "status": "complete", "payload": state["research"]}
        if not resume:
            yield {"agent": "human_review", "status": "paused", "payload": state}
            return
        yield {"agent": "dynamic_pricing", "status": "running", "payload": "Building pricing scenarios..."}
        state = await self.dynamic_pricing(state)
        yield {"agent": "dynamic_pricing", "status": "complete", "payload": state["pricing"]}
        yield {"agent": "system", "status": "complete", "payload": state}


workflow = OrchestrationGraph()
