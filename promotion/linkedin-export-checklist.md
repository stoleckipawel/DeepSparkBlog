# LinkedIn Promo Export Checklist (Frame Graph Series)

## Export Settings
- Canvas: `1080x1350` (4:5) per slide
- Format: `PNG`
- Color profile: `sRGB`
- Compression: lossless/high quality
- Naming: `fg-post{1..5}-slide{1..6}.png`

## Visual QA (must pass)
- Hook readable in 1 second at phone-feed size
- One dominant focal element per hook slide
- No tiny text that requires zoom/squint
- Contrast works in bright-mode mobile viewing
- Shared visual system kept consistent across posts

## Messaging QA (must pass)
- Slides 1–2 are benefit-first
- Tone is plain dev-to-dev (no marketing fluff)
- Includes priority order in early slides:
  - Memory
  - GPU time
  - Stalls/stability
  - Dev time
  - Bugs/reliability
- CTA includes:
  - "link in first comment"
  - discussion prompt

## Claim Qualification Rules
- Use `up to` for variable outcomes (e.g., memory reduction)
- Add short caveat where relevant: "depends on workload/hardware"
- Avoid absolute guarantees for async/split-barrier perf gains

## Final Pre-Publish Pass
- Verify per-post slide count is exactly 6
- Check slide numbers match (`1/6` to `6/6`)
- Re-read first hook aloud: sounds like a normal dev, not ad copy
- Verify references to memory/perf/stability/productivity are explicit
- Confirm first-comment link is ready before posting
