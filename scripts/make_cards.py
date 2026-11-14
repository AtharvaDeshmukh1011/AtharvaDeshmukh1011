from pathlib import Path

ASSETS = Path(__file__).parent.parent / "assets"
MONO = "ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"
BG, PANEL, LINE = "#0d1117", "#161b22", "#30363d"
TEXT, MUTED, GREEN, BLUE = "#c9d1d9", "#8b949e", "#39d353", "#58a6ff"

INFO = [
    ("", "atharva@github", GREEN),
    ("", "--------------", LINE),
    ("Role", "3rd Year Computer Engineering student, VIT Pune", TEXT),
    ("Now", "RAG pipelines and LangGraph agents on local LLMs", TEXT),
    ("Stack", "Python, Java, JavaScript", TEXT),
    ("ML", "LangChain, LangGraph, Advanced RAG, scikit-learn", TEXT),
    ("Web", "Spring Boot, React, Express, Flask, MySQL", TEXT),
    ("Tools", "PostgreSQL, Docker", TEXT),
    None,
    ("Built", "EvoMind: bug-risk ranking for Git repos", TEXT),
    ("", "LiveCricket: real-time scoring over SSE", TEXT),
    ("", "Doodhwala: milk delivery and billing", TEXT),
    ("", "UML Class Diagram Generator", TEXT),
    None,
    ("Reach", "atharva101106@gmail.com", TEXT),
]
SWATCHES = ["#f85149", "#d29922", GREEN, BLUE, "#bc8cff", TEXT]


def banner() -> str:
    nodes = [(80, 158, GREEN, 0), (270, 158, GREEN, 0.3), (440, 112, GREEN, 0.6), (440, 158, BLUE, 0.9), (630, 112, GREEN, 1.2), (790, 66, GREEN, 1.5)]
    dots = "".join(
        f'<circle class="pulse" cx="{x}" cy="{y}" r="6" fill="{BG}" stroke="{c}" stroke-width="2.5" style="animation-delay:{d}s"/>'
        for x, y, c, d in nodes
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 200" width="860" height="200">
<style>
.draw {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw 2.4s ease-out forwards; }}
.pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
.cursor {{ animation: blink 1s steps(1) infinite; }}
.rise {{ opacity: 0; animation: rise .8s ease-out forwards; }}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
@keyframes pulse {{ 50% {{ opacity: .35; }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<rect x="1" y="1" width="858" height="198" rx="12" fill="{PANEL}" stroke="{LINE}"/>
<path class="draw" d="M30 158 H270 C330 158 330 112 390 112 H630 C690 112 690 66 750 66 H830" fill="none" stroke="{GREEN}" stroke-width="2.5"/>
<path class="draw" d="M270 158 H540 C600 158 600 112 630 112" fill="none" stroke="{BLUE}" stroke-width="2.5" style="animation-delay:.5s"/>
{dots}
<text class="rise" x="40" y="72" font-family="{MONO}" font-size="36" font-weight="600" fill="#f0f6fc">Atharva Deshmukh</text>
<text class="rise" x="40" y="106" font-family="{MONO}" font-size="17" fill="{MUTED}" style="animation-delay:.3s">ML and LLM tools · full-stack apps<tspan class="cursor" fill="{GREEN}"> ▌</tspan></text>
</svg>"""


def info_card() -> str:
    rows, y = [], 84
    for i, item in enumerate(INFO):
        if item:
            key, value, colour = item
            delay = round(0.8 + i * 0.12, 2)
            label = f'<tspan fill="{BLUE}">{key}</tspan>' if key else ""
            rows.append(
                f'<text class="line" y="{y}" style="animation-delay:{delay}s"><tspan x="28">{label}</tspan>'
                f'<tspan x="{108 if i > 1 else 28}" fill="{colour}">{value}</tspan></text>'
            )
        y += 25
    swatches = "".join(f'<rect x="{28 + i * 30}" y="{y - 8}" width="24" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(SWATCHES))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 484" width="680" height="484">
<style>
.line {{ opacity: 0; animation: show .4s ease-out forwards; }}
@keyframes show {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<rect x="1" y="1" width="678" height="482" rx="10" fill="{BG}" stroke="{LINE}"/>
<rect x="1" y="1" width="678" height="40" rx="10" fill="{PANEL}"/>
<rect x="1" y="30" width="678" height="11" fill="{PANEL}"/>
<circle cx="24" cy="21" r="6" fill="#f85149"/><circle cx="46" cy="21" r="6" fill="#d29922"/><circle cx="68" cy="21" r="6" fill="{GREEN}"/>
<text x="340" y="26" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">atharva@github: ~</text>
<g font-family="{MONO}" font-size="17">
{chr(10).join(rows)}
</g>
<g class="line" style="animation-delay:2.6s">{swatches}</g>
</svg>"""


def badge(label: str, icon: str, width: int) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 40" width="{width}" height="40">
<rect x="1" y="1" width="{width - 2}" height="38" rx="8" fill="{PANEL}" stroke="{LINE}"/>
{icon}
<text x="46" y="25" font-family="{MONO}" font-size="14" fill="{TEXT}">{label}</text>
</svg>"""


MAIL_ICON = f'<rect x="14" y="12" width="22" height="16" rx="3" fill="none" stroke="{GREEN}" stroke-width="2"/><path d="M15 14 L25 22 L35 14" fill="none" stroke="{GREEN}" stroke-width="2"/>'
LINKEDIN_ICON = f'<rect x="14" y="10" width="20" height="20" rx="4" fill="{BLUE}"/><text x="24" y="25" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="{BG}">in</text>'

if __name__ == "__main__":
    files = {
        "banner.svg": banner(),
        "info-card.svg": info_card(),
        "gmail.svg": badge("atharva101106@gmail.com", MAIL_ICON, 262),
        "linkedin.svg": badge("LinkedIn", LINKEDIN_ICON, 132),
    }
    for name, svg in files.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(name, len(svg))
