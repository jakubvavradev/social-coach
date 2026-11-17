# Analytics & post-mortem

## What to ask for (screenshots are fine)
| Platform | Metrics |
|---|---|
| TikTok | views, avg watch time, % watched full video, retention graph, rewatches (if shown), shares, saves, comments, traffic source (For You / Search / Profile / Following), new followers |
| IG Reels | views, reach (followers vs non-followers), avg watch time, skip rate, retention graph, sends, saves, likes, comments, profile visits, follows |
| YT Shorts | views, viewed vs swiped away %, APV, avg view duration, retention graph, subscribers gained, traffic source |

Always compute **ratios**, not totals: sends/reach, likes/reach, follows/profile visits, profile visits/reach. Compare against **the creator's own median of the last 5–10 posts**. If there are fewer than 5 posts, say the baseline is weak.

## Benchmarks [3rd-party heuristics, label them as such]
| Metric | Weak | OK | Strong |
|---|---|---|---|
| YT viewed vs swiped | <50 % | 60–70 % | 75–80 %+ |
| YT APV (Shorts) | <50 % | 70 % | 90–100 %+ |
| TikTok % watched full | <10 % | 15–25 % | 35 %+ |
| IG skip rate | above typical | ~typical | below typical (IG labels it) |
| Hook / 3-s rate | <20 % | 25 % | 30–40 %+ |
| Avg watch / length | <40 % | 50–70 % | >80 % or loops |
| Profile visit → follow | <5 % | 10 % | 20 %+ |
Engagement rate depends a lot on account size; prefer the creator's own trend.

## Diagnosis tree
```
Low views?
├─ Viewed/swiped or skip rate bad → HOOK problem (frame 0, text, sound)  → fix rubric §1/§3
├─ Hook fine, retention falls off a cliff at second X → open analyze frame at X → that shot is the cause (no text, no change, payoff too late) → rubric §2
├─ Retention fine, few shares/sends → no SEND trigger → rubric §5, change topic angle
├─ Good metrics but reach stops at ~followers → distribution: unoriginal flag? posted at a dead hour? topic too narrow? → platforms.md suppression checklist
Good views, no follows?
└─ CONVERSION problem: CTA weak, profile doesn't promise a series, no pinned posts → growth.md §Profile
```

## Drop-off reading
- An early drop at 0–1 s is normal. Judge it against the platform's "typical" when one is shown.
- A **cliff** (steep drop) means a specific moment failed. Map the second to a frame.
- **Bumps** (the graph rising) mean rewatch moments. Do more of what is on screen there.
- A plateau to the end means the hook promise was good; the loop or the ending decides the rewatches.

## Learning log (write to profile `## Learnings`)
Format: `YYYY-MM-DD · video · platform · metric that moved · cause · rule (n=…)`. Treat a rule from fewer than 3 videos as a hypothesis.

## Testing protocol
Change one variable (hook text, first shot, length, sound, posting time). Post comparable content ≥24 h apart. Read results at 48 h and 7 d against your own median. On IG with 1k+ followers, use Trial Reels for hook A/B tests.
