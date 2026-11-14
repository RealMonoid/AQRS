# Open questions and safe defaults

**Milestone boundary:** v0.1 uses explicitly documented technical defaults. Only from M1/v0.2 onward must a real instrument/data-source contract be selected. Codex is **not** authorized to invent these choices for v1.0. See [`PRODUCT_VISION.md`](PRODUCT_VISION.md) and [`MILESTONE_DOD.md`](MILESTONE_DOD.md).

These issues were **intentionally left undecided**. Implement v0.1 using the labeled defaults; do not block on questions irrelevant to the walking skeleton.

| Question | v0.1 default | Later decision |
|---|---|---|
| Which real asset and venue? | `SYNTH_BTC_LIKE`, artificial dataset only | Venue, spot/perpetual/equity/future, liquidity, data quality |
| Which bar frequency and holding period? | Illustrative five-minute bars, three-bar horizon | Select horizons based on data and net trading economics |
| Which data source? | Seeded offline simulation | Binance BTCUSDT spot is [accepted for the bounded M1 research scope](MILESTONE_STATUS.md#m1-e11-learning-card-and-m1-acceptance-2026-11-09). Broader coverage and economic suitability remain open. The [Syncster/NQ screen](MILESTONE_STATUS.md#m1-e01-learning-card-syncsternq-2026-11-08) left coverage, bar timestamps and rollover unresolved. The [alternative NQ screen](MILESTONE_STATUS.md#m1-e03-learning-card-alternative-no-cost-nq-source-2026-11-08) found a free individual-contract sample with an unconfirmed bar boundary. |
| Which execution? | `open[t+1]` reference with taker-like cost approximation | Market/limit/partial fills, latency, slippage, depth and impact |
| Which costs? | Configurable illustrative bps, never represented as actual exchange rates | Venue-, volatility-, size- and time-dependent estimates |
| Are long and short available? | `allow_short=true` for **synthetic simulation only**, no broker | Spot/perpetual/borrow/margin/funding/liquidation risk |
| Which risk budget? | Simulated unit notional, no leverage | Capital, drawdown, exposure and pause/stop rules |
| Which models? | Ridge/simple scikit-learn models | LightGBM and Isolation Forest as distinct M2 discovery pilots; explicit HDBSCAN/autoencoder/other evaluation gates; adoption depends on data and incremental value |
| Which compute budget? | Two small candidates, few folds; hard YAML Governor defaults | Hardware-benchmarked trial/family budgets, explicit approvals |
| How is research prioritized? | Transparent deterministic round-robin plus feasibility checks | Empirically evaluated adaptive prioritization/bandits |
| What qualifies as real strategy success? | **No** real profit claim at v0.1 | Net edge, risk metrics, independent episodes, capacity, OOS stability |
| Must data begin in 2003? | No | Only if market mechanism/instrument/research question justify it |
| Which operating system? | **Decided:** native Windows 10/11 x86_64 is the primary local development/run environment; Ubuntu 24.04 LTS x86_64 headless/non-root is a required separate M0 acceptance target | Other Linux distributions/architectures and providers are added only after actual verification; no cloud vendor selected |
| Which internal language? | **English**, no exceptions for new repository artifacts | External user-facing localization is a separate feature, not required by v1.0 |

A future strict memory mode requires a separate enforcement and portability test. M0 uses
the configured observed-RSS policy and rejects strict requests. After an abrupt orchestrator
death, SQLite retains the last committed campaign and attempt states. Automatic reconciliation
of interrupted rows is outside the current restart contract.

## M2-E20-P06 report-only calibration

**Resolved 2026-11-14.** The owner authorized and AQRS executed the single
planning diagnostic below through the explicit P06 decision. The
[verified result](MILESTONE_STATUS.md#m2-e20-p06-learning-card-local-expansion-deferred)
is DEFER for a local outcome expansion; no larger data request is justified.
The original scope is preserved below and is bounded by the
[registered Card](MILESTONE_STATUS.md#m2-e20-p06-test-card-one-archived-report-calibration).
Quant Research recommended the bounded look because the
[P05 sensitivity](MILESTONE_STATUS.md#m2-e20-p05-learning-card-decision-specific-evidence-design)
showed that dispersion can change whether local longitudinal evidence is even
plausible. P02 explicitly reserves specific authorization for a new report
diagnostic; ordinary design, arithmetic and verification are already complete.
This is not a request for new dates, a rerun, or 6–12 months of data.

- **Research question / expected decision:** Can the observed scale of the
  fixed pair contrast support a feasible *planning* case within local
  development capacity, or should the contrast remain deferred? Return a
  bounded next-design recommendation or `INCONCLUSIVE / DEFER`, never alpha
  or an M2 acceptance decision.
- **Existing evidence / gap:** E18 already reports 18 matched pairs across
  six validation days with both candidates deferred. The pair SD is not in
  the current planning record. Future event yield, regime coverage and
  defensible between-block independence remain unknown. Six days cannot
  resolve these latter uncertainties.
- **Exact input and required properties:** BTCUSDT spot, derived matched-
  event report only; source window 2025-12-01 00:00 through 2025-12-11 00:00
  UTC, validation December 5–10. Read only
  `artifacts/m2-e18/windows/report.json` from
  [the retained bundle](../evidence/m2-e18-acceptance.zip).
  The [receipt](../evidence/m2-e18-verification.json) binds 572,495 bytes and
  SHA-256 `d314d0202953b52c87774716a12fd684a013e6e2f5840723e3ab755f633fb524`,
  executable revision `54fb8644b5a27c51fece7d89f3d9996a65356ad2`, run
  `bb9866a947c74c21a4ffdf2a8501f250` and its published source/data identities.
  Verify the member before parsing. Select only `VOL_CONFIRM_E18_V1`
  matched rows, retaining UTC band/day, pair identity and net pair difference.
- **Minimal calculation:** Preserve the existing pair-weighted estimand.
  Report sample pair SD, total and per-day/per-eight-hour-band counts and
  centered day contributions. Show P02's variance diagnostic for partitions
  of 1, 2 and 3 consecutive days anchored on December 5, retaining gaps.
  With 6/3/2 possible groups these are sensitivity diagnostics only: report
  effective independent count as `UNKNOWN`, with no HAC estimate,
  independence test, bootstrap, significance claim or automatic lag choice.
  Do not inspect other candidate outcomes. Use synthetic unequal-count and
  shared-shock examples to verify any calculation before the report read.
- **Why this scope / sensitivity:** One already exposed report is cheaper
  than acquiring or rerunning a longer series. At assumed SD 5/10/20/40 bps,
  the .05/.80 gap-2 calculation is 39/155/619/2,474 independent units.
  Recalculate the same fixed sensitivity at the observed SD without treating
  that six-day estimate as a population bound. Keep design effects 1/2/4,
  yields 1/1.5/3 and the original SD grid visible. The result can rule out a
  local capacity scenario *under its assumptions*, not guarantee sufficiency.
- **Predeclared planning branch:** At the observed SD, calculate the .05/.80
  gap-2 requirement for every fixed `(D,y)` cell. Compare
  `ceil(D * n / y)` with the optimistic metadata ceiling of 32 validation
  days / 96 band slots after four training days. If no cell fits, `DEFER`
  a local outcome expansion under that dispersion scale; record the
  conditional shortfall and request no larger period automatically. If
  any cell fits, record `CONDITIONAL_LOCAL_CASE` and prepare only the exact
  subsequent count/dependence question on December 11–24. Label which
  assumptions make it fit. That branch does not admit 32 validation days:
  a new chronological design would still need explicit handling of the
  two dates left by complete three-day folds, exposure and scoped access.
  Neither branch changes the inferential E20 result: it stays `INCONCLUSIVE`
  because between-block independence and population dispersion are unknown.
- **Expected informative units:** At most the same 18 pairs, six days,
  three two-day groups or two three-day groups. This creates no additional
  independent observations. Ubuntu is a reproducibility check, not a second
  sample. ETH is outside this packet.
- **Stop rule:** One member, one contrast, one prospectively registered
  planning diagnostic with the specified components. Abort on any identity,
  timestamp, duplicate, finite-value or count mismatch. Missing or degenerate
  variance leaves the planning branch `INCONCLUSIVE / DEFER`. Apply the
  fixed capacity branch above for a valid finite variance; unsupported
  independence always leaves inference open. Never automatically expand
  data, retune or take a second look. Qualification alone does not authorize
  reading the December 11–24 archives.
- **Holdout / exposure protection:** No raw ZIP payload, new downloads,
  January 6 holdout or other protected data. Keep historical E18 results
  closed. Publish the fixed diagnostic definition and prospective exposure
  registration before access, bind to the original run/member, then retain
  every calculated component under that view; do not count a new variant
  or hide the additional look. No changes to matching, thresholds or costs.
- **Resource Governor assessment:** At most 30 minutes of one-time work,
  one CPU process and 30 seconds for verification/calculation; abort on a
  larger-than-receipt member. Input is under 0.6 MB; output below 100 KB.
  Zero model trials/fits, resamples, raw-data reads, downloads, dependencies,
  paid services or recurring work. Existing budgets remain unchanged.
  Normal synthetic verification and independent review precede the look;
  bind A16-P01 to that practical test, without a separate audit.

## M2 supervised pilot replay

**Resolved 2026-11-14.** The owner approved the fixed Windows comparison
and conditional headless non-root Ubuntu replay. The
[P04 Learning Card](MILESTONE_STATUS.md#m2-e20-p04-learning-card-source-bound-e09-replay)
records both completed, independently verified runs. The original
source-linkage gap remains a historical limitation.

**Original decision.** Authorize a new source-bound M2-E09 reproduction as M2
software acceptance evidence, or leave the supervised reproducibility
criterion open until original run-linked source evidence appears. The
[M2-E16 recovery review](MILESTONE_STATUS.md#m2-e16-learning-card-historical-source-binding-2026-11-10)
found no exact source binding for both historical runs. The executed
reproduction preserves the LightGBM research disposition.

**Proposed scope.** Freeze and independently verify the
[versioned pilot](../scripts/m2_supervised_pilot.py), its configuration,
dependencies, four recorded BTCUSDT development archives for January 1–4,
2026 UTC and the effective Governor. Use the fixed M2-E08/1 comparison.
Approve at most one native Windows run and one headless non-root Ubuntu
replay only after a valid complete Windows comparison. Require source
snapshots and digest binding in both receipts, identical data,
configuration, folds and trade decisions, intact journals and the
existing absolute numeric tolerance of `1e-8`. Stop on a failed
preflight, scope or budget violation, incomplete Windows result or
platform mismatch. Keep the original reports and technical/scientific
dispositions as historical evidence.

**Prepared verification.** [M2-E20-P03](MILESTONE_STATUS.md#m2-e20-p03-learning-card-supervised-replay-readiness)
checked the source and archive metadata and exercised the read-only verifier
with synthetic receipts. The verifier implementation is separate from
the queue handoff. Confirm that it is available for the receipt checks.
Stage both execution trees from the same selected Git revision to get
byte-identical source and configuration. After the
authorized Windows run, use `python scripts/evidence_archive.py
--verify-supervised-replay WINDOWS_DIR --source-revision COMMIT`. After an
eligible Ubuntu run, insert `UBUNTU_DIR` after `WINDOWS_DIR` to verify parity.
The independent review also verifies the actual platform, admitted scope and
run limits. The archived January 6 holdout remains outside the comparison.

**Resource Governor assessment.** Allow up to two hours of one-time work
for freeze, qualification, execution and closeout, subject to the final
Test Card and cumulative effort check. At most one seed, two trials and
six fits per platform, including timing fits. Retain the existing
120-second trial, 300-second campaign and 4,096 MiB sampled RSS limits.
Check the deadline and input scope on the exact entry before execution.
Zero market-data downloads, protected access, tuning, automatic retries,
spend or recurring work. No change to defaults or research budgets.
[M2-E20](MILESTONE_STATUS.md#experiment-queue) tracks the affected gate.

## M2-E15 state persistence count

**Resolved 2026-11-14.** The owner approved the single bounded count in the
[execution card](MILESTONE_STATUS.md#m2-e15-count-entry-and-execution).

**Original decision.** Authorize the named BTCUSDT spot access for December
1–10, 2025 UTC and the single count in the
[M2-E15 Test Card](MILESTONE_STATUS.md#m2-e15-p01-test-card-state-persistence-count-design),
or keep the count deferred. The count uses the same completed-bar inputs
for both fixed rules and uses no forward outcomes, estimator fits, new
downloads or protected data. Require the exact data-scope guard, synthetic
entry checks and Governor preflight before reading the input. A coverage
pass only permits considering a
separately scoped outcome study.

## Protected evaluation design

The [adaptive research design](DECISIONS.md#adaptive-research-integration) leaves the deployment-specific threat model, runtime identities, eligible submission formats and release authority open. Resolve them before authorizing a real protected evaluation. Keep initial tests on synthetic data with planted secrets. The first bounded probe would inventory actual read, write and deployment rights, show that development data remain accessible, and attempt a direct protected read from the real research identity. Budget this as one development session on an already available test environment with zero trials, fits or real protected data. Infrastructure setup and ongoing costs require a separate estimate.

An initial denied read is limited evidence. The [protected evaluation gate](MILESTONE_DOD.md#m4--v05-rigorous-statistics-and-independent-candidate-admission) requires the full security matrix, including a successful frozen replay and authorized release. Refine [FTA-M4-A](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes) against the actual authority available to the researcher and generated code before implementation.

## Avoid over-specification

- The defaults are sufficient to start, not an assertion that every future choice has been resolved.
- Codex should document conservative defaults rather than repeatedly requesting irrelevant decisions.
- Without explicit authorization for brokerage and live capital, never integrate live order submission.
- Market selection later must have an economic rationale, not rely on supposed universal winning recipes.

## Prerequisites for later model families

Before DeepLOB: are sufficiently complete L2/L3 order-book and realistic fill data available? Before FinBERT/LLM: are publication times, processing delays and text availability understood? Before HDBSCAN/autoencoders: is compute available for causal out-of-sample anomaly testing? Before RL: is there a credible interactive simulation and a classical policy worth beating? See [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md).

## Compute and platform rules are not open-ended blockers

The v0.1 limits in `configs/research.yaml` are **technical starting budgets** Codex must implement and test. Later they may be consciously adjusted from real hardware benchmarks. Without a valid bounded configuration or required OS enforcement, expensive trials must not start; fail closed. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md) and [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).
