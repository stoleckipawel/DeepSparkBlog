---
title: "Next Gen RT Acceleration Structure: PTLAS vs TLAS"
date: 2026-06-17
lastmod: 2026-06-17
draft: true
authors: ["Pawel Stolecki"]
description: "A peer-level PTLAS article about what changes when an engine moves from classic TLAS maintenance to partitioned top-level updates."
tags: ["rendering", "ray-tracing", "ptlas", "vulkan", "d3d12", "engine-architecture"]
categories: ["analysis"]
summary: "PTLAS is not just a new API surface. It is a different top-level update model, and its value only appears when localized scene change becomes localized native top-level work."
showTableOfContents: false
keywords: ["PTLAS", "TLAS", "BLAS", "ray tracing", "partitioned TLAS", "Vulkan", "D3D12", "NVAPI", "rendering engine", "SparkleEngine"]
---

PTLAS is not interesting because the API exists.
PTLAS is interesting because it changes what an engine is allowed to do when only a small part of a scene changes.

To keep the discussion concrete, I use SparkleEngine as an implementation example. The useful question is not whether an engine has PTLAS-shaped code, but whether selective scene knowledge survives all the way down to native top-level work submission.

The article follows one line: classic TLAS is valid but coarse; PTLAS gives us a more selective top-level maintenance model; the implementation path decides whether that selectivity becomes real submitted work.

## First, The Classic TLAS Baseline

Before PTLAS, we need to give the classic model proper credit. [NVIDIA's DXR tutorial](https://developer.nvidia.com/rtx/raytracing/dxr/dx12-raytracing-tutorial-part-1) frames the starting point cleanly: a BLAS stores geometry, while a TLAS is built over instances that reference those BLAS objects and carry their own transforms. The [NVIDIA Vulkan ray tracing tutorial](https://nvpro-samples.github.io/vk_raytracing_tutorial_KHR/concepts/acceleration-structures/) uses the same shape: create BLAS from mesh geometry, create TLAS instances with transforms and BLAS references, then build the TLAS for scene traversal.

{{< rt-as-baseline >}}

The next piece of vocabulary is rebuild versus update/refit. A TLAS rebuild creates the top-level structure again from the current instance descriptions. A TLAS update/refit reuses a previous update-capable structure and changes the instance-side data, usually transforms.

That second path is real and useful, but it is not automatically better. [NVIDIA's RTX best-practices guidance](https://developer.nvidia.com/blog/rtx-best-practices/) is deliberately conservative here: in many cases, rebuilding the TLAS is easier to manage, and the saved refit cost may not justify lower TLAS quality. So the baseline is not "rebuild bad, refit good." The baseline is a tradeoff inside one classic top-level structure.

{{< rt-as-update-modes >}}

## The Problem We Want To Solve

After the classic baseline, the problem is narrow and concrete: scene changes are often local, but classic TLAS maintenance is still organized around one scene-level top-level structure.

A few moved instances may occupy a tiny part of the world, and classic rebuild/refit choices can still be perfectly valid. That is exactly the point: valid acceleration-structure maintenance is not automatically partition-local acceleration-structure maintenance.

The goal is not to make animation free. The goal is to make top-level work track the instances and regions that actually changed instead of treating a local update like a full-scene event.

## PTLAS As The Solution Shape

PTLAS is the answer to that granularity mismatch. It keeps the shader-facing role of a top-level acceleration structure, but changes how the engine can maintain that top level across frames.

Instances still reference BLAS objects. Rays still enter a top-level structure. The difference is that top-level state is organized into partitions, so update work can be described in terms of changed instances, touched partitions, and the global partition for highly dynamic cases.

{{< ptlas-structure-slide >}}

## The Behavior We Want To See

The behavior target is simple: most of the scene is present, but only the moving region becomes hot.

{{< interactive-ptlas-domino-field >}}

The domino sample also shows that PTLAS is not one automatic strategy. Moving instances create a policy choice.

{{< ptlas-partition-policy >}}

## The Delta In One Table

This is the compact delta behind the rest of the article.

| Aspect | BLAS | Classic TLAS | PTLAS |
|---|---|---|---|
| Owns | Geometry acceleration data for one mesh or mesh group | Scene-level instances of BLAS objects | Scene-level instances organized into partitions |
| Role | Accelerate geometry traversal | Accelerate scene instance traversal | Same top-level traversal role, different maintenance model |
| Typical frame change | Geometry updates, skinning, rebuild work | Instance transforms, membership, metadata | Instance changes plus partition ownership |
| Small localized motion cost | Usually local to changed geometry | Often still tied to broad top-level work | Intended to touch only changed instances and affected partitions |
| Main optimization question | When to rebuild vs update geometry | How much top-level work is redone per frame | How selective the instance and partition update stream really is |

Khronos and Microsoft both support the same framing here: PTLAS is not a different shader-facing concept from TLAS. It is a different model for maintaining top-level scene state.

## Who Owns The Update Work?

Once the top level is partitioned, the next integration question is who authors the update description.

The CPU still owns high-level policy, feature selection, sizing, allocation, command recording, and synchronization. Sparse per-frame update data can be produced on the CPU or GPU depending on where simulation and dirty detection live. The actual PTLAS build/update work is still GPU-executed native work.

The practical consequence is simple:

> PTLAS only pays off when the engine's logical update routing is reflected in the actual native work submission.

GPU-driven does not mean the CPU disappears. It means per-frame operation data can be generated and consumed without pulling the whole update decision back to the host.

{{< ptlas-cpu-gpu-split >}}

## The Vendor Model Converges More Than It Diverges

The APIs do not look identical, but the behavioral target is unusually consistent.

Khronos frames PTLAS around partitions, reuse of previously built top-level work, and explicit PTLAS operations. NVIDIA frames it around selective maintenance in dynamic scenes, plus concrete sizing and policy concerns through sample code and NVAPI. Microsoft frames PTLAS as a persistent partially rebuildable top-level structure with indirect RTAS operations and a first-class global partition concept.

That convergence matters because implementation details can differ without changing the behavioral test: local scene change should be expressible as local top-level work.

| Concept | Khronos / Vulkan | NVIDIA sample / NVAPI | Microsoft DXR spec | Implementation checkpoint |
|---|---|---|---|---|
| Partitioned top-level structure | `VK_NV_partitioned_acceleration_structure` | Partitioned TLAS | Partitioned TLAS / PTLAS | `PartitionedTlas` top-level provider |
| Write instance op | `WRITE_INSTANCE` | PTLAS write instance operation | Partitioned TLAS write instance | Native operation header `WriteInstance` |
| Update instance op | `UPDATE_INSTANCE` | PTLAS update instance operation | Partitioned TLAS update instance | Planned/native op concept |
| Global partition | Global partition concept | Global partition support | Global partition concept | `GlobalPartition` planner/update state |
| Logical dirty state | App-defined | Moving instances in sample | Indirect operation arguments | `RayTracingPtlasLogicalUpdateStream` |

## A Concrete Implementation Lens

At this point the idea is clear enough to ask an implementation question: where can selectivity survive, and where can it be lost?

The useful checkpoints are:

- frame planning chooses the top-level strategy
- partition planning decides spatial ownership
- the logical update stream records dirty or moved instances
- native operation packing turns logical state into backend work
- diagnostics expose whether the submitted work stayed selective

In SparkleEngine, that path currently looks like this:

{{< mermaid >}}
flowchart LR
    A["RenderSceneData"]
    B["RayTracingTopLevelScenePlanner::PlanFrame"]
    C["RayTracingPtlasPartitionPlanner"]
    D["RayTracingPtlasLogicalUpdateStream"]
    E["RayTracingPartitionedTlasStrategy::Prepare"]
    F["RayTracingPartitionedTlasStrategy::Build"]
    G["UploadLogicalUpdateRecords"]
    H["CPU native operation pack"]
    I["D3D12 NVAPI provider / Vulkan PTLAS services"]
    J["Smoke diagnostics / debug overlay"]

    A --> B
    B --> C
    B --> D
    C --> E
    D --> F
    E --> F
    F --> G
    G --> H
    H --> I
    C --> J
    D --> J
    F --> J
{{< /mermaid >}}

The important boundary is near `CPU native operation pack`. That is where a selective logical model can either remain selective or collapse back into broad writes.

Local files used for this article's implementation example:

- `RayTracingTopLevelScenePlanner.cpp`
- `RayTracingPtlasPartitionPlanner.cpp`
- `RayTracingPtlasLogicalUpdateStream.cpp`
- `D3D12NvapiRayTracingProvider.cpp`
- `VulkanPartitionedTlasServices.cpp`
- `RhiSmokeCaptureArtifacts.cpp`
- `ViewportRayTracingDebugOverlay.cpp`

## The Hard Part Is Not Naming the Feature

The logical update stream can filter changed instances and emit records for dirty or moved state rather than treating every instance as uniformly updated.

The relevant code points are:

- logical update eligibility:
  `RayTracingPtlasLogicalUpdateStream.cpp:8`
- changed-instance filtering:
  `RayTracingPtlasLogicalUpdateStream.cpp:64`
- record emission:
  `RayTracingPtlasLogicalUpdateStream.cpp:70`
- final logical count:
  `RayTracingPtlasLogicalUpdateStream.cpp:86`

But that is only half of the story.
The harder question is whether the backend-facing native PTLAS work preserves that selectivity.

Right now, that selectivity does not fully survive to the native operation pack.

The current partitioned strategy still constructs a single native operation pack around a broad full-scene `WriteInstance` path:

- PTLAS layout build:
  `RayTracingPartitionedTlasStrategy.cpp:461`
- `MaxOperations = 1`:
  `RayTracingPartitionedTlasStrategy.cpp:475`
- logical update handoff:
  `RayTracingPartitionedTlasStrategy.cpp:523`
- full instance write array build:
  `RayTracingPartitionedTlasStrategy.cpp:527`
- single native operation header:
  `RayTracingPartitionedTlasStrategy.cpp:584`

The internal design review describes the same gap directly:

- `PTLAS_TLAS_Design_Review.md:15`
- `PTLAS_TLAS_Design_Review.md:158`

{{< alert "triangle-exclamation" >}}
Selective knowledge is not the same thing as selective native work.
{{< /alert >}}

## What Still Has To Change

Once the gap is named precisely, the roadmap becomes much clearer.
The next step is making the logical update story survive all the way to native operation generation, submission policy, and steady-state measurement.

| Current state | Target state |
|---|---|
| selective logical update records exist | native operations are generated from changed-instance and changed-partition sets |
| writer-path selection is visible | writer-path policy becomes measurable and easier to compare |
| diagnostics expose PTLAS state | diagnostics expose selective native work more directly |
| smoke data exports core PTLAS fields | evidence bundles make selective native behavior auditable |

The most useful follow-on instrumentation would be:

- rewritten-instance count
- native op type breakdown
- partition occupancy histogram
- steady-state vs first-build markers
- requested runtime PTLAS config captured alongside evidence

## What Success Looks Like

For PTLAS, success should not mean only that the API exists or that the partitioned backend was selected.
Success is when localized scene motion reliably results in localized native top-level work, and the engine can prove that with diagnostics and evidence bundles.

That gives the article a practical acceptance checklist:

- changed instances do not imply broad full-scene native rewrite behavior
- partition migrations are visible and explainable
- provider selection and fallback reporting are trustworthy
- update timings are interpreted together with update counts
- backend comparisons stay honest about differences in maturity or proof quality

The internal design review already points in that direction:

- `PTLAS_TLAS_Design_Review.md:58`
- `PTLAS_TLAS_Design_Review.md:491`

## Closing

The shift from TLAS to PTLAS is only superficially about a new API surface.
The real change is that an engine starts treating top-level updates as selective work instead of broad scene-wide maintenance.

The remaining hard part is making native PTLAS work become as selective as the logical model that requested it.

When localized motion becomes localized native top-level work, PTLAS stops being mostly architectural intent and starts becoming measurable engine behavior.
