"use client";

import { FormEvent, useRef, useState } from "react";
import { Activity, ArrowUpRight, Database, Gauge, Orbit, Radio, Send, ShieldCheck } from "lucide-react";
import { AgentCard } from "../components/AgentCard";
import { StateEditor } from "../components/StateEditor";
import { Terminal } from "../components/Terminal";

type Event = { agent: string; status: string; payload: unknown };
const initialQuery = "Enterprise Analytics SaaS tool pricing";

export default function Home() {
  const [query, setQuery] = useState(initialQuery);
  const [events, setEvents] = useState<Event[]>([]);
  const [stateValue, setStateValue] = useState('{\n  "anchor": 99\n}');
  const [paused, setPaused] = useState(false);
  const [connected, setConnected] = useState(false);
  const socket = useRef<WebSocket | null>(null);
  const research = [...events].reverse().find((event) => event.agent === "market_research");
  const pricing = [...events].reverse().find((event) => event.agent === "dynamic_pricing");
  const logs = events.map((event) => `${event.agent.padEnd(17)} ${event.status}  ${typeof event.payload === "string" ? event.payload : "state synchronized"}`);

  function startRun(event: FormEvent) {
    event.preventDefault();
    const runId = crypto.randomUUID();
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000"}/ws/orchestrate/${runId}`);
    socket.current = ws;
    ws.onopen = () => { setConnected(true); ws.send(JSON.stringify({ query })); };
    ws.onmessage = (message) => { const next = JSON.parse(message.data) as Event; setEvents((current) => [...current, next]); if (next.status === "paused") setPaused(true); };
    ws.onclose = () => setConnected(false);
  }
  function resume() { try { const override = JSON.parse(stateValue); socket.current?.send(JSON.stringify({ action: "resume", override })); setPaused(false); } catch { setStateValue('{\n  "anchor": 99\n}'); } }

  return <main className="grid-paper min-h-screen"><header className="border-b border-line bg-ink/80 px-6 py-5 backdrop-blur"><div className="mx-auto flex max-w-[1500px] items-center justify-between"><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center bg-mint text-ink"><Orbit size={21} /></div><div><p className="text-sm font-bold tracking-wide">ORCHESTRA<span className="text-mint">/</span>HQ</p><p className="mono text-[9px] uppercase tracking-[.18em] text-muted">enterprise intelligence fabric</p></div></div><div className="flex items-center gap-6 text-xs"><span className="hidden text-muted sm:inline">runbook / v1.0.0</span><span className="flex items-center gap-2 text-mint"><span className="h-2 w-2 rounded-full bg-mint" />system nominal</span></div></div></header>
    <div className="mx-auto max-w-[1500px] px-6 py-8"><div className="mb-8 flex flex-col justify-between gap-5 lg:flex-row lg:items-end"><div><p className="mono mb-3 text-xs uppercase tracking-[.25em] text-signal">/ control room</p><h1 className="max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">Turn market signals<br /><span className="text-mint">into a pricing decision.</span></h1></div><div className="flex gap-3 text-xs"><div className="border border-line bg-panel px-4 py-3"><p className="mono text-[10px] text-muted">transport</p><p className="mt-1 flex items-center gap-2 font-semibold"><Radio size={14} className={connected ? "text-mint" : "text-signal"} />{connected ? "websocket live" : "ready to connect"}</p></div><div className="border border-line bg-panel px-4 py-3"><p className="mono text-[10px] text-muted">p95 sync</p><p className="mt-1 flex items-center gap-2 font-semibold"><Gauge size={14} className="text-mint" />&lt; 50 ms</p></div></div></div>
      <div className="grid gap-5 xl:grid-cols-[350px_1fr]"><aside className="space-y-5"><form onSubmit={startRun} className="border border-line bg-panel p-5"><div className="mb-5 flex items-center justify-between"><label className="text-sm font-semibold">New orchestration</label><span className="mono text-[10px] text-muted">01 / 02</span></div><label className="mono text-[10px] uppercase tracking-[.18em] text-muted">Product query</label><textarea value={query} onChange={(e) => setQuery(e.target.value)} className="mt-2 h-28 w-full resize-none border border-line bg-ink p-3 text-sm leading-6 text-slate-200 outline-none focus:border-mint" /><button className="mt-3 flex w-full items-center justify-center gap-2 bg-signal px-4 py-3 text-sm font-bold text-ink hover:bg-[#ffd086]"><Send size={15} /> Run market scan <ArrowUpRight size={15} /></button></form><StateEditor value={stateValue} onChange={setStateValue} onResume={resume} disabled={!paused} /><div className="grid grid-cols-2 gap-3"><div className="border border-line bg-panel p-4"><Database size={15} className="text-mint" /><p className="mt-3 text-xl font-semibold">{events.length ? "warm" : "idle"}</p><p className="mono mt-1 text-[10px] uppercase text-muted">semantic cache</p></div><div className="border border-line bg-panel p-4"><ShieldCheck size={15} className="text-mint" /><p className="mt-3 text-xl font-semibold">ready</p><p className="mono mt-1 text-[10px] uppercase text-muted">hitl gate</p></div></div></aside><section className="space-y-5"><div className="grid gap-5 lg:grid-cols-2"><AgentCard title="Market Research" eyebrow="agent 01 / discovery" event={research} /><AgentCard title="Dynamic Pricing" eyebrow="agent 02 / strategy" event={pricing} /></div><Terminal logs={logs.length ? logs : ["orchestrator        standing by", "market_research    waiting for query", "dynamic_pricing    locked behind HITL gate"]} /><div className="flex items-center gap-3 border border-line bg-panel/60 px-4 py-3 text-xs text-muted"><Activity size={15} className="text-mint" /><span>Graph checkpoint</span><span className="mono text-slate-300">{paused ? "paused / awaiting human review" : events.length ? "streaming state updates" : "no active run"}</span><span className="ml-auto mono text-[10px] text-muted">ASYNC / STATEFUL / TRACEABLE</span></div></section></div></div>
  </main>;
}
