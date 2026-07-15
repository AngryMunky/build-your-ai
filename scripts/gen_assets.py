#!/usr/bin/env python3
"""Generate the social-preview image and favicons for Build Your AI.

Requires Pillow (`pip install Pillow`) and the Segoe UI fonts (present on Windows;
swap FONT_BOLD / FONT_REG for any bold/regular TTF on other platforms).

Run from anywhere:  python scripts/gen_assets.py
Outputs into ../assets relative to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
os.makedirs(ASSETS, exist_ok=True)

BG     = (18, 22, 29)      # #12161d
TEXT   = (231, 236, 243)   # #e7ecf3
ACCENT = (124, 136, 255)   # #7c88ff
MUTED  = (154, 166, 182)   # #9aa6b6

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG  = r"C:\Windows\Fonts\segoeui.ttf"
def f(path, size): return ImageFont.truetype(path, size)


def draw_mark(d, cx, cy, r, ring_w):
    """The brand mark: an accent ring with the left half filled (a half-moon)."""
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=ACCENT, width=ring_w)
    inner = r - ring_w
    d.pieslice([cx-inner, cy-inner, cx+inner, cy+inner], 90, 270, fill=ACCENT)


def spaced_text(d, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=ACCENT)
    draw_mark(d, 96, 92, 26, 8)
    spaced_text(d, (140, 74), "BUILD YOUR AI", f(FONT_BOLD, 30), TEXT, 3)
    d.text((80, 190), "Don't just use an AI.", font=f(FONT_BOLD, 72), fill=TEXT)
    d.text((80, 280), "Decide how it works", font=f(FONT_BOLD, 72), fill=ACCENT)
    d.text((80, 362), "with you.", font=f(FONT_BOLD, 72), fill=ACCENT)
    d.text((84, 476), "A beginner-friendly personality & interaction builder",
           font=f(FONT_REG, 32), fill=MUTED)
    d.text((84, 518), "for ChatGPT, Claude, Gemini & Copilot.",
           font=f(FONT_REG, 32), fill=MUTED)
    url = "lawsonmode.github.io/build-your-ai"
    uw = d.textlength(url, font=f(FONT_REG, 26))
    d.text((W - uw - 60, 560), url, font=f(FONT_REG, 26), fill=MUTED)
    img.save(os.path.join(ASSETS, "og-image.png"))


def make_icon(size):
    ic = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dd = ImageDraw.Draw(ic)
    dd.rounded_rectangle([0, 0, size-1, size-1], radius=int(size*0.22), fill=BG)
    cx = cy = size / 2
    r = size * 0.26
    w = max(2, int(size * 0.07))
    dd.ellipse([cx-r, cy-r, cx+r, cy+r], outline=ACCENT, width=w)
    inner = r - w
    dd.pieslice([cx-inner, cy-inner, cx+inner, cy+inner], 90, 270, fill=ACCENT)
    return ic


SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#12161d"/>
  <circle cx="32" cy="32" r="16" fill="none" stroke="#7c88ff" stroke-width="5"/>
  <path d="M32 16 A16 16 0 0 0 32 48 Z" fill="#7c88ff"/>
</svg>
'''

if __name__ == "__main__":
    make_og()
    make_icon(32).save(os.path.join(ASSETS, "favicon-32.png"))
    make_icon(180).save(os.path.join(ASSETS, "apple-touch-icon.png"))
    with open(os.path.join(ASSETS, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(SVG)
    print("Wrote assets to", ASSETS)
