# Twitter/X Promo Plan &mdash; Frame Graph Series

> **Date:** March 4, 2026 (Day 1)
> **LinkedIn goes live:** 8:12 AM (your timezone)
> **Twitter starts:** staggered after LinkedIn (see schedule below)

---

## Platform Differences: LinkedIn vs Twitter/X

| | LinkedIn | Twitter/X |
|---|---|---|
| **Image ratio** | 4:5 portrait (1080&times;1350) | 16:9 landscape (1600&times;900) or 1:1 (1080&times;1080) |
| **Carousel** | Native carousel (up to 20 slides) | Thread with 1 image per tweet, or single tweet with up to 4 images |
| **Text length** | 3000 chars | 280 chars (or 25K with X Premium) |
| **Hashtags** | 3&ndash;8 at bottom | 2&ndash;3 max, inline or at end |
| **Link behavior** | First comment trick | Link in reply (or in post, but kills engagement) |
| **Audience** | Senior engineers, tech leads, hiring managers | Broader gamedev/graphics community, indie devs, engine hobbyists |
| **Tone** | Professional, detailed | Punchy, direct, slightly informal |

---

## Image Adaptation Strategy

### Export Settings
- **Canvas:** `1600x900` (16:9) for thread banners, `1080x1080` (1:1) for standalone
- **Format:** PNG, sRGB
- **Naming:** `fg-tweet{N}-1600x900.png`

### What to Change from LinkedIn Slides

| LinkedIn slide | Twitter adaptation | Why |
|---|---|---|
| Slide 1 (Hook: 50%) | **Thread banner image** &mdash; same 50% hero stat, but landscape, text larger, remove "Swipe &rarr;" | 16:9 fills timeline better, no swipe mechanic |
| Slide 2 (What this fixes) | **Tweet 2 image** &mdash; 2&times;2 grid of the 4 benefit cards only (drop Reliability row), text 30% larger | Must be readable in Twitter's smaller image preview |
| Slide 3 (Architecture) | **Tweet 3 image** &mdash; Declare &rarr; Compile &rarr; Execute bar, full width, drop the long sub-text | Horizontal layout works better in 16:9 |
| Slide 4 (Sound familiar?) | **Tweet 4 image** &mdash; 4 pain-point bullets stacked, "Frame graphs fix all four" punchline bigger | Direct conversion; quotes read well as image text |
| Slide 5 (The Series) | **Tweet 5 image** &mdash; 4-part roadmap as horizontal timeline instead of vertical list | Natural 16:9 layout |
| Slide 6 (CTA) | **No image** &mdash; text-only CTA tweet with link | Link tweet at the end of thread works on Twitter |

### CSS Overrides for Twitter Export

Add a `.twitter-slide` variant class with these differences from `.slide`:

```css
/* Twitter 16:9 landscape */
.slide.twitter-slide {
  aspect-ratio: 16 / 9;
  width: 1600px;
  height: 900px;
  padding: 3em 4em;
  flex-direction: row;          /* side-by-side layout where needed */
  justify-content: center;
  align-items: center;
  text-align: center;
}
.twitter-slide .hook {
  font-size: clamp(2.2rem, 3vw, 3rem);  /* 30% larger for small preview */
}
.twitter-slide .hero-metric .value {
  font-size: clamp(6rem, 8vw, 9rem);
}
.twitter-slide .micro { display: none; }  /* no "Swipe" on Twitter */
```

---

## Posting Schedule &mdash; Day 1

The idea: **LinkedIn first, Twitter thread 30 min later** so you can reference "just posted on LinkedIn" and cross-pollinate.

| Time | Platform | Action |
|---|---|---|
| **8:12** | LinkedIn | Publish Post 1 carousel (6 slides) + post text + first-comment link |
| **8:15** | LinkedIn | Add first comment with series link |
| **8:42** | Twitter/X | Publish thread (see below) |
| **12:00** | Twitter/X | Quote-retweet your own thread hook with a different angle |
| **18:00** | Twitter/X | Reply to your thread with engagement prompt |

---

## Twitter Thread Content

### Tweet 1 &mdash; Hook (with image)
**Image:** 16:9 banner &mdash; "50% LESS TRANSIENT VRAM" + "FRAME GRAPH SERIES"

```
Frame graphs can cut transient VRAM in half.

Fewer GPU stalls. Less crashes. Faster iteration.

Here's why every renderer should have one &mdash; thread 🧵

🔗 stoleckipawel.dev/posts/series/frame-graph
```

**Hashtags:** `#gamedev #rendering`

---

### Tweet 2 &mdash; What this fixes (with image)
**Image:** 2&times;2 benefit grid (Memory / GPU Performance / Productivity / Stability)

```
What a frame graph compiler actually gives you:

&bull; Memory &mdash; resource aliasing reclaims VRAM across passes
&bull; GPU perf &mdash; split barriers + async compute reduce stalls
&bull; Productivity &mdash; compiler orders passes and places barriers
&bull; Stability &mdash; dependency tracking catches bugs at build time
```

---

### Tweet 3 &mdash; How it works (with image)
**Image:** Declare &rarr; Compile &rarr; Execute pipeline bar

```
The core model is 3 phases:

1. Declare &mdash; register passes + resources
2. Compile &mdash; sort, cull, alias, sync
3. Execute &mdash; record GPU commands

You describe intent once. The compiler handles scheduling.
```

---

### Tweet 4 &mdash; Pain points (with image)
**Image:** 4 pain-point quotes with red X marks

```
Sound familiar?

&cross; "We're out of VRAM &mdash; again"
&cross; "Why did frame time spike?"
&cross; "Adding a pass broke three others"
&cross; "Device lost &mdash; no repro"

Frame graphs fix all four with one abstraction.
```

---

### Tweet 5 &mdash; Series roadmap (with image)
**Image:** 4-part horizontal timeline

```
I wrote a 4-part deep dive:

I. Theory &mdash; why pacing, stability, and memory improve
II. Build It &mdash; 3 C++ iterations, prototype to MVP
III. Beyond MVP &mdash; async compute, split barriers
IV. Production &mdash; UE5/Frostbite-scale patterns

Each builds on the last.
```

---

### Tweet 6 &mdash; CTA (no image)

```
Full series is live.

Start with Part I (Theory, ~20 min read) &mdash; it sets up everything else.

🔗 stoleckipawel.dev/posts/series/frame-graph

What's the hardest part of render graph implementation you've hit? Barrier debugging? Aliasing edge cases?
```

---

## Twitter-Specific Tips

### Thread Mechanics
1. **Write the full thread in advance** using a thread composer (Typefully, or Twitter's own draft threads)
2. **Post all tweets within 60 seconds** of each other &mdash; a thread that trickles in looks broken
3. **Number your images** visually (1/5, 2/5...) so readers know there's more even if they see a single tweet shared out of context
4. **Put the link in Tweet 1 AND Tweet 6** — Tweet 1 has the highest impression count, Tweet 6 is where readers land after the thread. The URL is baked into every slide image as a subtle watermark too, so even if someone screenshots a single slide, the URL is visible
5. **Self-reply with link** in addition — reply to the hook tweet with just the bare URL for easy click-through

### Engagement Tactics
- **Quote-retweet your own hook at noon** with a single pain-point angle: *"If 'device lost &mdash; no repro' gives you flashbacks, the series explains exactly how frame graphs prevent it"*
- **Reply to yourself at 6 PM** with a question: *"Curious: how many render passes does your pipeline run per frame? (ours is 40&ndash;60)"*
- **Pin the thread** to your profile for the week

### Image Export Workflow
1. Add the `.twitter-slide` class to the LinkedIn slides on the promo page (or create a separate section)
2. Update `export_linkedin_slides.py` &rarr; duplicate as `export_twitter_slides.py` with `TARGET_WIDTH=1600, TARGET_HEIGHT=900`
3. Export PNGs, QA at phone-screen size
4. Upload to thread composer

---

## Cross-Platform Timing Summary

```
8:12  LinkedIn Post 1 carousel  (6 slides + text + comment link)
8:15  LinkedIn first comment     (series URL)
8:42  Twitter thread             (6 tweets, 5 images, 1 link-only)
12:00 Twitter QRT                (pain-point angle)
18:00 Twitter self-reply          (engagement question)
```

---

## Day 2+ (Follow-up)
- **LinkedIn Post 2** (Reminder) &mdash; next day or 2 days later
- **Twitter:** Repost hook tweet, or post a standalone "iceberg analogy" tweet referencing the thread
- Track impressions, clicks, and thread read-through rate to decide spacing for Posts 3+
