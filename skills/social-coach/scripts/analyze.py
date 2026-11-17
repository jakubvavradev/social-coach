#!/usr/bin/env python3
"""social-coach analyzer: the mechanical half of a short-form video review.

Measures what a human eye is bad at (loudness, dead time, cut rhythm, loop seam,
specs) and exports frames so the model can judge what a script is bad at
(hook, text, story). Stdlib + ffmpeg/ffprobe only.

usage:
  python3 analyze.py VIDEO [OUTDIR] [--max-len SECONDS]
  python3 analyze.py --selftest
prints JSON to stdout; writes frames, hook sheet and safe-zone overlays to OUTDIR.
"""
import json, os, re, subprocess, sys, tempfile

# Generic 9:16 UI overlay (px at 1080x1920). Platforms publish no official spec;
# these are the conservative union of TikTok / Reels / Shorts measurements.
SAFE = {"top": 220, "bottom": 380, "right": 150, "left": 60}
LUFS_TARGET, LUFS_TOL, PEAK_MAX = -14.0, 2.5, -1.0


def ff(*args):
    p = subprocess.run(args, capture_output=True, text=True)
    return p.stdout + p.stderr


def probe(video):
    m = json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams",
                                   "-show_format", video], capture_output=True, text=True).stdout or "{}")
    if not m.get("streams"):
        sys.exit(f"not a readable video: {video}")
    v = next(s for s in m["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rot = int(v.get("tags", {}).get("rotate", 0)) or next(
        (int(d.get("rotation", 0)) for d in v.get("side_data_list", []) if "rotation" in d), 0)
    if abs(rot) in (90, 270):
        w, h = h, w
    num, den = (v.get("avg_frame_rate") or v["r_frame_rate"]).split("/")
    return {"duration_s": round(float(m["format"]["duration"]), 2), "width": w, "height": h,
            "fps": round(int(num) / max(int(den), 1), 2), "vcodec": v.get("codec_name"),
            "size_mb": round(int(m["format"].get("size", 0)) / 1e6, 1),
            "bitrate_mbps": round(int(m["format"].get("bit_rate", 0)) / 1e6, 1),
            "has_audio": any(s["codec_type"] == "audio" for s in m["streams"])}


def audio(video, dur):
    out = ff("ffmpeg", "-hide_banner", "-nostats", "-i", video, "-vn",
             "-af", "ebur128=peak=true,silencedetect=noise=-40dB:d=0.3", "-f", "null", "-")
    summ = out[out.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summ)
    pk = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summ)
    lufs = float(i[1]) if i and i[1] != "-inf" else None
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    lead = ends[0] if starts and starts[0] <= 0.05 and ends else 0.0
    if starts and not ends and starts[0] <= 0.05:
        lead = dur  # silent to the end
    return {"lufs": lufs, "true_peak_db": float(pk[1]) if pk and pk[1] != "-inf" else None,
            "leading_silence_s": round(lead, 2), "silent": lufs is None or lufs < -45}


def visuals(video, dur):
    # ponytail: scene>0.3 catches hard cuts only; zooms/pans/text pops are judged from frames by eye
    sc = ff("ffmpeg", "-hide_banner", "-nostats", "-i", video, "-an", "-filter_complex",
            "[0:v]split=2[a][b];[a]select='gt(scene,0.3)',showinfo[o1];"
            "[b]freezedetect=n=0.003:d=1.5,blackdetect=d=0.3:pix_th=0.1[o2]",
            "-map", "[o1]", "-f", "null", "-", "-map", "[o2]", "-f", "null", "-")
    cuts = sorted({round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", sc)})
    edges = [0.0] + cuts + [dur]
    shots = [round(b - a, 2) for a, b in zip(edges, edges[1:]) if b - a > 0.05]
    fz_s = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", sc)]
    fz_d = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", sc)]
    if len(fz_s) > len(fz_d):  # freeze runs to the end
        fz_d.append(dur - fz_s[-1])
    blk = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", sc)
    return {"cuts": cuts, "n_shots": len(shots), "shots_s": shots, "longest_shot_s": max(shots),
            "avg_shot_s": round(dur / len(shots), 2), "cuts_per_10s": round(len(cuts) / dur * 10, 1),
            "freezes": [[round(s, 2), round(d, 2)] for s, d in zip(fz_s, fz_d)],
            "black": [[round(float(a), 2), round(float(b), 2)] for a, b in blk]}


def frame(video, t, path, width=432):
    ff("ffmpeg", "-v", "quiet", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
       "-vf", f"scale={width}:-2", path)
    return path if os.path.exists(path) else None


def exports(video, dur, w, h, out):
    os.makedirs(out, exist_ok=True)
    times = sorted({0, .5, 1, 2, 3, *range(5, int(dur), 2), max(dur - .1, 0)})
    frames = [f for t in times if (f := frame(video, t, os.path.join(out, f"f_{t:06.2f}.jpg")))]
    # hook sheet: first 3 s at 4 fps in one 4x3 image -> one Read shows the whole hook
    hook = os.path.join(out, "hook_0-3s.jpg")
    ff("ffmpeg", "-v", "quiet", "-y", "-t", "3", "-i", video, "-vf",
       "fps=4,scale=270:-2,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=4x3",
       "-frames:v", "1", hook)
    if not os.path.exists(hook):  # drawtext missing in some ffmpeg builds
        ff("ffmpeg", "-v", "quiet", "-y", "-t", "3", "-i", video, "-vf", "fps=4,scale=270:-2,tile=4x3",
           "-frames:v", "1", hook)
    # safe-zone overlays (red = covered by platform UI)
    sx, sy = w / 1080, h / 1920
    boxes = ",".join(f"drawbox=x={x}:y={y}:w={bw}:h={bh}:color=red@0.35:t=fill" for x, y, bw, bh in [
        (0, 0, "iw", int(SAFE["top"] * sy)), (0, f"ih-{int(SAFE['bottom'] * sy)}", "iw", int(SAFE["bottom"] * sy)),
        (f"iw-{int(SAFE['right'] * sx)}", 0, int(SAFE["right"] * sx), "ih"), (0, 0, int(SAFE["left"] * sx), "ih")])
    safe = []
    for t in (0, dur / 2):
        p = os.path.join(out, f"safezone_{t:05.1f}s.jpg")
        ff("ffmpeg", "-v", "quiet", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
           "-vf", f"{boxes},scale=432:-2", p)
        if os.path.exists(p):
            safe.append(p)
    # loop seam: SSIM of first vs last frame (1.0 identical)
    a, b = frame(video, 0, os.path.join(out, ".first.png"), 270), frame(video, max(dur - .25, 0), os.path.join(out, ".last.png"), 270)
    m = re.search(r"All:([\d.]+)", ff("ffmpeg", "-hide_banner", "-i", a, "-i", b, "-lavfi", "ssim", "-f", "null", "-")) if a and b else None
    for p in (a, b):
        p and os.remove(p)
    return {"frames": frames, "hook_sheet": hook if os.path.exists(hook) else None,
            "safezone": safe, "loop_ssim": round(float(m[1]), 3) if m else None}


def flags(r, max_len):
    f = []
    add = lambda lvl, area, msg: f.append({"level": lvl, "area": area, "msg": msg})
    if abs(r["width"] / r["height"] - 9 / 16) > .02:
        add("high", "tech", f"not 9:16 ({r['width']}x{r['height']}); vertical full-screen gets the feed")
    if r["width"] < 1080 and r["height"] >= r["width"]:
        add("med", "tech", f"width {r['width']} < 1080; export 1080x1920")
    if r["fps"] < 24:
        add("med", "tech", f"{r['fps']} fps looks choppy; export 30/60")
    if r["duration_s"] > max_len:
        add("med", "pacing", f"{r['duration_s']} s > target {max_len} s; every extra second must earn its place")
    if not r["has_audio"] or r["audio"]["silent"]:
        add("high", "audio", "no audible audio track; add music/voice (silent shorts underperform)")
    else:
        a = r["audio"]
        if a["lufs"] is not None and abs(a["lufs"] - LUFS_TARGET) > LUFS_TOL:
            add("med", "audio", f"{a['lufs']} LUFS; target ~{LUFS_TARGET} (platforms normalise; too quiet loses punch)")
        if a["true_peak_db"] is not None and a["true_peak_db"] > PEAK_MAX:
            add("low", "audio", f"true peak {a['true_peak_db']} dBFS > {PEAK_MAX}; risk of clipping after transcode")
        if a["leading_silence_s"] >= 0.4:
            add("high", "hook", f"{a['leading_silence_s']} s of silence at the start; sound must hit at frame 0")
    v = r["visual"]
    if v["shots_s"][0] > 3 and v["n_shots"] > 1:
        add("med", "hook", f"first hard cut at {v['shots_s'][0]} s; check frames for motion/text change in 0-2 s")
    if v["longest_shot_s"] > 4:
        add("low", "pacing", f"longest shot {v['longest_shot_s']} s without a hard cut; verify by eye there is zoom/pan/text change")
    for s, d in v["freezes"]:
        add("high" if s < 2 else "med", "pacing", f"static picture {s}-{round(s + d, 2)} s ({d} s dead time)")
    for a, b in v["black"]:
        if a > 0.1:
            add("med", "tech", f"black frames {a}-{b} s")
    if r.get("loop_ssim") is not None and r["loop_ssim"] < 0.5:
        add("info", "loop", f"last frame differs from first (SSIM {r['loop_ssim']}); no seamless loop")
    return f


def analyze(video, out, max_len=15.0):
    r = {"file": os.path.abspath(video), **probe(video)}
    r["aspect"] = "9:16" if abs(r["width"] / r["height"] - 9 / 16) < .02 else f"{r['width']}:{r['height']}"
    r["audio"] = audio(video, r["duration_s"]) if r["has_audio"] else None
    r["visual"] = visuals(video, r["duration_s"])
    r.update(exports(video, r["duration_s"], r["width"], r["height"], out))
    r["flags"] = flags(r, max_len)
    return r


def selftest():
    with tempfile.TemporaryDirectory() as d:
        v = os.path.join(d, "t.mp4")
        # 1 s silence, then tone; colour change at 3 s; frozen picture 3-8 s
        ff("ffmpeg", "-v", "quiet", "-y", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=3",
           "-f", "lavfi", "-i", "color=c=blue:s=1080x1920:r=30:d=5",
           "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo:d=1", "-f", "lavfi", "-i", "sine=f=440:d=7:r=48000",
           "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v];[2:a][3:a]concat=n=2:v=0:a=1,volume=8[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", v)
        r = analyze(v, os.path.join(d, "o"))
        assert r["aspect"] == "9:16" and abs(r["duration_s"] - 8) < .2, r
        assert any(abs(c - 3) < .2 for c in r["visual"]["cuts"]), r["visual"]
        assert r["audio"]["leading_silence_s"] >= 0.8, r["audio"]
        assert any(s >= 2.8 and d >= 4 for s, d in r["visual"]["freezes"]), r["visual"]
        assert r["hook_sheet"] and len(r["safezone"]) == 2 and len(r["frames"]) >= 6
        areas = {f["area"] for f in r["flags"]}
        assert {"hook", "pacing"} <= areas, r["flags"]
    print("selftest OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--selftest":
        selftest(); sys.exit()
    ml = 15.0
    if "--max-len" in a:
        i = a.index("--max-len"); ml = float(a[i + 1]); del a[i:i + 2]
    vid = a[0]
    print(json.dumps(analyze(vid, a[1] if len(a) > 1 else os.path.splitext(vid)[0] + "_review", ml), indent=1))
