# PTLAS Review Implementation Prompts

Date: 2026-06-18

Input review:

- `notes/ptlas-article-raytracing-article-review.md`

Target article:

- `content/posts/ptlas-engine-transition/index.md`

Purpose:

- address the agreed review feedback without bloating the article
- keep the paper-style order
- add evidence and measurement value before adding more explanation

Global constraints:

- keep the body before `## Resources` below 2,300 words
- prefer one compact evidence block over more prose
- do not add another large visual unless it replaces an existing one
- do not add vendor explanation in the main body
- do not publish placeholder numbers as facts
- use `capture needed` when a value is not available yet
- run the rewrite quality gates after each pass

## Coverage Map

| Review feedback | Covered by pass |
|---|---|
| Add measurement axis under opening visual | Pass 1 |
| Add captured metrics or explicit missing values | Pass 2 |
| Extract engine values needed for evidence | Pass 2 |
| Review `The Delta In One Table` for redundancy | Pass 3 |
| Add small measurement checklist | Pass 4 |
| Keep evidence gaps honest | Pass 4 |
| Add optional TLAS/rebuild/refit depth only if needed | Pass 5 |
| Keep tradeoffs as tradeoffs | Pass 6 |
| Preview dense PTLAS structure visual | Pass 7 |
| Preserve size and narration readiness | Pass 8 |

## Pass 0: Baseline Audit

Goal:

- confirm the current article state before changing anything

Prompt:

```text
Audit the current PTLAS article before applying review feedback.

Check:
- current word count before Resources
- section order
- current visual count
- whether `The Delta In One Table` repeats Background, API Context, or Proposed Model
- whether the PTLAS structure visual feels overloaded in preview

Do not edit the article in this pass unless a broken build is discovered.
```

Deliverable:

- short notes in the terminal/final response

Exit criteria:

- article builds
- current size is known
- redundancy risk is identified before editing

## Pass 1: Opening Measurement Caption

Review source:

- "Open With The Workload, Not The API"

Goal:

- make the opening visual's measurement axis explicit without explaining obvious visual details

Prompt:

```text
Add one short caption near the opening TLAS/PTLAS domino widget.

Use this direction:
Same motion, different top-level maintenance footprint.

Keep it short.
Do not describe every color or object in the widget.
Do not add vendor/API context before the reader sees the problem.
```

Target location:

- immediately after `{{< interactive-ptlas-domino-field >}}`

Exit criteria:

- caption reinforces the comparison
- no new paragraph of visual narration
- build succeeds

## Pass 2: Evidence Snapshot

Review source:

- "Make Measurements First-Class"
- "Reader Value"
- "Technical Depth"

Goal:

- add one compact metric block so the article has concrete evidence discipline

Prompt:

```text
Add one compact `Evidence Snapshot` block.

Preferred location:
- after `## What The Domino Workload Adds`

Use 4-5 rows only.

Fields:
- scene instances
- changed instances
- touched partitions
- maintained top-level region
- top-level update time
- memory or scratch, only if space allows

Rules:
- use captured values when available
- if a value is not captured yet, write `capture needed`
- do not present sample UI values as SparkleEngine proof unless they came from SparkleEngine capture
- do not claim PTLAS is faster until backend command scope and timings are captured
```

Suggested table:

| Capture field | Classic TLAS | PTLAS |
|---|---:|---:|
| Scene instances | capture needed | capture needed |
| Changed instances | capture needed | capture needed |
| Maintained top-level region | full TLAS | capture needed |
| Top-level update time | capture needed | capture needed |
| Scratch or memory | capture needed | capture needed |

Engine data to extract:

- total scene instances
- changed instances
- touched partitions
- global partition instance count
- TLAS update time
- PTLAS update time
- TLAS memory
- PTLAS memory
- TLAS scratch
- PTLAS scratch

Exit criteria:

- evidence block exists
- unknowns are labeled honestly
- no unverified performance claim appears
- article remains below 2,300 words before Resources

## Pass 3: Redundancy Cut Or Rename

Review source:

- "Clarity"
- "Layout"
- "Size"

Goal:

- decide whether `The Delta In One Table` still earns its space after the evidence snapshot

Prompt:

```text
Review `## The Delta In One Table`.

If it repeats Background, API Context, and Proposed Model:
- remove it

If it still helps:
- rename it to `## Model Comparison`
- remove the generic sentence after the table
- compress table rows that repeat earlier sections

Prefer deletion if the evidence snapshot now gives the reader a stronger comparison.
```

Exit criteria:

- no repeated model explanation remains
- no consecutive table sequence feels heavy
- article stays compact

## Pass 4: Evidence Checklist And Claim Guardrails

Review source:

- "Be Honest About Evidence Gaps"
- "Reader should also leave with a measurement checklist"

Goal:

- make the evidence section actionable without turning it into roadmap filler

Prompt:

```text
At the end of `## Evidence And Current Limitations`, add a compact measurement checklist.

Keep it to 5 bullets maximum.

Include:
- changed-instance count
- rewritten-instance count
- touched-partition count
- native operation type/count
- global partition population

Also preserve the distinction between:
- engine-side dirty update records
- backend build/update command scope
```

Internal do-not-claim list:

- do not claim PTLAS is faster until backend command scope and timings are captured
- do not claim memory improves
- do not claim global partition is better than local partition
- do not compare backend maturity without matching captures

Exit criteria:

- checklist gives concrete fields to extract
- limitation remains measurable
- no roadmap-flavored prose is added

## Pass 5: TLAS/Rebuild/Refit Depth Gate

Review source:

- "Treat TLAS/Rebuild/Refit With More Respect Than A Glossary"
- "Concept ramp"

Goal:

- decide whether the Background section needs one small baseline table

Prompt:

```text
Preview the Background section.

If rebuild/refit still feels too compressed, add one 3-row mini-table after the rebuild/refit paragraph.

Use:

| Case | Common choice | Why |
|---|---|---|
| Transform-only movement | Refit/update | Reuse previous structure work |
| Broad membership/layout change | Rebuild | Builder can improve layout |
| Repeated refit drift | Rebuild checkpoint | Restore traversal quality |

If the existing update-modes visual already covers this, do not add the table.
```

Exit criteria:

- baseline is understandable to a rendering engineer who has not recently worked on AS update paths
- no beginner tutorial tone
- no redundant table if the visual already does the job

## Pass 6: Policy Tradeoff Check

Review source:

- "Keep Tradeoffs As Tradeoffs"

Goal:

- ensure local/global/hybrid policy is not framed as one mode winning everywhere

Prompt:

```text
Review `## Update Policy Tradeoffs`.

If the section feels too update-cost focused, add one sentence:
The policy should be compared with both update time and trace cost; update-only wins can move cost into traversal.

If the Discussion section already covers this clearly, do not add the sentence.
```

Exit criteria:

- no policy is framed as universally best
- update cost and trace cost are both visible
- no repeated discussion text

## Pass 7: PTLAS Structure Visual Density Check

Review source:

- "Use Tooling-Like Visuals, Not Decorative Visuals"
- "Preview the PTLAS structure visual"

Goal:

- decide whether the PTLAS structure visual should stay as one card or be split later

Prompt:

```text
Preview `ptlas-structure-slide.html` in the article.

Ask:
- does the visual answer one question?
- is it trying to show storage model and update model at the same time?
- are any arrows decorative rather than explanatory?
- does the visual compete with the opening widget?

If it feels dense, do not immediately add a new visual.
Create a follow-up note to split it into:
- storage model
- update model

Only split if one existing visual is removed or replaced.
```

Exit criteria:

- visual either stays unchanged with justification or gets a follow-up split task
- no sixth major visual is added in this pass

Pass 7 result:

- screenshot captured: `notes/screenshots/ptlas-pass7-proposed-model.png`
- tall page screenshot captured: `notes/screenshots/ptlas-pass7-tall-page.png`
- decision: keep the current visual for now
- reason: the rendered card is readable in context and does not compete with the opening TLAS/PTLAS widget
- risk: it combines storage model and update model in one card
- follow-up split task: if the card feels dense during live preview, replace it with two focused visuals instead of adding a new visual
- split target A: storage model, showing BLAS reuse, instance-index pool, partitions, and global partition
- split target B: update model, showing changed instance records, touched partitions, and indirect build/update operation input

## Pass 8: Final Review Against Quality Gates

Review source:

- all review sections
- rewrite quality gates from `notes/ptlas-paper-style-skeleton.md`

Goal:

- confirm the article is stronger without becoming larger and blurrier

Prompt:

```text
Run the final article review.

Check:
- body before Resources stays below 2,300 words
- section order still follows the paper-style skeleton
- article has one concrete evidence snapshot
- article has one measurement checklist
- no section repeats a visual
- no visual is decorative
- vendor links remain in Resources
- no raw implementation file enumeration
- no unverified performance claim
- no vague statement that sounds correct but teaches nothing
```

Commands:

```powershell
& "$env:USERPROFILE\tools\hugo\hugo.exe" -D --gc --minify
```

```powershell
rg -n "\b(handoff|real|really|actual|actually|hard part|just|signal|unlock|leverage|delve|robust|pivotal|seamless|tapestry|landscape|testament|underscore|furthermore|moreover|in conclusion|not just|not only|the key is|important|interesting|useful question|thing|stuff|properly|clearly)\b" content/posts/ptlas-engine-transition/index.md
```

Exit criteria:

- build succeeds
- guardrail scan has no matches or every match is intentionally accepted
- final article has more evidence value, not more bulk

## Recommended Execution Order

1. Pass 0: Baseline Audit
2. Pass 1: Opening Measurement Caption
3. Pass 2: Evidence Snapshot
4. Pass 3: Redundancy Cut Or Rename
5. Pass 4: Evidence Checklist And Claim Guardrails
6. Pass 5: TLAS/Rebuild/Refit Depth Gate
7. Pass 6: Policy Tradeoff Check
8. Pass 7: PTLAS Structure Visual Density Check
9. Pass 8: Final Review Against Quality Gates

## Expected Final Shape

After these passes, the article should:

- keep the scientific section order
- keep the strong opening visual
- include one concrete evidence snapshot
- include one measurement checklist
- remove or compress redundant comparison content
- preserve honest limitation language
- avoid bloat
- read as technical guidance for rendering engineers, not as vendor documentation or engine promotion
