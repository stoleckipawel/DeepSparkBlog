# PTLAS Stage 2 Evidence Package

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Article: `What Changes When an Engine Moves From TLAS to PTLAS`
Depends on:

- `notes/ptlas-article-design-doc.md`
- `notes/ptlas-article-creation-stages.md`
- `notes/ptlas-stage1-source-truth.md`

## 1. Purpose

This document is the working ledger for Stage 2.

Its job is to turn the article's planned visuals and proof points into a real evidence package:

- figure images
- metadata JSON files
- timing CSV files
- manual overlay screenshots
- short notes explaining what each capture proves

This document should be updated as captures are gathered.

## 2. Stage 2 Goal

Collect all screenshots, metadata, timings, and implementation evidence before drafting the article in full.

The article should be written against evidence, not against memory.

## 3. Stage 2 Deliverables

- figure images
- metadata JSON files
- timing CSV files
- manual overlay screenshots
- short notes describing what each capture proves

## 4. Stage 2 Exit Criteria

Stage 2 is complete when:

- every planned visual has a matching explanation
- every planned visual has a matching evidence source
- every automated capture has its image + JSON + CSV bundle
- every manual screenshot has a short note explaining why it exists

## 5. Evidence Package Structure

Recommended folder layout once assets are collected:

`article-evidence/ptlas/`

Under that, one folder per figure bundle:

- `E01-lit-reference/`
- `E02-rt-ptlas-partitions/`
- `E03-rt-ptlas-partition-updates/`
- `E04-rt-ptlas-instance-movement/`
- `E05-rt-top-level-mode-classic/`
- `E06-rt-top-level-mode-partitioned/`
- `E07-rt-native-operations/`
- `E08-rt-provider-status-d3d12/`
- `E09-rt-provider-status-vulkan/`
- `E10-rt-gpu-updates/`
- `E11-overlay-partition-updates/`
- `E12-overlay-native-operations/`

Recommended contents of each automated bundle:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

Recommended contents of each manual screenshot bundle:

- `image.png`
- `notes.md`

## 6. Capture Matrix

This matrix defines the minimum capture coverage.

### Backend / mode combinations

#### D3D12 classic TLAS

Needed for:

- baseline comparison
- top-level mode comparison
- provider status comparison

Required views:

- `Lit`
- `RayTracingTopLevelMode`
- `RayTracingProviderStatus`

#### D3D12 partitioned TLAS with CPU pack

Needed for:

- the main Sparkle PTLAS evidence set

Required views:

- `RayTracingPartitions`
- `RayTracingPartitionUpdates`
- `RayTracingInstanceMovement`
- `RayTracingTopLevelMode`
- `RayTracingNativeOperations`
- `RayTracingProviderStatus`
- `RayTracingGpuDrivenUpdates`

#### Vulkan partitioned TLAS with CPU pack

Needed for:

- cross-backend credibility

Required views:

- `RayTracingPartitions`
- `RayTracingPartitionUpdates`
- `RayTracingNativeOperations`
- `RayTracingProviderStatus`

### Optional future combinations

- D3D12 partitioned TLAS with `GpuLogicalDirtyCpuNativePack`
- D3D12 partitioned TLAS with `FullGpuNativePack`
- Vulkan alternate writer-path captures if supported later

## 7. Evidence Bundle Ledger

Use this as the Stage 2 checklist.

### E01: Lit reference

Purpose:

- establish the baseline scene
- give the reader a clean visual anchor

Type:

- automated clean renderer capture

View mode:

- `Lit`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- what the scene looks like without debug overlays
- what camera framing the later debug captures correspond to

Best article use:

- opening visual reference

Status:

- pending

### E02: PTLAS partitions

Purpose:

- show logical PTLAS partition layout

Type:

- automated clean renderer capture

View mode:

- `RayTracingPartitions`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- Sparkle already produces partition assignments
- the partition grid is visible in-engine

Best article use:

- section 2 or 3

Status:

- pending

### E03: PTLAS partition updates

Purpose:

- show dirty transforms and update-localized behavior

Type:

- automated clean renderer capture

View mode:

- `RayTracingPartitionUpdates`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- Sparkle distinguishes changed regions / changed instances
- the workload is not uniformly dirty

Best article use:

- section 3 or 6

Status:

- pending

### E04: PTLAS instance movement

Purpose:

- show transform changes vs partition crossings

Type:

- automated clean renderer capture

View mode:

- `RayTracingInstanceMovement`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- Sparkle tracks movement state beyond simple presence in a partition

Best article use:

- section 3

Status:

- pending

### E05: Top-level mode classic

Purpose:

- capture the classic TLAS baseline

Type:

- automated clean renderer capture

View mode:

- `RayTracingTopLevelMode`

Configuration:

- `r.RayTracing.PreferPartitionedTlas = false`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- the engine can be forced into classic mode
- gives a comparison partner for partitioned mode

Best article use:

- section 5 or evidence table

Status:

- pending

### E06: Top-level mode partitioned

Purpose:

- capture the PTLAS-selected state

Type:

- automated clean renderer capture

View mode:

- `RayTracingTopLevelMode`

Configuration:

- `r.RayTracing.PreferPartitionedTlas = true`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- the engine selects PTLAS when requested and supported

Best article use:

- section 5 or evidence table

Status:

- pending

### E07: Native operations

Purpose:

- show what the PTLAS native work looks like in the current build

Type:

- automated clean renderer capture

View mode:

- `RayTracingNativeOperations`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- the article's most important implementation reality
- this figure should be paired with `logicalUpdates` and `nativeOperations`

Best article use:

- section 6

Status:

- pending

### E08: Provider status D3D12

Purpose:

- show D3D12 PTLAS provider status and fallback reason state

Type:

- automated clean renderer capture

View mode:

- `RayTracingProviderStatus`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- backend/provider reporting is wired

Best article use:

- vendor / backend evidence

Status:

- pending

### E09: Provider status Vulkan

Purpose:

- show Vulkan PTLAS provider status

Type:

- automated clean renderer capture

View mode:

- `RayTracingProviderStatus`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- Vulkan backend path exists and is visible through diagnostics

Best article use:

- vendor / backend evidence

Status:

- pending

### E10: GPU updates view

Purpose:

- show requested vs selected update writer path behavior

Type:

- automated clean renderer capture

View mode:

- `RayTracingGpuDrivenUpdates`

Expected files:

- `image.bmp`
- `metadata.json`
- `timing.csv`
- `notes.md`

What this proves:

- the article can discuss requested vs selected writer path with visual support

Best article use:

- section 5 or 7

Status:

- pending

### E11: Manual overlay screenshot - partition updates

Purpose:

- show the in-editor PTLAS overlay with live counters

Type:

- manual editor screenshot

View mode:

- `RayTracingPartitionUpdates`

Expected files:

- `image.png`
- `notes.md`

What this proves:

- Sparkle exposes live PTLAS metrics in-editor
- the engine already has a practical debug surface for the feature

Best article use:

- section 5

Status:

- pending

### E12: Manual overlay screenshot - native operations

Purpose:

- show the in-editor PTLAS overlay in the most important view mode

Type:

- manual editor screenshot

View mode:

- `RayTracingNativeOperations`

Expected files:

- `image.png`
- `notes.md`

What this proves:

- live diagnostics can be paired directly with the hard-part section

Best article use:

- section 6

Status:

- pending

## 8. Required Metadata Fields To Record

For every automated capture, confirm the JSON contains:

- capture path
- frame index
- view mode name
- capture label
- capture purpose
- backend
- adapter name
- top-level provider
- top-level provider reason
- PTLAS provider
- PTLAS supported
- PTLAS capability reason
- total render instances
- traceable instances
- partitions
- dirty transforms
- moved partitions
- global partition instances
- logical updates
- native operations
- requested writer path
- selected writer path
- writer reason
- BLAS GPU ms
- classic TLAS GPU ms
- PTLAS update GPU ms
- RT pass GPU ms

## 9. Required CSV Fields To Record

For every automated capture, confirm the CSV contains:

- backend
- adapterName
- topLevelProvider
- topLevelProviderReason
- ptlasProvider
- ptlasSupported
- ptlasCapabilityReason
- partitionCount
- dirtyTransforms
- dirtyRatio
- movedPartitions
- globalPartitionInstances
- logicalUpdates
- nativeOperations
- selectedWriterPath
- writerReason
- cpuPackMs
- gpuDirtyMs
- gpuNativePackMs
- ptlasUpdateGpuMs
- rayTracingPassGpuMs
- finalFrameGpuMs

## 10. Notes Template For Each Bundle

Each `notes.md` should capture:

### Capture identity

- bundle ID
- backend
- top-level mode
- writer path
- view mode
- frame index

### Why this capture exists

- what article section it supports
- what specific claim it supports

### What to look at

- visual cues in the image
- the two or three most important JSON/CSV values

### Interpretation

- what a peer rendering engineer should infer from the capture

### Caveats

- anything temporary
- if the state is static vs update-active
- if the capture should not be interpreted as a performance claim

## 11. Capture Labels And Purpose Strings

To keep the metadata clean, use consistent labels.

Recommended `captureLabel` values:

- `ptlas-lit-reference`
- `ptlas-partitions`
- `ptlas-partition-updates`
- `ptlas-instance-movement`
- `ptlas-top-level-classic`
- `ptlas-top-level-partitioned`
- `ptlas-native-operations`
- `ptlas-provider-status-d3d12`
- `ptlas-provider-status-vulkan`
- `ptlas-gpu-updates`

Recommended `capturePurpose` values:

- `article-baseline-reference`
- `article-ptlas-partition-visualization`
- `article-ptlas-update-visualization`
- `article-ptlas-instance-movement-visualization`
- `article-top-level-mode-comparison`
- `article-native-operation-evidence`
- `article-provider-status-evidence`
- `article-writer-path-evidence`

## 12. Implementation Evidence To Pair With Visuals

Some article claims need code references next to the visuals.

Pair these explicitly:

- E02 / E03 / E04
  - `RayTracingPtlasPartitionPlanner.cpp`
  - `RayTracingTopLevelScenePlanner.cpp`

- E07
  - `RayTracingPtlasLogicalUpdateStream.cpp`
  - `RayTracingPartitionedTlasStrategy.cpp`

- E08 / E09
  - `D3D12NvapiRayTracingProvider.cpp`
  - `VulkanPartitionedTlasServices.cpp`

- E11 / E12
  - `ViewportRayTracingDebugOverlay.cpp`
  - `RhiSmokeCaptureArtifacts.cpp`

## 13. Evidence Gaps To Watch For

Stage 2 is not just “collect images”.
We should watch for missing proof.

If any of these are missing, note them explicitly:

- no capture with non-zero dirty transforms
- no capture with meaningful moved partitions
- no backend cross-check beyond D3D12
- no native-operations state that clearly supports the article's hard-part argument
- no overlay screenshot with readable live values

## 14. Stage 2 Status Summary

Current status:

- automated captures: not yet collected
- manual overlay screenshots: not yet collected
- JSON bundles: not yet collected
- CSV bundles: not yet collected
- per-bundle notes: not yet collected

## 15. Best Next Actions

The next best action is to make Stage 2 executable.

Recommended order:

1. create the evidence folder structure
2. define one reusable smoke-capture workflow
3. collect D3D12 classic + partitioned captures first
4. collect overlay screenshots
5. add Vulkan captures
6. write `notes.md` for each bundle immediately after capture

## 16. Completion Check

Use this before moving to Stage 3:

- every required bundle exists
- every automated bundle has image + JSON + CSV + notes
- every manual bundle has image + notes
- every figure in the article plan already has a candidate asset
- the article can now be outlined directly against evidence
