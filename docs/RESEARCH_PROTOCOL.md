# Research protocol — scientific and economic integrity

## 1. From research question to tradable hypothesis

**Both** approaches are allowed:

- Hypothesis first: a specific market mechanism (e.g. order flow, liquidity demand, trend continuation) motivates the test.
- Data first: a model discovers conditional predictive structure from which a **new hypothesis requiring independent testing** is formulated.

A discovery on a given dataset is **not** its independent confirmation. Rarity or an “anomaly score” is not automatically a return forecast. A predictor must add out-of-sample information beyond appropriate controls.

Before extensive validation, every candidate has a registered, versioned definition: asset/venue context or synthetic scenario, data range, features, target/horizon, expected effect, comparison hypothesis, execution assumptions and cost model.

## 2. Early economic screening

Early screening checks data availability, trading access, plausible liquidity, transaction costs and possible break-even edge size. It happens **before** expensive optimization, though a cheap initial effect estimate may inform it.

- Costs: per-side fees, the **full** quoted bid-ask spread (market-order round trip normally pays about half a spread each side), slippage/impact and relevant financing/funding.
- Units: gross edge and expected net difference must use matching units (e.g. bps per round-trip trade); do not double-count any component.
- Dynamics: costs vary with venue, order size, side, market regime and time. Average spread alone does not prove impossibility.
- Perpetual funding is not charged on every arbitrary 15-minute trade; the contract and actual settlement events govern it.
- Use `REJECTED` only when a credible rejection basis exists; otherwise `DEFERRED` / `INCONCLUSIVE` with reasons.
- Costs for synthetic runs are **illustrative settings**, not statements about actual BTC/equity commissions.

## 3. Information availability and event time

- All data require monotonic UTC event timestamps and an explicit `available_at` for bars or events.
- No future close, volume or completed daily aggregate may inform an earlier intraday decision.
- Compute rolling features causally; remove and document warm-up rows.
- Real news/fundamental feeds later require publication, receipt and revision times, not merely a reporting date.
- Train-only operations include imputation, scaling, feature selection, categorization, calibration and hyperparameter search.
- Never repair missing future labels by forward filling them.

## 4. Out-of-sample research validation

- Walk-forward is chronological and reproducible; no randomly shuffled time-series CV.
- Prevent labels from overlapping training/validation cutoffs using purging or temporal gaps. Account for overlapping trades and serial dependence when estimating effective independent sample size.
- Research fold results may guide research selection; they are **not** final proof.
- The final holdout is later in time, explicitly reserved and inaccessible to Research Manager metrics/reward signals.
- Do not endlessly retest a failed final holdout. Freeze the result and version, revise the hypothesis if necessary, and await genuinely new untouched data for another independent confirmation.
- Store sufficient model/data provenance for reproduction.

## 5. Baselines, ablations and controls

Minimum controls:

1. Predictive benchmark such as `y_hat=0` or a training-only historical mean return.
2. Trading benchmark such as simple momentum and **No Trade**.
3. Matching costs, holding conventions, position size and turnover assumptions as far as comparability permits.
4. Test incremental signal value: if “volume + downtrend” works, compare **downtrend only** on the same eligible timestamps.

Later add condition-matched random entries/placebos and **block or dependence-preserving** permutation/bootstrap procedures. Naïve permutations can destroy the dependence structure and yield invalid significance claims. Do not treat hundreds of correlated trades as hundreds of independent observations.

## 6. Multiple testing and research selection

- Journal every model, feature set, time window, threshold, cost assumption and manual retest.
- Never preserve only the single best-looking backtest.
- Do not keep adding filters until a random profitable subset appears.
- Multiple-testing corrections and reality checks (appropriate block bootstrap, Deflated Sharpe or alternatives depending on the research question) belong to later milestones; v0.1 must preserve trial history for them.
- Do not assume a scientifically unmeasured “99% failure rate” determines the correct throughput.

## 7. Separate forecasting, decisions, risk and execution

- A model forecasts future returns or distributions; it does **not** instruct a real broker to trade.
- A policy compares long/short/flat, costs, uncertainty, current positions and simple risk constraints. The option *wait* is represented at least by `flat`.
- v0.1 uses an explicit heuristic rule; neither RL nor MPC is required. More complex decision rules must establish incremental value later.
- Execution assumptions must respect when the signal is observable; filling for free at the same signal bar close is not valid.
- Directional hit rate alone is not net profitability. Report net PnL, count, turnover, exposure, drawdown and uncertainty metrics separately.

## 8. Older data and alpha decay

Very old data are useful for historical regimes and mechanisms, not automatic proof of present intraday profitability. For short horizons give more weight to newer, actually accessible market structures where warranted. Apparent drift has multiple causes: data errors, overfit, changed fees/spreads, liquidity changes, regimes and competition.

The later Alpha Monitoring loop distinguishes forecast drift, cost drift and strategy risk. Define pause/review triggers **in advance**, not retrospectively after losses.

## 9. Adaptive search and resource allocation

Do not impose universal bans such as “exclude all instruments with spread over 0.05% when horizon is under 15 minutes.”

Instead:

- Research families carry `priority`, `uncertainty`, `evidence_quality`, `estimated_compute_cost`, `status`, `review_after`, `reason`.
- Run cheap screens first; expensive tests require an articulated expected scientific benefit.
- Research-fold evidence may update priority, final-holdout results may not.
- Revisit `DEFERRED` families after material market/cost changes; reserve an **exploration budget** for under-examined directions.
- Compare bandits, Bayesian Optimization or Successive Halving against a transparent fixed baseline before adopting them.

## 9a. Scientific rigor under finite compute

No claim of “statistical completeness” justifies unplanned, unbounded computation. Before execution declare what a cheap screen can establish, what information a deeper analysis would add, and the terminal state at budget exhaustion. `BUDGET_EXHAUSTED` means **untested or insufficiently tested**, not “alpha does not exist.”

Adaptive scheduling may use research-validation reports but not final-holdout values as recurring tuning/reward signals. Count fits, trials, seeds, folds, bootstraps, permutations and cost-stress variants **before** launching. A plan containing 75,000 fits must be rejected after a small pilot and conservative cost estimate **before** full calibration. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md).

## 10. Reporting interpretation standard

Reports must clearly distinguish:

- Data type: `synthetic` versus `real`, always `synthetic` in v0.1.
- Research execution success (`pipeline_completed`) versus scientific signal evidence (`evidence_status`).
- Positive net performance versus statistical significance; significance versus economic relevance.
- `INSUFFICIENT_EVIDENCE` as a legitimate, often rational outcome.
- A hypothesis being **false** versus a software test failing.

Use English in reports, schemas, experiment metadata and CLI output. Results must be reproducible on the accepted Linux baseline.
