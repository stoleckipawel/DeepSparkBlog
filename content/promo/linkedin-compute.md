---
title: "LinkedIn Promo — Compute Article"
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
.carousel-version {
  margin-top: 1.4em;
  padding: 1em 1.05em 1.1em;
  border-radius: 14px;
  background: linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.carousel-version .version-head {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: .9em;
  align-items: start;
  margin-bottom: .9em;
}
.carousel-version .version-kicker {
  font-size: .82rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #ffb347;
  font-weight: 800;
}
.carousel-version .version-title {
  font-size: 1.02rem;
  color: #fff;
  font-weight: 800;
  line-height: 1.3;
}
.carousel-version .version-body {
  margin-top: .18em;
  color: rgba(255,255,255,.58);
  font-size: .9rem;
  line-height: 1.45;
}
.carousel-mini-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .7em;
}
.mini-slide {
  position: relative;
  aspect-ratio: 4 / 5;
  border-radius: 10px;
  overflow: hidden;
  padding: 1.15em 1.05em;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: linear-gradient(160deg, #0b0d12 0%, #0d1016 58%, #10141c 100%);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.mini-slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 18% 14%, rgba(255,255,255,.04) 0%, transparent 54%),
    radial-gradient(ellipse at 86% 78%, rgba(255,159,28,.07) 0%, transparent 42%);
  pointer-events: none;
}
.mini-slide * { position: relative; z-index: 1; }
.mini-slide .mini-num {
  font-size: .76rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: rgba(255,255,255,.34);
  font-weight: 800;
  margin-bottom: .72em;
}
.mini-slide .mini-title {
  font-size: 1.58rem;
  line-height: 1.02;
  color: #fff;
  font-weight: 900;
  letter-spacing: -.02em;
  margin-bottom: .55em;
}
.mini-slide .mini-copy {
  font-size: .98rem;
  line-height: 1.48;
  color: rgba(255,255,255,.6);
}
.slide-compare-row {
  margin-top: 1.25em;
  padding: 1em 1.05em 1.1em;
  border-radius: 14px;
  background: linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
}
.slide-compare-head {
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: .9em;
  align-items: start;
  margin-bottom: .9em;
}
.slide-compare-kicker {
  font-size: .82rem;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #ffb347;
  font-weight: 800;
}
.slide-compare-title {
  font-size: 1.02rem;
  color: #fff;
  font-weight: 800;
  line-height: 1.3;
}
.slide-compare-body {
  margin-top: .18em;
  color: rgba(255,255,255,.58);
  font-size: .9rem;
  line-height: 1.45;
}
.slide-compare-grid {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(280px, 320px);
  gap: .9em;
  overflow-x: auto;
  padding-bottom: .55em;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,159,28,.35) rgba(255,255,255,.05);
}
.slide-compare-grid::-webkit-scrollbar {
  height: 10px;
}
.slide-compare-grid::-webkit-scrollbar-track {
  background: rgba(255,255,255,.05);
  border-radius: 999px;
}
.slide-compare-grid::-webkit-scrollbar-thumb {
  background: rgba(255,159,28,.35);
  border-radius: 999px;
}
.mini-slide .mini-variant {
  font-size: .7rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #ffb347;
  font-weight: 800;
  margin-bottom: .45em;
}
@media (min-width: 1200px) {
  .slide-compare-grid {
    grid-auto-columns: minmax(300px, 340px);
  }
}
@media (max-width: 820px) {
  .compute-wire,
  .compute-arrow-row,
  .compute-metric-row,
  .compute-flow,
  .carousel-mini-grid {
    grid-template-columns: 1fr;
  }
  .compute-arrow-row { display: none; }
  .compute-ladder .row,
  .slide-compare-head,
  .carousel-version .version-head,
  .compute-carousel-outline .item {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="promo-lab">

## Compute Article — LinkedIn Promo

<div class="post-caption">
Final thumbnail direction for the compute article. The audience is Unreal-facing readers who want to understand what one familiar compute pass becomes underneath in D3D12.
</div>

<div class="compute-promo-note">
  <strong>Direction:</strong> keep the promise concrete and Unreal-oriented. One familiar pass on the surface, one explicit D3D12 path underneath.
</div>

<div class="compute-promo-note">
  <strong>Positioning:</strong> this is not selling compute in general. It is selling clarity about what the engine is hiding and why that helps when building or debugging a pass.
</div>

<div class="li-post-text">
<div class="li-hook">If you use Unreal, this is the layer under the pass you already know.</div>
<div class="li-body">
This article starts from a familiar Unreal-level goal: clear a texture with one small compute pass.
<br><br>
Then it walks one layer down and shows what that simple pass actually means in D3D12: binding contract, descriptors, PSO creation, command recording, queue submission, and the hand-off to the next pass.
<br><br>
The value is practical: a clearer model for where compute passes usually go wrong, what each layer is responsible for, and why a pass that looks simple in Unreal still has real API machinery underneath it.
</div>
<div class="li-cta">Full article draft → link in first comment</div>
<div class="li-tags">#rendering #graphicsprogramming #gamedev #d3d12 #unrealengine #hlsl #compute</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Final Thumbnail</span>
  <span class="slide-num">1 / 5</span>
  <div class="compute-kicker">Unreal To D3D12</div>
  <div class="hook">What does one Unreal pass<br>really become in D3D12?</div>
  <div class="sub">A concrete walkthrough of the binding, execution, and frame-level machinery underneath one small compute pass.</div>
  <div class="compute-flow">
    <div class="stage">
      <div class="step">Engine</div>
      <div class="headline">Clear texture</div>
      <div class="copy">The pass as it feels in Unreal.</div>
    </div>
    <div class="stage">
      <div class="step">Binding</div>
      <div class="headline">Root + descriptors</div>
      <div class="copy">Where the pass becomes a binding contract.</div>
    </div>
    <div class="stage">
      <div class="step">Execution</div>
      <div class="headline">PSO + command list</div>
      <div class="copy">Where the pass becomes real GPU work.</div>
    </div>
    <div class="stage">
      <div class="step">Frame</div>
      <div class="headline">State + hand-off</div>
      <div class="copy">Where the result survives the frame.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Promise:</strong> the article shows the layer Unreal usually hides, and turns one familiar pass into a clearer mental model for real D3D12 work.</div>
</div>

## 8-Slide Preview

<div class="post-caption">
Full-size preview of the selected carousel direction. Every slide now carries real structure so the preview matches the posting format more closely.
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">1 / 8</span>
  <div class="compute-kicker">Pull Back</div>
  <div class="hook">What does one Unreal pass<br>really become in D3D12?</div>
  <div class="sub">Start with the familiar pass, then pull the curtain back on the layers Unreal quietly handles for you.</div>
  <div class="compute-flow">
    <div class="stage">
      <div class="step">Engine</div>
      <div class="headline">Simple pass</div>
      <div class="copy">It feels local and lightweight.</div>
    </div>
    <div class="stage">
      <div class="step">API</div>
      <div class="headline">Real setup</div>
      <div class="copy">Resources, views, pipeline state.</div>
    </div>
    <div class="stage">
      <div class="step">GPU</div>
      <div class="headline">Real work</div>
      <div class="copy">Recorded commands and execution.</div>
    </div>
    <div class="stage">
      <div class="step">Frame</div>
      <div class="headline">Real result</div>
      <div class="copy">The output still has to survive.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Idea:</strong> Unreal gives you a clean pass abstraction. The article shows the explicit D3D12 path under that abstraction.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">2 / 8</span>
  <div class="compute-kicker">The Pass</div>
  <div class="hook">In Unreal, it starts as<br>one tiny clear pass.</div>
  <div class="sub">One output texture. One small parameter block. One dispatch. That is exactly why it is a good example.</div>
  <div class="compute-ladder">
    <div class="row">
      <div class="left">Goal</div>
      <div class="right"><strong>Clear a texture</strong> with compute</div>
    </div>
    <div class="row">
      <div class="left">Pass view</div>
      <div class="right"><strong>One render-graph-style step</strong> inside the frame</div>
    </div>
    <div class="row">
      <div class="left">Reader value</div>
      <div class="right"><strong>Small example</strong>, full API path underneath</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Why this example:</strong> once the shader stays simple, the machinery around it becomes the real subject.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">3 / 8</span>
  <div class="compute-kicker">Resource Work</div>
  <div class="hook">The pass needs a real<br>resource story first.</div>
  <div class="sub">Before the shader can write anything, the output has to exist as real GPU memory with the right usage model behind it.</div>
  <div class="compute-metric-row">
    <div class="compute-metric">
      <div class="k">Engine view</div>
      <div class="v">Output texture</div>
    </div>
    <div class="compute-metric">
      <div class="k">D3D12 view</div>
      <div class="v">Concrete resource</div>
    </div>
    <div class="compute-metric">
      <div class="k">Why it matters</div>
      <div class="v">No resource, no pass</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Unreal helps here:</strong> it hides much of the allocation and lifetime management that still has to be true underneath.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">4 / 8</span>
  <div class="compute-kicker">Binding Work</div>
  <div class="hook">The shader only sees<br>what binding makes legal.</div>
  <div class="sub">This is where friendly engine parameters turn into actual UAVs, CBVs, descriptors, and a root signature contract.</div>
  <div class="compute-flow">
    <div class="stage">
      <div class="step">Shader</div>
      <div class="headline">u0 / b0</div>
      <div class="copy">Registers define what the shader expects.</div>
    </div>
    <div class="stage">
      <div class="step">Views</div>
      <div class="headline">UAV / CBV</div>
      <div class="copy">Descriptors define what the GPU can see.</div>
    </div>
    <div class="stage">
      <div class="step">Contract</div>
      <div class="headline">Root signature</div>
      <div class="copy">Bindings become explicit and legal.</div>
    </div>
    <div class="stage">
      <div class="step">Engine</div>
      <div class="headline">Parameter block</div>
      <div class="copy">Unreal hides much of this translation.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Unreal helps here:</strong> it makes parameter setup feel friendly, while the underlying binding contract remains strict.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">5 / 8</span>
  <div class="compute-kicker">Pipeline Work</div>
  <div class="hook">The pass also needs<br>an executable shape.</div>
  <div class="sub">Shader bytecode is not enough. The pass has to be frozen into pipeline state that matches the binding contract.</div>
  <div class="compute-ladder">
    <div class="row">
      <div class="left">Shader</div>
      <div class="right"><strong>Compute bytecode</strong> expresses the work</div>
    </div>
    <div class="row">
      <div class="left">Contract</div>
      <div class="right"><strong>Root signature</strong> expresses legal bindings</div>
    </div>
    <div class="row">
      <div class="left">Executable</div>
      <div class="right"><strong>Compute PSO</strong> locks the path into shape</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Unreal helps here:</strong> it hides most of the plumbing between “I have a shader” and “the GPU has a legal pipeline to run.”</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">6 / 8</span>
  <div class="compute-kicker">Command Work</div>
  <div class="hook">Then the pass has to become<br>real recorded GPU work.</div>
  <div class="sub">Only here do command allocators, command lists, bindings, and Dispatch turn the pass into something the GPU can actually execute.</div>
  <div class="compute-metric-row">
    <div class="compute-metric">
      <div class="k">Before</div>
      <div class="v">Objects exist</div>
    </div>
    <div class="compute-metric">
      <div class="k">During</div>
      <div class="v">Commands record</div>
    </div>
    <div class="compute-metric">
      <div class="k">After</div>
      <div class="v">Dispatch is real</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Unreal helps here:</strong> it gives you a pass execution point instead of exposing the full command recording sequence every time.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">7 / 8</span>
  <div class="compute-kicker">Frame Survival</div>
  <div class="hook">Dispatch is not enough.<br>The frame still decides.</div>
  <div class="sub">The result has to survive resource state transitions, ordering, and the next pass that wants to read or sample it.</div>
  <div class="compute-flow">
    <div class="stage">
      <div class="step">Pass A</div>
      <div class="headline">Write</div>
      <div class="copy">The compute pass writes the output.</div>
    </div>
    <div class="stage">
      <div class="step">State</div>
      <div class="headline">Transition</div>
      <div class="copy">The resource has to be left in a usable state.</div>
    </div>
    <div class="stage">
      <div class="step">Order</div>
      <div class="headline">Barrier</div>
      <div class="copy">The frame needs a correct dependency story.</div>
    </div>
    <div class="stage">
      <div class="step">Pass B</div>
      <div class="headline">Consume</div>
      <div class="copy">The next pass has to see the result correctly.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Unreal helps here:</strong> it makes the frame feel continuous while a lot of explicit state and dependency work happens underneath.</div>
</div>

<div class="slide compute-slide">
  <span class="slide-label">Compute Article / Carousel Preview</span>
  <span class="slide-num">8 / 8</span>
  <div class="compute-kicker">What Unreal Does</div>
  <div class="hook">That is the curtain:<br>what the engine does for you.</div>
  <div class="sub">The article is not just about D3D12. It is about understanding the layer Unreal is carrying so you can reason, debug, and build with more confidence.</div>
  <div class="compute-bullet-list">
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>See the hidden layer:</strong> resource, binding, pipeline, command, and frame work.</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Debug better:</strong> most pass failures live around the shader, not inside it.</div>
    </div>
    <div class="compute-bullet-item">
      <div class="dot"></div>
      <div><strong>Learn the mental model:</strong> one small pass, one reusable path underneath.</div>
    </div>
  </div>
  <div class="compute-banner"><strong>Read the article:</strong> one Unreal-style compute clear, followed all the way down until it becomes real D3D12 work.</div>
</div>

</div>