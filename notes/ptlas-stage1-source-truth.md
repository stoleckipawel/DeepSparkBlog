# PTLAS Stage 1 Source Truth

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Article: `Next Gen RT Acceleration Structure: PTLAS vs TLAS`

## 1. Purpose

This document completes Stage 1: gather source truth.

It is the evidence ledger for the article.
Every major article claim should be traceable to either:

- an official external source
- a concrete SparkleEngine file
- a SparkleEngine diagnostic output path

If a claim cannot be traced back to one of those, it should not appear in the article as a confident statement.

## 2. Official External Sources

### 2.1 Khronos PTLAS proposal

Source:

- https://github.com/KhronosGroup/Vulkan-Docs/blob/main/proposals/VK_NV_partitioned_acceleration_structure.adoc
- https://docs.vulkan.org/features/latest/features/proposals/VK_NV_partitioned_acceleration_structure.html

What it gives us:

- the problem statement for PTLAS
- the rationale for moving beyond classic TLAS rebuild behavior
- the high-level PTLAS model
- the two-stage partition build description
- the tradeoff between update performance and trace performance
- the role of partitions and partition organization

What we should use it for:

- explaining why PTLAS exists
- framing PTLAS as an update-model change
- grounding the “selective reuse of previously built parts” argument

### 2.2 Khronos PTLAS reference page

Source:

- https://docs.vulkan.org/refpages/latest/refpages/source/VK_NV_partitioned_acceleration_structure.html

What it gives us:

- concise reference wording for PTLAS
- formal confirmation that PTLAS is shader-equivalent to TLAS from the pipeline point of view

What we should use it for:

- concise article phrasing
- confirming PTLAS behaves like TLAS at the shader-facing boundary

### 2.3 Khronos PTLAS operation semantics

Source:

- https://docs.vulkan.org/refpages/latest/refpages/source/VkPartitionedAccelerationStructureOpTypeNV.html

What it gives us:

- explicit operation semantics for:
  `WRITE_INSTANCE`
  `UPDATE_INSTANCE`
  `WRITE_PARTITION_TRANSLATION`

What we should use it for:

- explaining what a correct PTLAS native update stream should express
- distinguishing logical updates from native PTLAS operations

### 2.4 NVIDIA PTLAS sample

Source:

- https://github.com/nvpro-samples/vk_partitioned_tlas

What it gives us:

- a concrete PTLAS sample implementation
- a large dynamic workload with localized motion
- an example where only moving instances are updated
- partition visualization and dynamic update behavior

What we should use it for:

- explaining the intended behavioral pattern
- supporting claims about selective updates
- supporting screenshot / visualization expectations

### 2.5 NVIDIA RTX Mega Geometry article

Source:

- https://developer.nvidia.com/blog/nvidia-rtx-mega-geometry-now-available-with-new-vulkan-samples/

What it gives us:

- NVIDIA’s public framing of the PTLAS sample
- a concise description of rebuilding only parts of TLAS when part of a scene changes
- practical context for large dynamic scenes

What we should use it for:

- concise vendor framing
- practical narrative support for the sample

### 2.6 NVIDIA NVAPI D3D12 PTLAS docs

Source:

- https://docs.nvidia.com/nvapi/group__dx.html
- https://docs.nvidia.com/nvapi/struct__NVAPI__D3D12__BUILD__RAYTRACING__PARTITIONED__TLAS__INDIRECT__INPUTS.html

What it gives us:

- D3D12 PTLAS capability enums
- indirect PTLAS build input structure
- required sizing inputs:
  instance count
  partition count
  max per-partition instance count
  max global-partition instance count
- PTLAS capability flags

What we should use it for:

- explaining D3D12 / NVAPI backend requirements
- explaining sizing policy implications
- explaining why layout choices matter

### 2.7 Microsoft DirectX ray tracing functional spec

Source:

- https://microsoft.github.io/DirectX-Specs/d3d/Raytracing2.html

What it gives us:

- Microsoft’s PTLAS framing
- PTLAS as a partially rebuildable persistent top-level structure
- partition translation concept
- GPU-driven indirect RTAS operation model
- support for writing instances, updating instances, and translating partitions

What we should use it for:

- showing that the PTLAS model is not just a Vulkan-side curiosity
- supporting the article’s vendor-neutral architectural framing

## 3. SparkleEngine Local Sources

### 3.1 Existing internal PTLAS review

File:

- [PTLAS_TLAS_Design_Review.md](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:1>)

Key lines:

- strong foundation summary at [line 9](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:9>)
- core gap at [line 15](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:15>)
- official source list at [line 33](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:33>)
- PTLAS acceptance criterion framing at [line 58](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:58>)
- operation semantics discussion at [line 66](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:66>)
- NVIDIA sample behavior framing at [line 79](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:79>)
- current frame flow summary at [line 131](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:131>)
- full-scene rewrite finding at [line 158](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:158>)
- logical update pipeline discussion at [line 181](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:181>)
- live PTLAS selection note at [line 240](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:240>)
- success criteria wording at [line 491](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md:491>)

What it gives us:

- a local design-review baseline
- a clear articulation of current strengths and gaps
- strong internal wording for acceptance criteria

### 3.2 Top-level planner flow

File:

- [RayTracingTopLevelScenePlanner.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingTopLevelScenePlanner.cpp:1>)

What it gives us:

- the per-frame PTLAS planning flow
- partition planning
- logical update stream build
- debug data packaging into frame data
- planner metrics export

Use it for:

- the Sparkle architecture section
- proving that planning and logical updates already exist

### 3.3 PTLAS partition planner

Files:

- [RayTracingPtlasPartitionPlanner.h](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.h:1>)
- [RayTracingPtlasPartitionPlanner.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.cpp:1>)

Important details:

- partition grid generation
- stable instance identity
- dirty transform detection
- partition movement detection
- global partition eligibility
- packed debug visualization data

Use it for:

- explaining Sparkle’s partition model
- explaining what the PTLAS debug views are actually showing

### 3.4 Logical update stream

File:

- [RayTracingPtlasLogicalUpdateStream.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:1>)

Key lines:

- logical update eligibility at [line 8](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:8>)
- flag construction at [line 13](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:13>)
- stream build at [line 50](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:50>)
- changed-instance filtering at [line 64](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:64>)
- record emission at [line 70](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:70>)
- final logical count at [line 86](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp:86>)

What it gives us:

- direct proof that Sparkle already computes selective logical updates

### 3.5 PTLAS strategy and current native pack behavior

File:

- [RayTracingPartitionedTlasStrategy.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:1>)

Key lines:

- PTLAS layout build at [line 461](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:461>)
- `MaxOperations = 1` at [line 475](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:475>)
- PTLAS build entry at [line 493](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:493>)
- logical update handoff at [line 523](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:523>)
- full instance write array build at [line 527](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:527>)
- partition info lookup at [line 555](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:555>)
- single native operation header at [line 584](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:584>)
- one-operation pack desc at [line 589](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:589>)
- CPU pack buffer creation at [line 609](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:609>)
- active writer reason resolution at [line 671](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:671>)
- logical update upload function at [line 676](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp:676>)

What it gives us:

- direct proof that the live native PTLAS path still behaves as a full-scene write batch

### 3.6 D3D12 NVAPI backend

File:

- [D3D12NvapiRayTracingProvider.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/RHI/Private/D3D12/RayTracing/D3D12NvapiRayTracingProvider.cpp:178>)

What it gives us:

- PTLAS build sizing query through NVAPI
- D3D12 PTLAS build command path
- mapping from Sparkle layout to NVAPI indirect inputs

Use it for:

- backend-specific evidence
- D3D12 sizing policy discussion

### 3.7 Vulkan PTLAS backend

File:

- [VulkanPartitionedTlasServices.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/RHI/Private/Vulkan/RayTracing/VulkanPartitionedTlasServices.cpp:146>)

What it gives us:

- Vulkan PTLAS size query path
- Vulkan native operation buffer packing
- operation-type mapping to Vulkan PTLAS op enums

Use it for:

- backend-specific evidence
- Vulkan provider discussion

### 3.8 Smoke capture artifact export

File:

- [RhiSmokeCaptureArtifacts.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:89>)

Key lines:

- capture metadata write block begins at [line 89](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:89>)
- frame index export at [line 126](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:126>)
- PTLAS provider export at [line 152](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:152>)
- partition count export at [line 163](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:163>)
- native operation export at [line 171](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:171>)
- requested writer path export at [line 175](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:175>)
- GPU native pack availability export at [line 183](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:183>)
- timing block includes PTLAS timings at [line 194](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:194>)
- CSV header at [line 220](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:220>)
- CSV provider write at [line 237](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:237>)
- CSV writer path write at [line 256](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp:256>)

What it gives us:

- proof that article figures can be paired with machine-readable evidence

### 3.9 Smoke capture configuration / view mode forcing

Files:

- [RhiSmokeEditorValidation.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeEditorValidation.cpp:32>)
- [RhiSmokeRenderViewModeNames.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeRenderViewModeNames.cpp:20>)
- [RhiSmokeViewportCapture.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Application/Private/Validation/RhiSmokeViewportCapture.cpp:21>)

What they give us:

- supported PTLAS debug capture modes
- environment-variable-driven smoke captures
- deterministic capture path for article figures

### 3.10 Editor overlay proof

File:

- [ViewportRayTracingDebugOverlay.cpp](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:89>)

Key lines:

- PTLAS debug view mode gating at [line 17](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:17>)
- overlay draw entry at [line 89](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:89>)
- live workload note at [line 115](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:115>)
- partition metric at [line 125](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:125>)
- native op metric at [line 129](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:129>)
- writer-path metric at [line 133](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:133>)
- GPU timing metric at [line 151](</c:/Users/pawel.stolecki/Documents/GitHub/SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp:151>)

What it gives us:

- direct proof that Sparkle exposes PTLAS-specific live debug information in-editor

## 4. Claim-to-Source Map

### Claim: PTLAS exists to avoid full classic TLAS rebuild behavior when only a small part of the scene changes

External support:

- Khronos PTLAS proposal
- Vulkan PTLAS reference page
- Microsoft DXR functional spec

Local support:

- PTLAS design review framing

### Claim: PTLAS is a different top-level update model, not a shader-facing semantic change

External support:

- Khronos PTLAS proposal / reference page
- Microsoft DXR functional spec

Local support:

- Sparkle strategy split and backend-neutral top-level selection

### Claim: Sparkle already has a real PTLAS planning layer

Local support:

- `RayTracingTopLevelScenePlanner.cpp`
- `RayTracingPtlasPartitionPlanner.cpp`
- design review

### Claim: Sparkle already computes selective logical PTLAS updates

Local support:

- `RayTracingPtlasLogicalUpdateStream.cpp`

### Claim: Sparkle’s current live PTLAS native path still repacks full-scene writes

Local support:

- `RayTracingPartitionedTlasStrategy.cpp`
- design review

### Claim: Sparkle already has backend-specific PTLAS implementations for D3D12 and Vulkan

Local support:

- `D3D12NvapiRayTracingProvider.cpp`
- `VulkanPartitionedTlasServices.cpp`

### Claim: Sparkle already has PTLAS-specific debug views and smoke evidence

Local support:

- `RhiSmokeCaptureArtifacts.cpp`
- `RhiSmokeEditorValidation.cpp`
- `RhiSmokeRenderViewModeNames.cpp`
- `ViewportRayTracingDebugOverlay.cpp`

### Claim: PTLAS correctness / value should be proven with selective update evidence, not just capability exposure

External support:

- Khronos operation semantics
- NVIDIA PTLAS sample
- Microsoft DXR functional spec

Local support:

- internal design review
- Sparkle smoke metrics export

## 5. Major Claims That Are Safe To Make

These claims are well-supported by the current source set.

- PTLAS is designed to reuse previously built top-level work when scene changes are localized.
- PTLAS changes the update model under the top-level acceleration structure while preserving the shader-facing role of TLAS.
- SparkleEngine already contains real PTLAS-specific planning, diagnostics, and backend integration work.
- SparkleEngine already emits selective logical update records.
- SparkleEngine’s current live PTLAS native pack path still behaves as a full-scene write batch.
- SparkleEngine already exports enough PTLAS smoke data to support a proof-oriented article.

## 6. Claims That Should Be Framed Carefully

- Any direct performance win claim for Sparkle PTLAS today.
- Any implication that GPU-driven PTLAS native packing is already complete.
- Any suggestion that Sparkle already uses minimal native PTLAS operations per changed instance or partition.
- Any backend parity claim unless captures are gathered from both D3D12 and Vulkan.

These claims should either be avoided or clearly labeled as future target / pending proof.

## 7. Stage 1 Deliverables Status

Deliverables:

- source list with links: complete
- short notes per source: complete
- exact local code references: complete

Exit criteria:

- every major claim in the planned article can already be linked to a source or a local engine file: complete

## 8. Next Step

Stage 1 is ready.

The best next step is Stage 2:

- collect the actual capture bundles
- pair each capture with metadata and timing evidence
- then attach those bundles to the article skeleton
