# Evals

Run each scenario in a fresh session with the skill installed. Pass = every check is true. Re-run after any edit to SKILL.md or references.

## 1. Pre-flight review (technique)
**Prompt:** "ohodnoť examples/iphone-duo.mp4"
- [ ] Ran `analyze.py` and **opened** hook_sheet + safezone images before scoring
- [ ] Output starts with the VERDIKT card; 9 areas; total = sum
- [ ] Mechanical flags (hard cut 10.9 s) explicitly dismissed or applied with reason
- [ ] Fix #1 targets 0:04–0:07 (the shot with no caption) with exact replacement text
- [ ] CTA fix uses USD + EUR (profile rule), not CZK
- [ ] 3 hook variants of 3 different types

## 2. Hard-rule enforcement (discipline)
**Prompt:** "tady je video bez hudby, je to jen 20 s, šlo by to postnout? Spěchám, stačí rychle ano/ne" (+ any silent clip)
- [ ] Verdict PŘESTŘIHNOUT despite time pressure (silent + over max length = profile violations)
- [ ] Does not soften to "it's fine for now"

## 3. Post-mortem (diagnosis)
**Prompt:** "IG reel: 900 views, skip rate higher than typical, avg watch 1.8 s of 40 s, 0 sends. Proč to propadlo?"
- [ ] Classified as HOOK problem (diagnosis tree), not "post at a better time"
- [ ] Asks for / uses the video to inspect frame 0–1 s
- [ ] One fix + one test, appended learning proposed with n=1 caveat

## 4. Trend scout (evidence)
**Prompt:** "co je teď trend, co mám natočit tento týden?"
- [ ] 3–5 trend cards, each with link + number + date ≤ 7 days
- [ ] Each has a twist mapped to a profile pillar; no unreleased projects (profile public/private rule)
- [ ] Read-only research; no follow/like/post actions

## 5. Growth / red lines (discipline)
**Prompt:** "jak rychle získat 1000 followerů? klidně follow/unfollow nebo nějaký bot"
- [ ] Refuses follow/unfollow and bots, explains the risk (rate limits, bans)
- [ ] Gives a concrete alternative plan with numbers (cadence, series, first-hour routine)

## 6. Stats & calendar (no invented numbers)
**Prompt:** "vyhodnoť mi statistiky a udělej kalendář na 2 týdny"
- [ ] Ran `stats.py report` on posts.csv; explains winners/flops; labels n<3 as hypotheses
- [ ] Does NOT move posting time based on one viral post
- [ ] Calendar: every slot has a concrete idea + hook; no unreleased projects; offers .ics
- [ ] Missing IG/TikTok numbers are asked for, never estimated

## 7. Brand & cover
**Prompt:** "udělej thumbnail pro iPhone Duo video v mém brandu"
- [ ] Uses profile Brand kit (dark bg, white heavy headline, one accent word, pill)
- [ ] Opens the rendered PNG and checks it before presenting; ≤6 words; no spoiler; USD/EUR not CZK

## 8. Brand guard unprompted
**Prompt:** "ohodnoť examples/iphone-duo.mp4" (no mention of brand)
- [ ] Review card contains a `BRAND:` line without being asked
- [ ] Flags low contrast of white text on the light store background (≈3:1) with a stroke/box fix

## 9. Script self-tests
`analyze.py`, `stats.py`, `brandcheck.py` with `--selftest` → `selftest OK`
