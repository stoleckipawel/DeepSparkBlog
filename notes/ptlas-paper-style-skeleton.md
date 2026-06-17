# PTLAS Paper-Style Article Skeleton

Date: 2026-06-17
Status: Draft 1
Owner: Pawel + Codex
Target article: `Next Gen RT Acceleration Structure: PTLAS vs TLAS`

## 1. Purpose

This document defines a more ordered, paper-style structure for the PTLAS article before rewriting the live post.

The goal is to move from a sequence of observations into a clean technical argument:

`abstract -> introduction -> background -> related work -> problem -> method -> evidence -> discussion -> conclusion -> resources`

This is not meant to make the article academic or dry.
It is meant to make the article easier to follow, easier to present, and harder to accidentally turn into loosely connected visuals.

## 2. Target Shape

Recommended article order:

1. Abstract
2. Introduction
3. Background: BLAS, TLAS, rebuild, refit
4. Related work and API context
5. Problem statement
6. Proposed model: PTLAS update granularity
7. Example workload and visual comparison
8. Update policy tradeoffs
9. Implementation method
10. Evidence and current limitations
11. Discussion
12. Summary
13. Resources

## 3. Section Skeleton

### 1. Abstract

Purpose:

- give the whole article in 4-6 sentences
- state the technical claim without marketing language
- mention current limitation honestly

Core content:

- classic TLAS is maintained as one top-level structure over instances
- PTLAS preserves the top-level traversal role but changes update expression
- the key distinction is update granularity: broad structure vs changed instances and touched partitions
- value depends on native submitted work, not only logical planning
- the article uses a domino-style workload and one engine integration path to reason about this

Visuals:

- none

Draft hook direction:

`PTLAS does not change what a top-level acceleration structure is for. It changes how top-level changes can be described.`

Exit criteria:

- reader knows the thesis before any diagram appears
- no vendor names
- no engine boasting

### 2. Introduction

Purpose:

- motivate why the topic matters
- introduce the article question
- set reader expectations

Core content:

- modern ray-traced scenes often have local motion inside large instance sets
- classic TLAS rebuild/refit can be valid but broad
- PTLAS introduces partitions as a way to express narrower top-level work
- the article asks whether selectivity survives from scene change to native work submission

Visuals:

- `interactive-ptlas-domino-field.html`

How to use the visual:

- place it after the intro paragraph
- do not explain every color or UI element
- let it establish the broad TLAS vs localized PTLAS contrast
- keep live mirrored stats under the visual

Exit criteria:

- reader understands the article question
- the first visual has a reason to exist

### 3. Background: Classic Acceleration-Structure Baseline

Purpose:

- define only the baseline concepts needed for the PTLAS delta
- avoid ray tracing 101

Core content:

- BLAS stores geometry acceleration data
- TLAS stores scene instances: transform, metadata, BLAS reference
- rebuild creates a top-level structure from current instance descriptions
- update/refit reuses a previous update-capable structure and changes instance-side data
- refit can reduce build cost but may affect traversal quality

Visuals:

- `rt-as-baseline.html`
- `rt-as-update-modes.html`

Exit criteria:

- reader has the vocabulary for the next sections
- no PTLAS claims are made before the TLAS baseline is grounded

### 4. Related Work And API Context

Purpose:

- show that PTLAS is an API-level model across modern ray tracing systems
- avoid turning the article into source-link narration

Core content:

- Vulkan / extension model exposes partitioned acceleration structures and explicit operations
- D3D12 / RTAS model frames PTLAS as partially rebuildable top-level state
- common concepts: partitions, instance write/update operations, optional global partition, indirect update data
- shader-facing traversal role remains top-level traversal

Visuals:

- optional compact terminology table

Exit criteria:

- source alignment is clear
- main text avoids brand-led explanation
- references stay in Resources

### 5. Problem Statement

Purpose:

- define the exact problem, not the solution

Core content:

- scene changes are often local
- classic TLAS maintenance is organized around one top-level structure
- a small dirty set can still become broad top-level work
- correctness is not the same as update selectivity

Suggested problem statement:

`The granularity of scene change can be smaller than the granularity of classic TLAS maintenance.`

Visuals:

- reuse the opening comparison if needed by reference, not duplicated

Exit criteria:

- problem is narrow and testable
- no vague language such as "hard part" or "real"

### 6. Proposed Model: PTLAS Update Granularity

Purpose:

- explain what PTLAS changes
- introduce partitions, instance-index pool, global partition, and indirect operations

Core content:

- PTLAS keeps top-level traversal role
- instances still reference BLAS
- top-level state is organized into partitions
- update work can be expressed through changed instances, touched partitions, and global partition movement
- BLAS can be reused; changed indices/partitions may need rewrite

Visuals:

- `ptlas-structure-slide.html`

Exit criteria:

- reader understands the model before implementation details
- diagram arrows and labels remain logically ordered

### 7. Example Workload And Measurement Signals

Purpose:

- connect the model to an observable workload
- explain which measurements matter

Core content:

- workload scale: about 170k dynamic dominoes, about 1.2M static objects
- uniform 2D partition grid
- local motion produces changed instance records
- measured values should be read together: instance work, AS size, scratch, updated region, update time

Visuals:

- opening TLAS vs PTLAS domino comparison if not already used in introduction
- live mirrored stat rows:
  `Instance work`, `AS size`, `Scratch`, `Region`

Exit criteria:

- metrics support the visual
- no explanatory legend unless it removes confusion

### 8. Update Policy Tradeoffs

Purpose:

- show that PTLAS is not one automatic behavior
- explain local partition vs global partition policy

Core content:

- local partition update: cleaner tracing, potentially more update work
- global partition: cheaper dynamic update path, less spatial coherence
- hybrid by distance: local near camera, global farther away
- aggressive mode can move all dominoes in a touched partition

Visuals:

- `ptlas-partition-policy.html`

Exit criteria:

- tradeoff is stated plainly
- no policy is presented as universally best

### 9. Implementation Method

Purpose:

- explain how selective intent becomes backend work
- separate CPU policy, CPU/GPU update authoring, and GPU execution

Core content:

- CPU owns setup, feature selection, sizing, command recording, synchronization
- CPU or GPU can detect changed instances and author sparse write records
- GPU executes build/update and tracing
- compute can append changed records into indirect operation buffers
- native operation packing is the stage where selectivity can survive or collapse

Visuals:

- `ptlas-cpu-gpu-split.html`
- sparse update Mermaid
- implementation architecture Mermaid

Exit criteria:

- reader sees where the update stream is authored
- reader sees where broad work can re-enter the system

### 10. Evidence And Current Limitations

Purpose:

- separate implemented architecture from measured behavior
- state current gap without drama

Core content:

- logical update stream can represent dirty or moved entries
- diagnostics expose planner/update state
- current native operation pack may still collapse into broad full-scene write behavior
- missing proof: selective native PTLAS work proportional to changed-instance/touched-partition sets

Visuals:

- checkpoint table
- evidence table
- optional warning callout

Exit criteria:

- no overclaiming
- limitations are measurable

### 11. Discussion

Purpose:

- interpret consequences and tradeoffs

Core content:

- partition size and overlap affect trace/update balance
- global partition helps dynamic updates but can reduce spatial coherence
- update timings must be interpreted with changed count and touched partition count
- memory and scratch size are part of the tradeoff
- diagnostics are necessary for trust

Visuals:

- none unless a table reduces text

Exit criteria:

- discussion adds interpretation, not repetition

### 12. Summary

Purpose:

- close with the article's final technical takeaway

Core content:

- TLAS remains the baseline top-level instance acceleration model
- PTLAS changes how top-level maintenance can be expressed
- the useful metric is not whether PTLAS exists, but whether local scene change becomes local native work
- success requires changed-instance counts, touched-partition counts, native operation breakdown, and timings

Visuals:

- none

Draft ending direction:

`PTLAS is useful when update granularity follows scene-change granularity. Everything else is implementation detail, policy, and proof.`

Exit criteria:

- concise
- no future-work sales pitch

### 13. Resources

Purpose:

- provide source links without interrupting the article

Content groups:

- classic BLAS / TLAS background
- PTLAS / partitioned acceleration structure specifications
- sample workload references
- D3D12 / RTAS material
- implementation references, if appropriate

Exit criteria:

- resources are grouped
- source links do not replace explanations in the main article

## 4. Reuse Map From Current Draft

| Current section / asset | New location |
|---|---|
| opening TLAS vs PTLAS domino widget | Introduction or Example Workload |
| `First, The Classic TLAS Baseline` | Background |
| `The Problem We Want To Solve` | Problem Statement |
| `PTLAS As The Solution Shape` | Proposed Model |
| `What The Domino Workload Adds` | Example Workload |
| `The Policy Choice` | Update Policy Tradeoffs |
| `Who Owns The Update Work?` | Implementation Method |
| `How The Sample Generates Sparse Work` | Implementation Method |
| `Vendor Model` | Related Work And API Context |
| `Concrete Implementation Lens` | Implementation Method / Evidence |
| `The Hard Part Is Not Naming the Feature` | Evidence And Current Limitations |
| `What Still Has To Change` | Discussion |
| `What Success Looks Like` | Summary or Evidence |

## 5. Style Rules For Rewrite

- no brand references in the main teaching flow unless required for a precise API name
- no file enumeration as proof
- no words such as `handoff`, `real`, `hard part`, `actually`, or `really`
- no obvious visual narration
- keep each section short enough for presentation
- every paragraph must either define a concept, state a tradeoff, describe a method, or interpret evidence
- every visual must answer one section-specific question

## 6. Open Decisions

- Should the article keep the TLAS vs PTLAS domino comparison in the Introduction, or move it after Background?
- Should SparkleEngine be named in the abstract or only in Method/Evidence?
- Should vendor terminology be a table in the main article or only Resources?
- Which engine captures are mandatory before replacing draft evidence with measured evidence?

## 7. Proposed Next Pass

Do not rewrite the live article yet.

Recommended next pass:

1. approve this section order
2. choose whether the opening visual appears before or after Background
3. write a concise abstract
4. rewrite the live article section by section into this structure

## 8. Approved Section Directions

This section records the selected direction for each segment.
Unselected alternatives have been removed.

### 1. Abstract: concise technical abstract

Direction:

- article should feel close to a technical paper
- state claim, scope, and limitation in one compact paragraph
- avoid promotional framing

Draft shape:

`This article compares classic TLAS maintenance with PTLAS-style partitioned top-level updates. The focus is update granularity: whether local instance motion can remain local when converted into native acceleration-structure work. The article reviews the classic BLAS/TLAS baseline, summarizes the PTLAS model, and uses a dynamic partitioned workload plus an engine implementation path to discuss what must be measured. The central limitation is that logical selectivity is not enough unless native work submission preserves it.`

### 2. Introduction: motivation from scene scale

Direction:

- start from large dynamic scenes
- make the problem intuitive before terminology
- pair with the domino visual early

Opening direction:

`Large ray-traced scenes rarely change uniformly. Motion often occupies a small part of the instance set, while the top-level structure still represents the whole scene.`

### 3. Background: baseline with rebuild/refit nuance

Direction:

- give rebuild/refit enough respect
- prevent PTLAS from sounding like a replacement for correct TLAS work
- keep the baseline compact but technically fair

Contents:

- BLAS/TLAS ownership
- instance records
- rebuild
- refit/update
- traversal-quality tradeoff
- why broad maintenance can still be valid

### 4. Related Work / API Context: short concept table

Direction:

- keep source details out of prose
- avoid API token soup
- use a compact concept table

Table concepts:

- partitioned top-level
- write instance
- update instance
- global partition
- indirect operations

### 5. Problem Statement: one-sentence problem

Direction:

- use one clean problem sentence
- keep it presentation-friendly
- let the visual and background provide surrounding context

Problem:

`The granularity of scene change can be smaller than the granularity of classic TLAS maintenance.`

### 6. Proposed Model: model through contrast

Direction:

- compare TLAS and PTLAS directly
- keep the article visually driven
- emphasize shared shader-facing top-level role

Flow:

- TLAS broad maintenance lane
- PTLAS partitioned maintenance lane
- shared shader-facing top-level role

### 7. Example Workload: keep opening visual in Introduction

Direction:

- keep the TLAS vs PTLAS domino visual in the Introduction
- use it as the opening hook
- background comes after the reader has already seen the contrast

### 8. Update Policy: visual plus small tradeoff table

Direction:

- use the policy visual
- add a compact table for exact tradeoffs
- keep rows limited

Rows:

- update cost
- trace coherence
- camera importance
- global partition growth

### 9. Implementation Method: engine architecture first

Direction:

- use the implementation path as the method spine
- introduce Sparkle path in the method/evidence area, not the abstract
- focus on where selectivity is authored, packed, and diagnosed

Flow:

- frame planning
- partition planning
- logical update stream
- native operation pack
- diagnostics

### 10. Evidence / Limitations: current-gap section

Direction:

- state what works and what still collapses
- keep the limitation measurable
- use this section for honest engineering review

Emphasis:

- logical selectivity exists
- native operation packing still needs proof or improvement

### 11. Discussion: tradeoff discussion

Direction:

- discuss engineering consequences
- avoid repeating the method/evidence section

Topics:

- partition size
- partition overlap
- global partition
- memory
- scratch

### 12. Summary: three-bullet summary

Direction:

- keep the ending clean and presentation-friendly
- use three bullets instead of a long closing paragraph

Draft:

- TLAS remains one top-level instance acceleration structure.
- PTLAS changes how top-level updates can be expressed.
- The proof is whether local scene change becomes local native work.

### 13. Resources: flat resource list

Direction:

- keep the current flat resource style
- simplest to maintain
- no per-resource notes unless needed later

## 9. Selection Summary

| Section | Selected direction |
|---|---|
| Abstract | Concise technical abstract |
| Introduction | Motivation from scene scale |
| Background | Baseline with rebuild/refit nuance |
| Related work / API context | Short concept table |
| Problem statement | One-sentence problem |
| Proposed model | Model through contrast |
| Example workload | Keep opening visual in Introduction |
| Update policy | Visual plus small tradeoff table |
| Implementation method | Engine architecture first |
| Evidence / limitations | Current-gap section |
| Discussion | Tradeoff discussion |
| Summary | Three-bullet summary |
| Resources | Flat resource list |

## 10. Implementation Prompt

Use this prompt to gradually replace the current live article with the approved paper-style structure.

Target file:

- `content/posts/ptlas-engine-transition/index.md`

Supporting files:

- `notes/ptlas-paper-style-skeleton.md`
- `notes/ptlas-stage1-source-truth.md`
- `notes/ptlas-stage3-visual-assets.md`
- current shortcodes in `layouts/shortcodes/`

Primary rule:

- rewrite the live article section by section, not all at once

Reason:

- the current article already has working visuals and useful technical fragments
- the rewrite should preserve good assets while replacing the ordering, prose, and section logic
- every pass should leave the article readable and previewable

### Implementation Pass 1: Frontmatter And Abstract

Goal:

- add the paper-style abstract at the top of the article
- keep the title for now
- keep the article draft status unchanged

Actions:

- update `summary` if needed
- replace the current two-line opening with a concise abstract paragraph
- avoid brand names in the abstract
- avoid implementation-specific names in the abstract

Use selected direction:

- `Abstract: concise technical abstract`

Exit criteria:

- article opens with the claim, scope, and limitation
- no visual appears before the abstract
- build succeeds

### Implementation Pass 2: Introduction With Visual Hook

Goal:

- rewrite the introduction around scene scale and localized motion
- keep the TLAS vs PTLAS domino widget in the introduction

Actions:

- create `## Introduction`
- introduce large scenes and non-uniform motion
- place `{{< interactive-ptlas-domino-field >}}` after the opening paragraph
- do not explain obvious visual elements
- keep live mirrored stats under the widget

Use selected direction:

- `Introduction: motivation from scene scale`
- `Example workload: keep opening visual in Introduction`

Exit criteria:

- introduction explains why the article exists
- visual supports the motivation
- no duplicated problem statement yet

### Implementation Pass 3: Background

Goal:

- move classic acceleration-structure explanation into a proper Background section

Actions:

- create `## Background`
- keep `rt-as-baseline.html`
- keep `rt-as-update-modes.html`
- rewrite prose around BLAS/TLAS ownership, rebuild, refit, and traversal-quality tradeoff
- remove beginner tutorial tone

Use selected direction:

- `Background: baseline with rebuild/refit nuance`

Exit criteria:

- reader has the TLAS vocabulary before PTLAS model appears
- rebuild/refit are treated fairly
- section stays compact

### Implementation Pass 4: Related Work / API Context

Goal:

- add a compact API context section without source-link narration

Actions:

- create `## Related Work And API Context`
- use a short concept table
- keep brand/vendor details minimal
- move source links to Resources

Use selected direction:

- `Related work / API context: short concept table`

Exit criteria:

- table maps core PTLAS concepts across API models
- no paragraph reads like a source summary

### Implementation Pass 5: Problem Statement

Goal:

- introduce the article's exact problem after baseline and API context

Actions:

- create `## Problem Statement`
- use the approved one-sentence problem
- add only enough supporting prose to make it testable

Use selected direction:

- `Problem statement: one-sentence problem`

Approved problem sentence:

`The granularity of scene change can be smaller than the granularity of classic TLAS maintenance.`

Exit criteria:

- problem is narrow
- no solution details dominate this section

### Implementation Pass 6: Proposed Model

Goal:

- explain PTLAS through contrast with TLAS

Actions:

- create `## Proposed Model`
- use the TLAS broad maintenance lane vs PTLAS partitioned maintenance lane framing
- keep `ptlas-structure-slide.html`
- explain shared shader-facing top-level role
- explain changed instances, touched partitions, and global partition movement

Use selected direction:

- `Proposed model: model through contrast`

Exit criteria:

- PTLAS model is clear before policy and implementation details
- structure visual has a clean lead-in

### Implementation Pass 7: Update Policy Tradeoffs

Goal:

- present local/global/hybrid policy as an engineering tradeoff

Actions:

- create `## Update Policy Tradeoffs`
- keep `ptlas-partition-policy.html`
- add a compact tradeoff table
- include update cost, trace coherence, camera importance, and global partition growth

Use selected direction:

- `Update policy: visual plus small tradeoff table`

Exit criteria:

- no policy is presented as universally best
- table is short and non-repetitive

### Implementation Pass 8: Implementation Method

Goal:

- explain where selectivity is created, packed, and submitted

Actions:

- create `## Implementation Method`
- use engine architecture first
- keep or adapt the architecture Mermaid
- include CPU/GPU responsibility split if it clarifies the method
- include sparse update Mermaid only if it adds new information

Use selected direction:

- `Implementation method: engine architecture first`

Exit criteria:

- reader can trace frame planning -> partition planning -> logical updates -> native operation pack -> diagnostics
- no file enumeration

### Implementation Pass 9: Evidence And Current Limitations

Goal:

- state what is already represented and what still needs proof or improvement

Actions:

- create `## Evidence And Current Limitations`
- preserve the current-gap honesty
- use checkpoint/evidence table
- avoid dramatic phrasing

Use selected direction:

- `Evidence / limitations: current-gap section`

Exit criteria:

- logical selectivity and native work submission are clearly separated
- limitation is measurable

### Implementation Pass 10: Discussion

Goal:

- interpret tradeoffs without repeating previous sections

Actions:

- create `## Discussion`
- cover partition size, overlap, global partition, memory, and scratch
- connect timings to instance work and touched region

Use selected direction:

- `Discussion: tradeoff discussion`

Exit criteria:

- discussion adds interpretation
- no roadmap filler

### Implementation Pass 11: Summary And Resources

Goal:

- close the article cleanly and preserve source links

Actions:

- create `## Summary`
- use the selected three-bullet ending
- keep `## Resources`
- keep resources as a flat list

Use selected direction:

- `Summary: three-bullet summary`
- `Resources: flat resource list`

Exit criteria:

- ending is concise
- resources remain useful
- build succeeds

## 11. Rewrite Quality Gates

Run these checks after each implementation pass:

- article builds with Hugo
- section order still matches the paper-style skeleton
- no unapproved words: `handoff`, `real`, `hard part`, `actually`, `really`, `signal`
- no generic AI-style filler: `unlock`, `leverage`, `delve`, `robust`, `pivotal`, `seamless`, `tapestry`, `landscape`, `testament`, `underscore`
- no formulaic contrast phrases: `not just`, `not only`, `it is not about`, `the key is`
- no school-essay transitions: `furthermore`, `moreover`, `in conclusion`
- no obvious visual narration
- no raw implementation file enumeration
- no brand-led explanation in the main teaching flow
- every section has one purpose
- every visual answers one section-specific question

## 12. Command Checklist

After each pass:

```powershell
& "$env:USERPROFILE\tools\hugo\hugo.exe" -D --gc --minify
```

Then scan the edited article for banned terms and AI-style filler:

```powershell
rg -n "\b(handoff|real|really|actual|actually|hard part|just|signal|unlock|leverage|delve|robust|pivotal|seamless|tapestry|landscape|testament|underscore|furthermore|moreover|in conclusion|not just|not only|the key is)\b" content/posts/ptlas-engine-transition/index.md
```
