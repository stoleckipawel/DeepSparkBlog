---
title: "PTLAS vs TLAS: Sparse Top-Level Updates in Large Ray-Traced Scenes"
date: 2026-06-17
lastmod: 2026-06-18
draft: true
authors: ["Pawel Stolecki"]
description: "A peer-level comparison of classic TLAS rebuild/refit and PTLAS partitioned maintenance, grounded in a localized-motion sample workload."
tags: ["rendering", "ray-tracing", "ptlas", "vulkan", "d3d12", "engine-architecture"]
categories: ["analysis"]
summary: "A compact comparison of classic TLAS rebuild/refit and PTLAS partitioned updates, focused on sparse motion, update cost, traversal cost, and remaining evidence gaps."
showTableOfContents: false
keywords: ["PTLAS", "TLAS", "BLAS", "ray tracing", "partitioned TLAS", "Vulkan", "D3D12", "NVAPI", "rendering engine"]
---

Partitioned top-level acceleration structures change the maintenance unit of ray-tracing instance acceleration: from one scene-wide TLAS to partitioned top-level state plus sparse instance operations. This article compares that model with classic TLAS rebuild/refit, measures a localized-motion workload, and keeps the measurement boundary explicit: changed-instance counts are captured here, while touched partitions and native operation counts still need instrumentation.

## Introduction

Large ray-traced scenes rarely move uniformly. A frame may contain millions of renderable instances, while only a narrow wave of characters, debris, vegetation, or simulation objects changes transform data. The acceleration-structure question is whether top-level maintenance can follow that uneven motion instead of treating scene scale and changed work as the same input.

{{< interactive-ptlas-domino-field >}}

## Background

BLAS and TLAS split ray-tracing acceleration by ownership. A BLAS is built from geometry inputs. A TLAS is built from instance records: transform, instance metadata, and a reference to a BLAS.

{{< rt-as-baseline >}}

Classic TLAS maintenance is a cost-placement decision. Rebuild spends builder time to create a fresh top-level layout from the current instance set. Update/refit reuses an update-capable layout and refreshes instance data, usually transforms and bounds, but layout drift can move cost into traversal.

{{< rt-as-update-modes >}}

## Problem Statement

The target saving is top-level update work. If only a small moving set changes, the maintained top-level region should be closer to that moving set than to the full scene.

That saving is only worth claiming with the other costs beside it: render time for traversal quality, memory and scratch for structure overhead, and backend command scope for submitted work. A sparse engine-side dirty list is not enough if the backend still updates a broad top-level region.

## Proposed Model

Classic TLAS maintenance has one broad lane: instance records feed one top-level structure. PTLAS keeps the same shader-facing role, but adds a partitioned maintenance lane inside that top level.

Instance records still reference BLAS objects, and rays still traverse a top-level acceleration structure. The changed part is the update description: a frame can name changed instances, touched partitions, and a global partition for highly dynamic instances.

{{< ptlas-storage-model >}}

{{< ptlas-update-model >}}

## Measurement Workload

The captured workload keeps scene size fixed and lets motion vary over time:

- `1,389,406` total instances
- `169,231` dynamic domino instances
- `1,220,175` static board objects
- `50 x 50` partition grid

That creates the condition PTLAS is meant to exploit: high-motion bands report about `15.6k` changed instances, while low-motion bands report about `1.7k`.

### Evidence Snapshot

The regular TLAS refit row anchors the sample: same scene, same window layout, PTLAS disabled, refit enabled. The PTLAS rows are wider motion-window captures, so they show update behavior over sparse-to-dense movement, not a matched head-to-head speed ranking.

| Path | Changed instances | Top-level update | Render avg | AS memory / scratch |
|---|---:|---:|---:|---:|
| Classic TLAS refit | `4,011-5,084` | `0.670 ms` avg, `0.656-0.706 ms` range | `1.198 ms` | `285.68 MB / 103.97 MB` |
| PTLAS local partition | `760-16,157` | `1.042 ms` avg, `0.647-1.393 ms` range | `1.270 ms` | `320.18 MB / 110.24 MB` |
| PTLAS global role | `760-16,141` | `1.059 ms` avg, `0.688-1.364 ms` range | `1.407 ms` | `320.18 MB / 110.24 MB` |
| PTLAS hybrid distance | `788-16,132` | `1.060 ms` avg, `0.637-1.383 ms` range | `1.291 ms` | `320.18 MB / 110.24 MB` |

Within the PTLAS captures, top-level update time drops with the moving set: about `1.31 ms` in high motion and about `0.75 ms` in low motion, a roughly `43%` drop across all three policies.

| PTLAS policy | High motion | Mid motion | Low motion |
|---|---:|---:|---:|
| Local partition | `1.320 ms` at `15,648` changed | `1.053 ms` at `9,358` changed | `0.751 ms` at `1,707` changed |
| Global partition | `1.302 ms` at `15,584` changed | `1.119 ms` at `9,468` changed | `0.738 ms` at `1,721` changed |
| Hybrid distance `100.000` | `1.313 ms` at `15,609` changed | `1.102 ms` at `9,490` changed | `0.752 ms` at `1,765` changed |

This capture records changed instances, update time, render time, memory, and scratch. It does not report touched partitions, rewritten instances, global-partition population, or native operation count.

## Update Policy Tradeoffs

Partitioning adds a policy decision for moving instances: keep them in their spatial partition, route them through the global partition, or switch behavior by camera distance.

{{< ptlas-partition-policy >}}

In the global policy, moving instances are routed through one dynamic partition until they settle. That can reduce repeated local partition maintenance, but the global partition trades spatial grouping for a larger dynamic bucket.

## Implementation Method

The implementation path is easiest to audit at the backend operation pack. Earlier stages can describe sparse work; that boundary decides whether submitted commands remain scoped to changed instances and touched partitions.

{{< ptlas-implementation-pipeline >}}

{{< ptlas-cpu-gpu-split >}}

Sparse update authoring can happen on the CPU or GPU. The boundary to verify is the native operation pack: changed-instance records and touched partitions either remain compact there, or the backend receives broad top-level writes.

## Discussion

PTLAS shifts cost toward partition design. Smaller partitions can reduce the amount of maintained top-level state, but they also increase partition count and make overlap easier to create. Overlap matters because tracing still traverses spatial data; a partition layout that is cheap to update can be poor to trace.

The global partition is the dynamic bucket for scattered movers. It can reduce repeated local rewrites when motion is scattered, but it becomes less spatially coherent as it grows. A complete capture should report both touched local partitions and global-partition population.

Memory and scratch should be read as part of the method, not as the headline. PTLAS may carry more structure metadata than a classic TLAS path. The comparison that matters is top-level update time relative to changed instances, touched partitions, and full-scene instance count.

Timing numbers need those counts beside them. A lower update time with a much larger global partition may trade build cost for trace cost. A higher update time near the camera may be acceptable if it preserves better spatial grouping where rays are dense.

The measured policy rows follow that rule. Their update timings fall as the moving set shrinks, but their render averages are not identical. That makes the policy choice a measurement problem, not a naming problem.

## Summary

- Classic TLAS rebuild/refit chooses how one scene-wide top-level structure is maintained.
- PTLAS changes the maintenance vocabulary to changed instances, touched partitions, and optional global dynamic movement.
- The remaining proof point is native command scope: operation type, operation count, touched partitions, and rewritten instances.

## Resources

- [NVIDIA DXR tutorial: BLAS and TLAS ownership](https://developer.nvidia.com/rtx/raytracing/dxr/dx12-raytracing-tutorial-part-1)
- [NVIDIA Vulkan ray tracing tutorial: acceleration structure construction](https://nvpro-samples.github.io/vk_raytracing_tutorial_KHR/concepts/acceleration-structures/)
- [NVIDIA RTX best practices: TLAS rebuild and refit tradeoffs](https://developer.nvidia.com/blog/rtx-best-practices/)
- [NVIDIA best practices using RTX ray tracing](https://developer.nvidia.com/blog/best-practices-using-nvidia-rtx-ray-tracing/)
- [NVIDIA engine integration article](https://developer.nvidia.com/blog/effectively-integrating-rtx-ray-tracing-real-time-rendering-engine/)
- [NVIDIA optimal meshes for ray tracing](https://developer.nvidia.com/blog/creating-optimal-meshes-for-ray-tracing/)
- [NVIDIA vk_partitioned_tlas sample](https://github.com/nvpro-samples/vk_partitioned_tlas)
- [NVIDIA RTX Mega Geometry Vulkan samples overview](https://developer.nvidia.com/blog/nvidia-rtx-mega-geometry-now-available-with-new-vulkan-samples/)
- [NVIDIA RTX innovations: Mega Geometry foliage and Witcher context](https://developer.nvidia.com/blog/nvidia-rtx-innovations-are-powering-the-next-era-of-game-development/)
- [NVIDIA NVAPI DirectX documentation](https://docs.nvidia.com/nvapi/group__dx.html)
- [NVIDIA NVAPI PTLAS indirect input structure](https://docs.nvidia.com/nvapi/struct__NVAPI__D3D12__BUILD__RAYTRACING__PARTITIONED__TLAS__INDIRECT__INPUTS.html)
- [AMD GPUOpen Radeon Raytracing Analyzer overview](https://gpuopen.com/radeon-raytracing-analyzer/)
- [AMD GPUOpen: improving raytracing performance with RRA](https://gpuopen.com/learn/improving-rt-perf-with-rra/)
- [AMD GPUOpen RRA manual: TLAS windows](https://gpuopen.com/manuals/rra_manual/tlas_windows/)
- [AMD GPUOpen RRA 1.3 traversal analysis](https://gpuopen.com/learn/rra_1_3/)
- [AMD GPUOpen Far Cry 6 hybrid ray-traced reflections deck](https://gpuopen.com/download/GDC_Performant_Reflective_Beauty_Hybrid_Ray_Traced_Reflections_In_Far_Cry_6.pdf)
- [Khronos Vulkan PTLAS proposal](https://github.com/KhronosGroup/Vulkan-Docs/blob/main/proposals/VK_NV_partitioned_acceleration_structure.adoc)
- [Khronos Vulkan PTLAS reference page](https://docs.vulkan.org/refpages/latest/refpages/source/VK_NV_partitioned_acceleration_structure.html)
- [Khronos PTLAS operation type reference](https://docs.vulkan.org/refpages/latest/refpages/source/VkPartitionedAccelerationStructureOpTypeNV.html)
- [Microsoft DirectX ray tracing functional spec, part 2](https://microsoft.github.io/DirectX-Specs/d3d/Raytracing2.html)
- [Vulkan dynamic ray-tracing sample](https://docs.vulkan.org/samples/latest/samples/extensions/ray_tracing_extended/README.html)
