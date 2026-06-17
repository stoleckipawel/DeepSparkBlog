# PTLAS Article Creation Stages

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Depends on: `notes/ptlas-article-design-doc.md`

## 1. Purpose

This document translates the PTLAS article design into an execution plan.

It exists so article creation becomes a staged engineering task rather than an open-ended writing task.
The goal is to keep the final article:

- grounded in SparkleEngine
- backed by real captures and diagnostics
- aligned with the peer audience
- rich in evidence so it never feels generic

This is not the article itself.
It is the production document for making the article.

## 2. Target Outcome

Deliver one strong standalone PTLAS article that:

- explains the classic TLAS baseline briefly
- explains PTLAS as a top-level update-model change
- compares Khronos, NVIDIA, and Microsoft models where useful
- uses SparkleEngine as the central implementation case
- proves claims with engine screenshots, smoke captures, metrics, and code references
- clearly distinguishes current working architecture from incomplete behavioral payoff

## 3. Working Title Direction

Approved working title:

- `What Changes When an Engine Moves From TLAS to PTLAS`

Strong internal / more direct alternative:

- `SparkleEngine PTLAS: From Logical Updates to Real Selective Rebuilds`

This document uses the approved working title as the default reference.

## 4. Article Spine

The article should be built around this core argument:

"A PTLAS integration becomes real only when the engine's update stream controls which instances and partitions are rebuilt."

That is the line that should connect:

- the intro
- the structure overview
- the vendor comparison
- the Sparkle implementation review
- the metrics
- the conclusion

## 5. Production Stages

### Stage 0: Freeze the article intent

Goal:

- confirm the article is a standalone peer-level PTLAS piece
- confirm SparkleEngine is the central implementation case
- confirm the article is allowed to be honest about current gaps

Deliverable:

- approved design direction

Exit criteria:

- title direction chosen
- audience confirmed
- scope confirmed as one article, not a series entry

### Stage 0 decision record

Stage 0 is now considered confirmed for this article direction.

Approved intent:

- this is a standalone PTLAS article
- this is a peer-level article for experienced rendering engineers
- this is not a series entry
- SparkleEngine is the central implementation case
- the article is explicitly allowed to be honest about current architectural and behavioral gaps
- the article should use vendor references to strengthen the Sparkle discussion, not to replace it

Approved audience:

- primary: rendering engineers on the CDP / REKD side and similarly experienced peers
- secondary: external advanced readers who are comfortable with ray tracing architecture

Approved title direction:

- approved working title:
  `What Changes When an Engine Moves From TLAS to PTLAS`
- strong internal alternative:
  `SparkleEngine PTLAS: From Logical Updates to Real Selective Rebuilds`

Approved scope:

- one standalone article
- includes a compact BLAS / TLAS / PTLAS baseline overview
- focuses on PTLAS as an update-model change
- centers on SparkleEngine architecture, diagnostics, and current implementation reality
- does not require follow-up series context to be understood

Approved tone:

- analytical
- implementation-oriented
- peer-to-peer
- technically honest
- evidence-backed

Stage 0 deliverable status:

- approved design direction: complete

Stage 0 exit criteria status:

- title direction chosen: complete
- audience confirmed: complete
- scope confirmed as one article, not a series entry: complete

### Stage 1: Gather source truth

Goal:

- collect every authoritative source the article will rely on

Source buckets:

- Khronos PTLAS extension / proposal
- Vulkan PTLAS operation semantics
- NVIDIA PTLAS sample
- NVIDIA NVAPI PTLAS docs
- Microsoft DirectX PTLAS / RTAS spec material
- SparkleEngine implementation files
- SparkleEngine diagnostics / smoke capture evidence

Deliverables:

- source list with links
- short notes per source
- exact local code references

Exit criteria:

- every major claim in the planned article can already be linked to a source or a local engine file

### Stage 2: Build the evidence package

Goal:

- collect all screenshots, metadata, timings, and implementation evidence before drafting the article in full

Deliverables:

- figure images
- metadata JSON files
- timing CSV files
- manual overlay screenshots
- short notes describing what each capture proves

Exit criteria:

- every planned visual has a matching explanation and evidence source

### Stage 3: Draft the visual assets

Goal:

- create the diagrams and comparison tables that the article needs

Deliverables:

- BLAS / TLAS / PTLAS comparison table
- PTLAS update-model diagram
- Sparkle code-path / architecture diagram
- classic TLAS vs PTLAS evidence table

Exit criteria:

- visuals are specific enough to Sparkle and PTLAS
- visuals support the exact article claims

### Stage 4: Draft the article skeleton

Goal:

- write section headers, opening paragraphs, transitions, and planned evidence blocks

Deliverables:

- complete section outline
- intro
- ending
- per-section evidence notes

Exit criteria:

- no section remains vague
- every section knows what screenshot, table, metric, or code reference it will use

### Stage 5: Write the first full article draft

Goal:

- produce the full article from the skeleton and evidence set

Deliverables:

- first complete article markdown draft

Exit criteria:

- the article reads end to end
- all major claims are backed by proof
- no section depends on future work to make sense

### Stage 6: Engineering review pass

Goal:

- validate technical accuracy and tone for peer readers

Review focus:

- overclaiming
- ambiguity
- missing proof
- weak transitions
- too much beginner explanation
- any vendor statement that needs more precision

Deliverables:

- review notes
- revised article draft

Exit criteria:

- article is technically credible to experienced rendering engineers

### Stage 7: Final polish

Goal:

- make the article feel native to DeepSparkBlog

Deliverables:

- final frontmatter
- image placement
- table formatting
- callout placement
- caption cleanup

Exit criteria:

- the article is publishable

## 6. Section-by-Section Build Plan

### Section 1: The real bottleneck

Purpose:

- establish why PTLAS matters without teaching ray tracing from scratch

What this section must include:

- the classic TLAS pain point
- localized motion vs top-level rebuild cost
- why "valid" does not equal "valuable"

Best evidence:

- one concise problem statement
- one small comparison table or diagram

Avoid:

- generic ray tracing history

### Section 2: Ray tracing structure overview

Purpose:

- establish the baseline before PTLAS

What this section must include:

- BLAS
- TLAS
- PTLAS
- how they differ in ownership and update behavior

Best evidence:

- BLAS / TLAS / PTLAS comparison table

### Section 3: What PTLAS changes conceptually

Purpose:

- explain partitions, global partition, and selective updates

What this section must include:

- partitions
- two-stage mental model
- selective updates
- partition movement
- global partition
- optional partition translation mention

Best evidence:

- PTLAS update-model diagram

### Section 4: Vendor model

Purpose:

- show that Sparkle's framing is aligned with real vendor models

What this section must include:

- Khronos operation semantics
- NVIDIA behavioral sample expectations
- Microsoft PTLAS / indirect RTAS framing

Best evidence:

- compact terminology / model comparison table

Avoid:

- turning this into API token soup

### Section 5: SparkleEngine today

Purpose:

- show what already exists and why it matters

What this section must include:

- strategy split
- partition planner
- logical update stream
- backend abstractions
- smoke evidence

Best evidence:

- code references
- one small architecture diagram
- screenshot or table proving diagnostics exist

### Section 6: The hard part

Purpose:

- make the article's strongest point

What this section must include:

- selective logical updates already exist
- native PTLAS work still collapses into full-scene write behavior
- therefore the engine is not yet getting full PTLAS behavioral value

Best evidence:

- code references to logical update emission
- code references to full-scene write pack path
- native-operations screenshot
- logical vs native count table

### Section 7: What still has to change

Purpose:

- show the roadmap without pretending it is already done

What this section must include:

- selective native operation generation
- occupancy / sizing policy
- writer path strategy
- measurement plan
- simplification opportunities

Best evidence:

- short roadmap bullets
- optional table: current state vs target state

### Section 8: What success looks like

Purpose:

- end with measurable acceptance criteria

What this section must include:

- changed-instance-only or changed-partition-only native rewrites
- trustworthy provider / fallback reporting
- meaningful metrics
- cross-capture proof

Best evidence:

- acceptance criteria checklist
- final evidence table

## 7. Required Engine Evidence Inventory

This is the must-have evidence package.

### 7.1 Mandatory images

Required clean captures:

- lit reference
- PTLAS partitions
- PTLAS partition updates
- PTLAS instance movement
- PTLAS top-level mode
- PTLAS native operations
- PTLAS provider status

Required manual screenshot:

- one editor viewport screenshot with PTLAS overlay visible

### 7.2 Mandatory data files

For each automated capture:

- image
- metadata JSON
- timing CSV

### 7.3 Mandatory code references

Must cite or use:

- `SparkleEngine/Docs/Rendering/PTLAS_TLAS_Design_Review.md`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingTopLevelScenePlanner.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasPartitionPlanner.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPtlasLogicalUpdateStream.cpp`
- `SparkleEngine/Engine/Renderer/Private/RayTracing/RayTracingPartitionedTlasStrategy.cpp`
- `SparkleEngine/Engine/RHI/Private/D3D12/RayTracing/D3D12NvapiRayTracingProvider.cpp`
- `SparkleEngine/Engine/RHI/Private/Vulkan/RayTracing/VulkanPartitionedTlasServices.cpp`
- `SparkleEngine/Engine/Application/Private/Validation/RhiSmokeCaptureArtifacts.cpp`
- `SparkleEngine/Engine/Editor/Private/Panels/ViewportRayTracingDebugOverlay.cpp`

### 7.4 Mandatory metrics

Must extract:

- top-level provider
- PTLAS provider
- PTLAS supported flag
- PTLAS capability reason
- partition count
- dirty transforms
- moved partitions
- global partition instances
- logical update count
- native operation count
- selected writer path
- writer reason
- BLAS GPU ms
- classic TLAS GPU ms
- PTLAS update GPU ms
- RT pass GPU ms

## 8. Recommended Figure Inventory

### Figure 1: BLAS / TLAS / PTLAS comparison

Type:

- table or diagram

Purpose:

- provide the baseline structure overview

### Figure 2: PTLAS update model

Type:

- conceptual diagram

Purpose:

- explain partitions, global partition, and selective rebuilds

### Figure 3: Sparkle PTLAS architecture

Type:

- architecture / flow diagram

Purpose:

- show planner -> logical updates -> native ops -> backend build

### Figure 4: PTLAS partitions capture

Type:

- clean engine screenshot

Purpose:

- make partitioning visible

### Figure 5: PTLAS partition updates capture

Type:

- clean engine screenshot

Purpose:

- show dirty / moved state under live updates

### Figure 6: PTLAS native operations capture

Type:

- clean engine screenshot

Purpose:

- connect logical updates to submitted work

### Figure 7: PTLAS overlay screenshot

Type:

- manual editor screenshot

Purpose:

- show live Sparkle diagnostics and prove this is not theoretical

### Figure 8: Evidence table

Type:

- compact article table

Purpose:

- summarize classic vs partitioned or D3D12 vs Vulkan evidence

## 9. Capture Bundles To Produce

Each figure or comparison should have a matching bundle folder.

Recommended bundle structure:

- `figure-name/`
- `figure-name/image.bmp`
- `figure-name/metadata.json`
- `figure-name/timing.csv`
- `figure-name/notes.md`

Each `notes.md` should say:

- what the capture is
- what the camera / frame state was
- what claim it supports
- what metrics matter most

## 10. Drafting Inputs Per Section

The article draft should not be written from memory.
Each section should be assembled from prepared inputs.

### Inputs for the intro

- title
- one-sentence thesis
- two-sentence problem framing
- one compact reader payoff block

### Inputs for the structure overview

- BLAS / TLAS / PTLAS comparison table
- one small framing paragraph

### Inputs for vendor comparison

- source notes
- vendor terminology mapping
- one short “what converges across vendors” paragraph

### Inputs for Sparkle architecture

- code references
- small architecture figure
- one paragraph per subsystem

### Inputs for the hard-part section

- exact code references
- native-ops screenshot
- logical vs native metric notes

### Inputs for the conclusion

- acceptance criteria list
- current state summary
- next engineering step summary

## 11. Specific Non-Generic Details To Push Into The Article

These are the details that prevent the article from feeling interchangeable with any other PTLAS post.

Push these in aggressively:

- Sparkle has a real partition planner already
- Sparkle already packs per-instance PTLAS debug data into frame data
- Sparkle already exposes PTLAS debug view modes
- Sparkle already exports PTLAS smoke metadata and timings
- Sparkle already distinguishes requested vs selected writer path
- Sparkle already has backend-specific PTLAS service layers for D3D12 and Vulkan
- Sparkle currently emits selective logical updates but still full-scene native write behavior

If those specifics disappear, the article becomes generic.

## 12. Optional Engine Improvements Before Writing

These are not required, but they would improve the article materially.

Recommended optional instrumentation:

- partition occupancy histogram
- max / avg / p95 occupancy per partition
- explicit counts per native op type
- explicit rewritten-instance count
- explicit first-build vs steady-state marker
- capture of requested runtime PTLAS config in smoke metadata

Recommended optional UX improvement:

- reusable smoke capture script for PTLAS view modes

## 13. Draft Order Recommendation

Recommended drafting order:

1. build capture bundles
2. draft the comparison tables
3. draft the diagrams
4. write section 5 `SparkleEngine today`
5. write section 6 `The hard part`
6. write sections 1-4
7. write sections 7-8
8. polish intro and ending last

Reason:

- the Sparkle sections are the most specific and should define the voice of the article

## 14. Quality Gates

Before calling the article ready, check:

### Accuracy gate

- every major claim has a source or code reference
- no vendor feature is overstated
- Sparkle's current gaps are stated clearly

### Specificity gate

- the article could not plausibly be rewritten by swapping out Sparkle for a generic engine name
- screenshots, metrics, and code references are Sparkle-specific

### Evidence gate

- every screenshot has a matching evidence file
- every metric table is traceable to JSON or CSV

### Reader-value gate

- the article teaches through differences
- the article provides acceptance criteria, not just description
- the article respects the knowledge level of experienced rendering engineers

### Blog-fit gate

- strong opening problem statement
- visible early roadmap
- compact high-signal tables
- good section rhythm
- no series-only scaffolding

## 15. Suggested Deliverables Checklist

- approved article title direction
- approved article scope
- final evidence bundle list
- all required captures exported
- all required JSON / CSV files extracted
- BLAS / TLAS / PTLAS comparison table drafted
- vendor terminology table drafted
- Sparkle architecture diagram drafted
- PTLAS update model diagram drafted
- article skeleton drafted
- first article draft written
- technical review applied
- final article draft prepared for content folder

## 16. Recommended Next Action

The best next action is not to start prose immediately.

The best next action is:

- create the capture bundles
- collect the evidence
- then build the article skeleton directly against that evidence

That will make the article feel observed, not merely explained.

## 17. Related Documents

- `notes/ptlas-article-design-doc.md`
