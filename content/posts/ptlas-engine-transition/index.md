---
title: "Next Gen RT Acceleration Structure: PTLAS vs TLAS"
date: 2026-06-17
lastmod: 2026-06-17
draft: true
authors: ["Pawel Stolecki"]
description: "A peer-level PTLAS article about what changes when an engine moves from classic TLAS maintenance to partitioned top-level updates."
tags: ["rendering", "ray-tracing", "ptlas", "vulkan", "d3d12", "engine-architecture"]
categories: ["analysis"]
summary: "A compact comparison of classic TLAS rebuild/refit and PTLAS partitioned updates, focused on when localized scene changes can reduce top-level maintenance work."
showTableOfContents: false
keywords: ["PTLAS", "TLAS", "BLAS", "ray tracing", "partitioned TLAS", "Vulkan", "D3D12", "NVAPI", "rendering engine"]
---

Partitioned top-level acceleration structures change the maintenance unit of ray-tracing instance acceleration from one scene-wide top-level structure to partitions plus sparse instance updates. This article compares that model with classic TLAS rebuild/refit, shows the workload where the distinction matters, and keeps one limitation explicit: selectivity only helps if it survives into submitted build/update work.

## Introduction

Large ray-traced scenes rarely move uniformly. A frame may contain millions of renderable instances, while only a narrow wave of characters, debris, vegetation, or simulation objects changes transform data. The acceleration-structure question is whether top-level maintenance can follow that uneven motion instead of treating scene scale and changed work as the same input.

{{< interactive-ptlas-domino-field >}}

## Background

BLAS and TLAS split ray-tracing acceleration by ownership. A BLAS is built from geometry inputs. A TLAS is built from instance records: transform, instance metadata, and a reference to a BLAS.

{{< rt-as-baseline >}}

A TLAS rebuild constructs the top-level structure from the current instance set. A TLAS update/refit reuses an update-capable previous structure and refreshes instance-side data, most often transforms and bounds.

Rebuild and refit optimize different costs. Rebuild gives the builder freedom to improve top-level layout after broad change. Refit can reduce build work for transform-heavy motion, but repeated updates can preserve a layout that no longer matches the current scene as well.

{{< rt-as-update-modes >}}

## Related Work And API Context

The API surface differs by backend, but the useful comparison is small: what data names the top-level structure, what data names changed instances, and what data lets the update be submitted without rewriting the whole scene.

| Article term | Vulkan-side model | D3D12-side model | Role in the article |
|---|---|---|---|
| Classic TLAS | top-level acceleration structure | top-level RTAS / TLAS | Baseline scene-instance structure |
| PTLAS | partitioned acceleration structure | partitioned top-level RTAS / PTLAS | Top-level state split into maintained partitions |
| Partition | partition in the top-level structure | partition in the top-level structure | Spatial or policy-owned maintenance unit |
| Global partition | global partition | global partition | Dynamic bucket for instances that should not rewrite many local partitions |
| Instance operation | write/update instance operation | write/update instance operation | Sparse description of changed instance records |
| Indirect update data | device-authored operation arguments | GPU-authored operation arguments | Lets simulation or compute generate update work on the GPU |

## The Problem We Want To Solve

Scene changes are often local, but classic TLAS maintenance is still organized around one scene-level top-level structure.

A few moved instances may occupy a tiny part of the world, and classic rebuild/refit choices can still be perfectly valid. Valid acceleration-structure maintenance is not automatically partition-local acceleration-structure maintenance.

PTLAS targets the mismatch: local scene change should become local top-level maintenance, not a full-scene event disguised as an update.

## PTLAS As The Solution Shape

PTLAS keeps the shader-facing role of a top-level acceleration structure, but changes how that top level is maintained across frames.

Instances still reference BLAS objects. Rays still enter a top-level structure. The difference is that top-level state is organized into partitions, so update work can be described in terms of changed instances, touched partitions, and the global partition for highly dynamic cases.

{{< ptlas-structure-slide >}}

## What The Domino Workload Adds

The workload is large enough to separate scene size from changed work: about 170k dynamic dominoes, about 1.2M static board objects, and a uniform 2D partition grid.

| Workload fact | Technical implication |
|---|---|
| Uniform 2D partition grid | Partition ownership is spatial and predictable. |
| Saturated partition cells | The update region is smaller than the world. |
| Moving domino set | Per-frame change starts as changed instance transforms. |
| Updated instance count | Update cost should be read together with how much data changed. |
| TLAS / PTLAS memory and scratch stats | PTLAS is a different maintenance model, not a free-memory replacement for TLAS. |

Good measurements separate physics, sparse instance-update generation, and top-level update work.

## The Policy Choice

PTLAS does not remove update policy.
It exposes it.

When an instance moves, the engine still has to decide whether to keep that instance in its local partition or route it through a global dynamic partition.

{{< ptlas-partition-policy >}}

One aggressive global-partition variant marks all dominoes in a touched partition as dynamic.
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
| Main optimization question | When to rebuild vs update geometry | How much top-level work is redone per frame | How selective the instance and partition update stream is |

Across APIs, the same framing holds: PTLAS is not a different shader-facing concept from TLAS. It is a different model for maintaining top-level scene state.

## Who Owns The Update Work?

Partitioning creates a new authoring question: who writes the sparse update description?

The CPU still owns high-level policy, feature selection, sizing, allocation, command recording, and synchronization. Sparse per-frame update data can be produced on the CPU or GPU depending on where simulation and dirty detection live. PTLAS build/update work is still GPU-executed native work.

> PTLAS only pays off when the engine's logical update routing is reflected in native work submission.

GPU-driven does not mean the CPU disappears. It means per-frame operation data can be generated and consumed without pulling the whole update decision back to the host.

{{< ptlas-cpu-gpu-split >}}

## How The Sample Generates Sparse Work

GPU compute can author the per-frame PTLAS update list.

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

## A Concrete Implementation Lens

Selectivity has to survive five stages:

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

The decisive boundary is `CPU native operation pack`: sparse logical intent can either remain sparse or collapse into broad writes.

| Checkpoint | What it proves for the reader |
|---|---|
| Frame planning | The engine chooses between classic and partitioned top-level strategies before backend work is emitted. |
| Partition planning | Spatial ownership is explicit enough to reason about local versus global update policy. |
| Logical update stream | Changed instances can be represented sparsely before native work is packed. |
| Native operation pack | Sparse intent can either survive or become broad work again. |
| Diagnostics | Captures and overlays must make the selected path, counts, and fallback reasons auditable. |

## Native Submission Is The Deciding Step

Dirty-instance filtering happens before the native work packet is built.

| Evidence point | What to look for |
|---|---|
| Logical update stream | The update path filters changed instances and emits only dirty or moved records before native packing. |
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

Sparse logical updates still need to survive native operation generation, submission policy, and steady-state measurement.

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
