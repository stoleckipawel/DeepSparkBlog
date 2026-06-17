# Next Gen RT Acceleration Structure: PTLAS vs TLAS

Draft status: Stage 5 draft 1  
Audience: experienced rendering engineers  
Mode: narration-friendly article draft

> PTLAS only matters when localized scene changes become localized top-level work.

## What You Will Get From This Article

This article is not a ray tracing primer.
It is a compact implementation review of what PTLAS changes, how current vendor models converge on the same behavioral goal, what SparkleEngine already has in place, and where the remaining gap still lives.

The short version is simple:

- classic TLAS is often correct but too coarse
- PTLAS changes the top-level update model, not the shader-facing role
- SparkleEngine already computes selective logical PTLAS updates
- the remaining hard part is making native PTLAS work become equally selective

## The Real Bottleneck

The interesting problem around PTLAS is not API exposure.
It is update granularity.

In a large scene, a small amount of instance motion can still drag broad top-level rebuild work behind it.
That makes the engine valid, but not especially selective.
For experienced rendering engineers, that is the real question: when scene change is local, how much top-level work still behaves as if the whole scene changed?

That is the bottleneck PTLAS is meant to address.
It turns top-level maintenance from one broad scene-wide update path into a routing problem over smaller pieces of top-level state.

`Figure 1 placeholder: BLAS / TLAS / PTLAS comparison table`

## A Short Structure Baseline

BLAS is not the interesting variable in this article.
BLAS still owns geometry acceleration data.
Classic TLAS still owns scene-level instances over BLAS content.

PTLAS matters because it keeps the same top-level traversal role while changing how scene updates are represented and maintained.
That is the key distinction to hold onto for the rest of the article: PTLAS is not a new shader-facing concept.
It is a different update model for top-level structure maintenance.

| Aspect | BLAS | Classic TLAS | PTLAS |
|---|---|---|---|
| Owns | Geometry acceleration data for one mesh or mesh group | Scene-level instances of BLAS objects | Scene-level instances organized into partitions |
| Primary role | Accelerate ray traversal through geometry | Accelerate ray traversal through scene instances | Preserve TLAS shader-facing role while changing how top-level updates are expressed |
| Typical changes across frames | Geometry changes, skinning, LoD or rebuild work | Instance transforms, instance membership, scene composition | Instance transforms, partition membership, partition translation, selective top-level updates |
| Small localized motion cost | Usually local to changed geometry | Often still tied to broad top-level work | Intended to touch only changed instances and affected partitions |
| Shader-facing behavior | Geometry leaf input | Top-level traversal entry | Same top-level traversal role as TLAS |
| Optimization question | When to rebuild vs update geometry | How much top-level work is redone per frame | How selective the instance and partition update stream really is |

The vendor sources reinforce the same point.
Khronos and Microsoft both frame PTLAS as a top-level structure model that preserves TLAS-like usage at the shader-facing boundary while changing how internal updates are expressed and partially rebuilt.

Source anchors:

- Khronos PTLAS proposal and reference:
  [Stage 1 source truth](C:/Users/pawel.stolecki/Documents/GitHub/DeepSparkBlog/notes/ptlas-stage1-source-truth.md)
- Microsoft PTLAS framing:
  [Stage 1 source truth](C:/Users/pawel.stolecki/Documents/GitHub/DeepSparkBlog/notes/ptlas-stage1-source-truth.md)

## What PTLAS Changes Conceptually

The useful way to think about PTLAS is not "TLAS, but partitioned" as a label.
The useful way to think about it is that the engine now has to decide which subset of top-level state a change should touch.

Once partitions exist, several things become first-class:

- partition-local ownership
- localized updates
- partition migration
- global-partition handling
- native operations that describe what changed rather than resubmitting the whole world blindly

Khronos makes this explicit through PTLAS operation semantics such as `WRITE_INSTANCE`, `UPDATE_INSTANCE`, and `WRITE_PARTITION_TRANSLATION`.
NVIDIA's sample material reinforces the same intended behavior by updating moving objects selectively instead of treating all instances as uniformly dirty.
Microsoft's PTLAS and indirect RTAS framing pushes in the same direction from the DirectX side.

The important consequence is this:

> PTLAS only pays off when the engine's logical update routing is reflected in the actual native work submission.

`Figure 2 placeholder: PTLAS update-model diagram`

Recommended visual support for the final article:

- E02 `PTLAS partitions`
- E03 `PTLAS partition updates`
- E04 `PTLAS instance movement`

## The Vendor Model Converges More Than It Diverges

The APIs do not look identical, but the behavioral target is unusually consistent.

Khronos frames PTLAS around partitions, reuse of previously built top-level work, and explicit PTLAS operation semantics.
NVIDIA frames it around selective maintenance in dynamic scenes, including a practical sample and NVAPI structures that make sizing and partition policy concrete.
Microsoft frames PTLAS as a persistent partially rebuildable top-level structure, with indirect RTAS operations and first-class support for the global partition concept.

That convergence matters for SparkleEngine.
It means Sparkle's PTLAS architecture can be judged against a shared behavioral standard rather than against vendor-specific naming alone.

| Concept | Khronos / Vulkan | NVIDIA sample / NVAPI | Microsoft DXR spec | SparkleEngine |
|---|---|---|---|---|
| Partitioned top-level structure | `VK_NV_partitioned_acceleration_structure` | Partitioned TLAS | Partitioned TLAS / PTLAS | `PartitionedTlas` top-level provider |
| Write instance op | `WRITE_INSTANCE` | PTLAS write instance operation | Partitioned TLAS write instance | Native operation header `WriteInstance` |
| Update instance op | `UPDATE_INSTANCE` | PTLAS update instance operation | Partitioned TLAS update instance | Planned/native op concept |
| Global partition | Global partition concept | Global partition support | Global partition concept | `GlobalPartition` planner/update state |
| Logical dirty state | App-defined | Moving instances in sample | Indirect operation arguments | `RayTracingPtlasLogicalUpdateStream` |

This section should stay compact in the published article.
Its job is to show alignment, not to become a standards summary.

## SparkleEngine Already Has Real PTLAS Architecture

SparkleEngine is already past the stage where PTLAS is just an idea.
The engine has a top-level strategy split, a partition planner, a logical update stream, backend-specific PTLAS service layers, smoke-capture export, and a live debug overlay that exposes PTLAS state directly.

That matters because the article is not evaluating a design sketch.
It is evaluating a real working architecture with observable behavior.

At a high level, the Sparkle path already looks like this:

- frame planning decides top-level strategy and packages debug state
- the partition planner assigns instances, detects dirtiness, and tracks movement
- the logical update stream emits selective logical update records
- the partitioned strategy builds native PTLAS work for the backend
- diagnostics export provider state, planner state, and timings for proof-oriented inspection

`Figure 3 placeholder: Sparkle PTLAS architecture diagram`

Strong local anchors for this section:

- planning flow:
  [RayTracingTopLevelScenePlanner.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingTopLevelScenePlanner.cpp:1>)
- partition model:
  [RayTracingPtlasPartitionPlanner.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.cpp:1>)
- logical update emission:
  [RayTracingPtlasLogicalUpdateStream.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:50>)
- D3D12 backend:
  [D3D12NvapiRayTracingProvider.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/RHI/Private/D3D12/RayTracing/D3D12NvapiRayTracingProvider.cpp:178>)
- Vulkan backend:
  [VulkanPartitionedTlasServices.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/RHI/Private/Vulkan/RayTracing/VulkanPartitionedTlasServices.cpp:146>)
- smoke evidence export:
  [RhiSmokeCaptureArtifacts.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:89>)
- overlay proof:
  [ViewportRayTracingDebugOverlay.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:89>)

Recommended visual support for the final article:

- E06 `Top-level mode partitioned`
- E08 `Provider status D3D12`
- E09 `Provider status Vulkan`
- E10 `GPU updates view`
- E11 `Manual overlay screenshot - partition updates`

## The Hard Part Is Not Naming the Feature

This is the center of the article.

SparkleEngine already computes selective logical PTLAS updates.
That is not a hypothetical claim.
The logical update stream explicitly filters changed instances and emits records for dirty or moved state rather than treating every instance as uniformly updated.

The strongest local proof lives here:

- logical update eligibility:
  [RayTracingPtlasLogicalUpdateStream.cpp:8](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:8>)
- changed-instance filtering:
  [RayTracingPtlasLogicalUpdateStream.cpp:64](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:64>)
- record emission:
  [RayTracingPtlasLogicalUpdateStream.cpp:70](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:70>)
- final logical count:
  [RayTracingPtlasLogicalUpdateStream.cpp:86](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:86>)

But that is only half of the story.
The harder question is whether the backend-facing native PTLAS work preserves that selectivity.

Today, the strongest evidence says not fully yet.
The current partitioned strategy builds a PTLAS layout, hands off the logical updates, but still constructs a single native operation pack around a broad full-scene `WriteInstance` path.
The code trail for that is unusually explicit:

- PTLAS layout build:
  [RayTracingPartitionedTlasStrategy.cpp:461](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:461>)
- `MaxOperations = 1`:
  [RayTracingPartitionedTlasStrategy.cpp:475](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:475>)
- logical update handoff:
  [RayTracingPartitionedTlasStrategy.cpp:523](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:523>)
- full instance write array build:
  [RayTracingPartitionedTlasStrategy.cpp:527](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:527>)
- single native operation header:
  [RayTracingPartitionedTlasStrategy.cpp:584](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:584>)
- one-operation pack descriptor:
  [RayTracingPartitionedTlasStrategy.cpp:589](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:589>)

The internal design review says the same thing in more direct terms:

- core gap:
  [PTLAS_TLAS_Design_Review.md:15](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:15>)
- full-scene rewrite finding:
  [PTLAS_TLAS_Design_Review.md:158](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:158>)

That is the distinction that matters most:

> Sparkle is already selective in what it knows, but not yet fully selective in what it submits.

`Figure 4 placeholder: classic TLAS vs PTLAS evidence table`

`Optional callout placeholder:`

```text
Selective logical updates: yes
Selective native PTLAS rebuilds: not yet fully realized
```

Recommended visual support for the final article:

- E07 `Native operations`
- E12 `Manual overlay screenshot - native operations`

## What Still Has To Change

Once the gap is named precisely, the roadmap becomes much clearer.
The engine does not need a different PTLAS story.
It needs the current logical story to survive all the way to native operation generation, submission policy, and steady-state measurement.

The practical next steps are straightforward:

| Current state | Target state |
|---|---|
| selective logical update records exist | native operations are generated from changed-instance and changed-partition sets |
| writer-path selection is visible | writer-path policy becomes measurable and easier to compare |
| PTLAS diagnostics already exist | diagnostics expose selective native work more directly |
| backend integrations are real | backend submissions reflect localized update intent |
| smoke data exports core PTLAS fields | evidence bundles make selective native behavior auditable |

The most useful follow-on instrumentation would be:

- rewritten-instance count
- native op type breakdown
- partition occupancy histogram
- steady-state vs first-build markers
- requested runtime PTLAS config captured alongside evidence

This is a good place in the article to stay disciplined.
The roadmap should stay tied to an observed limitation, not drift into a generic optimization wishlist.

## What Success Looks Like

For PTLAS, success should not mean "the API exists" or even "the partitioned backend was selected."
Success is when localized scene motion reliably results in localized native top-level work, and the engine can prove that with both diagnostics and evidence bundles.

That gives the article a concrete acceptance checklist:

- changed instances do not imply broad full-scene native rewrite behavior
- partition migrations are visible and explainable
- provider selection and fallback reporting are trustworthy
- update timings are interpreted together with update counts
- backend comparisons are honest about differences in maturity or proof quality

The internal design review already points in that direction:

- PTLAS acceptance criterion framing:
  [PTLAS_TLAS_Design_Review.md:58](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:58>)
- success criteria wording:
  [PTLAS_TLAS_Design_Review.md:491](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:491>)

When the final capture set is ready, the closing proof table should summarize at least:

- top-level provider
- PTLAS provider
- partition count
- dirty transforms
- moved partitions
- logical updates
- native operations
- selected writer path
- PTLAS update GPU time

That will make the ending more than a conclusion.
It will make it auditable.

## Closing

The shift from TLAS to PTLAS is only superficially about a new API surface.
The real change is that an engine begins to treat top-level updates as selective work instead of broad scene-wide maintenance.

SparkleEngine already has many of the right pieces in place: a partition planner, a logical update stream, backend-specific PTLAS paths, smoke-capture export, and a live overlay that makes the feature inspectable.
The remaining hard part is not conceptual.
It is making native PTLAS work become as selective as the logical model already is.

That is the standard worth holding the integration to.
When localized motion becomes localized native top-level work, PTLAS stops being mostly architectural intent and starts becoming measurable engine behavior.

## Evidence And Figure Notes For Revision

This draft intentionally uses figure placeholders and evidence hooks so it can already support narration while Stage 2 capture bundles are still being gathered.

Final article revision should replace placeholders with:

- Figure 1 `BLAS / TLAS / PTLAS comparison table`
- Figure 2 `PTLAS update-model diagram`
- Figure 3 `Sparkle PTLAS architecture diagram`
- Figure 4 `Classic TLAS vs PTLAS evidence table`
- E06, E07, E08, E09, E10, E11, E12 capture inserts where noted

Claims already backed in this draft:

- PTLAS exists to avoid broad full classic TLAS rebuild behavior under localized change
- PTLAS is a top-level update-model change rather than a shader-facing semantic change
- Sparkle already has real PTLAS planning, diagnostics, and backend integration work
- Sparkle already emits selective logical PTLAS updates
- Sparkle's current live native PTLAS path still collapses into a broad full-scene write behavior

Claims intentionally avoided here:

- direct performance win claims for Sparkle PTLAS today
- backend parity claims without final capture proof
- any statement that Sparkle already achieves minimal native PTLAS work per changed instance or partition
