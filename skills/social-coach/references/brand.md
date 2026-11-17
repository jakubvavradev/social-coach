# Brand identity: visual + verbal

People recognise a brand before they read it, so every cover, thumbnail and text overlay should be identifiable as yours with the handle hidden. Store the tokens in the profile's `## Brand kit`. `cover.py` reads them from there.

## 1. Brand kit (tokens)
| Token | Rule |
|---|---|
| `bg` | One base background, usually near-black or off-white. Dark makes accents pop on phone feeds. |
| `text` | The main text color, with contrast ≥ 7:1 against `bg`. |
| `muted` | Secondary text, contrast ≥ 4.5:1 (WCAG AA). |
| `accent` | **One** default highlight color, used on the 1–2 words that carry the hook. |
| `pillar accents` | Optional: one accent per pillar or product, so viewers learn "yellow = TV, green = cars". Never two accents in one graphic. |
| `font` | One heavy display grotesk (headline, weight 800–900, tight tracking) + one UI weight (600) for subs. Max 2 weights per graphic. |
| Signature elements | 1–3 recurring devices: the accent word, a pill badge, an emoji prefix on the sub line, the logo corner. |

Check contrast before you adopt a color. Luminance ratio = (L1+0.05)/(L2+0.05). Yellow, green and orange on near-black all pass easily; blue and red on black often fail for small text.

## 2. Graphic templates (`scripts/cover.py`)
| Asset | Size | Layout |
|---|---|---|
| YT thumbnail | 1280×720 | Text left (≤6 words, 2–3 lines), subject right, tilted with a shadow. Must read at 160 px wide. |
| Short / Reel / TikTok cover | 1080×1920 | Text at the top inside the safe zone (y 260+), subject in the middle. Center the 3:4 grid crop. |
| Carousel slide | 1080×1350 | Slide 1 = hook cover. Slides 2–n = one idea each, same margins. Last slide = CTA. |
| End card / pinned comment image | 1080×1920 | Series name + "part N" + one CTA. |
Rules: one focal subject, ≤6 words, an accent on the stakes word, no spoiler of the result (curiosity or stakes instead), and faces or hands make the subject feel human.

## 3. Video brand layer (in-video)
- The same caption style in every video (font, size, stroke or box, position).
- The same text color system as the covers (white + accent word).
- An optional 0.3 s signature sound or transition, used consistently or not at all.
- Never a logo intro. The brand shows through style, not through a 2 s logo that costs you the hook.

## 4. Verbal identity (voice)
- 3 voice attributes with "this, not that", e.g. *curious, not hype* · *concrete, not vague* · *friendly, not cringe*.
- Write a vocabulary list: words you use and words you never use.
- For a deep voice doc, **use `brand-voice`**. For a full logo or identity system, **use `brand-identity`**.

## 5. Consistency checklist (brand audit)
Score 0–2 each: same handle + avatar everywhere · bio follows the positioning · covers recognisable without the name · max 1 accent per graphic · caption style consistent · pinned posts on-brand · color use matches the kit. **12+/14 = consistent.**

## 6. Automated check
`scripts/brandcheck.py` puts the mechanical half of the audit on every graphic: palette vs kit tokens (ΔE76 ≤15 on-kit, >30 off-kit), WCAG contrast of text/accent on the dominant colour, more than one accent, and a 160 px feed preview. The judgement half (font, caption style, spoilers, privacy) stays manual. See SKILL.md → Brand guard.

## 7. Deriving a kit from existing work
When a creator already has covers, sample them first. Don't invent a new style, codify what's already working. Take pixel values from the background, headline, accent words and badges, measure the contrast, and write the tokens into the profile.
