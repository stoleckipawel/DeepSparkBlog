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
keywords: ["PTLAS", "TLAS", "BLAS", "ray tracing", "partitioned TLAS", "Vulkan", "D3D12", "NVAPI", "rendering engine"]
---

Classic TLAS maintenance is scene-level work: rebuild or refit the top-level structure from the current set of instances.
PTLAS changes the unit of top-level maintenance from one broad structure to partitions, so a small scene change can be represented as changed instances plus touched partitions.

The hard part is the handoff from intent to execution.
If an engine detects a small dirty set but submits one broad native write, PTLAS is present architecturally but not yet paying off behaviorally.

## The Problem In One Picture

The NVIDIA domino demo is intentionally oversized: about 170k dynamic dominoes on a board with about 1.2M static objects.
That scale makes the PTLAS question visible: can the frame update only the moving instances and the partitions they touch?

{{< interactive-ptlas-domino-field >}}

Read the two panels as the same scene under two maintenance models.
The left side shows the classic TLAS problem: local motion still maps to a broad top-level update region.
The right side shows the PTLAS target: saturated cells stay near the touched partitions.

Muted cells show partition ownership, saturated cells show updated top-level work, and domino motion is shared between both panels.

## First, The Classic TLAS Baseline

BLAS stores geometry acceleration data. TLAS stores scene instances: transform, metadata, and a reference to a BLAS.

{{< rt-as-baseline >}}

A TLAS rebuild creates the top-level structure again from the current instance descriptions. A TLAS update/refit reuses a previous update-capable structure and changes instance-side data, usually transforms.

Refit can reduce build work, but it is not automatically better. The classic choice is build cost versus traversal quality inside one top-level structure.

{{< rt-as-update-modes >}}

## The Problem We Want To Solve

Scene changes are often local, but classic TLAS maintenance is still organized around one scene-level top-level structure.

A few moved instances may occupy a tiny part of the world, and classic rebuild/refit choices can still be perfectly valid. Valid acceleration-structure maintenance is not automatically partition-local acceleration-structure maintenance.

PTLAS targets the mismatch: local scene change should become local top-level maintenance, not a full-scene event disguised as an update.

## PTLAS As The Solution Shape

PTLAS keeps the shader-facing role of a top-level acceleration structure, but changes how that top level is maintained across frames.

Instances still reference BLAS objects. Rays still enter a top-level structure. The difference is that top-level state is organized into partitions, so update work can be described in terms of changed instances, touched partitions, and the global partition for highly dynamic cases.

{{< ptlas-structure-slide >}}

## What The NVIDIA Demo Adds

The sample is useful because it exposes the update problem at game-scene scale, not because dominoes are special.

| Demo signal | What it teaches |
|---|---|
| Uniform 2D partition grid | Partition ownership is spatial and predictable. |
| Saturated partition cells | The update region is smaller than the world. |
| Moving domino set | Per-frame change starts as changed instance transforms. |
| Updated instance count | Update cost should be read together with how much data changed. |
| TLAS / PTLAS memory and scratch stats | PTLAS is a different maintenance model, not a free-memory replacement for TLAS. |

In the screenshot state, PTLAS is active, a finite set of instances is moving, the updated partitions are highlighted, and the profiler separates physics, sparse instance-update generation, and top-level update work.

## The Policy Choice

PTLAS does not remove update policy.
It exposes it.

When an instance moves, the engine still has to decide whether to keep that instance in its local partition or route it through a global dynamic partition.

{{< ptlas-partition-policy >}}

The sample's extra checkbox, "mark all dominoes dynamic in partition", makes the tradeoff more aggressive.
If one domino in a partition starts moving, the whole partition's domino set can move to the global partition.
That can reduce partition rewrites, but it can also make the global partition larger and less spatially coherent.

## The Delta In One Table

The main delta is maintenance granularity.

| Aspect | BLAS | Classic TLAS | PTLAS |
|---|---|---|---|
| Owns | Geometry acceleration data for one mesh or mesh group | Scene-level instances of BLAS objects | Scene-level instances organized into partitions |
| Role | Accelerate geometry traversal | Accelerate scene instance traversal | Same top-level traversal role, different maintenance model |
| Typical frame change | Geometry updates, skinning, rebuild work | Instance transforms, membership, metadata | Instance changes plus partition ownership |
| Small localized motion cost | Usually local to changed geometry | Often still tied to broad top-level work | Intended to touch only changed instances and affected partitions |
| Main optimization question | When to rebuild vs update geometry | How much top-level work is redone per frame | How selective the instance and partition update stream really is |

Across APIs, the same framing holds: PTLAS is not a different shader-facing concept from TLAS. It is a different model for maintaining top-level scene state.

## Who Owns The Update Work?

Partitioning creates a new authoring question: who writes the sparse update description?

The CPU still owns high-level policy, feature selection, sizing, allocation, command recording, and synchronization. Sparse per-frame update data can be produced on the CPU or GPU depending on where simulation and dirty detection live. The actual PTLAS build/update work is still GPU-executed native work.

> PTLAS only pays off when the engine's logical update routing is reflected in the actual native work submission.

GPU-driven does not mean the CPU disappears. It means per-frame operation data can be generated and consumed without pulling the whole update decision back to the host.

{{< ptlas-cpu-gpu-split >}}

## How The Sample Generates Sparse Work

In the sample, GPU compute authors the per-frame PTLAS update list.

{{< mermaid >}}
flowchart LR
    A["Physics compute shader"]
    B["Marks moved dominoes"]
    C["Chooses local or global partition"]
    D["Instance update compute shader"]
    E["atomicAdd on PTLAS op argCount"]
    F["Writes changed instance records"]
    G["Host submits indirect PTLAS update"]
    H["Builder consumes device-side operation data"]

    A --> B --> C --> D --> E --> F --> G --> H
{{< /mermaid >}}

Two details matter.

First, the physics pass marks both instance motion and partition state.
If a domino moves to or from the global partition, the source and destination partitions need compact instance-index lists again.

Second, the update-instance pass does not write a full scene array.
Each changed domino atomically reserves one slot in the PTLAS write-instance operation, writes its updated transform and partition index there, and increments the operation argument count on the GPU.

That is the behavior to compare against a classic TLAS path: classic TLAS can rebuild or refit correctly, but the build call still reads the top-level instance input as one broad structure.
The PTLAS path can submit a device-authored operation list whose size follows the changed set.

## The Vendor Model Converges More Than It Diverges

The APIs differ, but the behavioral target is consistent: represent top-level change as partition-aware work.

Khronos frames PTLAS around partitions, reuse of previously built top-level work, and explicit PTLAS operations. NVIDIA frames it around selective maintenance in dynamic scenes, plus sizing and policy concerns through sample code and NVAPI. Microsoft frames PTLAS as a persistent partially rebuildable top-level structure with indirect RTAS operations and a first-class global partition concept.

The behavioral test stays the same across APIs: local scene change should be expressible as local top-level work.

| Concept | Khronos / Vulkan | NVIDIA sample / NVAPI | Microsoft DXR spec | Implementation checkpoint |
|---|---|---|---|---|
| Partitioned top-level structure | `VK_NV_partitioned_acceleration_structure` | Partitioned TLAS | Partitioned TLAS / PTLAS | `PartitionedTlas` top-level provider |
| Write instance op | `WRITE_INSTANCE` | PTLAS write instance operation | Partitioned TLAS write instance | Native operation header `WriteInstance` |
| Update instance op | `UPDATE_INSTANCE` | PTLAS update instance operation | Partitioned TLAS update instance | Planned/native op concept |
| Global partition | Global partition concept | Global partition support | Global partition concept | `GlobalPartition` planner/update state |
| Logical dirty state | App-defined | Moving instances in sample | Indirect operation arguments | Changed-instance update stream |

## A Concrete Implementation Lens

Selectivity has to survive five handoffs:

- frame planning chooses the top-level strategy
- partition planning decides spatial ownership
- the logical update stream records dirty or moved instances
- native operation packing turns logical state into backend work
- diagnostics expose whether the submitted work stayed selective

The current implementation path looks like this:

{{< mermaid >}}
flowchart LR
    A["RenderSceneData"]
    B["Frame planning"]
    C["Partition planning"]
    D["Logical update stream"]
    E["Strategy prepare"]
    F["Strategy build"]
    G["Upload update records"]
    H["CPU native operation pack"]
    I["Native PTLAS provider"]
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

The critical boundary is `CPU native operation pack`: sparse logical intent can either remain sparse or collapse into broad writes.

| Checkpoint | What it proves for the reader |
|---|---|
| Frame planning | The engine chooses between classic and partitioned top-level strategies before backend work is emitted. |
| Partition planning | Spatial ownership is explicit enough to reason about local versus global update policy. |
| Logical update stream | Changed instances can be represented sparsely before native work is packed. |
| Native operation pack | This is the critical handoff where sparse intent can either survive or become broad work again. |
| Diagnostics | Captures and overlays must make the selected path, counts, and fallback reasons auditable. |

## The Hard Part Is Not Naming the Feature

Dirty-instance filtering happens before the native work packet is built.

| Evidence point | What to look for |
|---|---|
| Logical update stream | The update path filters changed instances and emits only dirty or moved records before handoff. |
| Logical update count | The frame has a countable sparse update set before it reaches native operation packing. |

The missing proof is whether backend-facing native PTLAS work preserves that selectivity.

Right now, that selectivity does not fully survive to the native operation pack.

The current partitioned strategy still constructs a single native operation pack around a broad full-scene `WriteInstance` path.

| Evidence point | What it means |
|---|---|
| One native operation pack | Sparse logical intent is not yet expressed as multiple localized native operations. |
| Full instance write array | The backend-facing packet can still look broad even when the logical update set was sparse. |

{{< alert "triangle-exclamation" >}}
Selective knowledge is not the same thing as selective native work.
{{< /alert >}}

## What Still Has To Change

The next step is making sparse logical updates survive native operation generation, submission policy, and steady-state measurement.

| Current state | Target state |
|---|---|
| selective logical update records exist | native operations are generated from changed-instance and changed-partition sets |
| writer-path selection is visible | writer-path policy becomes measurable and easier to compare |
| diagnostics expose PTLAS state | diagnostics expose selective native work more directly |
| smoke data exports core PTLAS fields | evidence bundles make selective native behavior auditable |

Useful follow-on instrumentation:

- rewritten-instance count
- native op type breakdown
- partition occupancy histogram
- steady-state vs first-build markers
- requested runtime PTLAS config captured alongside evidence

## What Success Looks Like

PTLAS success is not API availability or backend selection. Success is localized scene motion producing localized native top-level work, with diagnostics that make the claim auditable.

Acceptance checklist:

- changed instances do not imply broad full-scene native rewrite behavior
- partition migrations are visible and explainable
- provider selection and fallback reporting are trustworthy
- update timings are interpreted together with update counts
- backend comparisons stay honest about differences in maturity or proof quality

## Closing

TLAS asks: how do we maintain one top-level structure?
PTLAS asks: which instances and partitions changed, and can native work stay that local?

When localized motion becomes localized native top-level work, PTLAS becomes measurable behavior instead of architectural intent.

## Resources

- [NVIDIA DXR tutorial: BLAS and TLAS ownership](https://developer.nvidia.com/rtx/raytracing/dxr/dx12-raytracing-tutorial-part-1)
- [NVIDIA Vulkan ray tracing tutorial: acceleration structure construction](https://nvpro-samples.github.io/vk_raytracing_tutorial_KHR/concepts/acceleration-structures/)
- [NVIDIA RTX best practices: TLAS rebuild and refit tradeoffs](https://developer.nvidia.com/blog/rtx-best-practices/)
- [NVIDIA vk_partitioned_tlas sample](https://github.com/nvpro-samples/vk_partitioned_tlas)
- [NVIDIA RTX Mega Geometry Vulkan samples overview](https://developer.nvidia.com/blog/nvidia-rtx-mega-geometry-now-available-with-new-vulkan-samples/)
- [NVIDIA RTX innovations: Mega Geometry foliage and Witcher context](https://developer.nvidia.com/blog/nvidia-rtx-innovations-are-powering-the-next-era-of-game-development/)
- Khronos Vulkan PTLAS material
- Microsoft DirectX ray tracing / RTAS material
