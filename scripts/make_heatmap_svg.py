import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
MONO = "ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BOLT, BOLT_CORE, FLASH = "#39d353", "#aff5b4", "#d2ffd9"
WIDTH = 860
WEEKS = 26
CELL, GAP = 20, 4
LOOP = 10
SHOTS = 22
FLIGHT = 0.022
BURST_GAP = 0.011


def times(*values: float) -> str:
    return ";".join(f"{min(max(v, 0), 1):.4f}" for v in values)


def animate(attribute: str, values: str, key_times: str) -> str:
    return f'<animate attributeName="{attribute}" dur="{LOOP}s" repeatCount="indefinite" values="{values}" keyTimes="{key_times}"/>'


def render(data: dict) -> str:
    weeks = data["weeks"][-WEEKS:]
    pitch = CELL + GAP
    grid_w = len(weeks) * pitch - GAP
    left = (WIDTH - grid_w) // 2
    top = 82
    bottom = top + 7 * pitch - GAP
    jet_y = bottom + 30
    height = jet_y + 34
    start, end = -20, WIDTH + 20
    total = sum(d["count"] for w in weeks for d in w)

    cells, days = [], []
    for x, week in enumerate(weeks):
        for day in week:
            y = (date.fromisoformat(day["date"]).weekday() + 1) % 7
            cx, cy = left + x * pitch, top + y * pitch
            delay = round((x + y) * 0.02, 2)
            cells.append(
                f'<rect class="cell" x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="4" fill="{PALETTE[day["level"]]}" style="animation-delay:{delay}s"/>'
            )
            days.append((day["count"], day["date"], cx, cy))

    busiest = [d for d in sorted(days, key=lambda d: (-d[0], d[1])) if d[0] > 0][:SHOTS]
    fired: dict[int, int] = {}
    shots = []
    for _, _, cx, cy in sorted(busiest, key=lambda d: (d[2], -d[3])):
        mx, my = cx + CELL / 2, cy + CELL / 2
        burst = fired.get(cx, 0)
        fired[cx] = burst + 1
        f = (mx - start) / (end - start) + burst * BURST_GAP
        hit = f + FLIGHT
        visible = times(0, f - 0.001, f, hit - 0.001, hit, 1)
        travel = times(0, f, hit, 1)
        shots.append(
            f'<rect x="{mx - 2.5:.1f}" width="5" height="16" rx="2.5" fill="{BOLT}" opacity="0">'
            f'{animate("y", f"{jet_y - 18};{jet_y - 18};{my - 8:.1f};{my - 8:.1f}", travel)}'
            f'{animate("opacity", "0;0;1;1;0;0", visible)}</rect>'
            f'<rect x="{mx - 1:.1f}" width="2" height="10" rx="1" fill="{BOLT_CORE}" opacity="0">'
            f'{animate("y", f"{jet_y - 15};{jet_y - 15};{my - 5:.1f};{my - 5:.1f}", travel)}'
            f'{animate("opacity", "0;0;1;1;0;0", visible)}</rect>'
            f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="4" fill="{FLASH}" opacity="0">'
            f'{animate("opacity", "0;0;1;0;0", times(0, hit - 0.001, hit, hit + 0.05, 1))}</rect>'
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="0" fill="none" stroke="{BOLT}" stroke-width="2" opacity="0">'
            f'{animate("r", f"0;0;{CELL * 1.3:.0f};{CELL * 1.3:.0f}", times(0, hit, hit + 0.06, 1))}'
            f'{animate("opacity", "0;0;1;0;0", times(0, hit - 0.001, hit, hit + 0.06, 1))}</circle>'
        )

    legend_x = left + grid_w - 150
    legend = "".join(f'<rect x="{legend_x + 40 + i * 16}" y="44" width="12" height="12" rx="3" fill="{c}"/>' for i, c in enumerate(PALETTE))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}">
<style>
.cell {{ opacity: 0; animation: drop .45s ease-out forwards; }}
.flame {{ animation: flicker .2s steps(2) infinite; }}
@keyframes drop {{ from {{ opacity: 0; transform: translateY(-8px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes flicker {{ 50% {{ opacity: .3; }} }}
</style>
<rect x="1" y="1" width="{WIDTH - 2}" height="{height - 2}" rx="12" fill="#0d1117" stroke="#30363d"/>
<text x="{left}" y="38" font-family="{MONO}" font-size="20" font-weight="600" fill="#f0f6fc">Contribution activity</text>
<text x="{left}" y="60" font-family="{MONO}" font-size="13" fill="#8b949e">{total} contributions in the last {WEEKS} weeks</text>
<text x="{legend_x}" y="55" font-family="{MONO}" font-size="12" fill="#8b949e">Less</text>
{legend}
<text x="{legend_x + 124}" y="55" font-family="{MONO}" font-size="12" fill="#8b949e">More</text>
{"".join(cells)}
{"".join(shots)}
<g>
<animateTransform attributeName="transform" type="translate" dur="{LOOP}s" repeatCount="indefinite" values="{start},{jet_y};{end},{jet_y}"/>
<path d="M0 -14 L8 8 L0 3 L-8 8 Z" fill="#f0f6fc"/>
<path class="flame" d="M-3 7 L0 17 L3 7 Z" fill="{BOLT}"/>
</g>
</svg>"""


if __name__ == "__main__":
    data = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    out = ROOT / "assets" / "contributions.svg"
    out.write_text(render(data), encoding="utf-8")
    print(out.name, out.stat().st_size)
