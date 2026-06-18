# PTLAS Vulkan Sample Performance Execution Prompts

Source plan:

- `notes/ptlas-vk-sample-performance-capture-plan.md`

Target app:

- `C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release\vk_partitioned_tlas.exe`

Output folder:

- `notes/ptlas-vk-sample-captures/`

Goal:

- launch the NVIDIA `vk_partitioned_tlas` sample
- configure comparable modes
- capture enough data to replace article placeholders safely
- average values instead of copying a single lucky frame
- keep claims limited to what the sample proves

## Pass 0: Prepare Capture Workspace

Goal:

- create a clean local workspace for sample evidence
- record the app path and capture assumptions

Prompt:

```text
Prepare the PTLAS Vulkan sample capture workspace.

Create:
- `notes/ptlas-vk-sample-captures/`
- `notes/ptlas-vk-sample-captures/screenshots/`
- `notes/ptlas-vk-sample-captures/manual-samples.csv`
- `notes/ptlas-vk-sample-captures/averaged-summary.csv`
- `notes/ptlas-vk-sample-captures/capture-notes.md`

Initialize `manual-samples.csv` with columns:

capture_id,sample_index,timestamp_note,dynamic_instances,static_instances,changed_instances,tlas_memory_mb,tlas_scratch_mb,ptlas_memory_mb,ptlas_scratch_mb,animation_physics_gpu_ms,animation_update_instances_gpu_ms,tlas_update_gpu_ms,render_gpu_ms,compositing_gpu_ms,frame_gpu_ms,frame_cpu_ms,screenshot_path,notes

Initialize `averaged-summary.csv` with columns:

capture_id,sample_count,dynamic_instances,static_instances,total_instances,changed_instances_avg,changed_instances_min,changed_instances_max,tlas_memory_mb,tlas_scratch_mb,ptlas_memory_mb,ptlas_scratch_mb,tlas_update_gpu_ms_avg,tlas_update_gpu_ms_min,tlas_update_gpu_ms_max,render_gpu_ms_avg,render_gpu_ms_min,render_gpu_ms_max,animation_update_instances_gpu_ms_avg,notes

Do not launch the app yet.
```

Exit criteria:

- capture folder exists
- CSV files exist with headers
- capture notes file exists

## Pass 1: Launch And Baseline App State

Goal:

- launch the NVIDIA app from the release folder
- confirm the UI matches the expected default scene

Prompt:

```text
Launch the NVIDIA PTLAS sample.

Command:
Start-Process -FilePath "C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release\vk_partitioned_tlas.exe" -WorkingDirectory "C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release"

Wait until the main window is visible.

Confirm in the UI:
- Settings panel is visible
- Profiler panel is visible
- Scene size is `1000.000`
- Partitions per axis is `50`
- Self-toppling dominoes is `2000`
- Current domino count is about `169,231`
- Current static object count is about `1,219,587`
- Statistics section is expanded

Take a screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/pass1-default-ui.png`

Record notes in:
- `notes/ptlas-vk-sample-captures/capture-notes.md`
```

Exit criteria:

- app is running
- default scene values are recorded
- screenshot proves Settings and Profiler are visible

Failure handling:

- if the app opens with a different scene, do not capture performance yet
- set scene values to the target defaults and click `Regenerate scene`
- wait until regeneration completes
- record that regeneration occurred

## Pass 2: Capture Static Memory And Scratch Baseline

Goal:

- capture memory and scratch values that do not require averaging

Prompt:

```text
Read the Statistics section from the app UI.

Record:
- TLAS memory MB
- TLAS scratch MB
- PTLAS memory MB
- PTLAS scratch MB

Expected ranges:
- TLAS memory: roughly `280-290 MB`
- TLAS scratch: roughly `100-105 MB`
- PTLAS memory: roughly `315-325 MB`
- PTLAS scratch: roughly `108-112 MB`

If values are outside those ranges:
- take a screenshot
- record the values
- stop before using them in the article

Take screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/pass2-static-stats.png`
```

Exit criteria:

- memory and scratch values are recorded in capture notes
- values are in the expected range or flagged as suspicious

## Pass 3: Capture `classic_tlas_refit`

Goal:

- capture classic TLAS refit behavior for comparison

App settings:

- `PTLAS Active`: unchecked
- `Refit TLAS`: checked
- scene settings unchanged

Prompt:

```text
Configure the app for `classic_tlas_refit`.

Steps:
1. Press Stop to reset animation.
2. Uncheck `PTLAS Active`.
3. Ensure `Refit TLAS` is checked.
4. Wait 2 seconds.
5. Press Play.
6. Ignore the first 2 seconds of motion.
7. Record 10 samples over roughly 10-15 seconds.

For each sample, record one row in `manual-samples.csv`:
- capture_id = `classic_tlas_refit`
- sample_index = 1..10
- dynamic_instances
- static_instances
- changed_instances from `Updated instances`
- TLAS/PTLAS memory and scratch
- Profiler `Animation physics`
- Profiler `Animation update instances` if visible, otherwise blank / n/a
- Profiler `TLAS Update`
- Profiler `Render`
- Profiler `Compositing`
- Profiler frame GPU average
- Profiler frame CPU average
- screenshot path if a screenshot is taken for that row

Take at least one screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/classic_tlas_refit.png`
```

Exit criteria:

- 10 rows exist for `classic_tlas_refit`
- `TLAS Update` is present
- changed-instance count is not copied from a reset frame

Sanity checks:

- `TLAS Update` should be comparatively stable across changing `Updated instances`
- do not claim this is faster or slower yet

## Pass 4: Capture `ptlas_local_partition`

Goal:

- capture PTLAS where moving instances stay in their local partition

App settings:

- `PTLAS Active`: checked
- `Partition update mode`: `Always update partition`
- `Mark all dominoes dynamic in partition`: disabled/off

Prompt:

```text
Configure the app for `ptlas_local_partition`.

Steps:
1. Press Stop to reset animation.
2. Check `PTLAS Active`.
3. Select `Always update partition`.
4. Confirm `Mark all dominoes dynamic in partition` is off or disabled.
5. Wait 2 seconds.
6. Press Play.
7. Ignore the first 2 seconds of motion.
8. Record 10 samples over roughly 10-15 seconds.

For each sample, append one row to `manual-samples.csv`.

Required screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition.png`
```

Exit criteria:

- 10 rows exist for `ptlas_local_partition`
- `Animation update instances` row is visible or marked missing
- `TLAS Update` is recorded

Sanity checks:

- PTLAS memory/scratch match the static baseline
- `Updated instances` varies during motion
- do not fill touched partitions from this capture unless instrumentation exists

## Pass 5: Capture `ptlas_global_partition`

Goal:

- capture PTLAS where moving instances are routed through the global partition

App settings:

- `PTLAS Active`: checked
- `Partition update mode`: `Always move dynamic to global`
- `Mark all dominoes dynamic in partition`: unchecked

Prompt:

```text
Configure the app for `ptlas_global_partition`.

Steps:
1. Press Stop to reset animation.
2. Check `PTLAS Active`.
3. Select `Always move dynamic to global`.
4. Ensure `Mark all dominoes dynamic in partition` is unchecked.
5. Wait 2 seconds.
6. Press Play.
7. Ignore the first 2 seconds of motion.
8. Record 10 samples over roughly 10-15 seconds.

For each sample, append one row to `manual-samples.csv`.

Required screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition.png`
```

Exit criteria:

- 10 rows exist for `ptlas_global_partition`
- update and render timings are both captured

Sanity checks:

- do not call this mode better than local partition
- compare update time beside render time because global partition can reduce update cost while affecting traversal coherence

## Pass 6: Capture `ptlas_hybrid_distance`

Goal:

- capture the hybrid mode used to balance nearby trace coherence and far-field update cost

App settings:

- `PTLAS Active`: checked
- `Partition update mode`: `Update partition nearby, move to global otherwise`
- `Mode change distance`: keep current/default unless deliberately testing a threshold
- `Mark all dominoes dynamic in partition`: unchecked

Prompt:

```text
Configure the app for `ptlas_hybrid_distance`.

Steps:
1. Press Stop to reset animation.
2. Check `PTLAS Active`.
3. Select `Update partition nearby, move to global otherwise`.
4. Ensure `Mark all dominoes dynamic in partition` is unchecked.
5. Record the `Mode change distance`.
6. Wait 2 seconds.
7. Press Play.
8. Ignore the first 2 seconds of motion.
9. Record 10 samples over roughly 10-15 seconds.

For each sample, append one row to `manual-samples.csv`.

Required screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/ptlas_hybrid_distance.png`
```

Exit criteria:

- 10 rows exist for `ptlas_hybrid_distance`
- mode-change distance is recorded in notes
- update and render timings are both captured

## Pass 7: Optional Stress Capture `ptlas_global_partition_whole_cell`

Goal:

- capture the case where the global partition receives more than the currently moving instances
- use only as tradeoff evidence, not as the main article comparison

App settings:

- `PTLAS Active`: checked
- `Partition update mode`: `Always move dynamic to global`
- `Mark all dominoes dynamic in partition`: checked

Prompt:

```text
Configure the app for `ptlas_global_partition_whole_cell`.

Steps:
1. Press Stop to reset animation.
2. Check `PTLAS Active`.
3. Select `Always move dynamic to global`.
4. Check `Mark all dominoes dynamic in partition`.
5. Wait 2 seconds.
6. Press Play.
7. Ignore the first 2 seconds of motion.
8. Record 10 samples over roughly 10-15 seconds.

For each sample, append one row to `manual-samples.csv`.

Required screenshot:
- `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition_whole_cell.png`
```

Exit criteria:

- 10 rows exist if this optional capture is performed
- notes explain that this is a stress/tradeoff mode

## Pass 8: Average Manual Samples

Goal:

- convert raw manual samples into stable article-facing numbers

Prompt:

```text
Read `notes/ptlas-vk-sample-captures/manual-samples.csv`.

For each capture_id:
- verify there are 10 usable samples
- compute average, min, and max for:
  - changed_instances
  - tlas_update_gpu_ms
  - render_gpu_ms
  - animation_update_instances_gpu_ms
- verify memory and scratch values are stable
- write one row to `averaged-summary.csv`

Reject a sample if:
- it is a reset frame
- it includes shader recompilation
- it has missing profiler values required for that mode
- scene settings changed

Write rejection notes to `capture-notes.md`.
```

Exit criteria:

- `averaged-summary.csv` contains one row per completed capture mode
- rejected samples are documented
- no unverified value is invented

## Pass 9: Validate Against Expected Ranges

Goal:

- catch measurement mistakes before updating the article

Prompt:

```text
Validate `averaged-summary.csv` against expected ranges.

Expected:
- dynamic instances about `169,231`
- static instances about `1,219,587`
- total instances about `1.38M`
- TLAS memory about `280-290 MB`
- TLAS scratch about `100-105 MB`
- PTLAS memory about `315-325 MB`
- PTLAS scratch about `108-112 MB`
- changed instances varies by simulation point
- classic TLAS update timing is less sensitive to changed-instance count than PTLAS timing
- render timing is present for every mode

If any range fails:
- do not update the article
- report the suspicious field
- inspect screenshots and raw rows
```

Exit criteria:

- every article-bound value has either passed validation or is marked unusable

## Pass 9: Validate Against Expected Ranges

Goal:

- catch measurement mistakes before updating the article

Prompt:

```text
Validate `averaged-summary.csv` against expected ranges.

Expected:
- dynamic instances about `169,231`
- static instances about `1,219,587`
- total instances about `1.38M`
- TLAS memory about `280-290 MB`
- TLAS scratch about `100-105 MB`
- PTLAS memory about `315-325 MB`
- PTLAS scratch about `108-112 MB`
- changed instances varies by simulation point
- classic TLAS update timing is less sensitive to changed-instance count than PTLAS timing
- render timing is present for every mode

If any range fails:
- do not update the article
- report the suspicious field
- inspect screenshots and raw rows
```

Exit criteria:

- every article-bound value has either passed validation or is marked unusable

## Pass 11: Instrumentation Decision Gate

Goal:

- decide whether manual capture is enough or whether we need backend-scope proof

Prompt:

```text
Review remaining `capture needed` fields after manual capture.

If the article still needs backend-scope proof, create an implementation plan for instrumenting the sample.

Required instrumented fields:
- rewritten-instance count from PTLAS operation argCount
- touched-partition count
- global partition population
- native operation type/count

Do not start instrumenting unless explicitly approved.
```

Exit criteria:

- manual-capture limits are clear
- instrumentation scope is clear

## Pass 12: Final Evidence Package Review

Goal:

- ensure the evidence package is complete before using it in the article

Prompt:

```text
Review:
- `manual-samples.csv`
- `averaged-summary.csv`
- screenshots
- `capture-notes.md`
- article Evidence Snapshot

Check:
- every article number maps to a CSV field
- every CSV summary maps to raw rows
- every mode has a screenshot
- no unsupported backend-scope value was filled
- no performance claim outruns evidence

Run Hugo build.
```

Exit criteria:

- evidence package is coherent
- article builds
- remaining limitations are explicit
