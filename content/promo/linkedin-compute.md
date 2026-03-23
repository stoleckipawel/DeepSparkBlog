---
title: "LinkedIn Promo R&D — Compute Article"
date: 2026-03-23
draft: true
robots: "noindex, nofollow"
sitemap:
  disable: true
showTableOfContents: false
showDate: false
showAuthor: false
showPagination: false
showTitle: false
---

<!-- ═══════════════════════════════════════════════════════════════
     LINKEDIN PROMO R&D — Compute Article
     Quiet, technical concepts for: "Making a Tiny Compute Clear
     Survive a Real Unreal Frame"
     ═══════════════════════════════════════════════════════════════ -->

<style>
.promo-lab { max-width: 660px; margin: 0 auto; }
.promo-lab h2 {
  font-size: clamp(1.18rem, 1.25vw, 1.4rem);
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: #FF9F1C;
  margin: 2.6em 0 .7em;
  padding-bottom: .38em;
  border-bottom: 1px solid rgba(255,159,28,.22);
}
.promo-lab h2:first-child { margin-top: 0; }
.promo-lab .post-caption {
  font-size: clamp(0.94rem, 0.95vw, 1.1rem);
  opacity: .66;
  margin-bottom: 1.5em;
  line-height: 1.58;
}

.slide {
  position: relative;
  aspect-ratio: 4 / 5;
  width: 100%;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.4em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 24px 46px rgba(0,0,0,.38);
  isolation: isolate;
}
.slide::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.slide::after {
  content: '';
  position: absolute;
  pointer-events: none;
}
.slide * { position: relative; z-index: 1; }

.li-post-text {
  background: linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
  border-radius: 10px;
  padding: 1.4em 1.6em;
  margin-bottom: 1.4em;
  font-size: clamp(1rem, 1vw, 1.16rem);
  line-height: 1.62;
  color: rgba(255,255,255,.68);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.li-post-text .li-hook {
  font-weight: 800;
  color: #fff;
  font-size: clamp(1.2rem, 1.3vw, 1.5rem);
  margin-bottom: .6em;
  line-height: 1.36;
}
.li-post-text .li-body { margin-bottom: .8em; }
.li-post-text .li-cta { color: #FF9F1C; font-weight: 700; }
.li-post-text .li-tags {
  color: rgba(255,159,28,.7);
  font-size: clamp(1.08rem, 1.02vw, 1.24rem);
  margin-top: .6em;
}

.compute-promo-note {
  background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border-radius: 12px;
  padding: 1.05em 1.2em;
  margin: 0 0 1.15em;
  color: rgba(255,255,255,.64);
  line-height: 1.58;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.compute-promo-note strong { color: rgba(255,255,255,.9); }

.compute-slide {
  background: linear-gradient(160deg, #0b0d12 0%, #0d1016 58%, #10141c 100%);
  padding: 2em 1.85em;
}
.compute-slide::before {
  background:
    radial-gradient(ellipse at 18% 14%, rgba(255,255,255,.045) 0%, transparent 54%),
    radial-gradient(ellipse at 86% 78%, rgba(255,159,28,.08) 0%, transparent 42%),
    linear-gradient(120deg, rgba(255,255,255,.02) 0%, rgba(255,255,255,0) 35%);
}
.compute-slide::after {
  width: 240px;
  height: 240px;
  bottom: -90px;
  right: -70px;
  background: radial-gradient(circle at 30% 30%, rgba(255,159,28,.1), rgba(255,159,28,0) 70%);
}
.compute-slide .slide-label {
  display: block;
  font-size: .84rem;
  letter-spacing: .09em;
  text-transform: uppercase;
  color: rgba(255,255,255,.42);
  font-weight: 800;
  margin-bottom: .8em;
}
.compute-slide .slide-num {
  display: block;
  position: absolute;
  top: 1.5em;
  right: 1.6em;
  font-size: .82rem;
  color: rgba(255,255,255,.28);
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.compute-kicker {
  font-size: .9rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #ffb347;
  font-weight: 800;
  margin-bottom: .7em;
}
.compute-slide .hook {
  max-width: 100%;
  font-size: clamp(2rem, 2.55vw, 2.55rem);
  line-height: 1.07;
  margin-bottom: .45em;
  color: #fff;
  font-weight: 900;
  letter-spacing: -.01em;
}
.compute-slide .sub {
  max-width: 100%;
  font-size: clamp(1.02rem, 1.02vw, 1.18rem);
  line-height: 1.52;
  color: rgba(255,255,255,.6);
}
.compute-wire {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: .45em;
  margin: 1.15em 0 .85em;
}
.compute-wire .node {
  border-radius: 10px;
  padding: .78em .72em;
  background: linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.07);
}
.compute-wire .node .tag {
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: rgba(255,255,255,.4);
  font-weight: 800;
  margin-bottom: .45em;
}
.compute-wire .node .title {
  font-size: .96rem;
  line-height: 1.22;
  color: #fff;
  font-weight: 800;
}
.compute-wire .node .body {
  margin-top: .35em;
  font-size: .82rem;
  line-height: 1.36;
  color: rgba(255,255,255,.58);
}
.compute-wire .node.hot {
  box-shadow: inset 0 0 0 1px rgba(255,179,71,.28);
  background: linear-gradient(145deg, rgba(255,179,71,.09), rgba(255,179,71,.03));
}
.compute-arrow-row {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: .45em;
  margin: -.15em 0 .55em;
  color: rgba(255,255,255,.18);
  text-align: center;
  font-weight: 700;
}
.compute-metric-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .55em;
  margin: 1.05em 0 .9em;
}
.compute-metric {
  border-radius: 10px;
  padding: .82em .82em;
  background: linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.compute-metric .k {
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: rgba(255,255,255,.4);
  font-weight: 800;
}
.compute-metric .v {
  margin-top: .38em;
  font-size: 1rem;
  line-height: 1.34;
  color: #fff;
  font-weight: 800;
}
.compute-ladder {
  margin: 1.05em 0 .8em;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.compute-ladder .row {
  display: grid;
  grid-template-columns: 146px 1fr;
}
.compute-ladder .row + .row { border-top: 1px solid rgba(255,255,255,.06); }
.compute-ladder .left {
  padding: .82em .9em;
  background: rgba(255,255,255,.035);
  font-size: .78rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: rgba(255,255,255,.45);
  font-weight: 800;
}
.compute-ladder .right {
  padding: .82em .95em;
  font-size: .98rem;
  line-height: 1.4;
  color: rgba(255,255,255,.82);
}
.compute-ladder .right strong { color: #fff; }
.compute-mini-caption {
  margin-top: auto;
  padding-top: 1em;
  font-size: .9rem;
  color: rgba(255,255,255,.42);
}
.compute-carousel-outline {
  display: grid;
  gap: .55em;
  margin-top: .9em;
}
.compute-carousel-outline .item {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: .85em;
  align-items: start;
  border-radius: 10px;
  padding: .78em .85em;
  background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.compute-carousel-outline .num {
  font-size: .8rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #ffb347;
  font-weight: 800;
}
.compute-carousel-outline .title {
  font-size: .98rem;
  line-height: 1.32;
  color: #fff;
  font-weight: 800;
}
.compute-carousel-outline .body {
  margin-top: .2em;
  font-size: .9rem;
  line-height: 1.46;
  color: rgba(255,255,255,.58);
}
.compute-selected {
  margin-top: 2.2em;
}
.compute-selected .title {
  font-size: clamp(1.04rem, 1vw, 1.18rem);
  text-transform: uppercase;
  letter-spacing: .06em;
  color: #FF9F1C;
  font-weight: 800;
  margin-bottom: .5em;
}
.compute-bullet-list {
  display: grid;
  gap: .45em;
  margin: 1em 0 .75em;
}
.compute-bullet-item {
  display: grid;
  grid-template-columns: 12px 1fr;
  gap: .65em;
  align-items: start;
  font-size: .98rem;
  line-height: 1.42;
  color: rgba(255,255,255,.8);
}
.compute-bullet-item .dot {
  width: 7px;
  height: 7px;
  margin-top: .45em;
  border-radius: 50%;
  background: #FF9F1C;
}
.compute-bullet-item strong {
  color: #fff;
}
.compute-flow {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .55em;
  margin: 1em 0 .85em;
}
.compute-flow .stage {
  border-radius: 10px;
  padding: .82em .8em;
  background: linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.compute-flow .stage .step {
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: rgba(255,255,255,.4);
  font-weight: 800;
  margin-bottom: .45em;
}
.compute-flow .stage .headline {
  font-size: .98rem;
  line-height: 1.25;
  color: #fff;
  font-weight: 800;
}
.compute-flow .stage .copy {
  margin-top: .3em;
  font-size: .82rem;
  line-height: 1.34;
  color: rgba(255,255,255,.58);
}
.compute-banner {
  margin: .95em 0 .8em;
  border-radius: 12px;
  padding: .95em 1em;
  background: linear-gradient(145deg, rgba(255,159,28,.08), rgba(255,255,255,.02));
  box-shadow: inset 0 0 0 1px rgba(255,159,28,.18);
  color: rgba(255,255,255,.82);
  font-size: 1rem;
  line-height: 1.42;
}
.compute-banner strong {
  color: #fff;
}
@media (max-width: 820px) {
  .compute-wire,
  .compute-arrow-row,
  .compute-metric-row,
  .compute-flow {
    grid-template-columns: 1fr;
  }
  .compute-arrow-row { display: none; }
  .compute-ladder .row,
  .compute-carousel-outline .item {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="promo-lab">

## Compute Article — LinkedIn R&D

<div class="post-caption">
Starting point for the compute article promo. The direction here should sell reader payoff: what they will understand, debug, and apply after reading.
</div>

<div class="compute-promo-note">
  <strong>Working angle:</strong> do not sell compute in general. Sell the concrete value of seeing one Unreal-style clear pass all the way down to D3D12, because that gives readers a model they can reuse in real engine work.
</div>

<div class="compute-promo-note">
  <strong>Visual direction:</strong> keep the existing dark editorial base from the repo, but lower the saturation, reduce the number of accent colors, and make the focal point a chain of responsibilities instead of a big KPI.
</div>

<div class="li-post-text">
<div class="li-hook">If you use Unreal or another engine, this shows what a compute pass actually needs underneath.<br>So you can debug it, reason about it, and build the next one faster.</div>
<div class="li-body">
This article starts from a familiar engine-level goal: clear a texture with one small compute pass.
<br><br>
Then it walks one layer down and shows what that innocent sentence actually means in D3D12: binding contract, descriptors, PSO creation, command recording, queue submission, and the hand-off to the next pass.
<br><br>
If you mostly work in Unreal or another engine, this gives you a clearer mental model for where compute passes usually go wrong and what each layer is responsible for.
</div>
<div class="li-cta">Full article draft → link in first comment</div>
<div class="li-tags">#rendering #graphicsprogramming #gamedev #d3d12 #unrealengine #hlsl #compute</div>
</div>

<div class="compute-promo-note">
  <strong>Suggested carousel shape:</strong> 5 slides is probably enough here. Reader payoff, path, where bugs come from, frame hand-off, CTA.
</div>

<div class="compute-carousel-outline">
  <div class="item">
    <div class="num">Slide 1</div>
    <div>
      <div class="title">What this helps you do</div>
      <div class="body">Lead with the payoff: understand what an engine-level compute pass really turns into and debug it with more confidence.</div>
    </div>
  </div>
  <div class="item">
    <div class="num">Slide 2</div>
    <div>
      <div class="title">Unreal pass idea → D3D12 path</div>
      <div class="body">Show the journey from engine-level intent to real API objects and commands.</div>
    </div>
  </div>
  <div class="item">
    <div class="num">Slide 3</div>
    <div>
      <div class="title">What this lets you diagnose</div>
      <div class="body">Binding mismatch, descriptor lifetime, wrong state, missing hand-off.</div>
    </div>
  </div>
  <div class="item">
    <div class="num">Slide 4</div>
    <div>
      <div class="title">Why the frame still matters after Dispatch</div>
      <div class="body">This is the main practical payoff: understanding the hand-off into the next pass, not just the dispatch itself.</div>
    </div>
  </div>
  <div class="item">
    <div class="num">Slide 5</div>
    <div>
      <div class="title">CTA</div>
      <div class="body">Invite readers into the article and ask where compute usually disappears for them.</div>
    </div>
  </div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Hook Direction A</span>
  <span class="slide-num">1 / 5</span>
  <div class="compute-kicker">Thumbnail concept A</div>
  <div class="hook">One small compute pass.<br>A reusable mental model underneath.</div>
  <div class="sub">Best if the goal is to sell reader understanding: what sits between an engine-facing pass idea and a real GPU dispatch.</div>
  <div class="compute-wire">
    <div class="node">
      <div class="tag">Intent</div>
      <div class="title">Clear texture</div>
      <div class="body">What the pass sounds like in Unreal.</div>
    </div>
    <div class="node">
      <div class="tag">Binding</div>
      <div class="title">Root signature</div>
      <div class="body">What the shader can legally see.</div>
    </div>
    <div class="node hot">
      <div class="tag">Views</div>
      <div class="title">Descriptors</div>
      <div class="body">The point most readers under-estimate.</div>
    </div>
    <div class="node">
      <div class="tag">Execution</div>
      <div class="title">PSO + Dispatch</div>
      <div class="body">The visible part.</div>
    </div>
    <div class="node">
      <div class="tag">Survival</div>
      <div class="title">State hand-off</div>
      <div class="body">What lets the next pass use it.</div>
    </div>
  </div>
  <div class="compute-arrow-row">
    <div>↓</div>
    <div>↓</div>
    <div>↓</div>
    <div>↓</div>
    <div>↓</div>
  </div>
  <div class="compute-mini-caption">This one is the clearest editorial match if the article should feel useful first and dramatic second.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Hook Direction B</span>
  <span class="slide-num">1 / 5</span>
  <div class="compute-kicker">Thumbnail concept B</div>
  <div class="hook">Know what to check<br>after Dispatch.</div>
  <div class="sub">Best if the goal is to sell the article through a debugging lens while still giving the reader an actionable checklist.</div>
  <div class="compute-metric-row">
    <div class="compute-metric">
      <div class="k">Shader</div>
      <div class="v">Compiled correctly</div>
    </div>
    <div class="compute-metric">
      <div class="k">GPU</div>
      <div class="v">Dispatch executed</div>
    </div>
    <div class="compute-metric">
      <div class="k">Frame</div>
      <div class="v">Next pass still wrong</div>
    </div>
  </div>
  <div class="compute-ladder">
    <div class="row">
      <div class="left">Maybe</div>
      <div class="right"><strong>Descriptor issue</strong> or root mismatch</div>
    </div>
    <div class="row">
      <div class="left">Maybe</div>
      <div class="right"><strong>Wrong state</strong> before or after dispatch</div>
    </div>
    <div class="row">
      <div class="left">Maybe</div>
      <div class="right"><strong>Bad hand-off</strong> into the next pass</div>
    </div>
  </div>
  <div class="compute-mini-caption">Best if the post should promise a practical debugging filter readers can apply immediately.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Hook Direction C</span>
  <span class="slide-num">1 / 5</span>
  <div class="compute-kicker">Thumbnail concept C</div>
  <div class="hook">Translate engine-level compute<br>into real D3D12 steps.</div>
  <div class="sub">Best if the goal is to make engine users feel explicitly invited and show that the article gives them a concrete translation layer.</div>
  <div class="compute-ladder">
    <div class="row">
      <div class="left">Engine view</div>
      <div class="right"><strong>Clear texture with compute</strong></div>
    </div>
    <div class="row">
      <div class="left">Binding view</div>
      <div class="right"><strong>Root signature + descriptors</strong></div>
    </div>
    <div class="row">
      <div class="left">Pipeline view</div>
      <div class="right"><strong>PSO + command list + queue</strong></div>
    </div>
    <div class="row">
      <div class="left">Frame view</div>
      <div class="right"><strong>Transitions, ordering, next-pass survival</strong></div>
    </div>
  </div>
  <div class="compute-mini-caption">Most welcoming to Unreal-heavy readers and probably the easiest direction to expand into a full carousel.</div>
</div>

<div class="compute-selected">

## Selected Direction — Full LinkedIn Post

<div class="compute-promo-note">
  <strong>Chosen base:</strong> Concept A. Keep the promise centered on reader understanding and build the full post around one reusable mental model.
</div>

<div class="li-post-text">
<div class="li-hook">One small compute pass.<br>A reusable mental model underneath.</div>
<div class="li-body">
If you mostly use Unreal or another engine, compute work can feel deceptively simple at the pass level.
<br><br>
This post is about the layer underneath that simplicity: what has to exist between “clear a texture with compute” and a real GPU dispatch that the rest of the frame can safely use.
<br><br>
The article walks through that path in D3D12: root signature, descriptors, PSO, command recording, submission, and the hand-off into the next pass.
<br><br>
The goal is practical: give you a mental model you can reuse when debugging a broken compute pass or building the next one.
</div>
<div class="li-cta">Full article draft → link in first comment</div>
<div class="li-tags">#rendering #graphicsprogramming #gamedev #d3d12 #unrealengine #hlsl #compute</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Selected Direction</span>
  <span class="slide-num">1 / 5</span>
  <div class="compute-kicker">Hook</div>
  <div class="hook">One small compute pass.<br>A reusable mental model underneath.</div>
  <div class="sub">Use this when the post should promise understanding first: what sits between an engine-facing pass idea and a real GPU dispatch.</div>
  <div class="compute-wire">
    <div class="node">
      <div class="tag">Intent</div>
      <div class="title">Clear texture</div>
      <div class="body">The pass as you think about it in the engine.</div>
    </div>
    <div class="node">
      <div class="tag">Binding</div>
      <div class="title">Root signature</div>
      <div class="body">What the shader is actually allowed to see.</div>
    </div>
    <div class="node hot">
      <div class="tag">Views</div>
      <div class="title">Descriptors</div>
      <div class="body">Where many “simple” passes become concrete API work.</div>
    </div>
    <div class="node">
      <div class="tag">Execution</div>
      <div class="title">PSO + Dispatch</div>
      <div class="body">The visible point in the chain.</div>
    </div>
    <div class="node">
      <div class="tag">Frame</div>
      <div class="title">Hand-off</div>
      <div class="body">What makes the result usable by the next pass.</div>
    </div>
  </div>
  <div class="compute-mini-caption">The first slide should already tell the reader what kind of understanding they are going to gain.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Selected Direction</span>
  <span class="slide-num">2 / 5</span>
  <div class="compute-kicker">Path</div>
  <div class="hook">From pass idea<br>to GPU work.</div>
  <div class="sub">This is the core translation the article provides: the thing you ask for in the engine is not the thing the API needs.</div>
  <div class="compute-flow">
    <div class="stage">
      <div class="step">1</div>
      <div class="headline">Declare the contract</div>
      <div class="copy">Root signature says what the shader can access.</div>
    </div>
    <div class="stage">
      <div class="step">2</div>
      <div class="headline">Describe the data</div>
      <div class="copy">Descriptors turn resources into bindable views.</div>
    </div>
    <div class="stage">
      <div class="step">3</div>
      <div class="headline">Freeze the pipeline</div>
      <div class="copy">The compute PSO locks the executable state.</div>
    </div>
    <div class="stage">
      <div class="step">4</div>
      <div class="headline">Record and submit</div>
      <div class="copy">Command list and queue turn intent into actual work.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Reader payoff:</strong> after this, “clear a texture with compute” stops being a black box phrase and becomes a sequence you can reason about.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Selected Direction</span>
  <span class="slide-num">3 / 5</span>
  <div class="compute-kicker">Debug Value</div>
  <div class="hook">What this helps you check<br>when a pass is wrong.</div>
  <div class="sub">The value is not trivia. The value is a better debugging filter.</div>
  <div class="compute-bullet-list">
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Binding contract:</strong> does the root signature actually match what the shader expects?</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Descriptor setup:</strong> did the pass get the right views and heap-backed bindings?</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Recorded work:</strong> did the command list bind the intended state before Dispatch?</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Frame hand-off:</strong> can the next pass legally read what this pass wrote?</div>
    </div>
  </div>
  <div class="compute-mini-caption">This slide should make the article feel immediately useful to people who already work on engine code.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Selected Direction</span>
  <span class="slide-num">4 / 5</span>
  <div class="compute-kicker">Frame View</div>
  <div class="hook">Dispatch is not the end.<br>The next pass still matters.</div>
  <div class="sub">A compute pass only becomes useful when its output is handed off correctly to the rest of the frame.</div>
  <div class="compute-ladder">
    <div class="row">
      <div class="left">Compute pass</div>
      <div class="right"><strong>Writes the texture</strong> through a UAV.</div>
    </div>
    <div class="row">
      <div class="left">Barrier/state</div>
      <div class="right"><strong>Transitions the usage</strong> so the next stage sees a legal resource state.</div>
    </div>
    <div class="row">
      <div class="left">Next pass</div>
      <div class="right"><strong>Reads or samples the result</strong> instead of inheriting undefined assumptions.</div>
    </div>
    <div class="row">
      <div class="left">Mental model</div>
      <div class="right"><strong>Dispatch ran</strong> is not enough; the frame needs a correct hand-off too.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Main payoff:</strong> this is the bridge from “the shader executed” to “the feature actually worked in the frame.”</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Selected Direction</span>
  <span class="slide-num">5 / 5</span>
  <div class="compute-kicker">CTA</div>
  <div class="hook">The full article follows<br>one pass all the way down.</div>
  <div class="sub">From an Unreal-style compute clear to the D3D12 objects, bindings, recording, submission, and frame hand-off underneath it.</div>
  <div class="compute-bullet-list">
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Read it</strong> if you want a clearer model for compute work below the engine layer.</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Use it</strong> when a compute pass behaves correctly in isolation but not in the full frame.</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Discuss it</strong> if you have a recurring compute bug pattern in your renderer or engine workflow.</div>
    </div>
  </div>
  <div class="compute-mini-caption">Discussion prompt: where do compute passes most often disappear for you: bindings, descriptors, barriers, or frame integration?</div>
</div>

</div>