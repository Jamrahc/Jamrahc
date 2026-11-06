"""Fetch live GitHub numbers and render the activity panel (dark + light).

Run by .github/workflows/profile.yml with the workflow's GITHUB_TOKEN.
Locally:  GITHUB_TOKEN=<token> python scripts/stats.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

from theme import THEMES, W, icon, panel_rect, svg, text_w, txt, write

USER = os.environ.get("PROFILE_USER", "Jamrahc")
TOP_N = 5
# Languages to leave out of the bar chart, e.g. {"HTML", "Jupyter Notebook"}
EXCLUDE: set[str] = set()

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    u = payload["data"]["user"]

    repos = u["repositories"]
    langs: dict[str, int] = {}
    for repo in repos["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in EXCLUDE:
                langs[name] = langs.get(name, 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:TOP_N]

    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    today = dt.date.today().isoformat()
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"]:
            current += 1
        elif i == 0 and d["date"] == today:
            continue  # today isn't over yet
        else:
            break

    return {
        "contributions": cal["totalContributions"],
        "current": current,
        "longest": longest,
        "repos": repos["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos["nodes"]),
        "langs": [(n, s / total) for n, s in top],
        "updated": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def render(data: dict | None, t: dict) -> str:
    x = 32
    prompt = txt(x, 44, "$", 15, t["accent"], 700)
    prompt += txt(x + 18, 44, f"gh stats --user {USER}", 15, t["text"])

    if data is None:
        h = 132
        b = panel_rect(W, h, t) + prompt
        b += txt(x, 80, "Waiting for the first workflow run.", 14, t["muted"])
        b += txt(x, 104, "Actions > Profile assets > Run workflow fills this in.", 13, t["faint"])
        return svg(W, h, b, "GitHub stats: pending first run")

    h = 248
    b = panel_rect(W, h, t) + prompt

    rows = [
        ("ui-git-commit-horizontal", "contributions, 1y", f"{data['contributions']:,}"),
        ("ui-flame", "current streak", plural(data["current"], "day")),
        ("ui-calendar", "longest streak", plural(data["longest"], "day")),
        ("ui-folder-git-2", "public repos", str(data["repos"])),
        ("ui-star", "stars earned", str(data["stars"])),
    ]
    for i, (ic, label, value) in enumerate(rows):
        y = 84 + i * 28
        b += icon(ic, x, y - 12, 15, t["muted"])
        b += txt(x + 26, y, label, 13, t["muted"])
        b += txt(x + 230, y, value, 14, t["text"], 700)

    lx, bar_w = 476, W - 476 - 32
    b += f'<line x1="{lx-28}" y1="68" x2="{lx-28}" y2="{h-28}" stroke="{t["rule"]}"/>'
    b += txt(lx, 44, "top languages", 13, t["muted"])
    for i, (name, share) in enumerate(data["langs"]):
        y = 80 + i * 28
        pct = f"{share*100:.1f}%"
        b += txt(lx, y, name, 13, t["text"])
        b += txt(lx + bar_w, y, pct, 13, t["muted"], anchor="end")
        track_y = y + 6
        b += f'<rect x="{lx}" y="{track_y}" width="{bar_w}" height="4" rx="2" fill="{t["inset"]}"/>'
        fill_w = max(4, bar_w * share)
        opacity = 1 - i * 0.15
        b += (
            f'<rect x="{lx}" y="{track_y}" width="{fill_w:.1f}" height="4" rx="2" '
            f'fill="{t["accent"]}" fill-opacity="{opacity:.2f}"/>'
        )
    b += txt(W - 32, h - 18, f"updated {data['updated']}", 11, t["faint"], anchor="end")
    summary = ", ".join(f"{label} {value}" for _, label, value in rows)
    return svg(W, h, b, f"GitHub stats: {summary}")


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    data = fetch(token)
    for scheme, t in THEMES.items():
        write("stats", scheme, render(data, t))
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
