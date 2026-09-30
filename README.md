# Multi-Agent Enterprise Orchestration Platform

A deliberately small control room for turning a product query into a traceable pricing strategy. It demonstrates two-agent orchestration, streaming state updates, human approval, persistence, and cost-aware caching without requiring an API key.

![Dashboard preview](assets/demo_dashboard.png)

## Architecture

```mermaid
flowchart LR
  UI[Next.js control room] <-->|JSON WebSocket| API[FastAPI]
  API --> G[LangGraph workflow]
  G --> R[Market Research]
  R --> H{HITL checkpoint}
  H --> P[Dynamic Pricing]
  API --> C[Semantic LRU / Redis boundary]
  API --> DB[(SQLite / PostgreSQL)]
```

## Quick start

### Local

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn main:app --app-dir backend --reload --port 8000
# in another terminal
cd frontend && npm install && npm run dev
```













