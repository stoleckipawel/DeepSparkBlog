# PTLAS Vulkan Sample Performance Capture Plan

Target app:

`C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release\vk_partitioned_tlas.exe`

Purpose:

- extract trustworthy comparison data from NVIDIA's `vk_partitioned_tlas` sample
- replace the article's current `capture needed` placeholders only with values that are traceable to a capture
- avoid claiming that PTLAS is faster unless timing, update scope, and trace/render cost are captured together

## 1. What The Sample Already Exposes

The existing UI exposes enough data for a first article evidence snapshot:

| Field | Existing source | Article use |
|---|---|---|
| dynamic instance count | Settings / Scene: `Current domino count` | changed-work context |
| static object count | Settings / Scene: `Current static object count` | scene-size context |
| TLAS memory | Settings / Statistics: `TLAS` | memory row |
| TLAS scratch | Settings / Statistics: `TLAS scratch` | scratch row |
| PTLAS memory | Settings / Statistics: `PTLAS` | memory row |
| PTLAS scratch | Settings / Statistics: `PTLAS scratch` | scratch row |
| changed instance count | Settings / Statistics: `Updated instances` | changed-instance row |
| top-level update time | Profiler row: `TLAS Update` | timing row |
| animation update time | Profiler row: `Animation update instances` | sparse-update generation context |
| render time | Profiler row: `Render` | trace-cost context |
| compositing time | Profiler row: `Compositing` | frame-cost context |

Important caveat:

- `Updated instances` is `AnimationGlobalState::instanceUpdateCount`.
- It counts dynamic instances whose physics state changed this frame.
- It is not the full PTLAS rewritten-instance count when the global-partition policy moves extra instances.
- For article wording, call it `changed instances`, not `rewritten instances`, unless we add instrumentation.

## 2. Existing UI Modes To Capture

Use the same scene settings for all captures:

| Setting | Value |
|---|---:|
| Scene size | `1000.000` |
| Partitions per axis | `50` |
| Self-toppling dominoes | `2000` |
| VSync | on, as shipped |
| Profiler tab | `Table` |

Capture four modes:

| Capture ID | PTLAS active | TLAS refit | PTLAS policy | Mark all dynamic in partition |
|---|---|---|---|---|
| `classic_tlas_refit` | off | on | n/a | n/a |
| `ptlas_local_partition` | on | n/a | Always update partition | off |
| `ptlas_global_partition` | on | n/a | Always move dynamic to global | off |
| `ptlas_hybrid_distance` | on | n/a | Update partition nearby, move to global otherwise | off |

Optional stress capture:

| Capture ID | PTLAS active | PTLAS policy | Mark all dynamic in partition | Why |
|---|---|---|---|---|
| `ptlas_global_partition_whole_cell` | on | Always move dynamic to global | on | shows the cost of moving more instances than are currently changing |

## 3. Manual Capture Protocol

Manual capture is acceptable for draft article evidence if we label it as sample evidence, not SparkleEngine proof.

For each capture ID:

1. Start the app from `_bin\Release`.
2. Use the default scene unless the UI already differs from the table above.
3. Press Stop to reset animation.
4. Configure the mode.
5. Wait 2 seconds after reset so profiler rows settle.
6. Press Play.
7. Ignore the first 2 seconds of motion.
8. Record values from 10 frames over roughly 10-15 seconds.
9. Include at least one high-motion frame and one lower-motion frame.
10. Save one screenshot per mode showing Settings and Profiler.

Record this per sampled frame:

| Column | Source |
|---|---|
| capture_id | manual |
| sample_index | manual |
| timestamp_note | manual |
| dynamic_instances | Settings / Scene |
| static_instances | Settings / Scene |
| changed_instances | Settings / Statistics: `Updated instances` |
| tlas_memory_mb | Settings / Statistics |
| tlas_scratch_mb | Settings / Statistics |
| ptlas_memory_mb | Settings / Statistics |
| ptlas_scratch_mb | Settings / Statistics |
| animation_physics_gpu_ms | Profiler |
| animation_update_instances_gpu_ms | Profiler |
| tlas_update_gpu_ms | Profiler row `TLAS Update` |
| render_gpu_ms | Profiler |
| compositing_gpu_ms | Profiler |
| frame_gpu_ms | Profiler |
| frame_cpu_ms | Profiler |
| screenshot_path | local file |

Average rule:

- Use the arithmetic mean of the 10 sampled frames.
- Also keep min and max for `changed_instances`, `tlas_update_gpu_ms`, and `render_gpu_ms`.
- If one sample is visually a reset frame or shader recompile hitch, discard it and document why.

## 4. Sanity Checks Before Using Numbers

Use a captured row only if these checks pass:

| Check | Expected result |
|---|---|
| `dynamic_instances` | about `169,231` in the default scene |
| `static_instances` | about `1,219,587` in the default scene |
| total workload objects | about `1.38M` |
| TLAS memory | roughly `280-290 MB` in current screenshots |
| TLAS scratch | roughly `100-105 MB` in current screenshots |
| PTLAS memory | roughly `315-325 MB` in current screenshots |
| PTLAS scratch | roughly `108-112 MB` in current screenshots |
| `changed_instances` | varies with simulation; should not stay fixed during motion |
| classic TLAS `TLAS Update` | should be comparatively stable across changed-instance count |
| PTLAS `TLAS Update` | should vary with update workload and policy |
| render time | must be compared beside update time because global partition can move cost into traversal |

Do not use a run if:

- the profiler is not visible
- the scene settings differ and are not recorded
- the app just regenerated the scene
- the first reset frame is included in the average
- render resolution/window size changed between modes

## 5. Article Evidence Mapping

Use sample capture values only for the article's sample-workload evidence. Do not present them as SparkleEngine measurements.

| Article field | Fill from capture | Safe wording |
|---|---|---|
| Scene instances | `dynamic_instances + static_instances` | measured in sample capture |
| Changed instances | `changed_instances` | dynamic instances changed this frame |
| Maintained top-level region | classic: `full TLAS`; PTLAS: `capture needed` unless touched partitions are instrumented | do not invent touched partition count |
| Top-level update time | `tlas_update_gpu_ms` | profiler GPU average |
| Scratch or memory | UI memory/scratch stats | sample allocation sizes |

Current values visible in existing screenshots can be used only as provisional targets:

| Field | Observed range from screenshots |
|---|---:|
| Dynamic instances | `169,231` |
| Static instances | `1,219,587` |
| TLAS memory | `284.82-285.58 MB` |
| TLAS scratch | `103.61-103.93 MB` |
| PTLAS memory | `319.13-320.06 MB` |
| PTLAS scratch | `110.23-110.30 MB` |
| Changed instances | `5,001-12,010` |
| Profiler `TLAS Update` | about `0.958-1.480 ms` in shown captures |

Those screenshot observations are not enough for final article data. They are useful for expected-range validation only.

## 6. Missing Data That Requires Instrumentation

The current UI does not expose every field needed for rigorous PTLAS claims.

| Missing field | Why it matters | Where to instrument |
|---|---|---|
| rewritten-instance count | separates changed physics instances from PTLAS write records | read back `ptlasOperations[0].argCount` after `animation_update_instances.comp.glsl` |
| touched-partition count | proves update region size | count `PartitionState.needInstanceIndicesRewrite` or `lastModified == frameIndex` |
| global partition population | shows trace-coherence risk | count dynamic instances whose `partitionID == globalPartitionIndex` |
| native operation type/count | verifies backend command scope | log `operationsCount` and each operation's `opType` / `argCount` |
| per-mode averaged CSV | avoids screenshot-only evidence | write a capture CSV after each sampled frame |

Recommended code instrumentation:

- add a small capture struct in `PartitionedTlasSample`
- add readback buffers for:
  - `m_ptlas.getBuffers().operationsInfo`
  - `m_ptlas.getBuffers().operationsCount`
  - `m_partitionState`
  - `m_state[(currentStateIndex + 1) % 2]`
- after the existing `m_globalState` readback, copy those buffers into host-visible staging buffers
- write one CSV row every N frames while capture is active

Minimum CSV columns for instrumented capture:

```csv
frame,capture_id,ptlas_active,policy,mark_all_dynamic,refit_tlas,dynamic_instances,static_instances,changed_instances,rewritten_instances,touched_partitions,global_partition_population,native_operation_count,native_operation_0_type,native_operation_0_arg_count,tlas_update_gpu_ms,animation_update_instances_gpu_ms,render_gpu_ms,tlas_memory_mb,tlas_scratch_mb,ptlas_memory_mb,ptlas_scratch_mb
```

## 7. Recommended Capture Set For The Article

For the current article, the best compact evidence package is:

| Artifact | Count | Purpose |
|---|---:|---|
| full app screenshot | 1 per mode | visual proof of settings and profiler |
| manual sample CSV | 10 rows per mode | first averaged evidence snapshot |
| averaged summary CSV | 1 row per mode | article table source |
| instrumented CSV | later | replaces manual values with backend-scope proof |

Article rule:

- Manual capture can fill scene size, memory/scratch, changed-instance count, and profiler update time.
- Instrumented capture is required before filling rewritten-instance count, touched partitions, global partition population, and native operation count.

## 8. Suggested Article Replacement Table

Only after manual capture:

| Capture field | Classic TLAS | PTLAS |
|---|---:|---:|
| Scene instances | measured total | measured total |
| Changed instances | averaged changed-instance count | averaged changed-instance count |
| Maintained top-level region | full TLAS | touched partitions: capture needed |
| Top-level update time | averaged `TLAS Update` GPU ms | averaged `TLAS Update` GPU ms |
| Scratch or memory | TLAS memory/scratch | PTLAS memory/scratch |

Only after instrumentation:

| Capture field | Classic TLAS | PTLAS |
|---|---:|---:|
| Rewritten instances | full TLAS instance buffer / n/a depending wording | PTLAS op `argCount` |
| Touched partitions | n/a | counted partitions |
| Native operation count | one TLAS build/update command | PTLAS operations count |
| Global partition population | n/a | counted dynamic instances in global partition |

## 9. Notes For Later Automation

The current release app does not expose a command-line benchmark/export path. It is an interactive sample.

Possible automation routes:

- use UI automation only for screenshots and mode toggles
- prefer source instrumentation for numeric evidence
- keep manual profiler readings as temporary, explicitly labeled sample observations

If we modify the sample locally for capture, keep the changes separate from the original NVIDIA sample and record the commit hash used for measurements.
