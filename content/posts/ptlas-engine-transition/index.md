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

## Problem Statement

The granularity of scene change can be smaller than the granularity of classic TLAS maintenance.

The test is concrete: count how many instances changed, count how much top-level state was maintained, and compare both numbers to the full scene. If those counts stay close to scene size, the update path is correct but still coarse.

## Proposed Model

Classic TLAS maintenance has one broad lane: instance records feed one top-level structure. PTLAS keeps the same shader-facing role, but adds a partitioned maintenance lane inside that top level.

Instance records still reference BLAS objects, and rays still traverse a top-level acceleration structure. The changed part is the update description: a frame can name changed instances, touched partitions, and a global partition for highly dynamic instances.

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

## Update Policy Tradeoffs

Partitioning adds a policy decision for moving instances: keep them in their spatial partition, route them through the global partition, or switch behavior by camera distance.

{{< ptlas-partition-policy >}}

| Policy | Update cost | Trace coherence | Camera use | Risk |
|---|---|---|---|---|
| Update local partition | Higher when a partition contains many instances | Strong spatial grouping | Good near the camera | Many local partition rewrites |
| Move dynamic to global | Lower for moving objects | Weaker spatial grouping | Useful away from focus | Global partition growth |
| Hybrid by distance | Mixed | Preserves nearby grouping | Distance threshold controls behavior | Threshold tuning becomes visible |

An aggressive global-partition variant can move every domino from a touched partition into global. That reduces local partition rewrites, but the global partition may contain more than the currently moving set.

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

## Implementation Method

The implementation path is easiest to audit as five boundaries. Each boundary can preserve selectivity or widen the work again.

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

Frame planning chooses the top-level strategy for the frame. Partition planning assigns spatial ownership and global-partition policy. The logical update stream records dirty or moved instances before backend packing. The native operation pack converts that stream into backend-visible PTLAS work. Diagnostics record counts, selected paths, and fallback reasons.

{{< ptlas-cpu-gpu-split >}}

Sparse update authoring can happen on the CPU or GPU. The important boundary is the native operation pack: changed-instance records and touched partitions either remain compact there, or the backend receives broad top-level writes.

| Boundary | What to verify |
|---|---|
| Frame planning | The selected path is classic TLAS or PTLAS before backend work begins. |
| Partition planning | Local and global ownership are explicit. |
| Logical update stream | Dirty instances are countable before packing. |
| Native operation pack | Backend work follows changed instances and touched partitions. |
| Diagnostics | Captures expose path, counts, and fallback reason. |

## Evidence And Current Limitations

The current evidence separates logical selectivity from submitted native work. That distinction matters: an engine can know which instances changed before it has proven that the backend received a similarly compact update.

| Evidence checkpoint | Represented now | Still needs proof |
|---|---|---|
| Frame strategy | Classic and partitioned paths can be selected and diagnosed. | Compare timings under the same scene and camera state. |
| Partition planning | Local and global ownership can be reasoned about before backend work. | Export partition occupancy and migration counts per frame. |
| Logical update stream | Dirty or moved instances can be counted before native packing. | Track rewritten-instance count beside changed-instance count. |
| Native operation pack | Backend submission is visible as a separate boundary. | Break down native op type, op count, and touched partitions. |
| Smoke capture / overlay | PTLAS path, counts, and fallback state can be captured. | Store runtime config with every evidence bundle. |

The measurable limitation is the native operation pack. Logical update records may be sparse while the submitted packet still covers more top-level state than the changed set requires.

## Discussion

PTLAS shifts cost toward partition design. Smaller partitions can reduce the amount of maintained top-level state, but they also increase partition count and make overlap easier to create. Overlap matters because tracing still traverses spatial data; a partition layout that is cheap to update can be poor to trace.

The global partition is the pressure valve for dynamic objects. It can reduce repeated local rewrites when motion is scattered, but it becomes less spatially coherent as it grows. A useful capture should report both touched local partitions and global-partition population.

Memory and scratch should be read as part of the method, not as the headline. PTLAS may carry more structure metadata than a classic TLAS path. The comparison that matters is top-level update time relative to changed instances, touched partitions, and full-scene instance count.

Timing numbers need those counts beside them. A lower update time with a much larger global partition may trade build cost for trace cost. A higher update time near the camera may be acceptable if it preserves better spatial grouping where rays are dense.

## Summary

- TLAS remains one top-level instance acceleration structure.
- PTLAS changes how top-level updates can be expressed: changed instances, touched partitions, and global dynamic movement.
- The useful measurement is whether changed scene work stays compact through native submission.

## Resources

- [NVIDIA DXR tutorial: BLAS and TLAS ownership](https://developer.nvidia.com/rtx/raytracing/dxr/dx12-raytracing-tutorial-part-1)
- [NVIDIA Vulkan ray tracing tutorial: acceleration structure construction](https://nvpro-samples.github.io/vk_raytracing_tutorial_KHR/concepts/acceleration-structures/)
- [NVIDIA RTX best practices: TLAS rebuild and refit tradeoffs](https://developer.nvidia.com/blog/rtx-best-practices/)
- [NVIDIA vk_partitioned_tlas sample](https://github.com/nvpro-samples/vk_partitioned_tlas)
- [NVIDIA RTX Mega Geometry Vulkan samples overview](https://developer.nvidia.com/blog/nvidia-rtx-mega-geometry-now-available-with-new-vulkan-samples/)
- [NVIDIA RTX innovations: Mega Geometry foliage and Witcher context](https://developer.nvidia.com/blog/nvidia-rtx-innovations-are-powering-the-next-era-of-game-development/)
- Khronos Vulkan PTLAS material
- Microsoft DirectX ray tracing / RTAS material
