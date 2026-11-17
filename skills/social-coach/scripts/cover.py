#!/usr/bin/env python3
"""social-coach cover: on-brand thumbnail / cover / carousel slide from one command.

  python3 cover.py --text "I built my *own TV*" [--sub "📺 Agentic TV · built with AI"] [--pill "FREE & OPEN SOURCE"]
                   [--image shot.jpg] [--format 16x9|9x16|4x5] [--accent "#ffd06a"] [--profile PROFILE.md] --out cover.png

*words in asterisks* get the accent colour. Brand tokens come from the profile's "## Brand kit"
section (bg, text, muted, accent, font) and CLI flags override them. Renders with headless Chrome.
"""
import argparse, html, os, re, shutil, subprocess, sys, tempfile

SIZES = {"16x9": (1280, 720), "9x16": (1080, 1920), "4x5": (1080, 1350)}
DEFAULT = {"bg": "#07080c", "text": "#ffffff", "muted": "#c9cbd3", "accent": "#ffd06a", "font": "Inter Tight"}


def brand(profile):
    b = dict(DEFAULT)
    if profile and os.path.exists(profile):
        sec = re.search(r"## Brand kit\n(.*?)(\n## |\Z)", open(profile, encoding="utf-8").read(), re.S)
        for k, v in re.findall(r"^-\s*(\w+):\s*`?([^`\n]+?)`?\s*$", sec[1] if sec else "", re.M):
            if k in b:
                b[k] = v.strip()
    return b


def page(a, b, w, h):
    title = re.sub(r"\*(.+?)\*", r'<em>\1</em>', html.escape(a.text))
    land = w > h
    img = f'<div class="img" style="background-image:url(\'file://{os.path.abspath(a.image)}\')"></div>' if a.image else ""
    fs = (96 if land else 120) if len(a.text) < 30 else (78 if land else 100)
    # 9:16: text block starts at y≈260 so it stays inside the UI safe zone
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={b['font'].replace(' ', '+')}:wght@600;800;900&display=block" rel="stylesheet">
<style>
*{{margin:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;overflow:hidden;background:radial-gradient(ellipse at {'85% 50%' if land else '50% 85%'},color-mix(in srgb,{b['accent']} 13%,{b['bg']}) 0%,{b['bg']} 60%);
 font-family:'{b['font']}',Inter,Roboto,'Noto Color Emoji',sans-serif;color:{b['text']};position:relative}}
.img{{position:absolute;background-size:cover;background-position:center;border-radius:28px;box-shadow:0 30px 80px #000c;
 {'right:-40px;top:110px;width:600px;height:500px;transform:perspective(1400px) rotateY(-14deg)' if land else 'left:90px;right:90px;bottom:300px;top:900px'}}}
.txt{{position:absolute;{'left:64px;top:50%;transform:translateY(-50%);width:640px' if land else 'left:90px;right:120px;top:260px'}}}
h1{{font-size:{fs}px;font-weight:900;line-height:.98;letter-spacing:-.045em}}
em{{font-style:normal;color:{b['accent']}}}
.sub{{margin-top:28px;font-size:{34 if land else 44}px;font-weight:600;color:{b['muted']}}}
.pill{{display:inline-block;margin-top:28px;background:#fff;color:#000;font-weight:800;font-size:{26 if land else 34}px;
 padding:14px 26px;border-radius:999px}}
</style></head><body>{img}<div class="txt"><h1>{title}</h1>
{f'<div class="sub">{html.escape(a.sub)}</div>' if a.sub else ''}{f'<div class="pill">{html.escape(a.pill)}</div>' if a.pill else ''}
</div></body></html>"""


def render(htm, w, h, out):
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    if not chrome:
        sys.exit("needs google-chrome or chromium")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "c.html"); open(f, "w", encoding="utf-8").write(htm)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--user-data-dir={d}/u", "--virtual-time-budget=4000", f"--window-size={w},{h}",
                        f"--screenshot={os.path.abspath(out)}", f"file://{f}"], capture_output=True, timeout=60)
    if not os.path.exists(out):
        sys.exit("render failed")
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text", required=True); p.add_argument("--sub"); p.add_argument("--pill"); p.add_argument("--image")
    p.add_argument("--format", default="16x9", choices=SIZES); p.add_argument("--accent"); p.add_argument("--profile")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    b = brand(a.profile)
    if a.accent:
        b["accent"] = a.accent
    w, h = SIZES[a.format]
    print(render(page(a, b, w, h), w, h, a.out))
