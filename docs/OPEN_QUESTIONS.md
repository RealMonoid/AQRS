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

**Owner decision.** Authorize the named BTCUSDT spot access for December
1–10, 2025 UTC and the single count in the
[M2-E15 Test Card](MILESTONE_STATUS.md#m2-e15-p01-test-card-state-persistence-count-design),
or keep the count deferred. The count uses the same completed-bar inputs
for both fixed rules and uses no forward outcomes, estimator fits, new
downloads or protected data. Require the exact data-scope guard, synthetic
entry checks and Governor preflight before reading the input. Default:
no data access or count. A coverage pass only permits considering a
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
