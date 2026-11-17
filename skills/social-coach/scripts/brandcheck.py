#!/usr/bin/env python3
"""social-coach brandcheck: does a cover / thumbnail / frame match the brand kit?

  python3 brandcheck.py IMAGE [IMAGE…] --profile PROFILE.md [--out DIR]
  python3 brandcheck.py --selftest

Per image: dominant palette with share %, each colour matched to the nearest kit token (ΔE76 in Lab),
off-kit saturated colours flagged, a WCAG contrast check of kit text/accent on the image's background,
and a 160 px "phone feed" preview to judge legibility by eye. Needs Pillow.
"""
import json, os, re, sys, tempfile

try:
    from PIL import Image
except ImportError:
    sys.exit("needs Pillow: pip install pillow")

NEAR, OFF = 15, 30  # ΔE: ≤15 = on-kit, >30 = clearly different colour


def hex2rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lab(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = map(lin, rgb)
    x, y, z = (r * .4124 + g * .3576 + b * .1805) / .95047, r * .2126 + g * .7152 + b * .0722, (r * .0193 + g * .1192 + b * .9505) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def de(a, b):
    return sum((p - q) ** 2 for p, q in zip(lab(a), lab(b))) ** .5


def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = map(ch, rgb)
    return .2126 * r + .7152 * g + .0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


def saturation(rgb):
    mx, mn = max(rgb), min(rgb)
    return 0 if mx == 0 else (mx - mn) / mx


def kit(profile):
    k = {}
    if profile and os.path.exists(profile):
        sec = re.search(r"## Brand kit.*?\n(.*?)(\n## |\Z)", open(profile, encoding="utf-8").read(), re.S)
        body = sec[1] if sec else ""
        for name, val in re.findall(r"^-\s*(bg|text|muted|accent):\s*`?(#[0-9a-fA-F]{6})", body, re.M):
            k[name] = val
        for i, (name, val) in enumerate(re.findall(r"([\w ]+?)\s*=\s*(#[0-9a-fA-F]{6})", body)):
            k.setdefault(f"pillar:{name.strip()}", val)
    return k or {"bg": "#07080c", "text": "#ffffff", "accent": "#ffd06a"}


def check(path, k, out):
    im = Image.open(path).convert("RGB")
    small = im.copy(); small.thumbnail((200, 200))
    q = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    tokens = {n: hex2rgb(v) for n, v in k.items()}
    palette, flags = [], []
    for c, idx in counts:
        rgb = tuple(pal[idx * 3:idx * 3 + 3])
        share = c / total
        name, d = min(((n, de(rgb, t)) for n, t in tokens.items()), key=lambda x: x[1])
        status = "on-kit" if d <= NEAR else "neutral" if saturation(rgb) < .25 else "off-kit" if d > OFF else "near-kit"
        palette.append({"hex": "#%02x%02x%02x" % rgb, "share": round(share, 3), "nearest": name, "deltaE": round(d, 1), "status": status})
        if status == "off-kit" and share >= .03:
            flags.append(f"off-kit colour #{'%02x%02x%02x' % rgb} covers {share:.0%} — footage (ok) or a graphic element (off-brand)? check by eye")
    bg = hex2rgb(palette[0]["hex"])
    cr = {n: round(contrast(t, bg), 1) for n, t in tokens.items() if n in ("text", "accent", "muted") or n.startswith("pillar:")}
    for n, v in cr.items():
        if v < 4.5 and n in ("text", "accent"):
            flags.append(f"{n} on this background only {v}:1 (<4.5 WCAG AA) — text will be hard to read")
    accents = [p for p in palette if p["status"] in ("on-kit", "near-kit") and p["nearest"] not in ("bg", "text", "muted") and p["share"] >= .01]
    if len({p["nearest"] for p in accents}) > 1:
        flags.append("more than one accent colour present — brand rule is one accent per graphic")
    if palette[0]["status"] not in ("on-kit", "near-kit") and de(bg, tokens.get("bg", bg)) > OFF:
        flags.append(f"dominant colour {palette[0]['hex']} is not the kit background — fine for a photo-led cover, otherwise off-brand")
    os.makedirs(out, exist_ok=True)
    prev = os.path.join(out, "feed160_" + os.path.splitext(os.path.basename(path))[0] + ".png")
    p = im.copy(); p.thumbnail((160, 284)); p.save(prev)
    return {"file": path, "size": im.size, "palette": palette, "contrast_on_dominant": cr, "flags": flags, "feed_preview": prev}


def selftest():
    with tempfile.TemporaryDirectory() as d:
        k = {"bg": "#07080c", "text": "#ffffff", "accent": "#ffd06a"}
        good = Image.new("RGB", (1280, 720), hex2rgb("#07080c"))
        good.paste(Image.new("RGB", (500, 120), (255, 255, 255)), (60, 200))
        good.paste(Image.new("RGB", (200, 120), hex2rgb("#ffd06a")), (60, 340))
        g = os.path.join(d, "g.png"); good.save(g)
        bad = good.copy(); bad.paste(Image.new("RGB", (400, 300), (230, 20, 200)), (700, 100))
        bad.paste(Image.new("RGB", (200, 120), (20, 200, 255)), (300, 340))
        b = os.path.join(d, "b.png"); bad.save(b)
        rg, rb = check(g, k, d), check(b, k, d)
        assert rg["flags"] == [], rg
        assert any("off-kit" in f for f in rb["flags"]), rb
        assert os.path.exists(rg["feed_preview"])
        assert abs(contrast((255, 255, 255), (0, 0, 0)) - 21) < .01
    print("selftest OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--selftest":
        selftest(); sys.exit()
    opt = lambda key: a.pop(a.index(key) + 1) if key in a else None
    prof, out = opt("--profile"), opt("--out")
    a = [x for x in a if x not in ("--profile", "--out")]
    k = kit(prof)
    print(json.dumps({"kit": k, "results": [check(p, k, out or os.path.dirname(os.path.abspath(p))) for p in a]}, indent=1))
