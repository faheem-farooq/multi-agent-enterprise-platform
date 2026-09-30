import { CheckCircle2, CircleDashed, PauseCircle } from "lucide-react";

type Event = { agent: string; status: string; payload: unknown };
export function AgentCard({ title, eyebrow, event }: { title: string; eyebrow: string; event?: Event }) {
  const active = event?.status === "running";
  const done = event?.status === "complete";
  return <section className="border border-line bg-panel/90 p-5 shadow-2xl shadow-black/10">
    <div className="mb-5 flex items-start justify-between"><div><p className="mono text-[10px] uppercase tracking-[.22em] text-mint">{eyebrow}</p><h2 className="mt-2 text-xl font-semibold">{title}</h2></div>{done ? <CheckCircle2 className="text-mint" size={20} /> : active ? <CircleDashed className="animate-spin text-signal" size={20} /> : <PauseCircle className="text-slate-600" size={20} />}</div>
    <div className="min-h-24 rounded-sm border border-line/70 bg-ink p-4 text-sm text-slate-300"><p className="mono text-xs leading-6">{event ? (typeof event.payload === "string" ? event.payload : JSON.stringify(event.payload, null, 2)) : "Awaiting graph execution..."}</p></div>
    <div className="mt-4 flex items-center justify-between text-xs text-muted"><span className="mono">{event?.status ?? "standby"}</span><span>{done ? "state committed" : active ? "streaming" : "queued"}</span></div>
  </section>;
}
