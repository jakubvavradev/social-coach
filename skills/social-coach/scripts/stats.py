#!/usr/bin/env python3
"""social-coach stats: evaluate the post log and build a posting calendar from it.

Post log = CSV, one row per post per platform (header names matter, order doesn't; blanks OK):
  posted_at (YYYY-MM-DD or YYYY-MM-DDTHH:MM, local time), platform, title, pillar, format,
  length_s, views, reach, avg_watch_s, completion_pct, likes, comments, shares, saves,
  follows, profile_visits

usage:
  python3 stats.py report   POSTS.csv                      -> markdown report
  python3 stats.py calendar POSTS.csv --profile PROFILE.md [--start YYYY-MM-DD] [--weeks 2]
                            [--per-week 3] [--time 18:00] [--ics out.ics]
  python3 stats.py --selftest
"""
import csv, datetime as dt, io, os, re, statistics as st, sys, tempfile
from collections import defaultdict

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MIN_N = 3  # groups with fewer posts are shown but never drive a finding
MIN_N_SLOT = 5  # moving the posting day/time needs more evidence: one viral outlier must not decide it


def num(v):
    try:
        return float(str(v).replace(",", "").replace(" ", "").replace("%", ""))
    except ValueError:
        return None


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
            if not r.get("posted_at") or not r.get("platform"):
                continue
            t = r["posted_at"]
            r["_dt"] = dt.datetime.fromisoformat(t if "T" in t or " " in t else t + "T00:00")
            r["_has_time"] = "T" in t or " " in t
            for k in ("length_s", "views", "reach", "avg_watch_s", "completion_pct", "likes", "comments",
                      "shares", "saves", "follows", "profile_visits"):
                r[k] = num(r.get(k, ""))
            r["platform"] = r["platform"].lower()
            rows.append(r)
    return rows


def ratio(a, b):
    return a / b if a is not None and b else None


def enrich(rows):
    """index = views / median views of that platform -> comparable across platforms."""
    by_p = defaultdict(list)
    for r in rows:
        by_p[r["platform"]].append(r)
    for p, rs in by_p.items():
        med = st.median([r["views"] for r in rs if r["views"] is not None] or [0]) or 1
        for r in rs:
            base = r["reach"] or r["views"]
            r["index"] = ratio(r["views"], med)
            r["watch_pct"] = ratio(r["avg_watch_s"], r["length_s"])
            parts = [x for x in (r["likes"], r["comments"], r["shares"], r["saves"]) if x is not None]
            r["eng_rate"] = ratio(sum(parts), base) if parts else None
            r["share_rate"] = ratio(r["shares"], base)
            r["follow_rate"] = ratio(r["follows"], base)
    return by_p


def length_bucket(s):
    return "?" if s is None else "<15s" if s < 15 else "15-30s" if s < 30 else "30-60s" if s < 60 else "60s+"


def hour_bucket(r):
    if not r["_has_time"]:
        return None
    h = r["_dt"].hour
    return f"{h // 3 * 3:02d}-{h // 3 * 3 + 3:02d}h"


def group(rows, key):
    g = defaultdict(list)
    for r in rows:
        k = key(r)
        if k and r.get("index") is not None:
            g[k].append(r["index"])
    return sorted(((k, st.median(v), len(v)) for k, v in g.items()), key=lambda x: -x[1])


def pct(x):
    return "–" if x is None else f"{x * 100:.2f} %" if x < .01 else f"{x * 100:.1f} %"


def report(rows):
    by_p = enrich(rows)
    o = io.StringIO()
    w = lambda s="": print(s, file=o)
    w(f"# Stats report — {len(rows)} posts, {min(r['_dt'] for r in rows):%Y-%m-%d} → {max(r['_dt'] for r in rows):%Y-%m-%d}")
    w(f"_Index = views ÷ platform median (1.0 = typical). Groups with n < {MIN_N} are hypotheses, not findings._\n")
    w("## Baseline per platform")
    w("| Platform | Posts | Median views | Median watch % | Median engagement | Median shares | Median follows |")
    w("|---|---|---|---|---|---|---|")
    for p, rs in sorted(by_p.items()):
        m = lambda k: (st.median(v) if (v := [r[k] for r in rs if r[k] is not None]) else None)
        w(f"| {p} | {len(rs)} | {m('views') or 0:,.0f} | {pct(m('watch_pct'))} | {pct(m('eng_rate'))} | {pct(m('share_rate'))} | {pct(m('follow_rate'))} |")
    ranked = sorted((r for r in rows if r.get("index") is not None), key=lambda r: -r["index"])
    w("\n## Winners & flops (vs own platform median)")
    w("| | Post | Platform | Index | Views | Watch % | Shares | Follows |")
    w("|---|---|---|---|---|---|---|---|")
    for r in ranked:
        tag = "🏆" if r["index"] >= 2 else "💀" if r["index"] <= 0.5 else ""
        w(f"| {tag} | {r.get('title', '')[:40]} | {r['platform']} | {r['index']:.2f}× | {r['views'] or 0:,.0f} | "
          f"{pct(r['watch_pct'])} | {pct(r['share_rate'])} | {pct(r['follow_rate'])} |")
    for name, key in [("Pillar", lambda r: r.get("pillar") or None), ("Format", lambda r: r.get("format") or None),
                      ("Length", lambda r: length_bucket(r["length_s"])), ("Weekday", lambda r: DAYS[r["_dt"].weekday()]),
                      ("Time of day", hour_bucket)]:
        g = group(rows, key)
        if not g:
            continue
        w(f"\n## By {name.lower()}")
        w(f"| {name} | Median index | n | |")
        w("|---|---|---|---|")
        for k, med, n in g:
            w(f"| {k} | {med:.2f}× | {n} | {'' if n >= MIN_N else 'low n'} |")
    # funnel: where does it leak?
    tot = lambda k: sum(r[k] or 0 for r in rows)
    v, pv, fo = tot("views"), tot("profile_visits"), tot("follows")
    w("\n## Funnel (all platforms)")
    w(f"views {v:,.0f} → profile visits {pv:,.0f} ({pct(ratio(pv, v))}) → follows {fo:,.0f} ({pct(ratio(fo, pv))} of visits)")
    w("\n## Automatic findings")
    for f in findings(rows, by_p):
        w(f"- {f}")
    return o.getvalue()


def findings(rows, by_p):
    out = []
    lg = [g for g in group(rows, lambda r: length_bucket(r["length_s"])) if g[2] >= MIN_N]
    if len(lg) >= 2 and lg[0][1] >= 1.5 * lg[-1][1]:
        out.append(f"Length: **{lg[0][0]}** performs {lg[0][1] / max(lg[-1][1], .01):.1f}× better than {lg[-1][0]} "
                   f"(n={lg[0][2]} vs {lg[-1][2]}).")
    for p, rs in by_p.items():
        w = [r["watch_pct"] for r in rs if r["watch_pct"] is not None]
        if w and st.median(w) < .4:
            out.append(f"{p}: median watch {pct(st.median(w))} of length → hook/length problem, run pre-flight review on the next cut.")
    v = sum(r["views"] or 0 for r in rows); pv = sum(r["profile_visits"] or 0 for r in rows); fo = sum(r["follows"] or 0 for r in rows)
    if v > 500 and pv / v < .01:
        out.append("Under 1 % of viewers visit the profile → CTA/series hook missing (growth.md §Profile).")
    if pv >= 10 and fo / pv < .1:
        out.append("Profile visits rarely turn into follows → fix bio + pinned posts (`/ig-profile`).")
    if not any(r["_has_time"] for r in rows):
        out.append("No posting times logged → log `posted_at` with HH:MM so time slots can be evaluated.")
    pg = group(rows, lambda r: r.get("pillar") or None)
    if pg and pg[0][2] >= MIN_N:
        out.append(f"Best pillar: **{pg[0][0]}** ({pg[0][1]:.2f}×, n={pg[0][2]}) → give it more calendar slots.")
    return out or ["Not enough data for findings yet — log at least 10 posts."]


def pillar_weights(profile_path, rows):
    """profile share × performance (clamped 0.5–2; only when n ≥ MIN_N)."""
    shares = {}
    if profile_path and os.path.exists(profile_path):
        txt = open(profile_path, encoding="utf-8").read()
        sec = re.search(r"## Pillars\n(.*?)(\n## |\Z)", txt, re.S)
        for line in (sec[1] if sec else "").splitlines():
            m = re.match(r"\|\s*([^|]+?)\s*\|.*\|\s*(\d+)\s*%\s*\|", line)
            if m:
                shares[m[1]] = int(m[2])
    enrich(rows)
    perf = {k: med for k, med, n in group(rows, lambda r: r.get("pillar") or None) if n >= MIN_N}
    if not shares:
        shares = {k: 1 for k in perf} or {"(any)": 1}
    def match(k):  # log pillar "Robots" matches profile pillar "Robots & competitions"
        kl = k.lower()
        return next((v for p, v in perf.items() if p.lower() in kl or kl in p.lower()), 1)
    return {k: v * min(2, max(.5, match(k))) for k, v in shares.items()}


def best_days(rows, per_week):
    g = [(k, m, n) for k, m, n in group(rows, lambda r: DAYS[r["_dt"].weekday()]) if n >= MIN_N_SLOT]
    defaults = {1: ["Thu"], 2: ["Tue", "Fri"], 3: ["Tue", "Thu", "Sun"], 4: ["Mon", "Wed", "Fri", "Sun"],
                5: ["Mon", "Tue", "Thu", "Fri", "Sun"]}.get(per_week, DAYS[:per_week])
    chosen = [k for k, _, _ in g[:per_week]]
    for d in defaults:  # fill with spread-out defaults when data is thin
        if len(chosen) < per_week and d not in chosen:
            chosen.append(d)
    return sorted(chosen, key=DAYS.index), bool(g)


def best_time(rows, default):
    g = [(k, m, n) for k, m, n in group(rows, hour_bucket) if n >= MIN_N_SLOT]
    return (f"{g[0][0][:2]}:00", True) if g else (default, False)


def calendar(rows, profile, start, weeks, per_week, time_, ics):
    enrich(rows)
    days, days_data = best_days(rows, per_week)
    t, time_data = best_time(rows, time_)
    weights = pillar_weights(profile, rows)
    total = sum(weights.values())
    owed = {k: 0.0 for k in weights}
    slots = []
    d = start
    while len(slots) < weeks * per_week:
        if DAYS[d.weekday()] in days:
            for k in owed:  # largest-remainder rotation keeps the mix proportional
                owed[k] += weights[k] / total
            p = max(owed, key=owed.get)
            owed[p] -= 1
            slots.append((d, p))
        d += dt.timedelta(days=1)
    o = io.StringIO()
    w = lambda s="": print(s, file=o)
    w(f"# Posting calendar {slots[0][0]:%Y-%m-%d} → {slots[-1][0]:%Y-%m-%d}")
    w(f"- Days: {', '.join(days)} ({'from your data' if days_data else 'default spread — not enough data per weekday'})")
    w(f"- Time: {t} ({'from your data' if time_data else 'default — log posting times to learn yours'})")
    w(f"- Pillar mix: " + ", ".join(f"{k} {v / total:.0%}" for k, v in sorted(weights.items(), key=lambda x: -x[1])))
    w("\n| Date | Day | Time | Pillar | Idea | Hook | Status |\n|---|---|---|---|---|---|---|")
    for day, p in slots:
        w(f"| {day:%Y-%m-%d} | {DAYS[day.weekday()]} | {t} | {p} |  |  | ☐ |")
    if ics:
        hh, mm = map(int, t.split(":"))
        ev = [f"BEGIN:VEVENT\r\nUID:sc-{day:%Y%m%d}-{i}@social-coach\r\nDTSTAMP:{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}\r\n"
              f"DTSTART:{day:%Y%m%d}T{hh:02d}{mm:02d}00\r\nDURATION:PT30M\r\nSUMMARY:📱 Post: {p}\r\n"
              f"DESCRIPTION:Pre-flight review → post → reply to comments for 60 min\r\nEND:VEVENT\r\n"
              for i, (day, p) in enumerate(slots)]
        with open(ics, "w", encoding="utf-8") as f:
            f.write("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//social-coach//EN\r\n" + "".join(ev) + "END:VCALENDAR\r\n")
        w(f"\n.ics written: {ics} (floating local time; import into Google Calendar)")
    return o.getvalue()


def selftest():
    csv_txt = "posted_at,platform,title,pillar,format,length_s,views,reach,avg_watch_s,likes,comments,shares,saves,follows,profile_visits\n"
    for i in range(12):
        short = i % 2 == 0
        csv_txt += (f"2026-10-{1 + i * 2:02d}T{18 if short else 9:02d}:00,instagram,post{i},{'Robots' if short else 'AI'},reel,"
                    f"{12 if short else 50},{2000 if short else 400},{1800 if short else 380},{7 if short else 5},50,5,10,3,2,20\n")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "posts.csv"); open(p, "w").write(csv_txt)
        prof = os.path.join(d, "profile.md")
        open(prof, "w").write("## Pillars\n| Pillar | Assets | Share |\n|---|---|---|\n| Robots | x | 50 % |\n| AI | y | 50 % |\n")
        rows = load(p)
        rep = report(rows)
        assert "<15s" in rep and "Length: **<15s**" in rep, rep
        assert "18-21h" in rep and "Best pillar: **Robots**" in rep, rep
        cal = calendar(load(p), prof, dt.date(2026, 11, 16), 2, 3, "18:00", os.path.join(d, "c.ics"))
        assert cal.count("| ☐ |") == 6 and "18:00 (from your data)" in cal, cal
        robots = cal.count("| Robots |")
        assert 4 <= robots <= 5, cal  # better pillar gets more slots
        assert open(os.path.join(d, "c.ics")).read().count("BEGIN:VEVENT") == 6
    print("selftest OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--selftest":
        selftest(); sys.exit()
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    rows = load(a[1])
    if not rows:
        sys.exit("no rows with posted_at + platform")
    if a[0] == "report":
        print(report(rows))
    elif a[0] == "calendar":
        start = dt.date.fromisoformat(opt("--start", str(dt.date.today() + dt.timedelta(days=1))))
        print(calendar(rows, opt("--profile"), start, int(opt("--weeks", 2)), int(opt("--per-week", 3)),
                       opt("--time", "18:00"), opt("--ics")))
    else:
        sys.exit(__doc__)
