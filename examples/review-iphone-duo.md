# Example: pre-flight review (real run, 2026-11-17)

Input: `iphone-duo.mp4`, 12.8 s, 1080×1920, 30 fps. Command:
`python3 scripts/analyze.py iphone-duo.mp4 rv --max-len 15`

Measured: −14.4 LUFS, true peak −4.9 dBFS, no leading silence, 1 hard cut (10.93 s), no freezes, loop SSIM 0.39.
Flags: `hook: first hard cut at 10.93 s` and `pacing: longest shot 10.93 s`. **Dismissed after looking at the frames:** it is one continuous handheld take with the phone moving the whole time and text beats at 0 / 2.75 / 7 / 9 / 11 s.

---

```
VERDIKT: POSTNOUT PO OPRAVÁCH — 75/100
Hook 20/25 · Retence 14/20 · Text 8/10 · Payoff+smyčka 6/10 · Sdílitelnost 7/10 · Audio 8/10 · CTA 2/5 · Tech 5/5 · Originalita 5/5

TOP 3 OPRAVY (podle dopadu)
1. [0:04–0:07] Záběr na ovládací centrum nemá text ani novou informaci, tady lidi odpadnou.
   → Zkrátit na 1 s, nebo přidat text "the hinge is invisible 👀". Celé video tím klesne na ~10 s.
2. [0:11–0:12.8] CTA "would you buy one?" nemá o co hrát (0 komentářů).
   → "would you pay $X / €Y for this?" (USD+EUR, ověřit oficiální cenu). Lidi rádi odpoví ano/ne.
3. [konec] Video končí zamčenou obrazovkou, takže se neopakuje.
   → Skončit znovu na přehnutí, které je na snímku 0. Smyčka zvýší rewatch.
CO NECHAT: přehýbání telefonu hned od snímku 0 (tohle je ten money shot) a text "it folds" na 2,75 s
HOOK TEXT – 3 varianty: "it folds in half 🤯" (výsledek) · "would you pay $X for this?" (otázka) · "first time holding the iPhone Duo" (novinka, současný)
PREDIKCE (odhad): propad 0:04–0:07, potom stabilní do konce
BRAND: ⚠️ bílý text na světlém pozadí obchodu má kontrast 3,0:1 → přidat černý obrys nebo tmavý podklad
CAPTION: "first time holding the iPhone Duo 📱 would you pay $X / €Y? 🎵 Cloud 9 (NCS)" + iphone duo, foldable iphone, apple foldable
```

Other notes: the price tag in the background shows CZK. That's fine as background, but don't repeat CZK in text or captions (profile rule). The hook text sits right at the top edge of the safe zone (y ≈ 230 px), so moving it down ~60 px makes it safer.

**Check against reality:** this video was the account's best performer, and IG reported its skip rate as better than typical. The sag the analytics measured at 0:04–0:07 is the same stretch this review ranks as fix #1. The CTA problem matches the measured 0 comments.
