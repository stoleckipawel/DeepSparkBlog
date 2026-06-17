# PTLAS Article Design Doc

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex

## 1. Goal

Design an article about PTLAS that is technically credible, grounded in current vendor documentation, and anchored in the real SparkleEngine integration already in progress.

This should not read like a generic "what is ray tracing" piece.
It should explain why PTLAS matters, what NVIDIA, Khronos, and Microsoft are actually proposing, what SparkleEngine already implements, and where the difficult engineering tradeoffs still are.

## 2. Recommended Thesis

Recommended article thesis:

"PTLAS is not just a new API surface for ray tracing. It is a different update model for top-level acceleration structures, and its real value only appears when an engine stops rewriting the whole scene and starts expressing selective instance and partition updates."

Core reader takeaway:

"PTLAS is designed so top-level update cost can follow the instances and partitions that actually changed, instead of behaving like the worst-case whole scene changed every frame."

Important wording nuance:

- do not say PTLAS guarantees we only pay for animated objects
- say PTLAS enables or is designed for update cost to scale with changed instances and touched partitions
- keep reminding the reader that partition quality, touched partition count, global partition policy, and native operation generation decide whether the theoretical benefit appears in practice

Why this is the strongest angle:

- It matches the official Khronos, NVIDIA, and Microsoft descriptions.
- It fits SparkleEngine's current state honestly.
- It gives the article a point of view instead of a neutral encyclopedia tone.
- It lets us talk about architecture, update behavior, instrumentation, and vendor-specific API design in one coherent story.

## 3. Audience

Primary audience:

- rendering engineers on the CDP / REKD side
- experienced engine and graphics programmers
- peers who already understand TLAS / BLAS, D3D12, Vulkan, and modern ray tracing architecture
- colleagues who care more about integration quality, tradeoffs, and measurements than introductory explanation

Secondary audience:

- experienced rendering learners reading DeepSparkBlog for implementation-oriented analysis
- external engine developers curious about large-world ray tracing and update-cost bottlenecks

This should be treated as a peer-level piece, not a beginner article.
We can assume the reader already knows what TLAS, BLAS, refit vs rebuild, and indirect GPU work submission are.
If we overexplain the basics, we will dilute the value for the actual intended audience.

### Audience implications

Because the target readers are experienced rendering engineers:

- skip ray tracing 101 framing
- define PTLAS mostly in terms of update model and engine consequences
- prioritize architecture boundaries, operation semantics, occupancy policy, and instrumentation
- include failure modes, not just the happy path
- speak in terms of acceptance criteria and implementation evidence

## 4. What The Article Should Deliver

The reader should leave with:

- a compact baseline model of how classic ray tracing structures are organized
- a clear understanding of what PTLAS changes relative to classic TLAS
- a mental model for partitions, global partition, and partition translation
- an understanding that PTLAS value is behavioral, not merely syntactic
- a grounded view of how SparkleEngine currently maps to that model
- a realistic sense of the remaining engineering work and tradeoffs
- a clear sense of what evidence would convince a rendering engineer that the integration is actually correct and worthwhile

## 5. Ground Truth From Current Vendor Sources

### Khronos / Vulkan

Key points from the current `VK_NV_partitioned_acceleration_structure` proposal and reference pages:

- PTLAS exists because classic TLAS requires full rebuilds even when only a few instances change.
- PTLAS organizes instances into partitions and internally builds in two stages:
  one structure per partition, then a top-level structure over partitions.
- PTLAS performance depends heavily on partition organization.
- Smaller partitions usually improve update cost, while overlap can hurt trace performance.
- The extension exposes explicit operation types:
  `WRITE_INSTANCE`, `UPDATE_INSTANCE`, and `WRITE_PARTITION_TRANSLATION`.
- The proposal also defines a special global partition and partition translation for large-world precision handling.

### NVIDIA

Key points from NVIDIA docs and samples:

- NVIDIA's PTLAS sample demonstrates partial updates driven by actual moving objects, not full-scene rewrites.
- The sample explicitly uses a global partition for fast updates of dynamic objects.
- The sample shows multiple update strategies, including keeping objects in their home partition or moving dynamic objects into the global partition.
- NVIDIA's NVAPI exposes PTLAS sizing and build APIs around:
  instance count, partition count, max instances per partition, and max instances in the global partition.
- NVAPI also exposes optimization flags such as fast-trace, fast-build, and partition translation support.

### Microsoft

Key points from the current DirectX ray tracing functional spec:

- Microsoft describes PTLAS as a persistent structure that can be partially rebuilt by modifying only some partitions.
- The DirectX model also includes a special global partition for frequently updated objects.
- Microsoft documents partition translation as a way to re-center large worlds without rebuilding the entire PTLAS.
- PTLAS in the DirectX spec is presented through GPU-driven indirect RTAS operations rather than classic TLAS build entrypoints.
- The spec frames PTLAS as capacity-based:
  instance count, partition count, max per-partition occupancy, and max global-partition occupancy.

## 6. Ground Truth From SparkleEngine

SparkleEngine already has substantial PTLAS work in place.

Current implementation strengths:

- a top-level strategy split between classic TLAS and partitioned TLAS
- a PTLAS partition planner
- a logical update stream that emits only dirty or moved entries
- backend-specific D3D12 and Vulkan PTLAS service layers
- smoke / diagnostics output for PTLAS capability, planner state, and timings
- architecture boundary checks that keep native PTLAS identifiers out of generic renderer code

Important implementation reality:

- SparkleEngine already computes selective logical PTLAS updates
- but the live build path currently repacks a full-scene `WriteInstance` operation every frame
- the engine is therefore closer to "PTLAS API integration" than fully realized "PTLAS behavioral optimization"

This is not a weakness for the article.
It is the article's most valuable honest insight.

## 7. Recommended Article Positioning

### Important framing addition

Yes, the article should include a ray tracing structure overview.

But for this audience it should be a comparison-oriented framing section, not a beginner tutorial.

The purpose of the overview is:

- establish the baseline structure the reader is moving from
- define where BLAS, TLAS, and PTLAS sit in the stack
- make the later PTLAS differences easier to reason about
- let the article teach through contrast rather than through isolated definitions

Recommended rule:

- explain only the parts of BLAS / TLAS that are necessary to understand why PTLAS exists
- spend the rest of the article on the consequences of the difference

### Best choice

Recommended article type:

"Implementation-oriented architecture article with SparkleEngine as the spine"

What that means:

- start from the vendor problem statement
- explain the PTLAS model
- map the model onto SparkleEngine's current architecture
- show what is already correct
- show what still blocks the full PTLAS payoff
- close with the practical engineering roadmap

Why this is better than a pure explainer:

- it differentiates the post from generic PTLAS summaries
- it leverages your existing engine work
- it gives readers real architecture they can learn from
- it keeps the article honest and specific
- it respects the fact that the intended audience is qualified to judge the design, not just learn the vocabulary

### Peer-audience variant

If this is explicitly for your colleagues rather than a broad public DeepSparkBlog audience, the article can lean even further into:

- design-review language
- acceptance criteria
- current gaps
- rollout priorities
- measurement strategy

In that mode, the piece becomes closer to:

"PTLAS integration review: what is architecturally in place, what still collapses into full-scene behavior, and what must change before the feature earns its complexity."

### Good alternative

"Cross-vendor PTLAS explainer with SparkleEngine callouts"

This is safer if you want broader appeal, but it is less distinctive.

### Weakest option

"We added PTLAS to SparkleEngine"

This would be risky today because the most important behavioral win is not fully complete yet.
It could overclaim unless framed very carefully.

## 8. Recommended Working Title Candidates

Best candidates:

1. `Next Gen RT Acceleration Structure: PTLAS vs TLAS`
2. `PTLAS Is More Than a New TLAS API`
3. `Designing PTLAS for a Real Engine`
4. `PTLAS in SparkleEngine: Architecture, Tradeoffs, and the Hard Part`
5. `From TLAS Rebuilds to PTLAS Updates`
6. `PTLAS Integration Review: Architecture, Gaps, and Proof`
7. `SparkleEngine PTLAS: From Logical Updates to Real Selective Rebuilds`

Approved working title:

`Next Gen RT Acceleration Structure: PTLAS vs TLAS`

Reason:

- clear and technically honest
- frames PTLAS as a model shift instead of a feature badge
- supports the baseline-to-difference article structure
- works for both peer readers and public blog readers
- avoids overclaiming implementation completeness

## 9. Recommended Structure

### Option A: strongest structure

1. Ray tracing structure overview
2. The problem classic TLAS still has
3. What PTLAS changes conceptually
4. How Khronos, NVIDIA, and Microsoft each express the model
5. What SparkleEngine already has
6. Where the hard part actually is
7. What a behavior-correct PTLAS path looks like
8. What evidence will prove the integration is truly working

### Suggested section breakdown

#### 1. Ray tracing structure overview

Start with a concise baseline:

- BLAS holds geometry-level acceleration data
- TLAS instances BLAS objects into the scene
- classic TLAS update cost is tied to rebuilding or refitting the whole top-level structure
- PTLAS keeps the shader-facing role of TLAS but changes the update model underneath

Recommended framing device:

- one small diagram or table comparing BLAS, TLAS, and PTLAS
- emphasis on ownership, update granularity, and what is persistent across frames

Good comparison axes:

- what data the structure owns
- what changes when scene transforms change
- what must be rebuilt when a small set of instances moves
- what the shader sees

This section should be short and difference-oriented.
Its job is to give the reader a baseline so the PTLAS model feels like an evolution, not a disconnected feature.

#### 2. The real bottleneck

Frame the problem:

- classic TLAS rebuild cost
- large scenes
- localized motion
- why "only a few instances changed" is still expensive

Keep this section short for the peer audience.
The goal is not to teach TLAS basics, but to align everyone on the exact bottleneck PTLAS is meant to solve.

#### 3. PTLAS in one mental model

Explain:

- partitions
- two-stage build
- persistent instance state
- global partition
- partition translation

This is where the article should make the transition from:

"here is the classic top-level structure model"

to:

"here is the new top-level update model"

#### 4. The vendor model

Compare:

- Khronos Vulkan extension model
- NVIDIA sample and NVAPI model
- Microsoft indirect RTAS operations model

This section should emphasize convergence, not vendor tribalism.
It should also highlight where vendor APIs imply concrete engine responsibilities around sizing, update granularity, and policy.

#### 5. SparkleEngine today

Show:

- strategy split
- planner
- logical updates
- backend abstraction
- diagnostics

For your colleagues, this section should probably be the center of gravity of the article.

#### 6. The hard part is not naming the feature

Key argument:

- the difficult part is not exposing PTLAS capability
- it is making the update path selective enough to realize the intended win

#### 7. What still has to change

Describe:

- turning logical updates into native selective operations
- sizing and occupancy policy
- deciding how much GPU-driven staging is worth today
- proving wins with measurements
- deciding what complexity should be cut rather than completed

#### 8. What success looks like

Success criteria:

- only changed instances or partitions get rewritten
- capability reporting is trustworthy
- diagnostics show update volume and timing shifts
- PTLAS beats or justifies itself against classic TLAS in real captures

## 10. Specific SparkleEngine Details Worth Using

These are especially useful anchors for the final article:

- `Docs/Rendering/PTLAS_TLAS_Design_Review.md`
- `Engine/Renderer/Private/RayTracing/RayTracingTopLevelScenePlanner.cpp`
- `Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.cpp`
- `Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp`
- `Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp`
- `Engine/RHI/Private/D3D12/RayTracing/D3D12NvapiRayTracingProvider.cpp`
- `Engine/RHI/Private/Vulkan/RayTracing/VulkanPartitionedTlasServices.cpp`
- `Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp`

Particularly strong implementation details:

- logical update records already distinguish dirty transforms and moved partitions
- the strategy layer already models PTLAS vs classic TLAS selection
- smoke data already records PTLAS provider and update metrics
- current full-scene repack behavior provides a natural "why the last mile matters" discussion point

For a peer audience, these details should be shown with concrete file and function references where useful, not only paraphrased.

## 11. Specific Vendor Details Worth Highlighting

### NVIDIA-specific details to use

- the `vk_partitioned_tlas` sample's moving-domino setup
- only moving instances are rewritten
- the sample's three update modes
- use of the global partition for dynamic movement
- NVAPI prebuild sizing and indirect PTLAS build entrypoints

### Microsoft-specific details to use

- PTLAS as a persistent partially rebuildable structure
- the global partition as a first-class concept
- partition translation for large-world precision
- GPU-driven indirect RTAS operations instead of classic TLAS build calls
- `FAST_TRACE` vs `FAST_BUILD` style policy choices

### Khronos-specific details to use

- PTLAS rationale in the extension proposal
- operation semantics from `VkPartitionedAccelerationStructureOpTypeNV`
- the partitioning / overlap tradeoff

## 12. Things The Article Should Avoid

Avoid these traps:

- do not present PTLAS as "just faster TLAS"
- do not imply SparkleEngine already has full selective native PTLAS updates if it still repacks the whole scene
- do not overfocus on API token soup
- do not turn the article into a Vulkan-only or D3D12-only piece unless that is a deliberate editorial decision
- do not oversell GPU-driven staging if the current strongest story is still CPU-packed selective correctness
- do not spend too much time re-explaining concepts your colleagues already know
- do not hide uncertainties; peer readers will trust the article more if risks and open questions are explicit
- do not let the ray tracing structure overview expand into a general DXR / Vulkan RT primer

## 13. Recommended Tone

Tone should be:

- analytical
- implementation-oriented
- honest about incomplete work
- excited but not marketing-heavy
- peer-to-peer
- comfortable with disagreement and technical scrutiny

The strongest version of this article sounds like:

"Here is what PTLAS is supposed to buy us, here is how the vendors frame it, here is what the engine already gets right, and here is the exact point where many integrations either become real or quietly collapse back into full-scene rebuild behavior."

## 14. Blog-Specific Best Practices To Reuse

After reviewing the Frame Graph series and the `About` page, there are several blog-native patterns worth reusing for this PTLAS article.

Important constraint:

- this should feel like one strong standalone article
- do not structure it like a series installment
- we can borrow the series' clarity and visual rhythm without borrowing its navigation or pacing

### 14.1 What already works well on DeepSparkBlog

From the Frame Graph articles:

- strong opening problem statement
- immediate reader payoff
- visible article roadmap
- comparison tables that reduce ambiguity quickly
- diagrams that explain systems through flow and contrast
- repeated use of short “why this matters” framing
- grounding abstract concepts in implementation consequences
- smooth alternation between conceptual explanation and concrete evidence

From the `About` page:

- clean section rhythm
- strong visual hierarchy
- compact, intentional blocks instead of long unbroken walls of text
- confidence in using custom layout sections when the content benefits from it

### 14.2 Best practices to reuse directly

#### Open with the engineering problem, not the definition

The Frame Graph series consistently starts with:

- the pain
- the scaling problem
- the reason the reader should care now

For PTLAS, do the same.

Do not begin with:

"PTLAS stands for Partitioned Top Level Acceleration Structure..."

Begin with something closer to:

"The classic TLAS bottleneck is not that it is incorrect. It is that small scene changes still tend to drag a large top-level rebuild policy behind them."

That is much closer to the Frame Graph series' best openings.

#### Give the reader a visible mental roadmap early

The Frame Graph posts are strong at telling the reader what structure they are about to follow.

For this PTLAS article, add a short early roadmap block like:

1. classic ray tracing structure baseline
2. what PTLAS changes
3. how vendors model it
4. where SparkleEngine is already strong
5. where the integration still falls back to full-scene behavior

This keeps a dense peer-level article easy to follow.

#### Teach through contrast

This is one of the biggest strengths of the Frame Graph series.
It frequently explains a system by putting two models side by side.

For PTLAS, the article should repeatedly compare:

- BLAS vs TLAS vs PTLAS
- classic TLAS rebuild behavior vs PTLAS selective update behavior
- logical update stream vs native operation stream
- vendor model vs current engine behavior
- claimed feature support vs measured real behavior

This is better than trying to explain PTLAS in isolation.

#### Use compact high-signal tables

The frame graph posts use tables very well when the reader needs quick orientation.

For PTLAS, the most useful tables are likely:

- BLAS / TLAS / PTLAS responsibility comparison
- Khronos / NVIDIA / Microsoft terminology comparison
- Sparkle “what already exists” vs “what still needs work”
- classic TLAS vs partitioned TLAS capture comparison

These should be compact and analytical, not decorative.

#### Alternate between concept and proof

The strongest Frame Graph sections do not stay abstract for too long.
They introduce an idea, then attach it to code, diagrams, or consequences.

For PTLAS, preserve that rhythm:

- concept
- vendor framing
- Sparkle implementation reality
- diagnostics / screenshot / metric

That pacing will help keep the article credible with your colleagues.

#### Use explanatory callouts sparingly and purposefully

The Frame Graph articles use callouts best when they:

- sharpen the takeaway
- highlight a trap
- state a tradeoff

For PTLAS, good callout candidates are:

- “PTLAS value is behavioral, not syntactic.”
- “Logical updates are not the same thing as selective native rebuilds.”
- “A valid API call can still miss the feature's intended payoff.”

Use a few strong ones, not many weak ones.

#### Prefer one standout visual per section over many small visuals

The Frame Graph series succeeds when a section has:

- one central diagram or visual anchor
- a short explanation around it

For this PTLAS article, avoid overloading every section with graphics.
A good one-article shape is:

- one baseline BLAS / TLAS / PTLAS comparison figure
- one PTLAS update model figure
- one Sparkle architecture or code-path figure
- one or two in-engine debug screenshots
- one compact evidence table

That is enough.

### 14.3 Things to avoid from the series pattern

Because this is not a series entry, avoid importing these patterns directly:

- part navigation bars
- repeated “Part I / Part II” references
- writing that depends on prior article context
- too much “we will cover the rest later” scaffolding

This article should feel complete on its own.

### 14.4 Best article shape for a one-off PTLAS piece

Based on the Frame Graph series, the strongest standalone shape is:

1. Hook with the real bottleneck
2. Give a short structure overview
3. Introduce PTLAS as a model change
4. Compare vendor framing
5. Show SparkleEngine's real current state
6. Show the gap between logical updates and selective native operations
7. End with proof criteria and next engineering steps

That gives the article the same clarity as the series without making it feel serialized.

### 14.5 Writing behaviors to copy from the Frame Graph posts

These are especially worth copying:

- short declarative paragraphs at section openings
- strong first sentence in each section
- explicit reader orientation
- concrete nouns over vague abstractions
- naming the tradeoff directly
- ending sections with a crisp takeaway

### 14.6 Writing behaviors to avoid for PTLAS

Do not:

- spend too long in generic ray tracing education
- overdo visual spectacle at the expense of the argument
- turn the post into an API token catalog
- bury SparkleEngine-specific insight under vendor summary
- let the article feel like setup for a future post instead of a finished statement

### 14.7 Recommended PTLAS article UX pattern

The best adaptation of the blog's current style is:

- short punchy intro
- one small “what you'll get from this article” block
- a few strong section separators
- dense but readable tables
- one or two standout diagrams
- matched screenshot + metric evidence
- strong concluding acceptance criteria

That will feel native to the blog and still work for an experienced engineering audience.

### 14.8 Narration-first constraint

This article also needs to work as a live narrated walkthrough for colleagues, not only as a static read.

That changes the UX target in useful ways:

- the article should be skimmable at a glance
- visuals should carry the main explanatory load
- prose should support spoken explanation rather than replace it
- sections should avoid repeating the same thesis in slightly different words
- each section should have one obvious visual or table the speaker can point at

Recommended practical rule:

- if a point can be shown clearly in a diagram, screenshot, table, or overlay, keep the surrounding prose short
- prefer compact framing paragraphs and strong captions over long dense explanation
- avoid long uninterrupted text blocks that would be tiring to read and awkward to present

## 15. Screenshot And Data Extraction Plan

This section turns the article into a capture checklist.

The good news is that Sparkle already has most of the infrastructure we need:

- smoke scene-color capture
- per-capture metadata JSON
- per-capture timing CSV
- PTLAS-specific debug view modes
- a viewport PTLAS debug overlay for manual screenshots

### 14.1 What the engine already gives us

Existing automated capture path:

- scene color image capture through `Renderer::CaptureViewportProductToBmp(...)`
- metadata export through `RhiSmokeCaptureArtifacts.cpp`
- timing export through `RhiSmokeCaptureArtifacts.cpp`

Existing PTLAS-focused view modes:

- `RayTracingPartitions`
- `RayTracingPartitionUpdates`
- `RayTracingInstanceMovement`
- `RayTracingGpuDrivenUpdates`
- `RayTracingTopLevelMode`
- `RayTracingNativeOperations`
- `RayTracingProviderStatus`

Existing PTLAS overlay metrics:

- top-level provider
- PTLAS provider
- PTLAS supported
- partition count
- dirty transform count
- moved partition count
- global partition instance count
- native operation count
- logical update count
- requested writer path
- selected writer path
- writer reason
- GPU API / writer availability flags
- BLAS GPU ms
- classic TLAS GPU ms
- RT pass GPU ms

Important capture caveat:

- the automated smoke capture grabs the renderer scene-color output
- the editor PTLAS overlay is UI
- therefore:
  automated captures are best for clean article figures
  manual editor screenshots are best when we want the overlay visible in the image

### 14.2 Recommended output set

Use two kinds of assets:

1. Clean renderer captures
   - generated automatically
   - no UI
   - best for article figures and side-by-side comparisons

2. Annotated editor screenshots
   - captured manually from the editor viewport
   - include the PTLAS overlay
   - best for one or two “proof / diagnostics” images

### 14.3 Recommended filename scheme

Use a stable naming scheme so later comparisons remain easy:

- `ptlas-lit-reference-<backend>-<mode>.bmp`
- `ptlas-partitions-<backend>-<mode>.bmp`
- `ptlas-partition-updates-<backend>-<mode>.bmp`
- `ptlas-instance-movement-<backend>-<mode>.bmp`
- `ptlas-top-level-<backend>-<mode>.bmp`
- `ptlas-native-ops-<backend>-<mode>.bmp`
- `ptlas-provider-status-<backend>-<mode>.bmp`
- `ptlas-gpu-updates-<backend>-<mode>.bmp`
- `ptlas-overlay-<backend>-<mode>.png`

Suggested mode suffixes:

- `classic`
- `partitioned-cpupack`
- `partitioned-gpulogical`
- `partitioned-fullgpu`

### 14.4 Minimum screenshot list

This is the minimum article-ready set I recommend.

#### Screenshot A: lit reference

Purpose:

- establish the baseline scene
- give the reader a visual anchor before debug views

Capture type:

- clean automated scene-color capture

View mode:

- `Lit`

#### Screenshot B: PTLAS partitions

Purpose:

- show the logical partitioning layout
- make the grid/global partition discussion concrete

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingPartitions`

#### Screenshot C: PTLAS partition updates

Purpose:

- show which instances or regions are currently dirty
- support the “localized motion” argument

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingPartitionUpdates`

Best taken:

- during a frame with active transform changes

#### Screenshot D: instance movement / partition crossing

Purpose:

- show the difference between dirty transforms and actual partition migration

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingInstanceMovement`

#### Screenshot E: top-level mode comparison

Purpose:

- show whether the engine selected classic TLAS or partitioned TLAS
- useful for one matched comparison between classic and partitioned modes

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingTopLevelMode`

Recommended pair:

- one capture with `r.RayTracing.PreferPartitionedTlas = false`
- one capture with `r.RayTracing.PreferPartitionedTlas = true`

#### Screenshot F: native operations

Purpose:

- show what the engine is actually submitting as PTLAS work
- especially valuable because the current engine still repacks a full-scene native write path

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingNativeOperations`

This is one of the most important figures for the article.

#### Screenshot G: provider status

Purpose:

- show backend/provider availability and fallback behavior
- useful for D3D12 vs Vulkan comparison

Capture type:

- clean automated scene-color capture

View mode:

- `RayTracingProviderStatus`

#### Screenshot H: one manual overlay screenshot

Purpose:

- show that the engine already exposes live PTLAS diagnostics in-editor
- make the metrics feel real and local to SparkleEngine

Capture type:

- manual editor screenshot

Recommended view mode:

- `RayTracingPartitionUpdates` or `RayTracingNativeOperations`

Reason:

- these are the most explanatory modes when paired with the overlay metrics

### 14.5 Optional screenshot list

Nice-to-have extras:

- `RayTracingGpuDrivenUpdates`
  - especially useful if you want to show requested vs selected writer path
- a second overlay screenshot on the alternate backend
- a classic TLAS screenshot paired with the PTLAS screenshot from the same camera
- an “after the fix” native-operations capture once selective native packing is implemented

### 14.6 Recommended capture matrix

For a strong peer-facing article, capture at least this matrix:

1. Backend: `D3D12`
   Mode: `classic`
   Views: `Lit`, `RayTracingTopLevelMode`, `RayTracingProviderStatus`

2. Backend: `D3D12`
   Mode: `partitioned-cpupack`
   Views: `RayTracingPartitions`, `RayTracingPartitionUpdates`, `RayTracingInstanceMovement`, `RayTracingNativeOperations`, `RayTracingProviderStatus`

3. Backend: `Vulkan`
   Mode: `partitioned-cpupack`
   Views: `RayTracingPartitions`, `RayTracingPartitionUpdates`, `RayTracingNativeOperations`, `RayTracingProviderStatus`

If time is limited, do D3D12 first.
If the article wants explicit cross-backend credibility, add Vulkan.

### 14.7 Recommended run states

For PTLAS article captures, collect two scene states:

1. Stable frame
   - low or zero dirty transforms
   - useful for partition layout and provider mode captures

2. Active update frame
   - non-zero dirty transforms and ideally non-zero moved partitions
   - required for update, movement, and native-operation captures

The article gets stronger if the same camera framing is reused across both states.

### 14.8 Smoke capture knobs to use

Relevant environment variables already supported by the engine:

- `SPARKLE_SMOKE_VALIDATE_RHI`
- `SPARKLE_SMOKE_SCENE_COLOR_CAPTURE`
- `SPARKLE_SMOKE_METADATA_PATH`
- `SPARKLE_SMOKE_TIMING_CSV`
- `SPARKLE_SMOKE_CAPTURE_PURPOSE`
- `SPARKLE_SMOKE_CAPTURE_LABEL`
- `SPARKLE_SMOKE_SCENE_COLOR_CAPTURE_FRAME`
- `SPARKLE_SMOKE_VIEW_MODE_NAME`
- `SPARKLE_SMOKE_PTLAS_CAPTURE_PRESET`
- `SPARKLE_SMOKE_FRAME_LIMIT`

Useful PTLAS runtime controls:

- `r.RayTracing.PreferPartitionedTlas`
- `r.RayTracing.Ptlas.PartitionsPerAxis`
- `r.RayTracing.Ptlas.GlobalPartition`
- `r.RayTracing.Ptlas.OperationWriterPath`

Recommended smoke capture pattern:

- one run per image
- fixed camera
- fixed frame index
- explicit capture label and purpose
- explicit metadata and CSV output path per capture

### 14.9 Recommended data files per capture

For each automated screenshot, save three files:

1. image
   - clean renderer output
2. metadata JSON
   - qualitative and configuration context
3. timing CSV
   - easy import into spreadsheet / charts

This gives every figure a matching evidence packet.

### 14.10 Data to extract from metadata JSON

Pull these fields into the article notes or a spreadsheet:

#### Capture identity

- `capture.path`
- `capture.frameIndex`
- `capture.viewModeName`
- `capture.captureLabel`
- `capture.purpose`

#### Renderer / hardware context

- backend
- adapter name
- driver description
- vendor ID
- device ID

#### Top-level mode / provider context

- `topLevelProvider`
- `topLevelProviderReason`
- `ptlasProvider`
- `ptlasSupported`
- `ptlasCapabilityReason`

#### Planner / scene state

- `totalRenderInstances`
- `traceableInstances`
- `staticTraceableInstances`
- `dynamicTraceableInstances`
- `partitionsPerAxis`
- `partitions`
- `gridPartitions`
- `dirtyTransforms`
- `movedPartitions`
- `globalPartitionEligibleInstances`
- `globalPartitionInstances`
- `duplicateStableIndices`
- `partitionOverflow`

#### Update-path state

- `logicalUpdates`
- `nativeOperations`
- `validationMismatches`
- `requestedOperationWriterPath`
- `operationWriterPath`
- `operationWriterReason`
- `gpuDrivenOperationApiSupported`
- `gpuLogicalUpdateWriterAvailable`
- `gpuNativePackAvailable`
- `gpuNativePackSubmitted`

#### Timing state

- `scenePrepareCpu`
- `sceneBuildCpu`
- `blasCpu`
- `blasGpu`
- `classicTlasCpu`
- `classicTlasInstancePreparationCpu`
- `classicTlasGpu`
- `ptlasCpuPackCpu`
- `ptlasGpuDirtyDetectionGpu`
- `ptlasGpuNativePackGpu`
- `ptlasUpdateGpu`
- `rayTracingPassGpu`
- `finalFrameGpu`

### 14.11 Data to extract from timing CSV

The CSV is the best source for compact comparison tables.

Use it to build:

- classic vs partitioned comparison table
- D3D12 vs Vulkan comparison table
- stable-frame vs update-frame comparison table
- requested writer path vs selected writer path comparison table

Derived metrics worth computing:

- dirty ratio = `dirtyTransforms / traceableInstances`
- global partition ratio = `globalPartitionInstances / traceableInstances`
- native op to logical update ratio = `nativeOperations / logicalUpdates`
- average instances per partition = `traceableInstances / partitionCount`

### 14.12 Data that is visible but better captured manually

Use the manual editor screenshot for:

- overlay text
- live writer selection
- live provider string
- live counts at the moment of the screenshot

Reason:

- these make excellent “trust anchor” visuals
- but they are presentation assets, not the cleanest source of numeric truth

For numbers, prefer the JSON / CSV.

### 14.13 Data gaps worth adding before the article

The current exports are good, but a few additions would make the article much stronger.

Most valuable missing metrics:

- partition occupancy histogram
- max / avg / p95 instances per partition
- explicit count of native op types:
  write instance vs update instance vs partition translation
- count of rewritten instances in the native operation pack
- explicit steady-state vs first-build marker
- explicit snapshot of requested config:
  prefer partitioned TLAS,
  partitions-per-axis,
  global partition enabled,
  requested writer path

If you want the article to make stronger claims, these are worth instrumenting first.

### 14.14 Recommended figure-to-evidence mapping

Each article figure should have a matching proof source.

- Partition layout image
  - proof: metadata JSON planner counts
- Partition update image
  - proof: dirty transform and moved partition counts
- Native operations image
  - proof: native operation count and logical update count
- Top-level mode comparison image
  - proof: top-level provider and provider reason
- Provider status image
  - proof: PTLAS supported flag and capability reason
- Any timing table
  - proof: timing CSV and metadata timings block

### 14.15 Small recommended capture script later

Not required for this design pass, but worth doing next:

- a small repeatable script that launches the editor with a chosen backend
- sets the smoke env vars
- sets one PTLAS debug view mode
- writes `.bmp`, `.json`, and `.timing.csv` into a per-figure folder

That will make article asset generation much less painful.

## 16. Evidence We Should Collect For The Final Article

If you want the final article to be especially strong, gather:

- one baseline diagram comparing BLAS, TLAS, and PTLAS responsibilities
- one or two diagrams of PTLAS vs classic TLAS update flow
- Sparkle smoke capture excerpts for provider selection and planner counters
- before/after metrics once selective native operation packing is live
- screenshots or visual debug output for partitions / global partition behavior
- one compact table mapping Khronos, NVIDIA, Microsoft, and Sparkle terminology
- one small code-path diagram showing where Sparkle currently diverges from the intended selective PTLAS model

## 17. Recommended Next Step For The Article

Best next drafting move:

Write the article around this claim:

"A PTLAS integration becomes real only when the engine's update stream controls which instances and partitions are rebuilt."

That gives the article:

- a thesis
- a baseline-to-difference teaching path
- a technical spine
- a reason to compare vendors
- a reason to discuss SparkleEngine honestly
- a natural ending in measurements and implementation roadmap

## 18. Open Questions For Pawel

These are the questions that most shape the article:

1. Do you want the article to be primarily:
   implementation-heavy SparkleEngine analysis,
   a broader cross-vendor PTLAS explainer,
   or a balanced hybrid?

2. Do you want to frame SparkleEngine as:
   "already integrating PTLAS and evolving toward behavior-correct selective updates",
   or more cautiously as
   "designing a PTLAS architecture and validating the right model"?

3. How much do you want Microsoft in the center of the story?
   Options:
   DirectX as co-equal with Vulkan/NVIDIA,
   or Microsoft as supporting context while Vulkan/NVIDIA remain the main concrete implementation references.

4. Do you want this article to stay architecture-first,
   or include performance claims and benchmarking once the selective update path is more complete?

5. Should the article explicitly discuss large-world precision and partition translation,
   or keep the first article focused on selective update behavior and global partitioning?

6. Since the main audience is your experienced rendering colleagues, do you want the final piece to read more like:
   an external article,
   or an internal-facing design review that just happens to live in the blog repo?

7. Do you want me to turn the capture plan into an actual reusable smoke-capture script next?

## 19. Source Set Used For This Design Pass

Primary external references:

- Khronos Vulkan PTLAS proposal:
  https://github.com/KhronosGroup/Vulkan-Docs/blob/main/proposals/VK_NV_partitioned_acceleration_structure.adoc
- Vulkan PTLAS reference page:
  https://docs.vulkan.org/refpages/latest/refpages/source/VK_NV_partitioned_acceleration_structure.html
- Vulkan PTLAS operation semantics:
  https://docs.vulkan.org/refpages/latest/refpages/source/VkPartitionedAccelerationStructureOpTypeNV.html
- Microsoft DirectX ray tracing functional spec, part 2:
  https://microsoft.github.io/DirectX-Specs/d3d/Raytracing2.html
- NVIDIA PTLAS sample:
  https://github.com/nvpro-samples/vk_partitioned_tlas
- NVIDIA RTX Mega Geometry / Vulkan sample announcement:
  https://developer.nvidia.com/blog/nvidia-rtx-mega-geometry-now-available-with-new-vulkan-samples/
- NVIDIA NVAPI DX docs:
  https://docs.nvidia.com/nvapi/group__dx.html
  https://docs.nvidia.com/nvapi/struct__NVAPI__D3D12__BUILD__RAYTRACING__PARTITIONED__TLAS__INDIRECT__INPUTS.html

Primary local references:

- `C:\Users\pawel.stolecki\Documents\GitHub\SparkleEngine\Docs\Rendering\PTLAS_TLAS_Design_Review.md`
- `C:\Users\pawel.stolecki\Documents\GitHub\SparkleEngine\Engine\Renderer\Private\RayTracing\RayTracingPtlasLogicalUpdateStream.cpp`
- `C:\Users\pawel.stolecki\Documents\GitHub\SparkleEngine\Engine\Renderer\Private\RayTracing\RayTracingPartitionedTlasStrategy.cpp`
- `C:\Users\pawel.stolecki\Documents\GitHub\SparkleEngine\Engine\RHI\Private\D3D12\RayTracing\D3D12NvapiRayTracingProvider.cpp`
- `C:\Users\pawel.stolecki\Documents\GitHub\SparkleEngine\Engine\RHI\Private\Vulkan\RayTracing\VulkanPartitionedTlasServices.cpp`
