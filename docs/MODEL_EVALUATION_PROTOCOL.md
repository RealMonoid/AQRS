# AQRS — Model and tool evaluation/adoption protocol

This protocol complements [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`RESEARCH_PROTOCOL.md`](RESEARCH_PROTOCOL.md). It defines **how a method earns inclusion** and why a model failing to generate alpha is not necessarily a product failure. The Resource Governor and Linux support requirements apply to every candidate.

## 1. Pre-registered model card (required before EVERY comparison)

For a new scientific question or method choice, include the
[decision-linked literature note](RESEARCH_PROTOCOL.md#decision-linked-literature-checks)
in the existing Card. A technical reproduction with no scientific change is
exempt from this literature check. A paper motivates a comparison only through a named open question,
mechanism and expected baseline advantage; it does not establish adoption.
Literature-driven changes after freeze use the existing variant/exposure rules.

Store a versioned model card for each new algorithm:

- `registry_id`, release/commit version and dependency versions.
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

For an exploratory idea, use the existing candidate record to name the proposed
mechanism, the observation that could contradict it, and when the observable
input becomes available. A delayed positioning proxy can be useful background
while being unsuitable for an intraday trigger. Use the existing feasibility
screen to defer ideas when the available data cannot answer the question. The
[Open Quant Trading Lab X2 review](https://github.com/privEgem/open-quant-trading-lab/blob/a4270df7d795cfda73ede1aed70371b53bb11f43/research/x2.md)
illustrates this stopping decision.

### Agent discovery handoff

Apply the following design in the [M2-E21 Scout pilot](MILESTONE_ARCHIVE.md#m2-e21-scout-pilot-feature-preflight).
The agent supplies a hypothesis or abstains. A proposal records the data view,
dated observations, the suggested mechanism or exploratory origin, a rival
explanation, the event and eligibility rule, direction, horizon, availability,
and a falsifier. The evaluator rechecks the cited observations, fixes the
executable rule and its identity before evaluation, and uses the existing
matched controls. Resolve material differences between the idea and its
formalization before registration. Keep the proposal, executable rule,
and resulting evidence linked in the candidate and attempt records.

Compare exact event and decision outputs on the same eligible development
opportunities to flag differently written rules with identical behavior.
Retain their proposal history and count searches already performed. Agreement
on a bounded slice only identifies duplicates on that slice. Add broader
behavioral similarity or automated filtering only if repeated proposals
justify their measured cost. In a later M3 feedback design, reuse eligible
development results and failed attempts in the research journal; keep protected
results outside the adaptive loop. These patterns are drawn from
[Strat Hunter's Scout](https://github.com/mohdhd/strat-hunter/blob/00c94a6/templates/GENERATE.md.j2),
[RD-Agent's workflow](https://github.com/microsoft/RD-Agent/blob/484776c/rdagent/components/workflow/rd_loop.py)
and [Alpha Foundry's behavior checks](https://github.com/Huang-Hg/alpha-foundry/blob/614378f/foundry/search/evaluator.py).

### Validation method selection

**Owner direction, 2026-11-11 (ADR-052):** consider the methods below in future
research design. This is a method-selection guide, not implementation approval
or a requirement to pass every test. The existing research protocol, frozen
campaigns and acceptance thresholds remain authoritative. None of these
methods establishes profitability or repairs leaked data, missing search
history, unrealistic fills or an exhausted final holdout.

| Method | Question and prerequisites | AQRS placement and current boundary |
|---|---|---|
| Walk-forward | Does a fixed training/selection procedure work on later observations? Refit preprocessing and models only on earlier training data; isolate overlapping labels. | Existing baseline: expanding chronological folds with a horizon gap. Freeze window, refit and selection rules; any later rolling-window alternative is a counted variant. |
| Performance attribution | What part of gross/net performance is associated with market exposure, known factors, signal decisions and costs? Use matched opportunities, sizing and execution; disclose factor and return-accounting conventions. | Begin with existing M2 controls, ablations and cost decomposition. Formal market/factor attribution is conditional on suitable data at M4/M5. An unexplained residual is not automatically alpha or a causal effect. |
| PBO via CSCV | How often does the in-sample winner rank below the out-of-sample median within the declared candidate family? Requires synchronized, comparable candidate return series, a fixed ranking metric and an even number of time blocks. | Conditional M4 selection-risk diagnostic. CSCV forms complementary equal-sized block selections; it is not chronological deployment replay. PBO of 60% describes those split-wise selection failures, not a 60% probability of losing money. [PBO paper](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf) |
| Deflated Sharpe Ratio (DSR) | Is a selected Sharpe convincing after accounting for search and non-normal returns? Record sample length, frequency, skewness/kurtosis, trial Sharpe dispersion and a justified treatment of dependent trials. | Conditional M4 Sharpe-specific assessment, not a general correction for any discovered effect. Report assumptions and missing exposure; do not treat correlated trials or serially dependent returns as independent without justification. [DSR paper](https://doi.org/10.3905/jpm.2014.40.5.094), [implementation assumptions](https://skfolio.org/generated/skfolio.measures.deflated_sharpe_ratio.html) |
| CPCV | How sensitive is performance to combinations of train/test blocks after removing overlapping information intervals and applying a justified embargo? Requires explicit label intervals and train-only preprocessing in every fit. | Conditional M4 robustness extension. Training can include blocks later than a test block; therefore CPCV is not a substitute for chronological walk-forward or fresh confirmation. Its recombined paths are dependent. [CPCV documentation](https://skfolio.org/generated/skfolio.model_selection.CombinatorialPurgedCV.html) |
| White's Reality Check | Can the joint null that no member of the declared family beats a fixed benchmark be rejected? Requires aligned performance/loss differences and dependence-preserving resampling. | Conditional M4 family-level test. Rejection does not independently certify the selected winner; non-rejection is not proof that every candidate lacks value. [White (2000)](https://doi.org/10.1111/1468-0262.00152) |
| Hansen's SPA | The same family-versus-benchmark question, with studentization and a null construction less sensitive to poor alternatives. | Conditional M4 alternative to Reality Check, not an additional mandatory certificate. Select and justify the procedure before results, rather than choosing whichever p-value passes. [Hansen (2005)](https://doi.org/10.1198/073500105000000063) |

**Priority and evidence.** Keep chronological validation, credible costs and
matched attribution/controls first. At the existing M4 gate, select diagnostics
for the actual claim: DSR for Sharpe selection, PBO/CSCV for family selection
instability, SPA or Reality Check for family superiority, and CPCV when extra
split robustness could change the decision. There is no universal order among
those conditional methods. PBO and DSR are not interchangeable significance
tests; agreement among methods on reused data is not independent confirmation.
Synthetic known-answer/null checks must qualify the chosen implementation
before scientific use under the existing M4 requirements.

In the existing Test Card and Research Journal, fix the candidate family,
benchmark, return/loss definition, observation frequency, complete opportunity
population, costs, selection rule, partitions, dependence assumptions, missing
data/tie treatment, decision thresholds and resampling plan before outcomes.
Preserve unsuccessful/manual variants and distinguish unknown historical
exposure from zero exposure. Retain aligned candidate/control series and their
timestamps/hashes when the approved method needs them; summary Sharpes or a
winner's equity curve alone are insufficient for family validation. Do not
retroactively invent unavailable series or silently rerun archived campaigns.
Any additional view influencing selection consumes research exposure.

**Resource Governor assessment.** Recording this guide adds zero research
trials, fits, resamples, dependencies or recurring computation. Implementation
effort and actual runtime remain unmeasured until a specific bounded Test Card.
With reusable series, DSR is mainly moment calculation and attribution may need
small regressions. CSCV can reuse a fixed return matrix but still evaluates
`C(S, S/2)` selections for S blocks. CPCV entails `C(N, k)` train/test splits
per candidate/seed, with every preprocessing/model/baseline fit counted.
Reality Check/SPA require a declared number of joint bootstrap resamples,
preserving both temporal dependence and cross-candidate alignment. Reuse of
metrics is not permission to skip any refits required by the chosen design.

Before integration, bound the complete workload, peak memory and series storage
per family/campaign; use a representative supervised pilot if estimates are
missing. No fit-free method is exempt from wall-time or memory controls. The
existing defaults remain two trials, twelve fits, one seed, one worker,
120 seconds/trial, 300 seconds/campaign and 4096 MiB sampled RSS. A simple CPCV
plan with six blocks and two test blocks already has fifteen splits for one
candidate, exceeding twelve fits before baselines. Reduce the declared scope
or request a separate budget; do not silently truncate after seeing results.
Quant Research revisits [M4-E01](MILESTONE_STATUS.md#experiment-queue) when an
authorized M4 claim and adequate inputs exist. Until then, retain the existing
workflow and report unavailable diagnostics explicitly.

## 3. Model adoption state machine

`REGISTERED → PRECHECKED → PILOT_RUNNING → {ADOPTED | REJECTED | DEFERRED | BLOCKED_*}`.

- `ADOPTED`: reproducible implementation/tests, feature/data contract, resource limit, model card, journal run and fair baseline report.
- `REJECTED`: evidence does not support usefulness for the *specified task/market period*, not an eternal universal ban.
- `DEFERRED`: insufficient priority/evidence, with a review trigger/date.
- `BLOCKED_DATA`: required inputs missing, unreliable or prohibitively expensive.
- `BLOCKED_RESOURCES`: CPU/RAM/runtime requirement exceeds approved bounds.

`configs/model_tool_registry.json` holds **planning labels**. Live experiment and adoption history belong in the persistent journal, not a repeatedly overwritten static source of truth.

## 4. Three independent acceptance dimensions

1. **Software acceptance:** algorithm runs reproducibly with tests, resource controls and valid APIs.
2. **Scientific acceptance:** incremental, reproducible discovery/predictive evidence with appropriate uncertainty and independent temporal validation.
3. **Economic acceptance:** incremental net policy value under credible execution, risk and cost assumptions.

Passing dimension 1 does not imply passing 2 or 3. An `EVALUATE` candidate may satisfy the software gate but fail the scientific/economic gate without making the software release invalid.

For a forecast comparison, record predictive and economic conclusions
independently in the existing report or linked Journal evidence, using the
registered effect and decision criteria. Reuse existing evidence statuses
and record the reason and tested scope of each conclusion. A supported
predictive improvement warrants more work only when plausible policy value
or another named research benefit can change a decision. A failed economic
screen leaves any separately established predictive result intact. Sparse
trades can leave economic evidence insufficient even when a fixed policy
misses its activity floor.

When the decision depends on why a forecast policy rarely trades, preregister
the decision-relevant aggregate or fold views under the
[diagnostic exposure rules](RESEARCH_PROTOCOL.md#descriptive-diagnostics-and-additional-exposure).
Use the forecasts and opportunity/position eligibility available during the
registered evaluation. Record relevant quantiles and the maximum, positive
and where relevant negative threshold exceedance counts and shares on the
same opportunity denominator, executed entries, and exceedances blocked by
an open position. Use the fixed policy's comparison operators and keep any
other reason for a skipped opportunity identifiable. Retain only evidence
needed for the stated decision under the existing budget. Where the saved
report cannot resolve the cause, state that limitation and assess whether a
future registered view could change the decision.

Keep costs, buffers and advancement thresholds frozen for the comparison.
Require better cost evidence, changed market or venue conditions, a confirmed
requirement, or an explicitly authorized new simulation with a stated
decision purpose for a new cost scenario. A desire for greater activity or
better results is insufficient. Register changes prospectively as new
variants and apply the same costs to comparable controls.

## 4a. Termination instead of endless calibration

Before comparing models, record a bounded timing/memory pilot and explicit worst-case compute limits. Active execution must stop when limits are reached. The Governor records `REJECTED_PREFLIGHT`, `BUDGET_EXHAUSTED`, `TIMED_OUT` or `MEMORY_LIMIT`, without silently starting another trial. A model that was never adequately trained must not be marked scientifically rejected. Forecasts of months/years of sweeping are **no-go** unless the owner makes a separate explicit scope/budget decision. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md).

## 5. Milestone-appropriate effort limits

- **v0.1:** NumPy, pandas, minimal scikit-learn model; no model zoo. Verify the registry/DoD is readable and consistent; Native Windows and independent Linux installation tests must pass.
- **v0.2:** real data; check input availability and timing before DeepLOB, FinBERT or GNN trials.
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
| Text/LLM | Later publication cannot affect earlier features; verify processing delays and availability. |
| DeepLOB | Reject OHLCV-only input; require appropriate LOB levels, events and fill/cost inputs. |
| GNN | No future delisting, index membership or graph-edge knowledge in past-time graphs. |
| RL/MPC | Same order and cost rules as baseline; RL remains deferred past v1.0. |
| Scheduler, Optuna, bandits | Final holdout metrics must be inaccessible as reward/tuning targets. |

When reviewing a new timing boundary, prefer a small synthetic case with a
known answer and a deliberately wrong counterpart. A bar stamped at its open
still has its final high, low, close and total volume available only at
completion or later. For a position closed at a scheduled bar open, that bar's
subsequent low cannot turn the open exit into a stop. Verify that the check
rejects the wrong clock and accepts the causal path. Reuse the existing
[momentum clock check](MILESTONE_ARCHIVE.md#m2-e05-learning-card-decision-time-causality-2026-11-09)
and [known-answer matched-control check](MILESTONE_ARCHIVE.md#aqrs-a08-learning-card-descriptive-signal-diagnostics)
as patterns. See the [discussion](https://www.reddit.com/r/mltraders/s/tRRqYbTiMt)
and [the X1-L limitation](https://github.com/privEgem/open-quant-trading-lab/blob/a4270df7d795cfda73ede1aed70371b53bb11f43/docs/LIMITATIONS.md).

If an authorized design uses shuffled training targets as a leakage diagnostic,
keep the evaluation targets intact, rerun the training-only fit pipeline, and
count all fits before launch. A null-like result cannot certify causal timing.
Any inference from a permutation needs a null design that respects relevant
time dependence. For cost sensitivity, isolate the effect of worse fills on the
same trades first. A rerun in which higher costs also change trade selection
answers a separate policy question. Use the same cost accounting for candidate
and control and avoid charging an explicit spread twice.

## 7. What does NOT constitute independent incremental value

- Better in-sample Sharpe without independent OOS comparisons.
- Feature importance or cluster separation without later conditional forecasting value.
- Choosing the best of a thousand configurations while ignoring search exposure.
- Net profit created by unfair baselines, unmatched trade frequency or unrealistic simulated fills.
- Complexity, popularity, parameter count or lower training loss by themselves.
- Positive synthetic-data results reported as evidence of tradable real-market alpha.

**Decision rule:** test when scientifically and economically plausible; adopt only with robust, independently supported incremental value; otherwise document the outcome and omit it for now.
