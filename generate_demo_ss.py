"""Generate a crisp dashboard preview without requiring a running app."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "demo_dashboard.png"
OUT.parent.mkdir(exist_ok=True)
W, H = 1800, 1100
image = Image.new("RGB", (W, H), "#0d1117")
draw = ImageDraw.Draw(image)
font = lambda size: ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size)
mono = lambda size: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
# quiet graph-paper backdrop
for x in range(0, W, 40): draw.line((x, 0, x, H), fill="#121c23", width=1)
for y in range(0, H, 40): draw.line((0, y, W, y), fill="#121c23", width=1)
draw.rectangle((0, 0, W, 82), fill="#0d1117", outline="#26313d")
draw.rectangle((44, 22, 82, 60), fill="#78e2c0")
draw.text((55, 29), "◈", font=font(23), fill="#0d1117")
draw.text((98, 23), "ORCHESTRA/ HQ", font=font(20), fill="#edf3f5")
draw.text((99, 49), "ENTERPRISE INTELLIGENCE FABRIC", font=mono(10), fill="#84909d")
draw.text((1510, 34), "●  SYSTEM NOMINAL", font=mono(12), fill="#78e2c0")
draw.text((64, 130), "/ CONTROL ROOM", font=mono(12), fill="#f4b860")
draw.text((64, 164), "Turn market signals", font=font(46), fill="#edf3f5")
draw.text((64, 219), "into a pricing decision.", font=font(46), fill="#78e2c0")
# cards
left, top, gap, cardw = 64, 332, 24, 320
right = 428
for x, title, value in [(64, "TRANSPORT", "websocket live"), (250, "P95 SYNC", "< 50 ms")]:
    draw.rectangle((x, 286, x + 160, 332), fill="#141a22", outline="#26313d")
    draw.text((x + 12, 295), title, font=mono(9), fill="#84909d")
    draw.text((x + 12, 312), value, font=font(12), fill="#78e2c0")
draw.rectangle((left, top, right, 930), fill="#141a22", outline="#26313d")
draw.text((left + 22, top + 22), "NEW ORCHESTRATION", font=font(16), fill="#edf3f5")
draw.text((left + 22, top + 72), "PRODUCT QUERY", font=mono(10), fill="#84909d")
draw.rectangle((left + 22, top + 98, right - 22, top + 240), fill="#0d1117", outline="#26313d")
draw.text((left + 38, top + 124), "Enterprise Analytics SaaS", font=font(15), fill="#edf3f5")
draw.text((left + 38, top + 151), "tool pricing", font=font(15), fill="#edf3f5")
draw.rectangle((left + 22, top + 260, right - 22, top + 310), fill="#f4b860")
draw.text((left + 105, top + 276), "↗  RUN MARKET SCAN", font=font(13), fill="#0d1117")
draw.rectangle((left, 954, right, 1030), fill="#141a22", outline="#26313d")
draw.text((left + 22, 970), "SEMANTIC CACHE", font=mono(10), fill="#84909d")
draw.text((left + 22, 990), "warm", font=font(18), fill="#78e2c0")
# agent cards
for i, (title, eyebrow, color, body) in enumerate([("Market Research", "AGENT 01 / DISCOVERY", "#78e2c0", "3 competitors indexed\nfeatures: dashboards, RBAC, alerts"), ("Dynamic Pricing", "AGENT 02 / STRATEGY", "#84909d", "awaiting human review...\npricing node is gated")]):
    x = 460 + i * 620
    draw.rectangle((x, top, x + 580, 660), fill="#141a22", outline="#26313d")
    draw.text((x + 26, top + 24), eyebrow, font=mono(10), fill=color)
    draw.text((x + 26, top + 56), title, font=font(24), fill="#edf3f5")
    draw.text((x + 26, top + 118), body, font=mono(13), fill="#aebbc2", spacing=12)
    draw.rectangle((x + 26, top + 230, x + 554, top + 280), fill="#0d1117", outline="#26313d")
    draw.text((x + 42, top + 248), "●  state synchronized", font=mono(11), fill=color)
# terminal
draw.rectangle((460, 695, 1696, 930), fill="#10161d", outline="#26313d")
draw.text((486, 720), "⌁  LIVE TRANSPORT / WEBSOCKET", font=mono(11), fill="#84909d")
for n, line in enumerate(["orchestrator        started     graph checkpoint created", "market_research     running     scanning competitor signals...", "market_research     complete    state synchronized", "human_review        paused      awaiting trajectory override"]):
    draw.text((486, 764 + n * 30), f"›  {line}", font=mono(12), fill="#78e2c0" if n == 3 else "#84909d")
image.save(OUT, quality=95)
print(f"Wrote {OUT}")
