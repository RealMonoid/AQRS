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

### Qualified Spot activity inputs

The data preparation path validates each complete daily one-minute Spot archive
and its published SHA-256. It normalizes pre-2025 millisecond and 2025-onward
microsecond timestamps to the same UTC bar boundary. Missing, duplicate,
out-of-order, foreign-day or wrong-unit rows are rejected. The M1 legacy wrapper
retains its BTCUSDT/microsecond contract, and January 6, 2026 remains rejected
before archive access by the supported entries.

`activity.csv` aligns `bar_open_time` and `available_at` with the corresponding
OHLCV bar. Its fields are `quote_volume`, integer `trade_count`,
`taker_buy_base_volume` and `taker_buy_quote_volume`. Require finite nonnegative
values, exactly representable trade counts below 2**53, and taker-buy volumes
no greater than their corresponding total volumes. Completed activity is known
at bar close only; it does not reveal within-bar event order or quotes.

Per-symbol manifests bind the archive digests, OHLCV identity and both output
file digests. A completed preparation is `qualified=true`,
`data_role=DEVELOPMENT`, `research_ready=false`, `evidence_status=NOT_EVALUATED`.
This is a quality result, not research admission. A failed overall attempt may
contain an individually qualified first symbol; consumers must check the
top-level completion receipt before treating the requested scope as complete.

## A2. External synthetic blind-test input (AQRS-B01)

This contract is frozen before external payload delivery and is independent of
the market importers and reserved market day.

- Deliver one flat directory, `artifacts/blind-test/inbox/`, containing exactly
  `manifest.json` and its declared CSV files. Each delivery contains at most 16
  datasets. Identifiers start at D001 and continue without gaps across deliveries,
  using the existing three-digit format through D999. Replace the inbox only
  after the preceding delivery's last verdict has been published. No archives,
  subdirectories, links, executables,
  generation code, labels, seeds, effect counts, descriptive filenames or keys.
- CSV: UTF-8 without BOM, comma separator, decimal point, LF or CRLF, exactly
  `timestamp_utc,open,high,low,close,volume` as the required header prefix. The
  optional suffix is defined below. No index, blank rows,
  comments, missing values, NaN or infinity. Finite positive prices; finite
  nonnegative volume; `low <= open,close <= high`. Gaps between previous close
  and next open are permitted. Prices represent synthetic mid prices.
- Timestamps: exactly `YYYY-MM-DDTHH:MM:00Z`, denoting bar OPEN. All bar values
  become available 60 seconds later. Use an artificial calendar wholly in year
  2000, starting at 00:00 UTC, with 30 to 60 complete consecutive UTC days
  (43,200 to 86,400 rows). Strict increasing one-minute cadence, no gaps or
  duplicates. Prefer 60 days for precision without adapting hidden effects to
  the search. Volume uses arbitrary consistent units.
- Maximum CSV: 16 MiB; manifest: 64 KiB; total CSV payload: 256 MiB.
  No automatic repair, sorting, resampling, filling or retry.
- The JSON manifest has exactly these keys, with consecutive dataset entries,
  integer counts and lowercase SHA-256 over the exact delivered CSV bytes:

```json
{
  "schema": "aqrs.external-synthetic-minute.v1",
  "dataset_type": "synthetic",
  "source": "external_blind",
  "timezone": "UTC",
  "bar_seconds": 60,
  "price_reference": "mid",
  "datasets": [
    {
      "id": "D001",
      "file": "D001.csv",
      "sha256": "<64 lowercase hexadecimal characters>",
      "rows": 86400,
      "start_utc": "2000-01-01T00:00:00Z",
      "end_utc": "2000-02-29T23:59:00Z"
    }
  ]
}
```

The producer sends the owner a SHA-256 commitment to the exact sealed solution
bytes before delivery. The owner retains both outside this inbox. Do not send
the solution, its location, generator notes or hints to AQRS. Reveal and verify
the commitment only after blind reports are frozen and published. CSV digests
establish transport consistency, not producer authenticity.

Admission requires the next ascending identifier and its published start
reservation. The preceding dataset's verdict must already be published. The
runner checks directory names and manifest declarations. It opens and inspects
the file type and size of only the authorized current CSV, after its declared
digest matches the approved digest. Links and Windows reparse points are rejected
on that turn. Its header, numbers, open/high/low/close relationships, cadence,
complete days, endpoints and row count are then validated. Sixteen files with
the individual 16 MiB limit preserve the 256 MiB delivery limit without probing
later files. The manifest digest and identifier range stay fixed until the
delivery is complete. Invalid manifest metadata rejects admission. An invalid
current CSV yields an incomplete dataset and an explicit gap. Reports carry
`dataset_type=synthetic`, `source=external_blind`, `market_evidence=false`.
The open rehearsal uses its own directory and `source=internal_open`; it never
reads the inbox. Data delivery alone is not run authorization.

The external sequence has one active dataset. The next CSV becomes eligible
after the current dataset's immutable verdict, short summary and gap ledger
are published together. A missing required artifact makes the verdict
`NOT_EVALUABLE`. A later correction is a new dated record naming the dataset
after which it arose and the original verdict digest. The original verdict and
evidence remain in place. Budget approval and worker time apply per dataset.

### Optional minute order flow

Append any subset of `buy_volume,sell_volume,trade_count` in that order, with
each chosen column populated on every row. Full header:

```text
timestamp_utc,open,high,low,close,volume,buy_volume,sell_volume,trade_count
```

`buy_volume` and `sell_volume` are executed volumes classified by aggressor
side within the minute, in the same units as `volume`. They are finite and
nonnegative. Each is at most `volume` and, when both are present, their sum
equals `volume`, with relative tolerance `1e-9` and zero absolute tolerance.
`trade_count` is the total number of executions in the minute. Use 1–16 ASCII
digits representing an integer from 0 through `2**53 - 1`. Omit unavailable
columns from the header. All aggregates become available with the completed bar.

Admission validates all supplied fields and binds the complete CSV to its
manifest digest. The search worker stages validated activity with OHLCV and
records the available fields before registering the [fixed rules](RESEARCH_PROTOCOL.md#11-aqrs-b01-frozen-blind-search-procedure).
An absent field selects its defined OHLCV fallback rules. The manifest schema,
cadence and byte limits apply to every allowed header.

### Deferred event input estimates

Single trades and best bid/ask quotes require distinct event contracts and a
separately authorized implementation. For ordered local synthetic CSVs, estimate
4–8 engineering hours for trade prints aggregated to minutes, or 8–16 hours
for quote validation and aggregation. Trades need event timestamps, stable
ordering, price, size and documented aggressor side. Quotes also need coherent
bid/ask state, same-time ordering and rules for stale quotes and minute-boundary
sampling. Both estimates include a bounded importer, validation and tests.
Event-level simulation, depth reconstruction and vendor integration are
separate scopes.

Illustrative 60-day storage, before staging or output: 100 trades/minute gives
8.64 million rows at 64–100 bytes (0.55–0.86 GB). Ten quote updates/second gives
51.84 million rows at 80–120 bytes (4.15–6.22 GB). Both sizing scenarios exceed
the 16 MiB minute CSV cap. A future pilot
could use one streaming worker, at most 100,000 events and 16 MiB, 60 seconds
and 512 MiB observed RSS, with zero trials or fits. Measure rows/second and peak
RSS before proposing full-run time, storage or budget. No event path is enabled.

### AQRS-B01 evidence field dictionary

This dictionary describes the machine evidence for one synthetic dataset.
CSV means comma-separated values, with a header and UTF-8 text encoding.
JSON means JavaScript Object Notation. JSON Lines has one JSON object per line.
UTC is Coordinated Universal Time. SHA-256 is Secure Hash Algorithm with a
256-bit digest, rendered as 64 lowercase hexadecimal characters. A basis point
(`bps`) is 0.01 percentage points. A MiB is 1,048,576 bytes. A Git revision is
the full 40-character hexadecimal commit identifier. Fields with timestamps
use UTC; bar timestamps use `YYYY-MM-DDTHH:MM:SSZ`. Null JSON values and blank
feature CSV cells indicate an unavailable value. A reference such as
`report.json#/results/0` identifies the first result using a JSON Pointer.

**Feature table (`features.csv`).** One row per input candle. Returns are
calculated from the current and earlier completed candles. None of these
columns uses the next open.

| Field | Meaning and time reference | Unit and allowed values |
|---|---|---|
| `bar_index` | Input row position at the candle | Integer, zero-based |
| `bar_open_time`, `available_at` | Candle start and completed information time, 60 seconds later | UTC timestamps |
| `partition` | Row use in the frozen split | `warmup`, `calibration`, `evaluation` |
| `return1`, `return5`, `return20` | Current close relative to close 1, 5, 20 minutes earlier | Basis points, signed number or blank |
| `relative_volume` | Current volume divided by mean of the preceding 20 completed minutes | Ratio, nonnegative or blank; zero if preceding mean is zero |
| `range_bps` | Current high minus low, divided by current close | Basis points, nonnegative |
| `close_location` | Current close minus low, divided by high minus low | Ratio, 0 to 1; 0.5 for a flat candle |
| `buy_share` | Current buy volume divided by total volume | Ratio, nonnegative, blank if absent, zero at zero volume; input tolerance applies |
| `sell_share_change20` | Current sell share minus its preceding 20-minute mean | Signed ratio or blank; zero-volume share is zero |
| `relative_trade_count20` | Current trade count divided by its preceding 20-minute mean | Nonnegative ratio or blank; zero if preceding mean is zero |

**Events and controls (`CANDIDATE-opportunities.csv`).** Each row is one
eligible signal time for the candidate in the file name.

| Field | Meaning and time reference | Unit and allowed values |
|---|---|---|
| `signal_index`, `available_at` | Signal candle index and close time | Zero-based integer and UTC timestamp |
| `entry_at`, `exit_at` | Reference opens one and four minutes after the signal candle opens | UTC timestamps |
| `event` | The registered rule fires at the signal close | Integer 0 or 1 |
| `complement`, `parent_a`, `parent_b` | Control membership at the same close; complement is the rule's non-events, parents are the first or second condition alone | 0 or 1; parent columns only for conjunctions |
| `evaluation_day`, `utc_band` | Join keys for events and controls in the same evaluation day and eight-hour UTC band | Zero-based day; band 0, 1 or 2 |
| `complement_matched`, `parent_a_matched`, `parent_b_matched` | Both groups exist in the row's day and band for this comparison. Use the event and control flags to select members | 0 or 1; parent flags only for conjunctions |
| `gross_long_bps`, `candidate_net_bps` | Observed forward return between entry and exit; candidate return after costs, with zero for flat decisions | Signed basis points |

**Structured records.** The tables below specify field families shared across
files. Each row applies to the named fields wherever they occur.

| Fields | Meaning and time reference | Unit and allowed values |
|---|---|---|
| `schema`, `source`, `dataset_type`, `market_evidence` | Record version and data provenance | Version string; `external_blind` or `internal_open`; `synthetic`; `false` |
| `dataset_id`, `attempt_id`, `candidate_id`, `candidate_ids`, `registered_candidates`, `claimed_candidates`, `untested_candidates`, `out_of_rehearsal_scope` | Dataset, run and candidate identities and recorded subsets | Identifiers or arrays; `D001`–`D999`, `AQRS-B01-...`, `S01`–`S12`, `P01`–`P12`, `T01`–`T06` |
| `file`, `path`, `bytes`, `sha256`, `*_sha256`, `source_hashes`, `verified_artifacts`, `artifacts` | Evidence identity at the corresponding checkpoint; file records contain base name, byte count and digest; maps key records by file | Repository-relative or run-relative name, integer bytes, digest or map; verdict/start hashes cover canonical JSON |
| `dataset_sha256`, `manifest_sha256`, `bars_sha256`, `summary_sha256`, `gaps_sha256` | Exact bytes of the selected input CSV, delivery manifest, staged array, published summary and published gap ledger | SHA-256 digests |
| `plan_sha256`, `start_sha256`, `previous_verdict_sha256`, `verdict_sha256`, `registration_sha256`, `owner_token_sha256`, `approval_sha256` | Canonical JSON digests of the frozen plan, published start, previous/original verdict, registered settings, local ownership token and owner approval | SHA-256 digest or null where no predecessor or registration exists; canonical JSON uses sorted keys, escaped non-ASCII characters and the serializer in `aqrs.storage` |
| `created_at`, `recorded_at`, `started_at`, `stopped_at`, `finished_at`, `closed_at`, `timestamp` | When the corresponding record or stage was created, started or ended | UTC timestamp |
| `source_revision`, `registration_revision`, `verdict_revision`, `admission_base_revision`, `revision` | Code, candidate publication, verdict, preceding sequence or execution Git commit | Full Git revision or null when unavailable |
| `execution_source` | Source snapshot at preparation; `files`, `source_id`, `git.commit`, `git.dirty`, `python`, `platform`, `dependencies` identify exact source and runtime | File/digest map, digest, commit, Boolean, strings, package-version map |
| `dataset`, `input_files`, `delivery` | Selected manifest entry, verified input identities, and delivery commitment; `verified` denotes bytes actually read and validated | File records and the input schema above; delivery has `manifest_sha256`, `first_dataset_id`, `last_dataset_id` |
| `plan`, `configuration`, `approval`, `budget`, `costs` | Frozen parameters, effective settings, owner authorization, resource limits and transaction cost assumptions before outcomes | Named settings in the versioned configuration; counts are integers, durations in seconds, storage bytes or MiB as named, costs in basis points; the approval includes the dataset and plan digests, trial count, wall limit and instruction |
| `planned_trials`, `planned_fits`, `predictive_model_fits`, `resamples`, `parallel_trials`, `auto_retry_count`, `estimated_wall_seconds`, `estimated_run_storage_bytes`, `memory_estimate_mb`, `limits`, `estimate_method`, `trial_count_exception` | Admission estimates and approved bounds before payload work | Nonnegative counts or seconds, bytes, MiB, configuration object, text, Boolean |
| `prepared`, `evaluation`, `parameters`, `cutoffs`, `train_start`, `train_end`, `evaluation_start`, `evaluation_end`, `calibration_fits`, `activity_columns`, `feature_table` | Training-only thresholds and split fixed in preparation. Cutoff pairs use the feature units above. Split ends are exclusive | Lower/upper quantile pair or null per feature, row indexes, count 6–9, column names, file record |
| `rule`, `full_space`, `full_search_space`, `hypothesis`, `order`, `controls`, `available_at`, `entry`, `exit`, `measurement_rule`, `metrics`, `reason`, `budget_allocated_seconds`, `budget_consumed_seconds` | Preregistered mechanical conditions, list/order and provenance before outcomes | Rule terms are feature and tail indexes; text hypothesis/timing; zero-based order; named control arms; null metrics, `PENDING` decision, numeric seconds |
| `execution_status`, `complete`, `started`, `stop_reason`, `runtime_wall_seconds`, `sampled_cpu_seconds`, `peak_rss_mb`, `started_trials`, `started_fits`, `completed_fits`, `indexed_artifact_bytes` | Lifecycle and observed use in preparation, worker or final checkpoint | Named state such as `PREPARING`, `AWAITING_PUBLICATION`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `TIMED_OUT`, `MEMORY_LIMIT`, `BUDGET_EXHAUSTED` or `REJECTED_PREFLIGHT`; Booleans; text/null reason; seconds, observed MiB, counts, bytes |
| `results`, `trials`, `resource`, `preparation`, `result`, `candidate_resolution`, `untested_candidate_count` | Ordered result rows, observed worker receipts and unregistered-stop state | Arrays/objects, execution receipt fields above, `NOT_REGISTERED` when appropriate, count |
| `mechanical_rule`, `decision`, `effect_claimed`, `rationale`, `interpretation`, `uncertainty_assumption`, `parent_gate_failures` | Measured rule, outcome classification and reasons after evaluation | Feature/operator/threshold clauses; `NOT_EVALUATED`, `INSUFFICIENT_COVERAGE`, `UNSTABLE`, `BELOW_THRESHOLD`, `NO_INCREMENTAL_EVIDENCE` or `EFFECT_CLAIMED`; Boolean or null; English text; control-to-gate lists |
| `contrasts`, `all_opportunity_net`, `estimate_bps`, `interval_bps`, `conditional_event_gross_bps`, `no_trade_bps`, `round_trip_cost_bps` | Group differences and candidate net result across evaluation opportunities | Basis points; signed estimates, interval pairs or null; no-trade value is zero |
| `strata`, `day`, `band`, `events`, `controls`, `matched`, `difference_bps`, `matched_events`, `matched_controls`, `eligible_opportunities`, `event_count`, `skipped_opportunities` | Counts and comparison differences per day/band and candidate | Indexes, nonnegative counts, Boolean, basis points when matched |
| `blocks`, `block_values_bps`, `block_ids`, `daily_values_bps`, `half_counts`, `half_means_bps`, `coverage_pass`, `stable`, `excludes_zero`, `passes` | Uncertainty calculation and gates on completed evaluation blocks | Counts, index lists, signed basis point arrays/maps or null, Booleans |
| `opportunity_file`, `opportunity_sha256`, `opportunity_bytes`, `preregistration`, `*_artifact`, `feature_table` | Links to individual checksummed evidence files | File names, digests, byte counts, file-record objects |
| `status`, `model_candidate_count`, `columns`, `records`, `fold`, `prediction`, `actual` | Model-prediction evidence for each evaluation candle/fold | Current rule plan emits `NOT_APPLICABLE`, count 0 and empty records. A model record would name a fold and include prediction and observed target in identical declared units. |
| `stage`, `code`, `item`, `gap_count` | When and why evidence is incomplete; `item` names its file, candidate or state | Phase and reason strings, count; includes `MISSING_EVIDENCE`, `CHANGED_EVIDENCE`, `INCOMPLETE_EXECUTION` and execution stop states |
| `verdict`, `facts`, `completed_by_kind`, `best`, `estimate_basis_points`, `interval_basis_points`, `planned_budget`, `evidence` | Final eligibility and traced summary statistics after terminal checks | `EVALUABLE` or `NOT_EVALUABLE`; counts by rule type, measurements in basis points or absent, budget object and JSON Pointer references |
| `corrects_dataset_id`, `after_dataset_id`, `verdict_sha256`, `note` | Separate correction naming its target and last published dataset at recording | Dataset identifiers, original verdict digest, English note |
| `comparisons`, `expected`, `recomputed`, `opportunity_rows_match`, `matches` | Read-only replay of two measured candidates after publication, using registered costs and comparing every opportunity row | Array with candidate and pointer; two comparable measurement objects and Boolean equality |

**File map.** `search-plan.json` contains the frozen plan and source bindings.
`registration.json` contains the selected dataset, preparation, budget and
artifact bindings. `preregistration.jsonl` contains one pending rule row per
candidate. `preparation.json` and `CANDIDATE-result.json` contain worker receipts
and measured results. `run-manifest.json` indexes evidence and lifecycle use.
`report.json` contains the dataset's provisional technical outcome. `terminal.json`
records completion of execution and expected evidence identities. The published
`DNNN-start.json`, `DNNN-verdict.json`, `DNNN-gaps.jsonl`, `DNNN-summary.txt` and
`Cnnnnnn-correction.json` are the ordered sequence, its short traced summary and
any later corrections. The local `gaps.jsonl` records each gap as it occurs.
`bars.npy` is a NumPy binary array with open time as seconds since 1970 UTC,
then open, high, low, close, volume and optional activity in input-column order.
Absent activity is represented by an unavailable numeric marker. The snapshot
and ledger supply the inputs for read-only replay. `report.md` mirrors the
technical report, and `research.sqlite3` is the local attempt journal described
in the candidate and journal contract below.

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

## F3. Structured next-question selection: format only

AQRS-W01-P00 supplies a format and five public examples, not a selector or
research authorization. The machine contract is
[`research_selection.schema.json`](../configs/research_selection.schema.json).
The single [public question registry](../examples/research_selection_questions.json)
is shared by all [five cases](../examples/research_selection_cases.json).
Selector implementation waits for workflow questions per run, central attempt
accounting and general data locks. Research remains stopped.

### Ownership of fields

| Object | Fields and authority |
|---|---|
| Central question registry | `question_id`, `state`, `evaluation_rule_id`, `current_action_id`, `blocks`, and complete `outcome_actions`. Only the trusted registry defines or changes these. |
| Evaluation rule | ID/revision, separate `known_answer` and `null_case` qualification records, optional registered `qualification_task_id`. Each test records status, tested revision and evidence reference. |
| Trusted request envelope | Registry/policy/state identity, remaining time and admitted plans. Cost bounds and admission receipts come from preflight/history, not proposal self-ratings. |
| Proposal | Exactly `proposal_id`, `question_id`, `plan_id`. Extra fields, including outcome maps, scores, qualification claims or costs, invalidate the request. |
| Response | `SELECT`, `QUALIFY_RULE`, `STOP` or `REJECT_INPUT`, identities, selected proposal or qualification task, and a fixed reason code. STOP/rejection carry neither selection. |

The orchestrator supplies the trusted envelope and registry separately from
proposals. Schema validation proves structure, not receipt truth, cost adequacy
or trusted origin. Later code must bind records to the actual rule revision,
source, permitted data scope, attempt history and remaining budget. Reject
generator-supplied replacements. IDs must be unique within each namespace;
resolve every reference, match registry revisions, match workflow-plan targets
to questions and qualification-plan targets to rules. Missing, duplicate, stale
or conflicting references reject the request before ranking. Canonical action
IDs denote distinct next decisions; aliases earn no credit. Descriptions and
public case notes never enter ranking.

### Qualification and outcome meaning

Both known-answer and null-case checks must be `PASSED` for the exact rule
revision and applicable scope. `FAILED`, `NOT_RUN`, an unresolvable receipt or
a revision/scope mismatch makes the proposal unselectable. No default true
value or qualification inferred from prose is allowed. A changed rule requires
new qualification. The registry maps the four complete outcomes `SUPPORTED`,
`REFUTED`, `INCONCLUSIVE`, `EXECUTION_ERROR` to actions. The registered evaluator
must define disjoint, exhaustive, executable outcome conditions before use.
These outcomes concern the workflow question. A proposal cannot add conditions
or mappings; technical failure is not scientific evidence.

An otherwise admissible, decision-relevant proposal with an unqualified rule
first requires its registered, ready, affordable engineering qualification
task: return `QUALIFY_RULE`. Fixed known-answer/null checks judge that task;
the unqualified rule cannot certify itself. A failed check for the current rule
revision is terminal in this first policy: do not return its qualification task
again automatically. Correction creates a new revision with fresh qualification
records; an unchanged retry needs separate recorded authority and is outside this
policy. Without an admitted qualification task, keep the
proposal ineligible and consider independent work. Only qualify rules referenced
by relevant current proposals; do not launch a qualification sweep.

### Proposed deterministic policy, not yet implemented

1. Reject malformed/inconsistent inputs. Apply scope, data, variant and resource
   admission before ranking. `blocks` records verified dependencies, not a
   proposal's importance claim.
2. For OPEN questions, binary relevance is 1 exactly when the three substantive
   outcomes map to at least two distinct actions, with at least one differing
   from the current action; otherwise it is 0. Exclude `EXECUTION_ERROR`.
   Count a question once; duplicate wording/outcomes add no relevance.
3. Ready qualification tasks have priority as above. Among them use blocking
   question first, smallest bounded wall time next, then task ID.
4. Among admitted proposals with qualified rules and relevance 1, use blocking
   question first, smallest bounded wall time next, then lexicographically
   smallest proposal ID. Array order has no priority meaning.
5. Return `STOP` when no proposal or prerequisite qualification task qualifies.
   Use `NO_DECISION_CHANGING_PROPOSAL` if no OPEN question in the request has
   relevance 1; otherwise `NO_ADMISSIBLE_WORK`. Never invent work to continue.
   Selection is a recommendation, not a launch: recheck actual admission at use.

Known limitation `BINARY_RELEVANCE_COST_BIAS`: a cheap less important question
can repeatedly displace an expensive important question of equal binary
relevance and blocking status. Public case 05 exposes this behavior. Binary
relevance is not expected scientific utility. Do not invent probabilities or
silently add importance weights. Improvements require a new policy version
and evidence against the fixed-order baseline under the same total budget.

### Public examples and external freeze

The public cases file is a reviewer wrapper. Validate each `request` separately:
01/03/04/05 are structurally valid; 02 deliberately adds a forbidden proposal
field. `expected_response` is a specification, never a selector input. The
wrapper and registry label qualification receipts and costs as public assumed
inputs. No evaluator, qualifier or selector ran. `PUBLIC_ASSUMPTION` references
are not evidence and cannot admit real work. These cases cover blocking priority,
central mapping protection, qualification priority, STOP and cost bias. They
do not establish independent selection quality or full implementation coverage.
Later tests must also cover ties/order invariance, failed/stale qualifications,
missing references, budget exhaustion, blocked tasks and preserved research locks.

Before the owner's hidden test, freeze executable, schema, policy, registry
interface, budget, fixed-order comparison and scoring/release protocol. This
format delivery is not an executable freeze. The owner retains encrypted cases,
answers and scoring outside agent-accessible storage and runs the test while
Codex is inactive. Only the owner-supplied SHA-256 of the exact encrypted bundle
belongs in the repository: no bundle, key, location, generator, secret seed or
answer. No checksum is supplied yet; do not invent one or request secret contents.
The frozen program receives only its request and trusted registry; expected
answers stay with the scorer. Cases/results used to revise a policy become
development exposure; a new independent claim needs fresh hidden cases. The
owner may release results afterward. Another local folder/chat is not isolation.

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

### Prospective retention selected from the research decision

Before an authorized comparison, the existing Test Card names the question,
required evidence, storage estimate and stop rule. For paired forecast-loss
or dependence analysis, retain aligned forecast-origin timestamps, target
availability, horizon, fold/block IDs and candidate/control losses (or the
forecasts and targets needed to reproduce those losses). Preserve the common
eligible population, not only executed trades. Use the existing source/data
binding; do not retain arbitrary arrays without a named decision need.

For execution diagnosis distinguish: forecast produced; cost/buffer threshold
crossed; entry eligible or blocked by a position/boundary; order simulated;
trade filled; gross and net outcome. A zero-trade result alone identifies none
of the preceding causes. Choose counts and fixed diagnostic views before the
run; store per-origin values only if the question requires them. Existing
aggregate reports remain sufficient for questions they can actually answer.

Resource assessment includes origins × policies × retained fields × bytes
plus serialization overhead, disk retention, runtime and memory. Estimate
from metadata first; select a bounded format and retention limit within the
campaign budget. No new default archive, automatic recomputation or permission
to inspect protected data follows. Historical missing arrays remain missing;
E18's aggregate forecast metrics cannot supply an ordered paired-loss series.

### Existing report and audit records

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
