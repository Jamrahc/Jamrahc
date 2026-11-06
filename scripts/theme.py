"""Shared design tokens and SVG helpers for the profile panels.

Every panel uses one typeface (JetBrains Mono, embedded so it renders the
same everywhere), one palette per colour scheme (GitHub's own dark/light
greys with a single blue accent), and one icon pipeline.
"""
from __future__ import annotations

import base64
import html
import re
from functools import lru_cache
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

W = 880  # every full-width panel shares this canvas width

THEMES = {
    "dark": {
        "panel": "#161b22",
        "inset": "#0d1117",
        "border": "#30363d",
        "rule": "#21262d",
        "text": "#e6edf3",
        "muted": "#9198a1",
        "faint": "#6e7681",
        "accent": "#79c0ff",
        "accent_soft": "#1f6feb",
        "kw": "#ff7b72",
        "fn": "#d2a8ff",
        "str": "#a5d6ff",
        "num": "#79c0ff",
        "attr": "#ffa657",
        "ok": "#7ee787",
        "ramp": ["#161b22", "#0c2d6b", "#1158c7", "#388bfd", "#79c0ff"],
    },
    "light": {
        "panel": "#f6f8fa",
        "inset": "#ffffff",
        "border": "#d1d9e0",
        "rule": "#e3e8ee",
        "text": "#1f2328",
        "muted": "#59636e",
        "faint": "#818b98",
        "accent": "#0969da",
        "accent_soft": "#54aeff",
        "kw": "#cf222e",
        "fn": "#8250df",
        "str": "#0a3069",
        "num": "#0550ae",
        "attr": "#953800",
        "ok": "#1a7f37",
        "ramp": ["#eff2f5", "#b6e3ff", "#54aeff", "#0969da", "#0a3069"],
    },
}

CHAR = 0.6  # JetBrains Mono advance width, in em


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text_w(s: str, size: float) -> float:
    return len(s) * size * CHAR


# ---------------------------------------------------------------- fonts
@lru_cache(None)
def _font_b64(weight: int) -> str:
    return base64.b64encode((SRC / "fonts" / f"jbm-{weight}.woff2").read_bytes()).decode()


def font_css(weights=(400, 700)) -> str:
    faces = "".join(
        "@font-face{font-family:'JBM';font-weight:%d;font-style:normal;"
        "src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, _font_b64(w))
        for w in weights
    )
    return (
        faces
        + "text{font-family:'JBM',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
        "font-variant-ligatures:contextual;}"
    )


# ---------------------------------------------------------------- icons
@lru_cache(None)
def _icon_src(name: str) -> tuple[str, float, str]:
    """Return (inner markup, viewBox size, kind) for an icon file."""
    raw = (SRC / "icons" / f"{name}.svg").read_text()
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    vb = float(re.search(r'viewBox="0 0 ([\d.]+)', raw).group(1))
    inner = raw[raw.index(">", raw.index("<svg")) + 1 : raw.rindex("</svg>")]
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r'\s(fill|stroke|style|class)="[^"]*"', "", inner)
    kind = "stroke" if name.startswith("ui-") else "fill"
    return inner.strip(), vb, kind


def icon(name: str, x: float, y: float, size: float, color: str, stroke_w: float = 2) -> str:
    inner, vb, kind = _icon_src(name)
    s = size / vb
    if kind == "stroke":
        paint = (
            f'fill="none" stroke="{color}" stroke-width="{stroke_w}" '
            'stroke-linecap="round" stroke-linejoin="round"'
        )
    else:
        paint = f'fill="{color}"'
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})" {paint}>{inner}</g>'


# ---------------------------------------------------------------- shell
def svg(w: float, h: float, body: str, title: str, weights=(400, 700), extra_css: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
        f"<title>{esc(title)}</title>"
        f"<style>{font_css(weights)}{extra_css}</style>"
        f"{body}</svg>"
    )


def panel_rect(w: float, h: float, t: dict, r: float = 12, fill: str | None = None) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" '
        f'fill="{fill or t["panel"]}" stroke="{t["border"]}"/>'
    )


def txt(x, y, s, size, color, weight=400, anchor="start", extra="") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
    )


def write(name: str, scheme: str, content: str) -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / f"{name}-{scheme}.svg").write_text(content)


# ---------------------------------------------------------------- shared pieces
def section_bar(label: str, ui_icon: str, meta: str, t: dict) -> str:
    """Section heading: icon, ~/path, hairline rule, right-aligned meta."""
    h = 52
    y = 32
    body = icon(ui_icon, 2, y - 17, 22, t["accent"])
    body += txt(34, y, "~/", 20, t["faint"], 700)
    body += txt(34 + text_w("~/", 20), y, label, 20, t["text"], 700)
    end = 34 + text_w("~/" + label, 20) + 16
    meta_w = text_w(meta, 13)
    body += (
        f'<line x1="{end:.1f}" y1="{y-6}" x2="{W - meta_w - 16:.1f}" y2="{y-6}" '
        f'stroke="{t["border"]}" stroke-width="1"/>'
    )
    body += txt(W, y - 1, meta, 13, t["faint"], 400, "end")
    return svg(W, h, body, f"{label} section")
