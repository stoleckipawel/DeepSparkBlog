# PTLAS Vulkan Sample Capture Notes

Target app:

`C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release\vk_partitioned_tlas.exe`

Working directory:

`C:\Users\pawel.stolecki\Documents\GitHub\vk_partitioned_tlas\_bin\Release`

Capture source plan:

- `notes/ptlas-vk-sample-performance-capture-plan.md`
- `notes/ptlas-vk-sample-performance-execution-prompts.md`

Assumptions:

- Use the default release scene unless explicitly recorded otherwise.
- Keep render resolution/window layout stable across modes.
- Record sample data from the existing UI and profiler unless instrumentation is added later.
- Treat `Updated instances` as changed dynamic instances, not rewritten PTLAS instance records.
- Keep touched partitions, rewritten instances, native operation count, and global partition population as `capture needed` until instrumented.

Expected default settings:

| Setting | Expected value |
|---|---:|
| Scene size | `1000.000` |
| Partitions per axis | `50` |
| Self-toppling dominoes | `2000` |
| Dynamic instances | about `169,231` |
| Static instances | about `1,219,587` |

Expected sanity ranges:

| Field | Expected range |
|---|---:|
| TLAS memory | `280-290 MB` |
| TLAS scratch | `100-105 MB` |
| PTLAS memory | `315-325 MB` |
| PTLAS scratch | `108-112 MB` |

Pass log:

- Pass 0: capture workspace prepared.
- Pass 1: launched NVIDIA `vk_partitioned_tlas` sample from `_bin\Release`.
  - Process: running and responsive.
  - Screenshot: `notes/ptlas-vk-sample-captures/screenshots/pass1-default-ui.png`.
  - Settings panel: visible.
  - Profiler panel: visible.
  - Statistics section: expanded.
  - Observed scene size: `1000.000`.
  - Observed partitions per axis: `50`.
  - Observed self-toppling dominoes: `2000`.
  - Observed current domino count: `169,231`.
  - Observed current static object count: `1,220,175`.
  - Note: static object count differs slightly from the earlier expected `~1,219,587`, but remains in the expected `about 1.2M` range. Use this run's exact value for this capture session.
- Pass 2: captured static acceleration-structure memory and scratch baseline.
  - Screenshot: `notes/ptlas-vk-sample-captures/screenshots/pass2-static-stats.png`.
  - Observed TLAS memory: `285.68 MB`.
  - Observed TLAS scratch: `103.97 MB`.
  - Observed PTLAS memory: `320.18 MB`.
  - Observed PTLAS scratch: `110.24 MB`.
  - Sanity check: all four values are inside the expected ranges for this capture setup.
- Pass 3: captured `classic_tlas_refit`.
  - Settings: `PTLAS Active` unchecked, `Refit TLAS` checked.
  - Raw samples: `notes/ptlas-vk-sample-captures/manual-samples.csv`.
  - Averaged summary: `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/classic_tlas_refit.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/classic_tlas_refit-readout-contact-sheet.png`.
  - Samples recorded: `10`.
  - Changed instances range: `4011-5084`.
  - TLAS update range: `0.656-0.706 ms`.
  - TLAS update average: `0.670 ms`.
  - Sanity check: `TLAS Update` remained comparatively stable while `Updated instances` changed.
  - Note: values are sample UI/profiler readings and should stay separate from SparkleEngine evidence.
- Pass 4: captured `ptlas_local_partition`.
  - Settings: `PTLAS Active` checked, partition mode `Always update partition`.
  - `Mark all dominoes dynamic in partition`: off/disabled.
  - Raw samples: `notes/ptlas-vk-sample-captures/manual-samples.csv`.
  - Averaged summary: `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition-readout-contact-sheet.png`.
  - Samples recorded: `10`.
  - Changed instances range: `5-206`.
  - `Animation update instances` row: visible, average `0.017 ms`.
  - `TLAS Update` range: `0.489-0.573 ms`.
  - `TLAS Update` average: `0.537 ms`.
  - Sanity check: PTLAS memory/scratch matched the static baseline.
  - Note: touched partitions and rewritten PTLAS instance records are not filled from this UI capture.
  - Comparability warning: `Updated instances` was much lower than the classic TLAS pass. Treat this pass as preliminary until reset/sample-window parity is validated.
- Pass 5: captured `ptlas_global_partition`.
  - Settings: `PTLAS Active` checked, partition mode `Always move dynamic to global`.
  - `Mark all dominoes dynamic in partition`: unchecked.
  - Raw samples: `notes/ptlas-vk-sample-captures/manual-samples.csv`.
  - Averaged summary: `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition-readout-contact-sheet.png`.
  - Samples recorded: `10`.
  - Changed instances range: `3-173`.
  - `Animation update instances` row: visible, average `0.018 ms`.
  - `TLAS Update` range: `0.464-0.601 ms`.
  - `TLAS Update` average: `0.551 ms`.
  - Render range: `1.189-1.362 ms`.
  - Render average: `1.233 ms`.
  - Sanity check: update and render timings were both captured; do not compare this mode by update timing alone.
  - Comparability warning: `Updated instances` was much lower than the classic TLAS pass. Treat this pass as preliminary until reset/sample-window parity is validated.

Capture correction needed:

- Redo PTLAS policy captures with an explicit reset verification screenshot before playback.
- After pressing Stop, confirm `Updated instances: 0`.
- After pressing Play, start sampling from a comparable animation interval, preferably when `Updated instances` is in the same order of magnitude across modes.
- If PTLAS modes naturally report a different `Updated instances` definition, document that before comparing timings.

Capture correction completed:

- Verified reset screenshot before rerun: `notes/ptlas-vk-sample-captures/screenshots/retake-reset-verification-pre.png`.
- Confirmed reset state showed `Updated instances: 0`.
- Correct control sequence:
  - middle toolbar button: stop/reset
  - left toolbar button: play after reset
- Added preferred rerun capture IDs:
  - `ptlas_local_partition_verified`
  - `ptlas_global_partition_verified`
- Local verified reset evidence:
  - Reset screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition_verified-reset.png`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition_verified.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/ptlas_local_partition_verified-readout-contact-sheet.png`.
  - Changed instances range: `760-16157`.
  - Changed instances average: `8949.7`.
  - `TLAS Update` average: `1.042 ms`.
  - Render average: `1.270 ms`.
- Global verified reset evidence:
  - Reset screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition_verified-reset.png`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition_verified.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/ptlas_global_partition_verified-readout-contact-sheet.png`.
  - Changed instances range: `760-16141`.
  - Changed instances average: `8978.4`.
  - `TLAS Update` average: `1.059 ms`.
  - Render average: `1.407 ms`.
- Use the `*_verified` PTLAS rows for any article-facing sample comparison.
- Keep the earlier `ptlas_local_partition` and `ptlas_global_partition` rows only as discarded preliminary captures.
- Pass 6: captured `ptlas_hybrid_distance`.
  - Settings: `PTLAS Active` checked, partition mode `Update partition nearby, move to global otherwise`.
  - `Mark all dominoes dynamic in partition`: unchecked.
  - Mode change distance: `100.000`.
  - Reset screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_hybrid_distance-reset.png`.
  - Primary screenshot: `notes/ptlas-vk-sample-captures/screenshots/ptlas_hybrid_distance.png`.
  - Readout contact sheet: `notes/ptlas-vk-sample-captures/screenshots/ptlas_hybrid_distance-readout-contact-sheet.png`.
  - Raw samples: `notes/ptlas-vk-sample-captures/manual-samples.csv`.
  - Averaged summary: `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Samples recorded: `10`.
  - Changed instances range: `788-16132`.
  - Changed instances average: `9008.0`.
  - `Animation update instances` row: visible, average `0.019 ms`.
  - `TLAS Update` range: `0.637-1.383 ms`.
  - `TLAS Update` average: `1.060 ms`.
  - Render range: `1.165-1.416 ms`.
  - Render average: `1.291 ms`.
- Pass 8: averaged manual samples for article-facing use.
  - Summary file rewritten: `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Accepted capture IDs:
    - `classic_tlas_refit`
    - `ptlas_local_partition_verified`
    - `ptlas_global_partition_verified`
    - `ptlas_hybrid_distance`
  - Rejected capture IDs:
    - `ptlas_local_partition`
    - `ptlas_global_partition`
  - Rejection reason: preliminary PTLAS captures were sampled from a late animation window; `Updated instances` was much lower than the verified reset captures and not comparable.
  - Memory/scratch stability check: all accepted rows used one stable set, `TLAS 285.68 MB`, `TLAS scratch 103.97 MB`, `PTLAS 320.18 MB`, `PTLAS scratch 110.24 MB`.
  - Classic TLAS note: `Animation update instances` is `n/a` because the row is not emitted for that mode; it was not required for acceptance.
  - No reset frames, shader recompilation frames, or scene-setting changes were included in the accepted summary rows.
- Pass 9: validated averaged summary against expected ranges.
  - Validation result: passed for all article-bound values in `notes/ptlas-vk-sample-captures/averaged-summary.csv`.
  - Dynamic instances: `169,231`, within expected range.
  - Static instances: `1,220,175`, slightly different from the earlier planning value but within the expected about-1.2M range for this run.
  - Total instances: `1,389,406`, within expected about-1.38M range.
  - Memory/scratch: all accepted rows stayed at `TLAS 285.68 MB`, `TLAS scratch 103.97 MB`, `PTLAS 320.18 MB`, `PTLAS scratch 110.24 MB`.
  - Render timing: present for every accepted capture mode.
  - Changed-instance timing note: classic TLAS refit stayed in a narrow `0.656-0.706 ms` update range while `Updated instances` varied from `4011-5084`; PTLAS verified policy captures show wider update-time movement over a much wider `Updated instances` span. Treat this as sample behavior, not a universal sensitivity proof.
  - No suspicious article-bound value was found.
- Pass 12: final evidence package review.
  - `manual-samples.csv`: accepted summary rows map to `10` raw samples each.
  - `averaged-summary.csv`: contains only article-facing accepted modes.
  - Screenshots: each accepted mode has a primary screenshot; PTLAS modes also have reset screenshots and readout contact sheets.
  - Article Evidence Snapshot: still uses placeholders for detailed measurements, so it does not yet claim unsupported backend-scope values.
  - Backend-scope limitation remains explicit: touched partitions, rewritten-instance count, native operation type/count, and global partition population still require instrumentation.
  - Hugo build: passed with warnings unrelated to this article's evidence package.
