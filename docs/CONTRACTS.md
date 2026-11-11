# Data, time and experiment contracts for v0.1

This is a **domain contract**, not an imposed class hierarchy. Codex may simplify implementation details but must not silently change event-time semantics. All values, reports and comments are in English; see [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## A. Synthetic market data

Each bar record contains at minimum:

| Field | Type and meaning |
|---|---|
| `bar_open_time` | UTC timestamp; inclusive start of bar interval |
| `bar_close_time` | UTC timestamp; interval end and time at which the completed bar becomes available |
| `open`, `high`, `low`, `close` | Finite positive floating values; `low <= open,close <= high` |
| `volume` | Finite number `>= 0` |
| `symbol` | e.g. `SYNTH_BTC_LIKE`, clearly identified as artificial |
| `dataset_id` | Stable identifier/data fingerprint |

For v0.1 use **one synthetic time series**; no real venue and no mandatory multi-instrument abstraction.

Scenarios:

- `null`: No deliberately planted predictable signal. An apparently positive research result may still occur by chance and must not be reported as proven real-world alpha.
- `planted_weak_signal` (optional): A clearly documented weak, causally generated relation for functional testing, not a financial discovery.

Data-quality checks: monotonically increasing unique timestamps, consistent bar interval, no negative/nonfinite prices, OHLC invariants, no NaN/Inf volume, nonempty series and documented removal of feature warm-up observations.

## B. Feature availability and targets

A feature vector `X_t` describes historical bars **up to and including `t` only**, with `available_at = bar_close_time[t]`.

**Binding v0.1 reference convention** for horizon `h` bars:

- Compute a signal immediately **after** `bar_close_time[t]`.
- Earliest OHLCV-based simulation fill: `open[t+1]` (not known ex ante).
- Exit after holding `h` bars: `open[t+h+1]`.
- Gross forward-return label: `open[t+h+1] / open[t+1] - 1`.
- For `h=3`: signal after `close[t]`, entry `open[t+1]`, exit `open[t+4]`.
- Never create missing tail labels by `fillna(0)` or forward filling.
- The v0.1 next-open fill is an **explicit modeling assumption**, not a claim that market orders can always execute at that price.

Features must not see future fill prices such as `open[t+1]`. Targets may contain such future observations only for training cases whose target horizon has already ended by the model-fit cutoff.

## C. Research folds and purging

A fold defines `train_start`, `train_end`, `val_start`, `val_end` and `label_last_required_at`.

Minimum safe rule: every training example's full target must be observable **before the validation period begins**. For the target above this requires the timestamp of `t+h+1` to precede the validation cutoff; using a larger conservative purge/gap is allowed. No training-label dependence may extend into validation.

The implementation uses a shared 12-bar warm-up. Relative volume divides the current
completed bar's volume by the preceding 12 bars' average, with zero used when the average
is zero. Rolling volatility uses the last 12 close-to-close returns. Training and validation
tails are both purged so a label's exit precedes the next interval. At a contiguous boundary
the signal's close time and the next open can share a UTC timestamp. The modeled event order
still uses the distinct next bar for execution.

Also:

- Fixed or expanding training windows and finite validation windows.
- No random cross-validation across time.
- Each transformer and model is fit using its fold's training subset only.
- Persist fold boundaries and relevant index sets in the journal.
- Reserve a final time segment (e.g. 20%, configurable) as `purpose=final_holdout_reserved`. The Research Manager must not read its performance results.

## D. Cost and decision contract

Use **illustrative** costs in basis points (`bps`; 1 bp = 0.01%) for v0.1. Config fields: `fee_bps_per_side`, `quoted_spread_bps`, `slippage_bps_per_side`.

For an immediate buy/sell referenced to the mid price, approximate **one-way cost** as:

```text
fee_bps_per_side + (quoted_spread_bps / 2) + slippage_bps_per_side
```

A fully entered and exited position incurs **two one-way costs** under symmetric assumptions. If the OHLCV reference price is not treated as mid, document a consistent alternative fill convention and **do not double-count spread**. Order-book market impact and state-dependent spreads come later with appropriate real data.

**No funding component in synthetic spot/instrument-neutral v0.1.** Later funding must be instrument-specific and only charged at actual funding events.

The early plausibility screen compares the first training window's 90th percentile absolute
target return with round-trip costs and the buffer. Passing allows evaluation. It gives no
scientific status upgrade. Costs are charged against the fixed entry notional. Momentum uses
the most recent completed close-to-close return as its score and shares the Ridge policy
threshold, holding horizon, sizing and fill assumptions.

Decision policy for v0.1:

- `flat`, `long`, `short`; short permission configurable; no leverage.
- Forecast model predicts forward returns; policy requires a direction and expected **net margin** over costs plus a configurable buffer. `flat` is a legitimate outcome.
- Avoid presenting overlapping holding periods as independent positions. Either permit at most **one open position** or use explicitly non-overlapping entry timestamps.
- Fixed documented holding period; no execution at the signal bar's close.
- Use identical fill, cost and position-sizing rules for all candidate policies and trading controls.
- The v0.1 rule is **heuristic**, not a proven optimal risk-adjusted multi-step policy.

## E. Candidate and journal contract

Each candidate has at least:

```text
candidate_id, family, version, hypothesis,
feature_set, target_horizon_bars, model_type,
config_hash, dataset_id, created_at, status
```

Minimal v0.1 candidates may be:

- `C_LAG`: linear regression using only past returns.
- `C_LAG_VOL`: same model adding past returns, relative volume and volatility.

This compares incremental feature value without a giant model search. The pair is an engineering starting point, not a preordained economic winner.

Maintain **two distinct status dimensions**:

- `execution_status`: `PROPOSED | RUNNING | COMPLETED | FAILED | CANCELLED | REJECTED_PREFLIGHT | BUDGET_EXHAUSTED | TIMED_OUT | MEMORY_LIMIT`
- `evidence_status`: `NOT_EVALUATED | REJECTED | INSUFFICIENT_EVIDENCE | RESEARCH_PROMISING | FINAL_TEST_PASSED`

`FINAL_TEST_PASSED` must **never** be set automatically in v0.1; the final holdout is reserved. A successfully executed negative run may be `execution_status=COMPLETED` and `evidence_status=REJECTED`.

Persistent SQLite experiment records contain at least:

```text
experiment_id, run_id, candidate_id, timestamp_utc,
seed, scenario, dataset_fingerprint, config_fingerprint,
code_version_or_commit_if_available,
train_intervals, validation_intervals, holdout_reserved_interval,
feature_list, model_params_json, execution_status,
evidence_status, rejection_or_failure_reason, runtime_seconds,
metrics_json, cost_model_json, artifact_paths_json
```

If practical store fold- and trade-level detail in linked tables or structured artifacts. Rejected variants retain their identity and are never overwritten silently.

## F. Research Manager v0.1

Minimum functionality: register two candidates, compute an explainable priority, choose the next, update run state and journal results.

For the first implementation, a deterministic round-robin order with a feasibility check and small exploration preference is adequate. Complex reward estimates are not justified yet; do not fabricate pseudo-probabilities.

Later priority formula (design only, **do not implement**):

```text
priority = f(research_oos_evidence, evidence_quality,
             estimated_eval_cost, uncertainty,
             exploration_quota, age_and_environment_change)
```

Only **research evidence**, never final-holdout performance, may update priority. Negative findings may reduce priority without permanently banning investigation after material market/cost changes.

## F2. Resource Governor and resource-journal contract

Normative detail: [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md). The v0.1 Research Manager must obtain governor approval **before** starting any trial.

Minimum campaign/trial record: `planned_trials`, `started_trials`, `planned_fits`, `completed_fits`, `estimated_wall_seconds`, `estimate_method`, `runtime_wall_seconds`, `peak_rss_mb`, `max_wall_seconds_per_trial`, `max_wall_seconds_per_campaign`, `max_memory_mb`, `stop_reason`, `auto_retry_count`, `preflight_status` and the relevant configuration version.

`execution_status=REJECTED_PREFLIGHT|BUDGET_EXHAUSTED|TIMED_OUT|MEMORY_LIMIT` describes **execution/resource status only**. The scientific `evidence_status` remains `NOT_EVALUATED` or `INSUFFICIENT_EVIDENCE`, never automatically `REJECTED` or `FINAL_TEST_PASSED`. Partial runs must not be reported as successful fold evaluations. Any manual resume must retain trial lineage and must not silently inflate the independent evidence count. No automatic retries in v0.1.

The Resource Governor must use a genuinely supported Windows/Linux enforcement mechanism for the active platform or reject work that requires unavailable guarantees. An RSS polling value is a measurement, not proof of strict kernel-backed RAM limiting; see [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## G. Reporting contract

Machine-readable `report.json` and readable `report.md` include:

- `run_id`, `dataset_type=synthetic`, `scenario`, `timeframe`, `horizon`, `seed` and config/data fingerprints;
- candidate list with execution and evidence statuses;
- campaign `evaluation_status` distinguishes `SCREENED_OUT`, `COMPLETED`, and `NOT_COMPLETED` independently of the process outcome. A completed economic screen can exit successfully while skipping candidate fits and simulation;
- training/validation folds and reserved final holdout;
- predictive baselines versus candidate metrics, with definitions;
- trading baselines versus candidate **gross/net** results, fees/spread/slippage, trade count, turnover and drawdown;
- explicit rationale for promising, unsuitable or inconclusive decisions;
- uncertainty, sample size, limitations and the statement **no real-world alpha has been demonstrated**.

Keep the supervised pilot's source snapshot and report together. The report and campaign journal bind the snapshot by file digests and list the installed dependency versions. The source identity identifies an execution and leaves the scientific variant lineage intact.

Core numerical results must reproduce with the same seed. Run IDs, timestamps and measured durations may vary. Define every metric's units and favorable direction.

Prediction reports add `diagnostics` to aggregate and fold metrics. Spearman
`rank_correlation` uses average ranks for ties; it is null with `rank_status`
`CONSTANT_PREDICTION`, `CONSTANT_TARGET` or `INSUFFICIENT_OBSERVATIONS` when
undefined, and otherwise `DEFINED`. Means and population standard deviations
use simple returns in JSON and bps in Markdown. No p-value, independence estimate
or economic claim follows. Reject empty, non-finite or misaligned vectors.
The training movement screen remains unchanged; a screened-out run has no
prediction diagnostics and an empty `diagnostic_exposure` list.

Each diagnostic exposure entry names its definition ID, metric, aggregate/fold
view, validation index intervals (exclusive stops) and target horizon. The parent
attempt binds the dataset, source and candidate. Preserve entries on duplicate
model attempts in both the journal and consolidated exposure index. These are
additional data views, not additional fits or independent confirmations. Current
reports remain schema 2 with additive fields; old evidence is not rewritten.

## H. Audit-compatible reporting and provenance

Current reports use `schema_version="2"`; records without it remain legacy evidence. Record source bytes/digests, available Git commit and dirty state (null when unavailable), Python/platform and installed dependencies. Source identity is separate from scientific variant identity. New metadata never repairs missing execution-time bindings in M2-E08/E09. Core workers execute their saved source snapshot.

`SCREENED_OUT` belongs only to `evaluation_status`; a completed screen is an execution success. A positive development screen may set a separate decision/boolean but keeps `evidence_status=INSUFFICIENT_EVIDENCE`. Literal holdout fields describe authorization (`authorized_reads=0`, `access_measurement=not_instrumented`), never measured access counts. Existing reservations remain binding. List zero-valued cost/buffer components without silently substituting costs or forbidding synthetic controls.

The [exposure index](../evidence/exposure.json) links definitions to attempts, data scopes and original journals. The [manifest](../evidence/manifest.json) identifies recoverable records, including SQLite backup snapshots preserving committed WAL state. Unknown historical exposure and preregistration remain explicit. These additive report fields and audit records require no database schema migration.

AQRS-A07 adds `economic_evidence` to simulations: `NO_TRADES`, `SINGLE_TRADE`
or `DESCRIPTIVE_ONLY`, always with `supports_economic_claim=false` and unknown
independent sample size. These are descriptive labels, not execution or alpha
statuses. `feasibility.scope=TRAINING_MOVEMENT_SCALE_ONLY` limits the screen's
meaning; the momentum benchmark explicitly uses an uncalibrated one-bar score.

M2-E10's `common_opportunity_trading` uses all 24 fixed UTC hours per validation
day. Each arm's net return uses the existing long-or-flat simulator, unit
notional and frozen costs; no action contributes zero. Record every hourly
action/skip case, summed incremental net bps and its mean divided by 24.
Preserve the old conditional absolute-movement fields and decision rule.
The new diagnostic cannot be used as a predeclared historical test.
