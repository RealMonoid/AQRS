# AQRS — Compute Budget First / Resource Governor

**Binding from M0/v0.1.** Implementation evidence is recorded in [`MILESTONE_STATUS.md`](MILESTONE_STATUS.md). No research campaign may silently initiate hours, days or years of calibration. A theoretically exhaustive search is not a reason to ignore available compute.

## 1. Responsibility and boundary

The **Research Manager** decides *what research is scientifically worth doing*. The **Resource Governor** decides *whether it can run and how much approved compute it may consume*. It operates **before and during** each expensive trial, does not trade, and does not judge alpha. A resource stop is not a negative scientific finding.

**Rule:** No hyperparameter sweep, large walk-forward campaign, calibration, bootstrap/permutation campaign or automatic retraining without a reviewed resource estimate, explicit limits and defined termination state.

### Resource assessment for every feature proposal

Include a **Resource Governor assessment** in every new AQRS feature proposal,
including proposals in discussion. Codex prepares it using the active limits in
`configs/research.yaml` before the owner decides and before implementation.

- Estimate one-time development effort separately from additional research work.
  Say when the work recurs, such as per candidate, instrument, or campaign.
- Where relevant, report added trials, fits, folds, seeds, resamples, expected
  wall time and peak memory. Include material storage or concurrency changes.
  State the assumptions and identify values that still need measurement.
- Give a budget verdict in plain language. The proposal fits the existing budget
  on the stated evidence, exceeds it, or needs a measurement before we can tell.
  If it exceeds the budget or the estimate is uncertain, name the smallest useful
  scope reduction or bounded measurement. A proposal with zero additional
  research work needs only a short explanation of that result.

The assessment informs feature selection. Execution still requires the applicable
run preflight and existing limits.

## 2. Preflight before each campaign

1. **Count the explicit plan:** markets × datasets × candidates × parameter configurations × seeds × folds × other repeats; count baselines and extra fits. Dynamically generated searches also need a **hard maximum**. In v0.1 count at least `candidate_count × seeds × folds` plus disclosed baseline fits.
2. **Estimate cost:** run a **separately time- and memory-bounded**, representative small pilot per model family, or conservatively use the upper permitted trial budget if a trustworthy estimate is unavailable. Record fit wall time, predicted serial campaign wall time, observed peak RSS and rough dataset size. Do not assume unverified linear scaling; disclose the method and safety factor.
3. **Compare with budgets:** campaign/trial wall time, planned fit and trial counts, RAM and concurrency. If data are missing or predicted demand exceeds a binding limit, **do not start the full campaign**. Propose a clearly labeled smaller pilot or journal `REJECTED_PREFLIGHT` / `BLOCKED_RESOURCES`.
4. **Persist a plan manifest:** trial/fit counts, estimates, method, constraints, seed, configuration hash, status and any proposed reduction. No silent truncation or automatic budget increase.

### Example: the eight-year trap

Five models × 100 parameter combinations × five folds × three seeds × ten markets = **75,000 fits**. At 60 minutes each, serial runtime is **75,000 hours ≈ 8.56 years**. Preflight must reject such a plan **before** starting the full model search. Faster hardware changes the estimate but not the rule.

The current single-family pilot uses an independent synthetic matrix with the largest configured
training shape and one Ridge fit, counted in the campaign fit plan. It has a five-second upper
limit and shares the campaign deadline and sampled RSS threshold. Preflight rejects count and
configuration overages before the pilot. The estimate includes conservative startup and fit
allowances. Measured pilot time and the safety factor can raise the estimate. The memory estimate
reserves 256 MiB plus 4096 bytes per bar. These estimates are planning heuristics. Sampled CPU time sums the user and system
time observed in each worker tree. Sampling can miss work by short-lived processes.

## 3. Default limits for the first local walking skeleton

These are **technical starting defaults, not universal scientific thresholds**. The authoritative settings are under `resource_governor` in `configs/research.yaml`. Any increase must be explicit, reviewed and journaled.

| Budget | v0.1 default | Required behavior |
|---|---:|---|
| Research trials per campaign | 2 | Reject extras before start; two configured candidates form the minimal test |
| Model fits per campaign | 12 | Count folds/seeds/baselines; reject excess in preflight |
| Seeds | 1 | Do not silently add seeds |
| Parallel trials | 1 | Sequential, reproducible CPU execution |
| Trial wall time | 120 seconds | Terminate worker/process tree and journal reason |
| Campaign wall time | 300 seconds | Do not launch new work after exhaustion; terminate active work safely |
| Peak trial RSS policy | 4096 MiB | Monitor memory and enforce supported stop policy; never call monitoring a hard kernel cap |
| Missing/unreliable estimates | Fail closed | Permit only a separately approved small bounded pilot, never silently launch full plan |

**Later milestone guidelines (not automatic approvals):** technical smoke tests around 2 minutes; inexpensive screening around 5 minutes; individual model training around 15 minutes; advanced evaluations up to 60 minutes; larger validation up to 2 hours **only after separate budget approval**. Calibrate these reference values against actual hardware. Any extension must be justified and recorded.

## 4. Enforcement mechanics

- **Post-hoc timing is insufficient**: the trial must run under an external watchdog capable of terminating a model blocked inside `fit()`. An `if elapsed > limit` after the blocking call is not enforcement.
- A separately supervised worker process per trial is sufficient for v0.1. Use a **Windows-native** supervisor (such as Job Objects where suitable) and a **Linux-native** process-group/cgroup strategy behind a small adapter; terminate descendants on both systems. Monitoring with `psutil` may detect rising RAM use but is not a strict kernel memory cap.
- **Hard memory guarantee nuance:** sampled RSS is not equivalent to a kernel-enforced memory cap. If the configuration requires a strict cap, use an actually available OS mechanism (e.g. Windows Job Object memory limits, or delegated Linux cgroup v2 with ownership/permissions verified), otherwise **fail closed before the trial**. `RLIMIT_AS` is an address-space limit with different semantics from resident-memory RSS; do not mislabel it. Record the selected mechanism and unsupported platform capabilities explicitly.
- Measure wall time using a monotonic clock; record CPU time and peak RSS when measurable. Crashes or frozen processes must not block the scheduler forever.
- After a timeout, RAM stop or budget stop, bring journal/database state into a consistent terminal state. Partial results must not count as validated output.
- No silent retries, no automatic budget increases, no recursive `retrain → test → retrain` cycles. A manual retry is a **new recorded trial** with explicit lineage and separate approved budget.
- Resuming must be idempotent with respect to scientific attempt counts: a restarted process does not become a new independent piece of evidence merely through a new run ID.
- Exhausting a budget is **not** `evidence_status=REJECTED`; use `NOT_EVALUATED` or `INSUFFICIENT_EVIDENCE` as appropriate.

## 5. Separate statuses and audit trail

Execution statuses in addition to `PROPOSED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`:

- `REJECTED_PREFLIGHT`: full plan rejected due to invalid, unbounded or incompatible requirements.
- `BUDGET_EXHAUSTED`: remaining approved campaign/trial budget cannot cover pending work.
- `TIMED_OUT`: running trial was terminated for wall-time consumption.
- `MEMORY_LIMIT`: running trial stopped after a supported memory guard triggered.

`BLOCKED_RESOURCES` is a research/model adoption state, not a substitute for precise execution cause.

Persist at least `planned_fits`, `completed_fits`, `planned_trials`, `started_trials`, `estimated_wall_seconds`, `estimate_method`, `runtime_wall_seconds`, `peak_rss_mb`, `max_wall_seconds_trial`, `max_wall_seconds_campaign`, `max_memory_mb`, `stop_reason`, `auto_retry_count` (v0.1=0) per relevant campaign/trial. Never fabricate train/test metrics for skipped work.

## 6. Testable M0 acceptance cases

- **G01:** Normal two-candidate run stays within configured budgets; plan, logs and reports record planned/observed use.
- **G02:** An intentionally huge plan, e.g. 75,000 fits with pilot/default estimates, is rejected in preflight **without executing the full search**. Journal does not claim successful evaluation.
- **G03:** Artificially blocking worker is actually killed on trial timeout. Journal shows `TIMED_OUT`; no automatic retry.
- **G04:** A controlled RAM stress test causes `MEMORY_LIMIT` under the supported enforcement mode. If strict guarantees are unavailable, preflight rejects the trial before it allocates the test memory; do not endanger the host.
- **G05:** Planned trial/fit budget overages are rejected; a waiting trial is **not started** after campaign exhaustion.
- **G06:** Aborted/failed attempts remain in SQLite and never influence the final holdout. Negative evidence remains distinct from budget stops.
- **G07:** Identical inputs/limits produce the same execution plan (allowing measured runtime variation). Restarting does not create an infinite series of attempts.

Additionally, verify timeout/process-tree behavior on **native Windows and actual Linux separately**, document each OS-level memory guard, and demonstrate fail-closed preflight when a required mechanism is absent. See [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## 7. Future expansion: do not overload v0.1

**v0.4/M3:** Governor manages budget for all model families, Successive Halving, Optuna/bandit pilots and multi-stage validation. The Research Manager may **allocate** approved budgets but must never increase them autonomously. Measure research value as independently supported findings **per compute budget**, not maximum fits per second or best in-sample Sharpe.

**v0.8/M7:** Hardware/platform profiles, accuracy of resource predictions, safe resume, alerts and measured resource/quality trade-offs for real workloads, including native Windows and provider-neutral Linux server usage.

**v0.9/v1.0:** End-to-end tests must verify that a multi-year calibration estimate is rejected before launch. A correctly bounded or terminated job is a valid *Governor* outcome, not an alpha finding.

## 8. Execution scope and audit records

AQRS-A06 checks remaining time even when timing is disabled. Core data staging runs in an isolated worker after static admission and before timing/model fits; all these workers share the original campaign deadline and sampled-RSS policy. Preparation CPU/RSS is recorded separately and included in campaign totals. Source snapshot, journal/report I/O and cleanup remain outside a hard external deadline. Both pilots validate the approved configuration; their parent-side archive/report I/O also remains outside hard timeout enforcement. A new entry needs its own boundary review.

Supported estimator/calibration calls reserve the fit allowance before starting. A reserved attempt remains in `started_fits` even if fitting fails; a rejected reservation starts no fit. Keep this count separate from `completed_fits`. This protects trusted AQRS workers, not hostile Python. No global lifetime budget is invented: each manual campaign requires its own authorization, and the exposure index retains repetitions. No automatic retries or budget increases are introduced.
