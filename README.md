<div align="center">

# 🎬 social-coach

**A blunt short-form video coach for Claude Code.**
It measures what scripts measure well, looks at what only eyes can judge, and grounds every claim in sourced research.

TikTok · Instagram Reels · YouTube Shorts · X · Threads

![license](https://img.shields.io/badge/license-MIT-blue) ![claude code](https://img.shields.io/badge/Claude%20Code-skill%20%2B%20agent-orange) ![deps](https://img.shields.io/badge/deps-python3%20%2B%20ffmpeg-green)

</div>

---

## Why

Most "make it go viral" prompts produce generic advice: "hook in the first 3 seconds!" social-coach does more:

- **Measures** the video: loudness in LUFS and true peak, silence at the start, hard cuts, frozen and black frames, how well the end loops into the start, and whether the content sits in the 9:16 safe zone.
- **Looks** at it: a 12-frame hook sheet of the first 3 s, overlays of the areas the app UI covers, and a frame every 2 s.
- **Scores** it on a 9-area, 100-point rubric with anchors, then gives the **top 3 fixes with timestamps and exact replacement text**.
- **Knows your account**: a creator profile holds your hard rules and learnings from your own analytics, and those override generic advice.
- **Guards your brand**: every review and every graphic is checked against your brand kit (colours, contrast, one accent, legibility at feed size) without you asking.
- **Labels its evidence**: each benchmark is tagged as official or a third-party estimate, with sources.

## What it does

| Mode | Ask | You get |
|---|---|---|
| 🎯 **Pre-flight review** | "rate this video" + `.mp4` | Verdict card: score, top 3 fixes, 3 hook variants, drop-off prediction, caption |
| 🔬 **Post-mortem** | "why did this flop?" + stats | Diagnosis (distribution / hook / retention / conversion), the frame where viewers left, one fix and one test |
| 📈 **Trend scout** | "what's trending, what should I film?" | 3–5 trend cards with evidence ≤7 days old, stage, your twist, hook text, shoot-by date |
| 🧭 **Growth coach** | "how do I grow / why did reach drop?" | Concrete routine with numbers, suppression checklist, red lines |
| ♟️ **Strategy** | "make me a content strategy" | Positioning, one goal with a KPI taken from your baseline, pillar mix, series, funnel |
| 🎨 **Brand & graphics** | "brand colors", "make a thumbnail" | Brand kit tokens (sampled from your existing work), contrast checks, rendered thumbnails, covers and carousel slides |
| 📅 **Stats & calendar** | "evaluate my stats", "posting calendar" | Report (baselines, winners/flops, pillar/length/slot breakdowns, funnel) plus a 2-week calendar weighted by performance, with `.ics` |

## Example

```
VERDIKT: POSTNOUT PO OPRAVÁCH — 75/100
Hook 20/25 · Retence 14/20 · Text 8/10 · Payoff+smyčka 6/10 · Sdílitelnost 7/10 · Audio 8/10 · CTA 2/5 · Tech 5/5 · Originalita 5/5

TOP 3 OPRAVY
1. [0:04–0:07] Control-centre shot has no text and nothing new → cut to 1 s or add "the hinge is invisible 👀"
2. [0:11] CTA "would you buy one?" has no stakes → "would you pay $X / €Y for this?"
3. [end] Ends on the lock screen → end on the fold again so it loops
```
The full real run is in [`examples/review-iphone-duo.md`](examples/review-iphone-duo.md). Its fix #1 lands on the exact second where the published video's analytics later showed viewers dropping off.

## Install

**As a plugin**
```bash
claude plugin marketplace add jakubvavradev/social-coach
claude plugin install social-coach@social-coach
```

**Or manually**
```bash
git clone https://github.com/jakubvavradev/social-coach
ln -s "$PWD/social-coach/skills/social-coach" ~/.claude/skills/social-coach
ln -s "$PWD/social-coach/agents/social-coach.md" ~/.claude/agents/social-coach.md
```
Requirements: `python3` (+ Pillow for brandcheck) and `ffmpeg`/`ffprobe`; `google-chrome`/`chromium` for covers. Whisper is optional, for transcripts.

**First run:** the skill copies `profile.example.md` to `~/.claude/social-coach/profile.md` and asks 6 questions (handle, pillars, audience, posting time, hard rules, max length). Your profile stays outside the repo.

## Usage

```text
> ohodnoť ~/Videos/my-short.mp4
> why did my last reel flop? [screenshot]
> what's trending in tech this week?
> use the social-coach agent to review all videos in ~/Videos/batch/
```

Standalone analyzer:
```bash
python3 skills/social-coach/scripts/analyze.py video.mp4 out/ --max-len 15
python3 skills/social-coach/scripts/analyze.py --selftest

python3 skills/social-coach/scripts/stats.py report posts.csv
python3 skills/social-coach/scripts/stats.py calendar posts.csv --profile profile.md --weeks 2 --per-week 3 --ics plan.ics
python3 skills/social-coach/scripts/cover.py --text "I built my *own TV*" --sub "📺 built with AI" --pill "OPEN SOURCE" \
        --image frame.jpg --format 16x9 --accent "#ffd06a" --out thumb.png
```

<p align="center"><img src="examples/thumb-16x9.png" width="49%"> <img src="examples/cover-9x16.png" width="22%"></p>

## Layout

```
.claude-plugin/          plugin + marketplace manifest
agents/social-coach.md   subagent (read-only advisor)
skills/social-coach/
  SKILL.md               routing, workflows, output contracts
  profile.example.md     creator profile template
  scripts/analyze.py     measuring pass (stdlib + ffmpeg, self-test)
  scripts/stats.py       post-log report + data-driven calendar + .ics (stdlib, self-test)
  scripts/cover.py       on-brand thumbnails / covers / carousel slides (headless Chrome)
  scripts/brandcheck.py  brand guard: palette vs kit (ΔE), WCAG contrast, feed-size preview
  references/
    rubric.md            9 areas, anchors, flag → deduction map
    hooks.md             14 hook types, 40 templates, text rules
    platforms.md         signals, specs, safe zones, suppression per platform
    analytics.md         metrics, benchmarks, diagnosis tree, testing protocol
    trends.md            8 sources, stage model, twist framework, trend card
    growth.md            posting routine, engagement, profile, red lines, safety
    strategy.md          positioning, goal → KPI, pillars, funnel, quarterly review
    brand.md             brand kit tokens, contrast, templates, voice, brand audit
    calendar.md          post-log schema, stats loop, calendar rules, weekly review
    sources.md           every source with A/B/C confidence
examples/                real outputs
evals/scenarios.md       behaviour tests for the skill
```

## Principles

1. **Your data beats benchmarks.** No platform publishes ranking weights. Third-party thresholds are labelled as estimates.
2. **Measure, then look.** The JSON flags are leads that get confirmed or dismissed by eye, never scored blindly.
3. **Fixes must be executable:** a timestamp, the change, and the exact text.
4. **Never game the platform.** The coach is read-only and never suggests follow/unfollow, pods, bots or reposting.

## Contributing

Platforms change monthly. PRs that update `references/` with a dated, sourced claim are the most valuable kind. Run `evals/scenarios.md` before and after changing the skill.

## License

MIT
