# Content strategy

A strategy is a set of choices about who the account is for, what it promises, and what it will *not* post. Review it every quarter, or after 30 posts, using `stats.py report`.

## 1. Positioning (one sentence)
`For <audience> who want <desire>, I'm the <creator type> who <unique proof>.`
- *Unique proof* is something only this creator can show, such as finished projects, real data, access, or a skill.
- Test: if a bigger account could post the same sentence, sharpen it.
- Turn the sentence into the bio, the pinned posts, and the first line of every About section.

## 2. Goals → KPIs (pick ONE primary goal per quarter)
| Goal | Primary KPI | Secondary | Content bias |
|---|---|---|---|
| Discovery (new account) | non-follower reach, viewed vs swiped | shares/sends | trends with a twist, short and broad hooks |
| Community | follows per 1k views, returning viewers | comments, DMs | series, behind the scenes, replies to comments |
| Conversion (app installs, GitHub stars, sales) | link clicks, installs | profile visits | demos, problem → solution, social proof |
| Authority | saves, long-form watch time | search traffic | tutorials, breakdowns, data |
Set numeric targets from your **own baseline** (`stats.py report`), for example "median views +50 %" or "follows per 1k views from 0 to 2". Don't set targets from other creators' numbers.

## 3. Content pillars (3–5)
Each pillar needs: a theme, assets you actually have, the formats it suits, and a planned share of posts.
- One **discovery** pillar (broad appeal or trends). One or two **core** pillars (your proof). One **conversion** pillar (product or project).
- Re-weight shares quarterly from performance. `stats.py calendar` already scales the profile's shares by each pillar's measured index (clamped 0.5–2×, n≥3).
- Drop a pillar that stays under 0.5× for 10+ posts unless it serves the conversion goal.

## 4. Formats and series
- Have 2–3 **repeatable formats** per pillar (e.g. "first look in 10 s", "$ vs $$", "day N of building X"). Repeating formats lowers production cost and teaches the audience what to expect.
- A **series** with a number gives people a reason to follow. Put the series name on the cover and in the first line of the caption.

## 5. Funnel (each platform has a job)
```
Shorts/Reels/TikTok (discovery) → profile (promise + pinned) → long-form / GitHub / app (depth, conversion) → community (comments, DMs, X/Threads)
```
Each short should point to one next step that fits that funnel. Don't send every viewer to the link in bio.

## 6. Quarterly review checklist
1. `stats.py report` → which pillar, length, format and slot beat the median? (n≥3, otherwise it's a hypothesis)
2. Funnel: views → profile visits → follows. Where is the biggest leak?
3. Keep / kill / test: keep 1 thing, kill 1 thing, test 1 new format.
4. Update the profile: pillar shares, hard rules, learnings, KPI targets.
5. Plan the next 4 weeks with `stats.py calendar`.

## Output: strategy one-pager
```
POZICE: …
CÍL Q: … (KPI: … z … na …)
PILÍŘE: A 30 % · B 25 % · C 20 % · D 15 % · E 10 %  (změna oproti minule: …)
FORMÁTY/SÉRIE: …
FUNNEL: short → … → …
NECHAT / ZABÍT / TESTOVAT: … / … / …
```
