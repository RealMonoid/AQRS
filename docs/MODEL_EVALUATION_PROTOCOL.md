# AQRS — Model and tool evaluation/adoption protocol

This protocol complements [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`RESEARCH_PROTOCOL.md`](RESEARCH_PROTOCOL.md). It defines **how a method earns inclusion** and why a model failing to generate alpha is not necessarily a product failure. The Resource Governor and Linux support requirements apply to every candidate.

## 1. Pre-registered model card (required before EVERY comparison)

Store a versioned model card for each new algorithm:

- `registry_id`, release/commit version, library license and separate model-weight/data licenses if relevant.
- `problem`: forecast, anomaly/regime hypothesis, feature representation, decision, execution or research scheduling.
- Market, instrument, data source, bar/event interval, feature availability, target variable and label horizon.
- For unsupervised methods, the **downstream test** that distinguishes a rare state from future predictive value.
- Comparison baseline(s) and explicit null hypothesis; for filters, include the version **without** the original signal.
- Train/research-validation/final-holdout boundaries and required label-overlap purge/embargo.
- Data quality, costs/slippage/funding assumptions, fills, holding period and trade directions.
- Tuning/feature/model trial budget, seeds, CPU time and RAM cap; count every trial.
- Primary forecasting metric, primary **net-trading metric** and uncertainty estimate; lock the selection rule **before** testing.
- False-discovery threats, controls, expected incremental benefit and stopping conditions.

## 2. Evaluation sequence

1. **Data and economic gate:** are reliable inputs and venue rules available? Could a plausible gross edge exceed realistic costs? Do not exclude on average spread alone.
2. **Causal representation:** no future leakage via scaling, normalization, label features, session aggregates, publication timestamps or smoothed market regimes.
3. **Simplest baseline first:** zero/Ridge/rule model and appropriate momentum, mean-reversion or matched control.
4. **Identical evaluation protocol for challenger:** same information, folds, execution costs/fills, sampling and comparable tuning budget.
5. **Unsupervised is discovery, not profit:** anomaly/cluster/HMM scores do not predict returns automatically. Generate causally available events, then compare future conditional return/risk to matched placebo events.
6. **Ablation and added information:** e.g. volume-plus-downtrend **versus** downtrend only. Built-in feature importance is not causal proof.
7. **Temporal robustness:** walk-forward, effective independent episodes, volatility/market regimes and recent OOS periods. Older periods only where market structure warrants comparison.
8. **Multiple testing:** journal every trial, overlapping family, selection method and validation boundary. A final holdout is for frozen candidates only; repeated peeking makes it research data.
9. **Economic evaluation:** net of fees, spread, slippage and relevant funding; include turnover, drawdown, risk constraints, size/capacity and sensitivity. Do not adopt based only on accuracy/F1.
10. **Resource review:** is incremental benefit over baseline large and robust enough to justify additional CPU, RAM, data and maintenance costs?

## 3. Model adoption state machine

`REGISTERED → PRECHECKED → PILOT_RUNNING → {ADOPTED | REJECTED | DEFERRED | BLOCKED_*}`.

- `ADOPTED`: reproducible implementation/tests, feature/data contract, resource limit, model card, journal run and fair baseline report.
- `REJECTED`: evidence does not support usefulness for the *specified task/market period*, not an eternal universal ban.
- `DEFERRED`: insufficient priority/evidence, with a review trigger/date.
- `BLOCKED_DATA`: required inputs missing, unreliable or prohibitively expensive.
- `BLOCKED_LICENSE`: code/weights/data rights prevent intended use.
- `BLOCKED_RESOURCES`: CPU/RAM/runtime requirement exceeds approved bounds.

`configs/model_tool_registry.json` holds **planning labels**. Live experiment and adoption history belong in the persistent journal, not a repeatedly overwritten static source of truth.

## 4. Three independent acceptance dimensions

1. **Software acceptance:** algorithm runs reproducibly with tests, resource controls and valid APIs.
2. **Scientific acceptance:** incremental, reproducible discovery/predictive evidence with appropriate uncertainty and independent temporal validation.
3. **Economic acceptance:** incremental net policy value under credible execution, risk and cost assumptions.

Passing dimension 1 does not imply passing 2 or 3. An `EVALUATE` candidate may satisfy the software gate but fail the scientific/economic gate without making the software release invalid.

## 4a. Termination instead of endless calibration

Before comparing models, record a bounded timing/memory pilot and explicit worst-case compute limits. Active execution must stop when limits are reached. The Governor records `REJECTED_PREFLIGHT`, `BUDGET_EXHAUSTED`, `TIMED_OUT` or `MEMORY_LIMIT`, without silently starting another trial. A model that was never adequately trained must not be marked scientifically rejected. Forecasts of months/years of sweeping are **no-go** unless the owner makes a separate explicit scope/budget decision. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md).

## 5. Milestone-appropriate effort limits

- **v0.1:** NumPy, pandas, minimal scikit-learn model; no model zoo. Verify the registry/DoD is readable and consistent; Native Windows and independent Linux installation tests must pass.
- **v0.2:** real data; check access/licenses before DeepLOB, FinBERT or GNN trials.
- **v0.3:** LightGBM and Isolation Forest as distinct learning families; evaluate XGBoost, HDBSCAN, PCA, autoencoders and Random Forest with bounded pilots or explicit blocking decisions. If needed real data are missing, record `BLOCKED_DATA` and a test plan instead of silently skipping.
- **v0.4:** research budget becomes part of selection; compare Successive Halving to a static scheduler.
- **v0.5:** selection-bias protection applies to all attempted models, even those generating no final candidate.
- **v0.6–v0.7:** cost/risk and monitoring requirements apply to **adopted** models, not to every catalog item.
- **v0.9/v1.0:** complete `model_registry_audit`, with every catalog entry's decision and reason plus run ID when relevant; demonstrate both a supervised and an unsupervised discovery workflow.

## 6. Reproducible adversarial tests by model class

| Model family | Minimum adversarial test |
|---|---|
| Supervised ML | Inject future-only features; earlier predictions/train/OOS selection must remain unchanged. Same seed and fold config reproduce. |
| PCA, clustering, autoencoders | Scaling/representation fit on training data only; validation observations cannot define training clusters. |
| HDBSCAN, HMM, regimes | Historical decisions cannot use future regime labels; OOS/inductive scoring procedure explicitly tested. |
| Text/LLM | Later publication cannot affect earlier features; separately inspect weights licensing. |
| DeepLOB | Reject OHLCV-only input; require appropriate LOB levels, events and fill/cost inputs. |
| GNN | No future delisting, index membership or graph-edge knowledge in past-time graphs. |
| RL/MPC | Same order and cost rules as baseline; RL remains deferred past v1.0. |
| Scheduler, Optuna, bandits | Final holdout metrics must be inaccessible as reward/tuning targets. |

## 7. What does NOT constitute independent incremental value

- Better in-sample Sharpe without independent OOS comparisons.
- Feature importance or cluster separation without later conditional forecasting value.
- Choosing the best of a thousand configurations while ignoring search exposure.
- Net profit created by unfair baselines, unmatched trade frequency or unrealistic simulated fills.
- Complexity, popularity, parameter count or lower training loss by themselves.
- Positive synthetic-data results reported as evidence of tradable real-market alpha.

**Decision rule:** test when scientifically and economically plausible; adopt only with robust, independently supported incremental value; otherwise document the outcome and omit it for now.
