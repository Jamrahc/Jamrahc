"""Generate every static profile panel (dark + light) and README.md.

Edit the data below, then run:  python scripts/build.py
Live GitHub numbers come from scripts/stats.py, run daily by the workflow.
"""
from __future__ import annotations

import re

from theme import (ASSETS, ROOT, THEMES, W, esc, icon, panel_rect, section_bar,
                   svg, text_w, txt, write)

USER = "Jamrahc"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/{BRANCH}/assets"
DARK_ONLY = True  # False: follow each viewer's light/dark setting

NAME = "Jamiur Rahman"
TAGLINE = "Credit risk MIS by day. Building toward data engineering."
FACTS = [
    ("ui-map-pin", "Dhaka, Bangladesh"),
    ("ui-briefcase", "Credit risk, banking"),
    ("ui-graduation-cap", "B.Sc. CSE, BRAC Univ."),
    ("ui-target", "Next: data engineering"),
]

SOCIALS = [
    ("linkedin", "brand-linkedin", "LinkedIn", "https://linkedin.com/in/jamiurc"),
    ("medium", "brand-medium", "Medium", "https://medium.com/@jamiur.chowdhury"),
    ("email", "brand-gmail", "Email", "mailto:jamiur.chowdhury@gmail.com"),
]

ABOUT = '''class Jamiur:
    """Banker by day, data engineer in progress."""

    location   = "Dhaka, Bangladesh"
    role       = "MIS & Credit Monitoring, Credit Risk Management"
    experience = "4 yrs in banking: regulatory reporting -> credit MIS"
    education  = "B.Sc. Computer Science & Engineering, BRAC University"

    stack      = ["Python", "SQL", "Pandas", "Power BI", "Docker"]
    heading_to = "Data engineering: the pipelines behind good decisions"
    motto      = "Strong fundamentals over shortcuts."

    def currently(self):
        return [
            "100 days of Python, one focused hour a day",
            "shipping an Obsidian plugin to the community store",
            "automating credit-monitoring reports",
        ]'''

STACK = [
    ("languages", [("brand-python", "Python"), ("brand-javascript", "JavaScript"),
                   ("brand-csharp", "C#"), ("brand-html5", "HTML"), ("brand-css", "CSS"),
                   ("brand-gnubash", "Bash"), ("brand-powershell", "PowerShell"),
                   ("ui-sigma", "LaTeX")]),
    ("data & ml", [("brand-pandas", "Pandas"), ("brand-numpy", "NumPy"),
                   ("brand-scipy", "SciPy"), ("brand-scikitlearn", "sklearn"),
                   ("brand-pytorch", "PyTorch"), ("brand-keras", "Keras"),
                   ("brand-jupyter", "Jupyter")]),
    ("storage & bi", [("brand-postgresql", "PostgreSQL"), ("brand-mysql", "MySQL"),
                      ("brand-mongodb", "MongoDB"), ("brand-matplotlib", "Matplotlib"),
                      ("brand-plotly", "Plotly"), ("ui-chart-column", "Power BI")]),
    ("web & design", [("brand-django", "Django"), ("brand-flask", "Flask"),
                      ("brand-react", "React"), ("brand-tailwindcss", "Tailwind"),
                      ("brand-dotnet", ".NET"), ("brand-figma", "Figma"),
                      ("ui-pen-tool", "Affinity")]),
    ("cloud & tools", [("brand-googlecloud", "GCP"), ("brand-docker", "Docker"),
                       ("brand-git", "Git"), ("brand-github", "GitHub"),
                       ("brand-notion", "Notion"), ("brand-confluence", "Confluence"),
                       ("brand-obsidian", "Obsidian")]),
]

TAG_ICONS = {"Python": "brand-python", "sklearn": "brand-scikitlearn",
             "Jupyter": "brand-jupyter", "Pandas": "brand-pandas",
             "MySQL": "brand-mysql", "Power BI": "ui-chart-column",
             "C#": "brand-csharp", ".NET": "brand-dotnet"}

PROJECTS = [
    ("Credit-Risk", "ui-shield-check", "Credit risk analysis using machine learning",
     ["Python", "sklearn", "Jupyter"]),
    ("Customer-Churn-Analysis", "ui-trending-down", "Modelling customer churn with Python",
     ["Python", "Pandas", "Jupyter"]),
    ("HR-Data-Analysis-project-Python-Power-BI-and-SQL", "ui-users",
     "HR analytics across MySQL, Python and Power BI", ["MySQL", "Python", "Power BI"],
     ),
    ("Book-Recommendation-System", "ui-library", "Book recommender, collaborative filtering",
     ["Python", "Jupyter"]),
    ("Walmart-Sales-data-analysis", "ui-shopping-cart", "Exploratory analysis of Walmart sales",
     ["Python"]),
    ("Movet", "ui-code", "University software engineering project", ["C#", ".NET"]),
]
SHORT_NAMES = {"HR-Data-Analysis-project-Python-Power-BI-and-SQL": "HR-Data-Analysis",
               "Walmart-Sales-data-analysis": "Walmart-Sales-Analysis"}

QUOTE = ("Without data, you're just another person with an opinion.", "W. Edwards Deming")


# ------------------------------------------------------------------ header
def header(t: dict) -> str:
    h = 236
    b = panel_rect(W, h, t)
    b += icon("ui-square-terminal", 20, 12, 16, t["muted"])
    b += txt(44, 25, "jamiur@dhaka: ~", 13, t["muted"])
    b += txt(W - 20, 25, f"github.com/{USER}", 13, t["faint"], anchor="end")
    b += f'<line x1="1" y1="40.5" x2="{W-1}" y2="40.5" stroke="{t["rule"]}"/>'

    x = 32
    b += txt(x, 80, "$", 15, t["accent"], 700) + txt(x + 18, 80, "whoami", 15, t["text"])
    b += txt(x - 2, 134, NAME, 44, t["text"], 800, extra='letter-spacing="-1"')
    b += txt(x, 168, TAGLINE, 15, t["muted"])

    cmd = "cat README.md"
    cx = x + 18
    end = cx + text_w(cmd, 15) + 3
    b += txt(x, 210, "$", 15, t["accent"], 700)
    b += f'<text x="{cx}" y="210" font-size="15" fill="{t["text"]}" class="ty">{esc(cmd)}</text>'
    b += f'<rect class="cur" x="{end:.1f}" y="197" width="9" height="17" fill="{t["accent"]}"/>'

    dx = 624
    b += f'<line x1="{dx}" y1="62" x2="{dx}" y2="214" stroke="{t["rule"]}"/>'
    for i, (ic, label) in enumerate(FACTS):
        y = 82 + i * 38
        b += icon(ic, dx + 28, y - 13, 16, t["accent"])
        b += txt(dx + 54, y, label, 13, t["text"])

    dist = text_w(cmd, 15) + 3
    css = (
        ".ty{animation:ty 1.2s steps(13,end) .5s both}"
        "@keyframes ty{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}"
        ".cur{animation:mv 1.2s steps(13,end) .5s both,bl 1.1s step-end 1.7s infinite}"
        f"@keyframes mv{{from{{transform:translateX(-{dist:.1f}px)}}to{{transform:none}}}}"
        "@keyframes bl{50%{opacity:0}}"
        "@media (prefers-reduced-motion:reduce){.ty,.cur{animation:none}}"
    )
    return svg(W, h, b, f"{NAME}: {TAGLINE}", (400, 700, 800), css)


# ------------------------------------------------------------------ socials
def social(ic: str, label: str, t: dict) -> str:
    w, h = 176, 48
    b = panel_rect(w, h, t, r=10)
    b += icon(ic, 18, 15, 18, t["text"])
    b += txt(48, 29, label, 14, t["text"], 700)
    b += icon("ui-arrow-up-right", w - 34, 16, 16, t["faint"])
    return svg(w, h, b, label)


# ------------------------------------------------------------------ about
KW = {"class", "def", "return"}


def highlight(line: str, t: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if line.strip().startswith('"""'):
        lead = len(line) - len(line.lstrip())
        return [(" " * lead, t["text"]), (line.strip(), t["faint"])]
    for m in re.finditer(r'"[^"]*"|\w+|\s+|[^\w\s]', line):
        tok = m.group()
        if tok.startswith('"'):
            c = t["str"]
        elif tok in KW:
            c = t["kw"]
        elif tok == "self":
            c = t["attr"]
        elif tok in "=":
            c = t["kw"]
        elif out and out[-2:-1] and out[-2][0] in ("class", "def"):
            c = t["fn"]
        else:
            c = t["text"]
        out.append((tok, c))
    return out


def about(t: dict) -> str:
    lines = ABOUT.split("\n")
    lh, top, size = 26, 34, 15
    h = top + lh * (len(lines) - 1) + 30
    b = panel_rect(W, h, t)
    b += f'<rect x="1" y="1" width="51" height="{h-2}" rx="11" fill="{t["inset"]}"/>'
    b += f'<rect x="40" y="1" width="12" height="{h-2}" fill="{t["inset"]}"/>'
    b += f'<line x1="52.5" y1="1" x2="52.5" y2="{h-1}" stroke="{t["rule"]}"/>'
    for i, line in enumerate(lines):
        y = top + i * lh
        b += txt(38, y, str(i + 1), 13, t["faint"], anchor="end")
        if not line.strip():
            continue
        spans = "".join(
            f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in highlight(line, t)
        )
        b += f'<text x="72" y="{y}" font-size="{size}" xml:space="preserve">{spans}</text>'
    return svg(W, h, b, "About: " + TAGLINE)


# ------------------------------------------------------------------ stack
def stack(t: dict) -> str:
    tile_h, gap, row, x0, top, pad = 68, 10, 80, 148, 20, 24
    per_row = max(len(items) for _, items in STACK)
    tile_w = (W - pad - x0 - gap * (per_row - 1)) / per_row
    h = top + row * len(STACK) - (row - tile_h) + top
    b = panel_rect(W, h, t)
    for r, (group, items) in enumerate(STACK):
        ty = top + r * row
        b += txt(28, ty + tile_h / 2 + 5, group, 13, t["muted"])
        for i, (ic, label) in enumerate(items):
            tx = x0 + i * (tile_w + gap)
            b += (
                f'<rect x="{tx+.5}" y="{ty+.5}" width="{tile_w-1}" height="{tile_h-1}" '
                f'rx="9" fill="{t["inset"]}" stroke="{t["rule"]}"/>'
            )
            b += icon(ic, tx + (tile_w - 26) / 2, ty + 11, 26, t["text"])
            b += txt(tx + tile_w / 2, ty + 56, label, 11, t["muted"], anchor="middle")
    names = ", ".join(label for _, items in STACK for _, label in items)
    return svg(W, h, b, "Tech stack: " + names)


def stack_count() -> int:
    return sum(len(items) for _, items in STACK)


# ------------------------------------------------------------------ projects
def project(name: str, ic: str, desc: str, tags: list[str], t: dict) -> str:
    h = 84
    b = panel_rect(W, h, t)
    b += f'<rect x="20.5" y="18.5" width="47" height="47" rx="10" fill="{t["inset"]}" stroke="{t["rule"]}"/>'
    b += icon(ic, 33, 31, 22, t["accent"])
    b += txt(88, 38, SHORT_NAMES.get(name, name), 16, t["text"], 700)
    b += txt(88, 61, desc, 13, t["muted"])

    x = W - 56
    for tag in reversed(tags):
        has_icon = tag in TAG_ICONS
        cw = text_w(tag, 12) + 20 + (18 if has_icon else 0)
        x -= cw
        b += (
            f'<rect x="{x+.5:.1f}" y="30.5" width="{cw-1:.1f}" height="23" rx="6" '
            f'fill="{t["inset"]}" stroke="{t["rule"]}"/>'
        )
        lx = x + 10
        if has_icon:
            b += icon(TAG_ICONS[tag], lx, 36, 12, t["muted"])
            lx += 18
        b += txt(lx, 46, tag, 12, t["muted"])
        x -= 8
    b += icon("ui-arrow-up-right", W - 40, 34, 16, t["faint"])
    return svg(W, h, b, f"{SHORT_NAMES.get(name, name)}: {desc}")


# ------------------------------------------------------------------ footer
def footer(t: dict) -> str:
    h = 96
    q, who = QUOTE
    b = f'<line x1="{W/2-24}" y1="1" x2="{W/2+24}" y2="1" stroke="{t["border"]}"/>'
    b += txt(W / 2, 46, f"“{q}”", 14, t["muted"], anchor="middle")
    b += txt(W / 2, 72, f"— {who}", 13, t["faint"], anchor="middle")
    return svg(W, h, b, f"{q} {who}")


# ------------------------------------------------------------------ stats placeholder
def stats_pending(t: dict) -> str:
    from stats import render  # same renderer the workflow uses
    return render(None, t)


# ------------------------------------------------------------------ README
def pic(name: str, alt: str, width: str | None = "100%") -> str:
    w = f' width="{width}"' if width else ""
    if DARK_ONLY:
        return f'<img alt="{esc(alt)}" src="{RAW}/{name}-dark.svg"{w}>'
    return (
        "<picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="{RAW}/{name}-dark.svg">'
        f'<source media="(prefers-color-scheme: light)" srcset="{RAW}/{name}-light.svg">'
        f'<img alt="{esc(alt)}" src="{RAW}/{name}-dark.svg"{w}>'
        "</picture>"
    )


def readme() -> str:
    socials = "\n  ".join(
        f'<a href="{url}">{pic(f"social-{key}", label, "21%")}</a>'
        for key, _, label, url in SOCIALS
    )
    projects = "\n".join(
        f'<a href="https://github.com/{USER}/{n}">{pic(f"project-{i}", f"{SHORT_NAMES.get(n, n)}: {d}")}</a>'
        for i, (n, _, d, _) in enumerate(PROJECTS, 1)
    )
    snake_dark = f"https://raw.githubusercontent.com/{USER}/{USER}/output/snake-dark.svg"
    snake = (
        f'<img alt="Contribution graph being eaten by a snake" src="{snake_dark}" width="100%">'
    ) if DARK_ONLY else (
        "<picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{USER}/{USER}/output/snake-dark.svg">'
        f'<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{USER}/{USER}/output/snake-light.svg">'
        f'<img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/{USER}/{USER}/output/snake-dark.svg" width="100%">'
        "</picture>"
    )
    return f"""<!-- Generated by scripts/build.py. Edit the data there, then run: python scripts/build.py -->

<p align="center">
  {pic("header", f"{NAME}: {TAGLINE}")}
</p>

<p align="center">
  {socials}
</p>

<p>{pic("section-about", "About")}</p>

<p>{pic("about", "About: " + TAGLINE)}</p>

<p>{pic("section-stack", "Tech stack")}</p>

<p>{pic("stack", "Tech stack")}</p>

<p>{pic("section-projects", "Projects")}</p>

<p>
{projects}
</p>

<p>{pic("section-activity", "Activity")}</p>

<p>{pic("stats", "GitHub stats for " + USER)}</p>

<p>{snake}</p>

<p align="center">
  {pic("footer", QUOTE[0])}
</p>
"""


def main() -> None:
    for scheme, t in THEMES.items():
        write("header", scheme, header(t))
        for key, ic, label, _ in SOCIALS:
            write(f"social-{key}", scheme, social(ic, label, t))
        write("section-about", scheme, section_bar("about", "ui-code", "about.py", t))
        write("about", scheme, about(t))
        write("section-stack", scheme, section_bar("stack", "ui-layers", f"{stack_count()} tools", t))
        write("stack", scheme, stack(t))
        write("section-projects", scheme,
              section_bar("projects", "ui-folder-git-2", f"{len(PROJECTS)} pinned", t))
        for i, p in enumerate(PROJECTS, 1):
            write(f"project-{i}", scheme, project(*p, t))
        write("section-activity", scheme,
              section_bar("activity", "ui-activity", "refreshed daily", t))
        if not (ASSETS / f"stats-{scheme}.svg").exists():
            write("stats", scheme, stats_pending(t))
        write("footer", scheme, footer(t))
    (ROOT / "README.md").write_text(readme())
    print(f"wrote {len(list(ASSETS.glob('*.svg')))} svgs + README.md")


if __name__ == "__main__":
    main()
