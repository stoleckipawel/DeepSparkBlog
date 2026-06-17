# PTLAS Stage 4 Article Skeleton

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Article: `Next Gen RT Acceleration Structure: PTLAS vs TLAS`
Depends on:

- `notes/ptlas-article-design-doc.md`
- `notes/ptlas-article-creation-stages.md`
- `notes/ptlas-stage1-source-truth.md`
- `notes/ptlas-stage2-evidence-package.md`
- `notes/ptlas-stage3-visual-assets.md`

## 1. Purpose

This document completes Stage 4 in draft form.

Its job is to turn the article plan, source truth, evidence package, and visual drafts into a real writing skeleton that can be expanded into the first full article draft.

This document is not the final article.
It is the article's assembly blueprint.

## 2. Stage 4 Goal

Write section headers, opening paragraphs, transitions, and planned evidence blocks.

## 3. Stage 4 Deliverables

- complete section outline
- intro
- ending
- per-section evidence notes

## 4. Stage 4 Exit Criteria

Stage 4 is complete when:

- no section remains vague
- every section knows what screenshot, table, metric, or code reference it will use
- the article can be drafted end to end without inventing structure mid-write

## 5. Article Thesis

Working thesis:

`PTLAS matters only when an engine turns localized scene changes into localized top-level work.`

Narration spine:

`classic acceleration structures -> classic TLAS update problem -> PTLAS solution model -> implementation proof`

The article should make that progression visible:

- baseline: BLAS / TLAS / update-refit-rebuild vocabulary
- problem: local scene changes can still feed broad TLAS maintenance
- solution: PTLAS partitions top-level state so work can be expressed locally
- proof: logical updates can be selective; native submission must preserve that selectivity

Core reader takeaway:

`PTLAS is designed so top-level update cost can follow the instances and partitions that actually changed, instead of behaving like the worst-case whole scene changed every frame.`

Wording guardrail:

- avoid saying PTLAS guarantees paying only for animated objects
- prefer `enables`, `is designed for`, or `lets the engine express`
- connect the benefit to changed instances, touched partitions, partition quality, and native operation generation

Implementation thesis:

`Selective logical PTLAS updates are only valuable if the native top-level work remains selective.`

## 6. Reader Contract

This article should feel like:

- a peer-to-peer implementation review
- a grounded explanation of what PTLAS changes in practice
- an honest account of where implementation evidence supports the model and where the payoff is still incomplete
- a narration-friendly visual article that supports live explanation

This article should not feel like:

- a long ray tracing 101 refresher
- a vendor API catalog
- a generic "future optimization ideas" post
- a wall of text that requires careful line-by-line reading

## 7. Presentation Constraints

Because this article will also support a live walkthrough for colleagues, the article should optimize for scanability and narration support, not just static reading.

Practical constraints:

- keep section prose compact
- avoid repeating the same idea in multiple sections
- prefer one strong visual anchor per section
- let visuals, tables, and overlays carry as much meaning as possible
- keep paragraph blocks short enough to skim while listening
- use text to frame visuals, not to compete with them

Recommended writing rules for Stage 5:

- target 2 to 4 short paragraphs per main section before figures or tables
- prefer one clear takeaway sentence over long explanatory buildup
- if a point can be shown with a table, diagram, capture, or overlay, do not also explain it at full length in prose
- use captions and short callouts to support spoken narration
- each section should still make sense silently, but should feel even stronger when presented aloud
- each section should clearly belong to baseline, problem, solution, or proof

## 8. Draft Intro

### Opening paragraph draft

For an experienced rendering engineer, the interesting question about PTLAS is not whether the API exists. The interesting question is what actually changes inside an engine once top-level updates stop being treated as one broad scene-wide operation. If a small amount of instance motion still collapses into effectively full-scene top-level work, then PTLAS is present as infrastructure but not yet fully present as behavior.

### Follow-up paragraph draft

That is the frame I want to use for the implementation example. SparkleEngine gives us a concrete path to inspect: partition planning, logical update generation, backend service layers, and diagnostics. The harder part, and the one that matters most, is whether those selective logical updates become genuinely selective native rebuild work on the backend path.

### Reader payoff paragraph draft

This article is a technical walk through of that transition. It starts from a compact BLAS / TLAS / PTLAS baseline, lines the model up against Khronos, NVIDIA, and Microsoft material, and then uses local code, captures, and diagnostics to show where selectivity is preserved, where it can collapse, and what success should look like.

### Intro evidence block

Use:

- Figure 0A `Classic BLAS / TLAS ownership baseline`
- Figure 0B `Classic TLAS rebuild vs update/refit baseline`
- Figure 1 `BLAS / TLAS / PTLAS comparison table`
- one sentence preview of Figure 3 `Implementation PTLAS architecture`

Do not use:

- performance claims
- dense vendor terminology

## 9. Full Section Outline

### Section 0: Classic TLAS baseline

#### Section goal

Establish the minimum acceleration-structure vocabulary needed before PTLAS appears, without putting ownership, rebuild/refit, and the PTLAS motivation into one overloaded visual.

#### Opening paragraph draft

Before PTLAS makes sense, the article needs one shared baseline: BLAS owns geometry acceleration data, TLAS owns scene instance acceleration data, and classic top-level updates operate against one scene-level structure. Update/refit and rebuild are not the same tool, so they need their own short explanation before PTLAS changes the granularity of top-level maintenance.

#### Section development notes

Keep this section compact and visual, but split the visuals by question.

Explain only:

- BLAS as geometry acceleration
- TLAS as instance acceleration over BLAS references
- update/refit as preserving an existing structure shape where possible
- rebuild as reconstructing the structure more fully
- why a small set of moved instances can still feed a broad TLAS update path

Visual split:

- `rt-as-baseline.html` answers what BLAS and TLAS own
- `rt-as-update-modes.html` answers how classic TLAS rebuild and update/refit differ
- the problem statement comes after those visuals, not inside them

This is not a beginner tutorial. It is the comparison point that makes the PTLAS delta obvious.

#### Transition out

Once that baseline is established, PTLAS can be introduced as a change in top-level update granularity rather than as a disconnected new structure.

#### Planned evidence

- Figure 0A `Classic BLAS / TLAS ownership baseline`
- Figure 0B `Classic TLAS rebuild vs update/refit baseline`
- Figure 1 `BLAS / TLAS / PTLAS comparison table` later as the compact delta table

#### Planned metrics

- none required here

#### Risks to avoid

- spending too long explaining ray tracing basics
- making BLAS sound like the main optimization target of the article

### Section 1: The real bottleneck

#### Section goal

Establish why PTLAS matters without re-explaining ray tracing fundamentals.

#### Opening paragraph draft

After the classic baseline, the problem is narrow and concrete: scene changes are often local, but classic TLAS maintenance is still organized around one scene-level top-level structure. A frame with a handful of moved instances may still drive broad top-level work, which means the engine is correct but not especially selective.

#### Section development notes

This section should quickly define the problem shape:

- localized scene motion
- top-level work amplification
- the difference between valid updates and valuable updates
- problem statement:
  `the granularity of scene change is often smaller than the granularity of classic TLAS maintenance`

Keep it short.
This is the motivation section, not the architecture dump.
This section should read almost like a spoken opening setup.

#### Transition out

To make that concrete, the article should briefly re-establish what BLAS, TLAS, and PTLAS each own and what kind of update behavior they imply.

#### Planned evidence

- Figure 1 `BLAS / TLAS / PTLAS comparison table`

#### Planned code/source support

- Stage 1 vendor/source truth summary only

#### Planned metrics

- none required here

#### Risks to avoid

- too much history
- repeating standard DXR/Vulkan explanations the audience already knows

### Section 2: Ray tracing structure overview

#### Section goal

Give the shortest possible shared baseline for BLAS, TLAS, and PTLAS.

#### Opening paragraph draft

For this article, BLAS is not the interesting variable. BLAS still owns geometry acceleration data, and TLAS still defines the scene-level traversal entry over instances. PTLAS matters because it changes how top-level scene change is represented and updated, while keeping the shader-facing role recognizably top-level.

#### Section development notes

Walk the table row by row only where the delta matters:

- ownership
- typical frame-to-frame change
- what localized motion invalidates
- what optimization question each structure creates

This section should explicitly say:

`PTLAS is not a different shader-facing concept from TLAS. It is a different update model for top-level structure maintenance.`

Keep the prose tight and let Figure 1 do most of the teaching work.

#### Transition out

Once that baseline is shared, the next step is the important conceptual shift: partitioning turns top-level change from one large scene update problem into a selective update-routing problem.

#### Planned evidence

- Figure 1 `BLAS / TLAS / PTLAS comparison table`
- optional crop from E02 `PTLAS partitions` if the article benefits from an early visual

#### Planned code/source support

- Khronos PTLAS proposal and semantics
- Microsoft RTAS/PTLAS framing

#### Planned metrics

- none required here

#### Risks to avoid

- using this section as a glossary
- introducing the implementation example too early before the concept is clear

### Section 3: What PTLAS changes conceptually

#### Section goal

Explain partitions, global partition behavior, and selective updates as the mental model the rest of the article depends on.

#### Opening paragraph draft

The useful way to think about PTLAS is not "TLAS, but partitioned" as a label. The useful way to think about it is that the engine now has to decide which subset of top-level state a scene change should touch. Once partitions exist, instance movement, partition crossings, global-partition cases, and top-level maintenance all become routing decisions instead of one monolithic update path.

#### Section development notes

Core ideas to explain:

- scene instances are assigned into partitions
- partitions create localized top-level ownership
- some updates affect only a subset of partitions
- some updates affect partition membership
- the global partition exists for cases that do not map cleanly to local partition ownership
- partition translation exists in the model but should stay secondary in this first article

This section should set up the sentence that drives the rest of the article:

`PTLAS only pays off when the engine's logical update routing is reflected in the actual native work submission.`

The diagram and captures should do most of the heavy lifting here.

#### Transition out

That conceptual model is not just local implementation vocabulary. The vendor material converges on the same idea, even if each API surface exposes it differently.

#### Planned evidence

- Figure 2 `PTLAS update-model diagram`
- E02 `PTLAS partitions`
- E03 `PTLAS partition updates`
- E04 `PTLAS instance movement`

#### Planned code/source support

- Khronos operation semantics
- NVIDIA sample behavior around moved instances
- Microsoft indirect RTAS / PTLAS framing

#### Planned metrics

- `partitionCount`
- `dirtyTransforms`
- `movedPartitions`
- `globalPartitionInstances`

#### Risks to avoid

- overspecifying vendor enums in the main prose
- making partition translation sound central if it is not needed for the first article

### Section 4: Vendor model

#### Section goal

Show that the article's framing is aligned with real vendor concepts rather than being private engine vocabulary.

#### Opening paragraph draft

One encouraging part of the PTLAS space is that the vendor material converges on the same practical question. Khronos exposes explicit PTLAS operations and structure semantics, NVIDIA's samples and NVAPI documentation frame PTLAS in terms of selective top-level maintenance, and Microsoft's ray tracing spec material pushes in the same direction through partitioned TLAS and indirect RTAS language. The syntax differs, but the behavioral target is consistent.

#### Section development notes

This section should stay compact.

Organize it around convergences:

- partitioned top-level structure
- write/update style operations
- partition-local maintenance
- global partition handling
- indirect/native work generation

Then map those ideas into the implementation checkpoints.
This should likely be the shortest section in the article.

#### Transition out

With that alignment in place, the article can stop speaking abstractly and inspect one concrete implementation path.

#### Planned evidence

- optional `Vendor terminology map` from Stage 3
- one short pull-quote style summary sentence from each vendor family, paraphrased not quoted heavily

#### Planned code/source support

- Khronos PTLAS extension / proposal
- NVIDIA sample
- NVIDIA NVAPI docs
- Microsoft ray tracing 2 / RTAS spec material

#### Planned metrics

- none required here

#### Risks to avoid

- turning the section into a standards summary
- pretending perfect parity between APIs where the evidence is thinner

### Section 5: Concrete implementation lens

#### Section goal

Use a concrete implementation path to show where PTLAS selectivity can survive or collapse.

#### Opening paragraph draft

At this point the useful question is not whether PTLAS-shaped systems exist in the code. The useful question is where selectivity is authored, where it is packed into native work, and where diagnostics can prove what happened. SparkleEngine is used here as the inspectable implementation example.

#### Section development notes

This is where the article should introduce the implementation shape:

- `RayTracingTopLevelScenePlanner::PlanFrame`
- `RayTracingPtlasPartitionPlanner`
- `RayTracingPtlasLogicalUpdateStream`
- `RayTracingPartitionedTlasStrategy`
- backend PTLAS services
- smoke metadata and overlay diagnostics

Recommended subsection flow:

1. strategy selection and frame planning
2. partition planning and logical dirty-state generation
3. backend execution layer
4. diagnostics surface

The architecture figure and overlay screenshot should carry a large share of the explanation.

#### Transition out

At this point the article should have earned the right to ask the hard question: if logical PTLAS updates are selective, where exactly can the behavioral gap still remain?

#### Planned evidence

- Figure 3 `Implementation PTLAS architecture`
- E06 `Top-level mode partitioned`
- E08 `Provider status D3D12`
- E09 `Provider status Vulkan`
- E11 `Manual overlay screenshot - partition updates`
- E10 `GPU updates view`

#### Planned code/source support

- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingTopLevelScenePlanner.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp`
- `SparkleEngine/Engine/RHI/Private/D3D12/RayTracing/D3D12NvapiRayTracingProvider.cpp`
- `SparkleEngine/Engine/RHI/Private/Vulkan/RayTracing/VulkanPartitionedTlasServices.cpp`
- `SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp`
- `SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp`

#### Planned metrics

- `topLevelProvider`
- `topLevelProviderReason`
- `ptlasProvider`
- `ptlasSupported`
- `ptlasCapabilityReason`
- `selectedWriterPath`
- `writerReason`
- `partitionCount`
- `logicalUpdates`

#### Risks to avoid

- burying the debug/diagnostics story even though it is one of the clearest proof points
- overloading the reader with file names before showing the shape visually

### Section 6: The hard part

#### Section goal

Make the article's strongest technical point: selective logical updates are not enough if the native path still collapses into broader write behavior.

#### Opening paragraph draft

The missing piece is not conceptual. The implementation can know which instances are dirty, which partitions are affected, and which logical updates should exist. The harder problem is the last mile: whether the backend-facing PTLAS work preserves that selectivity or whether it gets repacked into something closer to a full-scene write batch.

#### Section development notes

This section should be the most code-backed section in the article.
It should not become the longest wall of prose.

Recommended structure:

1. show that logical update generation is selective
2. show that the native PTLAS write path still repacks broad scene state
3. explain why this is the difference between architecture presence and behavioral payoff
4. connect visible diagnostics to the code path

Prefer short prose blocks followed by evidence.

This section should contain the clearest single statement in the article:

`Selective knowledge is not the same thing as selective native work.`

#### Transition out

Once that gap is named precisely, the remaining work becomes much easier to describe as engineering targets rather than vague aspirations.

#### Planned evidence

- Figure 4 `Classic TLAS vs PTLAS evidence table`
- E07 `Native operations`
- E12 `Manual overlay screenshot - native operations`
- optional `Current gap callout` from Stage 3

#### Planned code/source support

- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp`
- `SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md`

#### Planned code points to cite

- logical update eligibility and emission in `RayTracingPtlasLogicalUpdateStream.cpp`
- single-op/native pack setup in `RayTracingPartitionedTlasStrategy.cpp`
- full-scene write batch behavior described in the design review

#### Planned metrics

- `dirtyTransforms`
- `movedPartitions`
- `logicalUpdates`
- `nativeOperations`
- `selectedWriterPath`
- `ptlasUpdateGpuMs`
- `rayTracingPassGpuMs`

#### Risks to avoid

- accidental overclaiming that the current implementation has no PTLAS value yet
- accidental underclaiming that full selectivity is already achieved
- presenting raw timings without update-volume context

### Section 7: What still has to change

#### Section goal

Turn the identified gap into a concrete engineering roadmap.

#### Opening paragraph draft

Once the gap is described in those terms, the next steps become fairly concrete. The logical story needs to survive all the way to native operation generation, submission policy, and steady-state measurement. That is a tractable engineering roadmap, and it is much more specific than "optimize PTLAS later."

#### Section development notes

Recommended roadmap bullets:

- generate native operations from changed-instance and changed-partition sets
- track occupancy and partition sizing health
- make writer-path policy measurable rather than implicit
- separate first-build behavior from steady-state update behavior
- add instrumentation that makes selective native work directly observable

This section should be practical, not aspirational.
Use a compact current-state vs target-state format if possible.

#### Transition out

That roadmap also gives the article a clean definition of success, which matters more than any single screenshot or timing number.

#### Planned evidence

- short current-state vs target-state table
- optional E10 `GPU updates view`
- optional reuse of Figure 4 with a "current vs desired inference" emphasis

#### Planned code/source support

- design review success criteria
- writer-path diagnostics and metadata export

#### Planned metrics

- `selectedWriterPath`
- `writerReason`
- `logicalUpdates`
- `nativeOperations`
- optional future metrics:
  - rewritten-instance count
  - native op type breakdown
  - partition occupancy histogram

#### Risks to avoid

- turning the roadmap into a generic optimization backlog
- proposing changes the article cannot connect back to a specific current limitation

### Section 8: What success looks like

#### Section goal

Close the article with measurable acceptance criteria instead of a vague summary.

#### Opening paragraph draft

For a feature like PTLAS, success should not be defined as "the engine supports the API" or even "the engine selected the partitioned backend." Success is when localized motion reliably results in localized top-level native work, diagnostics report that state clearly, and captures make the improvement visible enough that another rendering engineer can audit the claim.

#### Section development notes

This section should end on acceptance criteria such as:

- changed instances do not imply broad full-scene native rewrite behavior
- partition migrations are visible and explainable
- provider selection and fallback state are trustworthy
- update timings are interpreted together with update counts
- D3D12 and Vulkan evidence are compared honestly, not flattened

This ending should feel presentation-friendly: short, decisive, and easy to speak over while showing the final proof table.

#### Ending paragraph draft

That is the standard I want to hold a PTLAS implementation to. The remaining task is to make native work become as selective as the logical model that requested it. When that happens, the shift from TLAS to PTLAS stops being mostly conceptual and starts being measurable engine behavior.

#### Planned evidence

- Figure 4 `Classic TLAS vs PTLAS evidence table`
- acceptance criteria checklist

#### Planned code/source support

- `SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md`
- Stage 2 evidence bundles as proof backing

#### Planned metrics

- `logicalUpdates`
- `nativeOperations`
- `ptlasUpdateGpuMs`
- `topLevelProvider`
- `ptlasProvider`

#### Risks to avoid

- ending with only "future work"
- losing the main thesis in a generic conclusion

## 10. Section-to-Evidence Map

| Section | Visuals | Capture bundles | Code / source anchors | Metrics |
|---|---|---|---|---|
| 0. Classic TLAS baseline | Figure 0A, Figure 0B | none | NVIDIA DXR tutorial, NVIDIA Vulkan tutorial, NVIDIA RTX best practices | none |
| 1. The real bottleneck | Figure 1 | optional E01 | vendor/source truth only | none |
| 2. Structure overview | Figure 1 | optional E02 | Khronos + Microsoft | none |
| 3. What PTLAS changes conceptually | Figure 2 | E02, E03, E04 | Khronos + NVIDIA + Microsoft | partitionCount, dirtyTransforms, movedPartitions, globalPartitionInstances |
| 4. Vendor model | optional terminology table | E08, E09 optional | Khronos, NVIDIA, NVAPI, Microsoft | none |
| 5. Concrete implementation lens | Figure 3 | E06, E08, E09, E10, E11 | planner, strategy, provider, smoke, overlay files | topLevelProvider, ptlasProvider, selectedWriterPath, partitionCount, logicalUpdates |
| 6. The hard part | Figure 4, optional gap callout | E07, E12 | logical update stream, partitioned strategy, design review | dirtyTransforms, movedPartitions, logicalUpdates, nativeOperations, ptlasUpdateGpuMs |
| 7. What still has to change | short roadmap table | optional E10 | design review + diagnostics | selectedWriterPath, writerReason, logicalUpdates, nativeOperations |
| 8. What success looks like | Figure 4 + checklist | E05, E06, E07, E08, E09 | design review + Stage 2 bundles | logicalUpdates, nativeOperations, ptlasUpdateGpuMs, topLevelProvider, ptlasProvider |

## 11. Mandatory Drafting Inputs Before Stage 5

Before writing the full article draft, confirm these inputs exist:

- final Figure 0A classic BLAS / TLAS ownership baseline
- final Figure 0B classic TLAS rebuild vs update/refit baseline
- final Figure 1 table text
- final Figure 2 diagram rendering
- final Figure 3 diagram rendering
- final Figure 4 table populated with real bundle data
- at least one strong D3D12 PTLAS evidence set
- at least one provider-status capture per backend discussed
- one readable manual overlay screenshot for section 5
- one readable manual overlay screenshot for section 6

If these are missing, Stage 5 can still start, but the article should clearly mark placeholders rather than improvising claims.

## 12. Stage 4 Status

Current status:

- complete section outline: drafted
- intro: drafted
- ending: drafted
- per-section evidence notes: drafted

## 13. Best Next Step

After this skeleton, the next step is Stage 5:

- create the first full article markdown draft
- keep the prose close to this structure
- pull every concrete claim from Stage 1, Stage 2, or local Sparkle code references
