# Posting calendar & stats loop

## The loop (weekly)
```
log posts → stats.py report → decide (keep/kill/test) → stats.py calendar → fill ideas (trends.md) → film → pre-flight → post → log
```

## 1. Post log: `~/.claude/social-coach/posts.csv`
One row per post **per platform**. Headers (order doesn't matter, blanks are OK):
`posted_at, platform, title, pillar, format, length_s, views, reach, avg_watch_s, completion_pct, likes, comments, shares, saves, follows, profile_visits, note`
- `posted_at` is local time, `YYYY-MM-DDTHH:MM`. Without the time, time slots can't be learned.
- `pillar` uses names that match the profile pillars (prefix matching is fine).
- Log metrics **at a fixed age**, ideally 7 days. Mark early snapshots in `note`.
- Sources: YouTube via the API (`snippet,statistics,contentDetails`). IG and TikTok from the insights screens: read the user's screenshots and transcribe exact numbers only, never estimate.
- Keep long-form separate (`youtube-long`), so long videos don't distort the Shorts medians.

## 2. Evaluate: `python3 scripts/stats.py report posts.csv`
It gives: a per-platform baseline (medians), winners and flops by **index** (views ÷ the platform median), breakdowns by pillar, format, length, weekday and time slot, the funnel, and automatic findings.
How to read it:
- Index ≥2× = winner. Study it in post-mortem mode and repeat its format.
- Index ≤0.5× = flop. Is it hook, retention or topic? (`analytics.md` tree)
- Groups with n<3 are **hypotheses**, so say "low n" out loud. Moving the posting day or time needs n≥5 per slot.
- Compare platforms by ratios (watch %, shares/reach, follows/reach), not by raw views.

## 3. Plan: `python3 scripts/stats.py calendar posts.csv --profile profile.md --weeks 2 --per-week 3 --ics plan.ics`
- **Days:** the best weekdays from the data (n≥5), otherwise a spread default (3/week = Tue, Thu, Sun).
- **Time:** the best 3-hour slot from the data (n≥5), otherwise `--time` or the profile's posting time.
- **Pillars:** profile shares × measured pillar index (clamped 0.5–2×, n≥3), rotated in proportion.
- `.ics` imports into Google or Apple Calendar. Each event reminds you of the pre-flight → post → 60-min reply routine.
Then fill in the Idea + Hook columns from a trend scout and the backlog. Every slot gets a concrete video, not just "robots".

## 4. Cadence rules
- Pick a sustainable number (3/week beats 7/week followed by burnout). Keep 3–5 finished videos in the backlog.
- Same time slot. The audience learns it, and your comparisons stay clean.
- Space similar posts ≥24 h apart so they don't cannibalise each other.
- Newsjacking can override the calendar: a launch or trend in the 24–72 h window beats a planned evergreen post. Move the planned one back.
- Cross-post the same video natively to every platform the same day. Stagger by platform only if the data shows different peak times.

## 5. Weekly review (15 min, Sunday)
1. Update `posts.csv` with 7-day numbers.
2. Run `stats.py report` and pick 1 keep, 1 kill, 1 test.
3. Add a dated learning to the profile (with n).
4. Run `stats.py calendar` for the next 2 weeks and fill in the ideas.
