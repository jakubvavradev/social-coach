# Platforms: signals, specs, suppression

No platform publishes ranking weights or thresholds. Below, **[official]** marks statements from the platform or its head, and **[3rd-party]** marks estimates from blogs and tools. Present each with that label.

## TikTok
**How distribution works:** a video is tested on a small pool and moves to larger pools if it performs. There are separate systems for For You, Search and Following. Follower count is not a direct factor [3rd-party, consistent with TikTok's public position].
**Signals, roughly by weight [3rd-party consensus]:** watch time and completion > rewatches > shares > comments and saves > likes.
**Heuristics [3rd-party, conflicting]:** completion ~35 % to pass the first pool, 70 %+ for viral; rewatch rate 15–30 % is strong.
**Search / SEO:** TikTok works as a search engine. Say the keyword out loud, put it in the on-screen text, and put it in the first line of the caption.
**For You eligibility [official, Community Guidelines "FYF eligibility"]:** content can stay on the platform but not be recommended. Unoriginal or reposted content without creative edits, other-app watermarks, low-quality minimally edited clips, and repeated violations make the whole account temporarily ineligible.
**Specs:** 9:16, 1080×1920. Most edits sit in 10–60 s; up to 10 min upload. The web uploader is sometimes picky about size and needs re-encoding (use the profile's note if there is one). Captions up to 4,000 characters. Use 3–5 relevant hashtags.
**Tools:** TikTok Studio analytics (retention graph, % watched full video, traffic sources, search terms). Creative Center for trends.

## Instagram Reels
**Top signals [official, Mosseri, Jan 2025]:** watch time, likes, **sends**. Track average watch time, likes per reach and sends per reach. Sends weigh more for reaching non-followers; likes weigh more with followers.
**Originality [official]:**
- Eligible for recommendation means: original, no visible watermarks, follows Community Guidelines and Recommendation Guidelines.
- **Apr 30, 2026:** accounts that *mostly* post unoriginal content (Reels, photos, carousels) are removed from recommendations. Followers still see them.
- Status shows in **Settings → Account Status**, where you can remove posts or appeal. Eligibility returns ~30 days after the last unoriginal post.
**Hashtags:** Mosseri said they don't really drive reach. Use 3–5 specific ones; keywords in the caption, on-screen text and speech matter more for search.
**Trial Reels [official feature]:** shown only to non-followers for 24–72 h, then you share it or archive it. Needs a public professional account with ≥1,000 followers. Use it to A/B test hooks, one variable per test, with tests ≥24 h apart.
**Specs:** 9:16, 1080×1920, up to 3 min in feed recommendations (shorter usually performs better). The first ~125 caption characters are visible before "more". Hold the cover frame in mind for the grid (center 3:4 crop).
**Insights:** views, accounts reached (followers vs non-followers), average watch time, skip rate (IG labels it vs typical), sends, saves, profile activity, follows.

## YouTube Shorts
**Key feed metric [official, Studio]:** "Viewed vs. swiped away". Heuristics [3rd-party]: below 30–50 % viewed the video stalls, 70 %+ it expands, 80 %+ is typical of viral.
**APV (average percentage viewed):** 70 %+ is excellent; over 100 % happens with loops [3rd-party].
**Views:** since 2025 a "view" counts every start. Monetization uses engaged views, so headline views can rise while swipe-away gets worse.
**Specs:** vertical or square, up to 3 min (since Oct 2024). Music from the library may cap length at 60 s, but sources conflict, so check in the app. Use a related-video link to lead viewers to long-form.
**Strategy:** Shorts work as discovery. Link each Short to a long video on the same topic. Subscribers from Shorts watch less long-form unless the topics match.

## X and Threads (text-first)
Native video autoplays muted, so text on screen is essential. Replies and conversation drive reach; an outbound link in the main post often reduces it (put the link in a reply). Threads is a teen-restricted surface on some accounts, so respect the restrictions and don't bypass them.

## Safe zone (9:16, 1080×1920 px) [3rd-party measurements, union of platforms]
- Keep important content inside **x 60–930, y 220–1540**.
- The top ~220 px holds tabs and the search bar. The bottom ~380 px holds the caption, music and username. The right ~150 px holds the like/comment/share icons.
- A cross-platform box of 900×1400 px, centered, is a simpler rule.
- `analyze.py` draws these red zones. Check the real result in a draft or preview, because UI layouts change.

## Audio loudness
Mix to about **−14 LUFS integrated, true peak ≤ −1 dBTP** [3rd-party consensus; platforms normalize but publish no target]. Too quiet sounds weak next to the videos around it; too hot gets squashed or clips after transcoding.

## Suppression checklist (reach suddenly dropped)
1. IG **Account Status** / TikTok **account check** / YT **copyright and community strikes**: are there any flags?
2. Was anything posted recently that is unoriginal (another app's watermark, reposts, reused clips)?
3. A copyright or music claim that muted the video?
4. Spam-like behavior: mass follows or unfollows, repeated identical comments, link spam, third-party automation or "growth" apps?
5. Did the format change (longer, different topic)? Compare retention with your own median. Most "shadowbans" are really just weaker videos.
6. Normal variance: one flop is noise. Judge a trend over 5+ posts.
