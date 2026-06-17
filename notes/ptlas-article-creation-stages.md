# PTLAS Article Creation Stages

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Depends on: `notes/ptlas-article-design-doc.md`

## 1. Purpose

This document translates the PTLAS article design into an execution plan.

It exists so article creation becomes a staged engineering task rather than an open-ended writing task.
The goal is to keep the final article:

- grounded in a concrete implementation example
- backed by captures and diagnostics
- aligned with the peer audience
- rich in evidence so it never feels generic
- focused on reader understanding, not engine promotion

This is not the article itself.
It is the production document for making the article.

## 2. Target Outcome

Deliver one strong standalone PTLAS article that:

- explains the classic BLAS / TLAS acceleration-structure baseline first
- defines update / refit / rebuild vocabulary before introducing PTLAS
- explains PTLAS as a top-level update-model change
- compares Khronos, NVIDIA, and Microsoft models where useful
- uses SparkleEngine as the concrete implementation case
- proves claims with engine screenshots, smoke captures, metrics, and code references
- clearly distinguishes current working architecture from incomplete behavioral payoff

## 3. Working Title Direction

Approved working title:

- `Next Gen RT Acceleration Structure: PTLAS vs TLAS`

Strong internal / more direct alternative:

- `PTLAS: From Logical Updates to Real Selective Rebuilds`

This document uses the approved working title as the default reference.

## 4. Article Spine

The article should read as one continuous narration line:

`problem visual -> classic acceleration structures -> classic TLAS update problem -> PTLAS solution model -> implementation proof`

That means each major section should answer one question:

- baseline: what is the classic structure/update model?
- opening visual: what problem are we trying to make obvious before terminology?
- problem: why is classic TLAS update granularity too broad for local scene changes?
- solution: what does PTLAS change so the engine can express local top-level work?
- proof: does implementation preserve that selectivity from logical update planning to native submission?

The article should also be built around this core argument:

"A PTLAS integration pays off only when the engine's update stream controls which instances and partitions are rebuilt."

That is the line that should connect:

- the intro
- the structure overview
- the vendor comparison
- the implementation review
- the metrics
- the conclusion

## 5. Production Stages

### How to use the stages

These stages should now be treated as implementation prompts, not only as status markers.

Use each stage like this:

- choose the current stage
- use its prompt block as the instruction for the next work pass
- make the output land in the live site article when possible, not only in notes
- update the stage status after each meaningful pass

Prompt rule:

- Stage 0 to Stage 4 can produce planning artifacts
- Stage 5 and later should default to changing the live article in `content/posts/ptlas-engine-transition/index.md`
- notes should support the article, not replace it

### Stage 0: Freeze the article intent

Goal:

- confirm the article is a standalone peer-level PTLAS piece
- confirm SparkleEngine is the concrete implementation case
- confirm the article is allowed to be honest about current gaps

Deliverable:

- approved design direction

Exit criteria:

- title direction chosen
- audience confirmed
- scope confirmed as one article, not a series entry

Implementation prompt:

`Freeze the article intent for the PTLAS piece. Confirm title, audience, scope, and tone. Record the decision in the stage notes so later writing passes do not reopen core framing questions.`

### Stage 0 decision record

Stage 0 is now considered confirmed for this article direction.

Approved intent:

- this is a standalone PTLAS article
- this is a peer-level article for experienced rendering engineers
- this is not a series entry
- SparkleEngine is the concrete implementation case
- the article is explicitly allowed to be honest about current architectural and behavioral gaps
- the article should use vendor references to strengthen the PTLAS model, not to replace implementation evidence

Approved audience:

- primary: rendering engineers on the CDP / REKD side and similarly experienced peers
- secondary: external advanced readers who are comfortable with ray tracing architecture

Approved title direction:

- approved working title:
  `Next Gen RT Acceleration Structure: PTLAS vs TLAS`
- strong internal alternative:
  `PTLAS: From Logical Updates to Real Selective Rebuilds`

Approved scope:

- one standalone article
- includes a compact BLAS / TLAS / PTLAS baseline overview
- includes a short classic TLAS update/refit/rebuild baseline before PTLAS is introduced
- focuses on PTLAS as an update-model change
- uses SparkleEngine architecture, diagnostics, and current implementation reality as evidence
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

Implementation prompt:

`Gather the authoritative source truth for the PTLAS article. Add only sources that can support article claims. For each source, record what it proves, what claim it should support, and which SparkleEngine file or diagnostic path it connects to.`

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

Implementation prompt:

`Build the PTLAS evidence package for the live article. Define or collect every screenshot, metadata file, timing CSV, and overlay capture the article will need. For every capture, record what it proves and where it should appear in the article.`

### Stage 3: Draft the visual assets

Goal:

- create the diagrams and comparison tables that the article needs

Deliverables:

- BLAS / TLAS / PTLAS comparison table
- classic BLAS / TLAS update-refit-rebuild baseline visual
- PTLAS update-model diagram
- domino sample partition-policy tradeoff visual
- implementation code-path / architecture diagram
- classic TLAS vs PTLAS evidence table
- interactive widgets that let the reader explore why PTLAS changes update behavior

Exit criteria:

- visuals are specific enough to the implementation and PTLAS
- visuals support the exact article claims

Implementation prompt:

`Draft the article visuals so they can be inserted into the live PTLAS post. Prefer compact tables, clear diagrams, concrete evidence framing, and interactive widgets where interactivity clarifies a behavior difference faster than prose. Every visual must support one concrete article claim.`

Stage 3 working document:

- `notes/ptlas-stage3-visual-assets.md`

Current Stage 3 draft status:

- classic BLAS / TLAS update-refit-rebuild baseline visual: drafted
- BLAS / TLAS / PTLAS comparison table: drafted
- PTLAS update-model diagram: drafted
- domino sample partition-policy tradeoff visual: drafted
- implementation code-path / architecture diagram: drafted
- classic TLAS vs PTLAS evidence table: drafted

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

Implementation prompt:

`Turn the PTLAS article plan into a narration-friendly article skeleton. Define section order, opening text, transitions, and evidence placement so the article can be written directly into the website without inventing structure mid-pass.`

Stage 4 working document:

- `notes/ptlas-stage4-article-skeleton.md`

Current Stage 4 draft status:

- complete section outline: drafted
- intro: drafted
- ending: drafted
- per-section evidence notes: drafted

### Stage 5: Write the first full article draft

Goal:

- produce the full article from the skeleton and evidence set

Deliverables:

- first complete article markdown draft

Exit criteria:

- the article reads end to end
- all major claims are backed by proof
- no section depends on future work to make sense

Implementation prompt:

`Advance the live PTLAS website article from structured draft toward publishable prose. Work directly in content/posts/ptlas-engine-transition/index.md. Keep the article concise, visual-first, and presentation-friendly. Replace weak generic phrasing with concrete evidence, add tables/diagrams/callouts where they reduce text, and make sure every major statement is backed by Stage 1 source truth or SparkleEngine implementation evidence. Do not let notes become the main artifact; the live article is the main artifact.`

Stage 5 execution rules:

- prefer editing `content/posts/ptlas-engine-transition/index.md`
- improve one or more complete sections per pass
- keep prose skimmable and non-repetitive
- add placeholders only when they map to a defined Stage 2 or Stage 3 asset
- preserve technical honesty around current PTLAS gaps
- when a behavior difference is easier to feel than to read, prefer adding or improving an interactive widget

Stage 5 pass checklist:

- does the edited section advance the baseline -> problem -> solution -> proof narration?
- does every visual answer a distinct reader question?
- can any paragraph, bullet, or visual be removed without weakening the story?
- does each topic end with a concrete takeaway or transition instead of stopping abruptly?
- does the edited section read cleanly in the website?
- does it have a clear visual anchor or planned visual anchor?
- does any Sparkle detail explain a TLAS/PTLAS concept, prove a claim, or expose a useful gap?
- does the NVIDIA domino sample coverage explain scale, partition colors, update policies, sparse operation generation, and measurement signals?
- does it avoid repeating another section's point?
- does it support spoken narration as well as silent reading?

Stage 5 reader-focus guardrails:

- SparkleEngine is evidence, not the protagonist
- avoid phrases such as `already has a real`, `well past exploring`, `many right pieces`, or anything that sounds like feature boasting
- avoid throat-clearing such as `this article follows`, `to keep this concrete`, or `the useful question is`
- avoid vague AI-flavored terms such as `handoff`, `real`, `hard part`, `actually`, and `really`; prefer the precise subsystem, boundary, or measurement
- prefer `implementation example`, `local proof anchor`, `current path`, and `observable gap`
- keep a Sparkle reference only if it explains TLAS/PTLAS behavior, supports a concrete claim, or makes a limitation visible
- remove any sentence whose main effect is to praise the engine rather than help the reader understand PTLAS
- remove any sentence whose main effect is to describe article intent rather than teach a TLAS/PTLAS concept
- do not ask readers to care about SparkleEngine by name; show behavior, evidence, and tradeoffs
- do not enumerate implementation files in the live article as proof
- use diagrams, checkpoint tables, metrics, captures, or specific line citations instead of raw source-file lists
- keep source referrals out of the teaching flow; put reference links in a compact `Resources` section unless an inline link is essential to understand the sentence
- use the NVIDIA sample as behavioral evidence, not as a copied walkthrough of its files
- prefer "what the UI/source proves" over "which source file contains it"

Stage 5 working document:

- `notes/ptlas-article-draft-1.md`

Current Stage 5 draft status:

- first complete article markdown draft: drafted

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

Implementation prompt:

`Review the live PTLAS article like a rendering engineer reviewing a peer draft. Identify overclaims, weak proof, ambiguity, repeated points, poor section rhythm, and any place where vendor or Sparkle behavior is imprecise. Revise the article directly after the review notes are known.`

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

Implementation prompt:

`Polish the live PTLAS article for DeepSparkBlog. Finalize frontmatter, section rhythm, image placement, captions, table formatting, and callouts so the piece feels native to the site and presentation-ready for live narration.`

## 6. Section-by-Section Build Plan

### Section 0: Classic acceleration-structure baseline

Purpose:

- establish the minimum BLAS / TLAS / update vocabulary needed before PTLAS appears

What this section must include:

- BLAS owns geometry acceleration data
- TLAS owns scene instance acceleration data
- TLAS instance records reference BLAS objects
- update/refit keeps an existing acceleration-structure shape where possible
- rebuild reconstructs the structure more fully
- classic TLAS can update correctly but still acts as one scene-level top-level maintenance path

Best evidence:

- bite-size visual showing geometry data -> BLAS and instance data -> TLAS
- separate rebuild vs update/refit visual
- short problem statement after those visuals, not inside the same diagram

Avoid:

- turning the article into a beginner ray tracing tutorial
- spending more time on BLAS than needed for the PTLAS contrast
- putting ownership, rebuild/refit vocabulary, and PTLAS motivation into one overloaded visual

### Section 1: The update-granularity bottleneck

Purpose:

- state the exact problem the article is solving after the classic TLAS baseline

What this section must include:

- the classic TLAS pain point
- localized motion vs top-level rebuild cost
- why "valid" does not equal "valuable"
- one explicit problem statement:
  `the granularity of scene change is often smaller than the granularity of classic TLAS maintenance`

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
- policy tradeoff:
  local partition update vs global partition update vs hybrid camera-distance mode
- optional partition translation mention

Best evidence:

- PTLAS update-model diagram

### Section 4: Vendor model

Purpose:

- align the article framing with vendor models

What this section must include:

- Khronos operation semantics
- NVIDIA behavioral sample expectations
- Microsoft PTLAS / indirect RTAS framing

Best evidence:

- compact terminology / model comparison table

Avoid:

- turning this into API token soup

### Section 5: Concrete implementation lens

Purpose:

- use one implementation path to explain where PTLAS selectivity can survive or collapse

What this section must include:

- strategy split
- partition planner
- logical update stream
- backend abstractions
- smoke evidence

Best evidence:

- checkpoint table or diagram
- specific code references only when tied to a claim
- one small architecture diagram
- screenshot or table proving diagnostics exist

### Section 6: Where selectivity collapses

Purpose:

- make the article's strongest point

What this section must include:

- selective logical updates exist
- native PTLAS work still collapses into full-scene write behavior
- therefore the implementation is not yet getting full PTLAS behavioral value

Best evidence:

- code references to logical update emission
- code references to full-scene write pack path
- native-operations screenshot
- logical vs native count table

### Section 7: What still has to change

Purpose:

- describe the remaining engineering work without implying it is already complete

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

### Figure 3: Implementation PTLAS architecture

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

- show live diagnostics and prove the behavior is observable

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

### Inputs for implementation architecture

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

Use these only when they teach a concept, prove a claim, or expose the implementation gap:

- partition planning as the place where spatial ownership is decided
- per-instance PTLAS debug data as proof that the engine can inspect partition state
- PTLAS debug view modes as proof that the behavior is visible, not assumed
- smoke metadata and timings as audit evidence
- requested vs selected writer path as proof that policy and fallback can be inspected
- backend-specific service layers as proof that API differences exist below the shared PTLAS model
- selective logical updates plus broad native write behavior as the central implementation gap

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
4. write section 5 `Concrete implementation lens`
5. write section 6 `Where selectivity collapses`
6. write sections 1-4
7. write sections 7-8
8. polish intro and ending last

Reason:

- the implementation-evidence sections are the most specific and should define the voice of the article

## 14. Quality Gates

Before calling the article ready, check:

### Accuracy gate

- every major claim has a source or code reference
- no vendor feature is overstated
- Sparkle's current gaps are stated clearly

### Specificity gate

- concrete implementation details teach something a generic article could not
- screenshots, metrics, and code references support reader understanding instead of praising the engine

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

### Narration gate

- the article can be summarized as:
  classic acceleration structures -> classic TLAS update problem -> PTLAS solution model -> implementation proof
- no section feels like an unrelated observation
- technical details appear only when they support the current step of the story
- the reader always knows whether they are looking at baseline, problem, solution, or proof

### Visual gate

- every visualization answers one explicit reader question
- if a visual answers more than one reader question, split it
- no two visuals are used to prove the same point unless the second adds new evidence
- each visual is introduced before it appears
- visual introductions explain how to read the asset, not why the asset is impressive
- unused widgets can stay in the repo, but should not appear in the live article unless they earn a distinct role

## 15. Suggested Deliverables Checklist

- approved article title direction
- approved article scope
- final evidence bundle list
- all required captures exported
- all required JSON / CSV files extracted
- BLAS / TLAS / PTLAS comparison table drafted
- vendor terminology table drafted
- implementation architecture diagram drafted
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
