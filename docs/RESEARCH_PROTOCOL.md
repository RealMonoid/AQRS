# Research protocol — scientific and economic integrity

## 11. AQRS-B01 frozen blind-search procedure

**Scope:** owner-authorized preparation on 2026-11-11. This is a diagnostic of
the implemented finite search, not an unrestricted search or a market study.
Input contract: [A2](CONTRACTS.md#a2-external-synthetic-blind-test-input-aqrs-b01).
The code, this section and `configs/blind_search.json` are frozen and published
before external delivery. Owner choices that change them require a new freeze
before looking at external outcomes. The solution stays with the independent
producer; only the owner verifies its prior commitment after report freeze.

**Search space and order.** Six OHLCV features known at close t: close returns over
1, 5 and 20 minutes (bps); current volume / mean of the preceding 20 volumes
(zero when the denominator is zero); (high-low)/close in bps; and
(close-low)/(high-low), using 0.5 for a zero range. An available optional field
also contributes one feature at the close of minute t:

| Required CSV field | Feature | Definition at minute t |
|---|---|---|
| `buy_volume` | `buy_share` | Buy volume / total volume |
| `sell_volume` | `sell_share_change20` | Sell share minus the mean sell share of the preceding 20 completed minutes |
| `trade_count` | `relative_trade_count20` | Trade count / mean trade count of the preceding 20 completed minutes |

Each side share is zero for a zero-volume minute. Relative trade count is zero
when the preceding mean is zero. Preceding windows are t-20 through t-1.
Calibrate each available feature's
20th/80th percentiles on bars 20 through the end of the first floor(0.4*days)
complete days, once per dataset (six to nine charged calibration fits). Rules use
`<= q20` or `>= q80`; ties remain included. No outcomes choose cutoffs.

S01–S12 are the low/high tails of each feature in that order. P01–P12 are
low-low/high-high conjunctions of the fixed pairs (return1, volume), (return5,
volume), (return20, volume), (return1, range), (return5, close-location), and
(volume, range), in that order. Evaluate S01–S06, P01–P06, S07–S12, then the
six final slots in this order:

| Field present | Low and high single-feature tails | Fallback if absent |
|---|---|---|
| `buy_volume` | T01–T02 | P07–P08 |
| `sell_volume` | T03–T04 | P09–P10 |
| `trade_count` | T05–T06 | P11–P12 |

The qualified header alone determines which slots are replaced. Register its
available fields and the 24 resolved candidates before outcome measurement,
even if the approved budget cannot admit
them. No candidate generation, ranking, horizon changes, additional plots,
feature engineering, retuning or cross-dataset learning after freeze. Manual
looks outside the registered views are additional exposure and require a new
owner decision before proceeding. Payload inspection is allowed by the owner,
but this chosen procedure intentionally uses a fixed analysis plan.

**Timing and population.** Remaining complete days are evaluation data, with
first/second halves reported separately; neither half selects candidates.
No claim of protected confirmation is made. Opportunities are indices
`t = 20 + 4*k`, inside evaluation, with exit before its end. Signal availability
is minute t's close; entry open[t+1], exit open[t+4], horizon three minutes,
at most one position. Persist every opportunity's event/entry/exit time and
candidate/control membership. Features do not use future bars. Primary outcome
is long gross forward return in bps. Positive or negative conditional effects
can be claimed; a negative effect is not silently converted into a new short
strategy. No fitted trading model, optimization or funding is used.

**Controls and measurements.** Compare a rule with its complement within each
UTC date and 8-hour band. For a conjunction A&B also compare against A&!B and
B&!A within the same strata. Record empty/unmatched strata; do not impute them.
Each matched stratum contributes event mean minus control mean; average those
within a day, then in fixed adjacent two-day blocks. Record raw event/control
counts, matched counts, per-day contrasts and both evaluation-half signs.
Also report conditional event gross return, no-trade (zero), and long-or-flat
net contributions for all eligible opportunities, including skipped ones. The
net interval and estimate use the means of complete adjacent two-day blocks.
An unpaired trailing evaluation day does not enter that block estimate.
Use existing illustrative costs: fee 4 bps/side, quoted spread 3 bps, slippage
2 bps/side, total 15 bps per entered round trip. Net-positive is distinct from
predictability and from recovering the hidden mechanism. There is no cost
screen that discards a statistically detectable sub-cost effect.

**Uncertainty and decisions.** For each contrast, a two-sided Student interval
over adjacent two-day block means uses alpha `0.05/(24*4)` (96 predeclared
endpoint slots: complement, two parent contrasts, all-opportunity net). No
resampling, repeated seeds or post-hoc selection of dependence length. Require
at least eight complete blocks, 60 matched events and 60 matched controls per
contrast, at least four block values in each chronological half, same nonzero
direction in both halves, and an interval excluding zero. Conjunctions must
pass all three contrasts in the same direction. Otherwise report
`INSUFFICIENT_COVERAGE`, `BELOW_THRESHOLD`, `UNSTABLE` or
`NO_INCREMENTAL_EVIDENCE`, preserving measurements and each failed parent gate.
A failed parent comparison does not prove that the simpler condition completely
explains the signal; low coverage, low precision and instability remain distinct.
These intervals
assume sufficiently independent, stable two-day block means; arbitrary hidden
long-memory or regime changes can violate that assumption. The blind exercise
does not establish calibrated false-positive rates for all possible generators.
The open fixture tests software behavior only. Mechanical rules and complete
measurements survive rejection, enabling post-reveal diagnosis.

**Preregistration and stopping.** One immutable JSON object per candidate in
`preregistration.jsonl`, created and committed/pushed before outcomes. It holds
ID/order, one-sentence hypothesis, rule AST, feature/cutoff parameters, horizon
and availability, exact dataset hash/window, controls, fixed metrics/decision
rules, allocated budget, `metrics=null`, `decision=PENDING`, consumed budget
zero, plan/source hashes and attempt ID. A single push may publish all entries;
the remote commit and exact file/source content must be verified before the
supervisor releases a worker. Each result is a separate immutable JSON linked
to that entry; SQLite retains all attempts and execution/evidence status.
Quantile values and coverage-only input metadata are registered before outcome
access. Git publication proves ordering relative to this runner, not absence
of out-of-band human analysis. Do not send data payloads to Git.

**Machine-readable evidence.** Publish `configs/blind_search.json` and its
bound protocol and code before delivery. After authorization, copy the frozen
plan and source digests into `search-plan.json` before reading the CSV. One
dataset runs per attempt. `evidence/blind/ATTEMPT/preregistration.jsonl` is the
published one-row-per-candidate ledger. `registration.json` binds it to the
selected input and pre-run artifacts. All other files below are local under
`artifacts/aqrs-b01/runs/ATTEMPT/`.

| File | Format and contents |
|---|---|
| `search-plan.json` | UTF-8 JSON with frozen parameters, source identity and SHA-256 bindings. |
| `features.csv` | UTF-8 CSV, one row per candle, with index, UTC open and availability timestamps, partition and the nine named feature columns. Empty cells represent unavailable features or insufficient history. |
| `CANDIDATE-opportunities.csv` | UTF-8 CSV, one row per eligible opportunity. `available_at` is the event or control time. Join rows within a file by `(evaluation_day, utc_band)` and the control arm. `event=1` marks events. The named control flag marks control members. `ARM_matched=1` means both arms are present in that group and enter that comparison. The grouping is many-to-many. Entry, exit and observed outcomes are included. |
| `predictions.json` | UTF-8 JSON with the prediction record fields and `NOT_APPLICABLE` status for the fixed rule-only plan. There are zero model candidates and the records list is empty. |
| `report.json` | UTF-8 JSON closing statement for the dataset, including status, effect claims and untested IDs. |
| `run-manifest.json` | UTF-8 JSON with code identity, effective configuration, current input SHA-256 digests, budget, preparation and candidate runtimes, status and artifact file sizes/digests. |
| `gaps.jsonl` | UTF-8 JSON Lines. Append technical stops and evidence gaps as they are detected. An empty file denotes no recorded gap. |
| `terminal.json` | UTF-8 JSON with terminal execution status and the expected artifact identities for closure. |

The [central evidence field dictionary](CONTRACTS.md#aqrs-b01-evidence-field-dictionary)
defines units, timing, allowed values and file relationships.

Feature export is part of supervised preparation and contains no forward
outcomes. The publication gate checks the candidate ledger's digest and exact
resolved rows, including order, rules and pending status. It verifies the local
plan, feature and prediction file digests before any candidate starts.
The runner promotes opportunity CSVs from `pending-opportunities/` only after
a completed worker receipt and source/file checks. A stopped attempt retains
its status and completed evidence. Files remaining in the pending directory
are unconfirmed. The run manifest records completion after the journal and
reports are persisted. A process killed outside the supervisor can leave the
latest checkpoint incomplete. The runner blocks closure without a terminal
receipt rather than assuming a killed or unobservable process is finished.

**Sequential admission and verdicts.** Publish one `DNNN-start.json` under
`evidence/blind/sequence/` for the next identifier before admitting its input.
The start binds the dataset-scoped approval, preceding verdict, frozen source
and a token held in the local workspace. A competing workspace cannot use that
start without its token. The runner checks the current remote head and
append-only Git ancestry and commit ordering. Only the current CSV is opened or probed. A delivery's
manifest digest and range stay fixed until its last dataset is closed. The next
delivery begins at the next identifier. There is no shared or carried budget.

After execution, `close` checks the terminal receipt, original published
candidate ledger and registration, staged bars, worker receipts, feature and
opportunity files, prediction status, local gap log, reports, run manifest and
closed SQLite journal. Publish `DNNN-verdict.json`,
`DNNN-summary.txt` and `DNNN-gaps.jsonl` together in one commit. Missing or changed evidence
or incomplete execution yields `NOT_EVALUABLE` and no scientific claim. An
evaluable closure retains the measured claim and its evidence references. The
summary is at most 40 lines, with counts by rule type, strongest recorded
contrast and net result when available, decision, budget use and file pointers.
Earlier verdicts cannot be modified or removed in the published lineage.
`correct` adds a separate `Cnnnnnn-correction.json` between datasets, naming
the original verdict digest and the last closed dataset at recording. The
runner does not use corrections or earlier outcomes to change the search.
The invariant applies to the runner and inspected published history; an
administrator rewriting the remote history outside this workflow is a separate
repository protection boundary.

Stop after 24 candidates or the first worker failure, exhausted budget,
integrity failure or owner cancellation. Do not stop early because a result is
positive or negative. Never retry automatically; record all remaining IDs as
untested with a reason. Refuse an existing attempt directory and any new
start for the same dataset in this series. Initial external
execution requires the delivery, an exact dataset-scoped owner start record,
and explicit approval of the proposed 24-trial exception. Defaults stay at two;
the base Governor file is unchanged. All datasets need an aggregate approved
count/time envelope; never launch a 16-dataset batch under a one-dataset budget.

**Dataset result.** `report.json` and `report.md`: synthetic/external provenance,
market_evidence=false, completeness, execution status, effect_claimed boolean,
all claimed candidate IDs/mechanical rules/event-time files, signed bps effect
and interval, parent comparisons, gross/net distinctions, spent/unused budget,
tested/untested space, source/data/publication identity and limitations. A
complete `effect_claimed=false` means nothing met this procedure, not that the
generator contained no effect. An incomplete run is never a completed null.
These technical reports supply the evidence; the published verdict is the
final decision. The two-candidate `replay` command verifies recorded artifacts
and recalculates only the requested previously measured rules under the frozen
source and published costs. It also compares every event and control CSV row.
It emits both recorded and recomputed results with their exact JSON
Pointers. It writes no artifacts and does not select candidates or advance the
sequence. A candidate without recorded evidence has no expected replay value.

**After owner-authorized reveal.** First freeze and push blind results. Verify
the owner's solution commitment. Create one adjudication row per hidden effect
and per unmatched claim: `OUTSIDE_SEARCH_SPACE`, `IN_SPACE_NOT_TESTED`,
`MEASUREMENT_ERROR`, `BELOW_THRESHOLD`, `VISIBLE_REJECTED`,
`RELATED_NOT_CAUSE`, `UNPLANTED_CLAIM`, `EARLY_STOP`. Preserve rule expressibility,
candidate IDs, attempted/skipped stages, numeric contrasts/thresholds, event
overlap, causal-parent mapping and stop reasons. Assign the earliest decisive
failure plus secondary tags; do not force a false causal conclusion from price
data alone. Recommend exact/mechanically equivalent rule AND timing recovery
as the primary success count, with predictive related conditions counted
separately. The producer's truth must decide mechanism equivalence.

The informed/oracle comparison applies the true rule/events to the same
eligible grid, horizon, costs, contrasts and uncertainty procedure; additionally
report losses from unsupported horizons or off-grid events. It is a diagnostic
upper reference, not necessarily a passing score. The stubborn single-feature
baseline exhausts S01–S12 and the available T01–T06 rules under the same
measurements and reports its separate
cost/coverage; reuse already obtained results without creating independent
evidence. Oracle work, missing single-feature attempts and any new measurements
need their own post-reveal approval and bounded budget. Nothing automatically
opens a solution file or starts those comparisons.

## 1. From research question to tradable hypothesis

**Both** approaches are allowed:

- Hypothesis first: a specific market mechanism (e.g. order flow, liquidity demand, trend continuation) motivates the test.
- Data first: a model discovers conditional predictive structure from which a **new hypothesis requiring independent testing** is formulated.

A discovery on a given dataset is **not** its independent confirmation. Rarity or an “anomaly score” is not automatically a return forecast. A predictor must add out-of-sample information beyond appropriate controls.

Before extensive validation, every candidate has a registered, versioned definition: asset/venue context or synthetic scenario, data range, features, target/horizon, expected effect, comparison hypothesis, execution assumptions and cost model.

### Define new signals around the event under study

From M2, define each new signal by the observable market event or decision
condition the hypothesis concerns. Register the trigger, required inputs,
observation cadence, earliest time the trigger is knowable, and forecast horizon.
Use a market boundary such as a session open when the hypothesis depends on it.

For example, if the hypothesis concerns a sharp five-minute price drop, evaluate
the trailing five-minute return when each completed one-minute observation
becomes available. The event starts when the return first crosses the registered
threshold. The usual validation applies, including chronological research folds,
matched controls, and a simulated entry no earlier than the next eligible
execution point. Research campaigns have no recurring shifted-grid backtest
requirement.

## 2. Early economic screening

Early screening checks data availability, trading access, plausible liquidity, transaction costs and possible break-even edge size. It happens **before** expensive optimization, though a cheap initial effect estimate may inform it.

- Costs: per-side fees, the **full** quoted bid-ask spread (market-order round trip normally pays about half a spread each side), slippage/impact and relevant financing/funding.
- Units: gross edge and expected net difference must use matching units (e.g. bps per round-trip trade); do not double-count any component.
- Dynamics: costs vary with venue, order size, side, market regime and time. Average spread alone does not prove impossibility.
- Perpetual funding is not charged on every arbitrary 15-minute trade; the contract and actual settlement events govern it.
- Use `REJECTED` only when a credible rejection basis exists; otherwise `DEFERRED` / `INCONCLUSIVE` with reasons.
- Costs for synthetic runs are **illustrative settings**, not statements about actual BTC/equity commissions.

### Lean research funnel

Start with one bounded screen on research data. Advance a candidate to a later
research window only when the screen leaves a specific question whose answer
could change the decision. Reserve independent assessment for a frozen candidate
under the later admission gate. The Resource Governor's existing limits apply
at each stage. Count the candidate, controls, and any resampling work in
preflight. Defer work that exceeds the approved budget. Record every variant
that informed selection in the Research Journal.

Base the screen on coverage, incremental value against a simple control, and
estimated costs at the times when the hypothesis calls for a decision. Use
global correlation only as a descriptive measure. For a feature added to an
existing event rule, compare the rule with and without the feature at the same
eligible event timestamps.

For the price-drop signal, register one instrument, one short chronological
research window, one drop threshold, and one holding period before the screen.
For example, hold for 15 minutes from the simulated entry after the first
threshold crossing.
Set minimum event coverage and minimum net and incremental effects before
reviewing results. Detect crossings from completed minute observations with
continuous coverage for the lookback. Use the next eligible execution point.
Compare with entries without a trigger from the same session time bands and
similar prior volatility. Match on information available at entry and use the
same fill, holding, sizing, and cost rules.
The corrected count reference is `PRICE_DROP_V2` in `aqrs.events`: keep the
five-minute, -50-bps crossing and 15-minute hold, but select only earlier
same-hour controls with `control_entry + 15 < event_entry - 5`. Equality is
unsafe because the control exit would use the next open after the lookback's
first close, and those prices can differ even at the same timestamp. Choose the
nearest eligible earlier control using the original prior-volatility criterion.
This excludes the event-defining fall from its control return. Do not exclude
other controls by inspecting their subsequent returns. Unmatched coverage is a
result; do not relax the gap to obtain pairs. This retrospective contrast still
requires a confounding assessment and does not identify a causal effect.
`PRICE_DROP_V1` counts remain historical evidence for that old rule; neither
their five pairs nor their coverage qualify V2 or a future outcome study.
Use the flat policy as the zero-return reference. This rule and its controls
require zero model fits. Report the event count, the number of non-overlapping
holding periods, gross and net return, and the net difference versus the matched
control across the observed time blocks. Account for remaining dependence when
interpreting coverage.

- **Advance** when coverage meets the registered minimum and the estimated net
  return and net advantage over the control clear their thresholds under
  plausible costs. Evaluate the unchanged rule and controls once on a later
  research window to check whether the effect persists.
- **Defer** when sparse events, uncertain costs, or mixed results leave the
  decision open. Name the missing evidence. Schedule a follow-up only if that
  evidence could change the decision and the work fits the approved budget.
- **Stop** when a credible feasibility check rules out the setup, or sufficient
  evidence places its plausible net or incremental effect below the registered
  minimum. Record the reason. A resource stop leaves the evidence unresolved.

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
- **Confirmation budget.** Before starting any protected campaign, record and independently approve a fixed number of confirmation slots, the permitted data scopes (snapshots, instruments and time windows), and the prespecified test family and error-control rule. Block protected execution if this plan is incomplete, the request falls outside it, or the slot budget is exhausted. Apply the existing [slot and exposure rules](ADAPTIVE_QUANT_RESEARCH_PROPOSAL.md#1012-holdout-access-feedback-and-repetition) across campaigns.
- Do not endlessly retest a failed final holdout. Freeze the result and version, revise the hypothesis if necessary, and await genuinely new untouched data for another independent confirmation.
- Store sufficient model/data provenance for reproduction.

## 5. Baselines, ablations and controls

**What does the model improve about a specific baseline rule?** When proposing
a model that changes a rule, name the baseline rule, the decision the model
would change, and the minimum improvement needed to advance. Compare the rule
with and without the model on the same eligible decision opportunities under
the same execution and cost assumptions. Report opportunities skipped by
either variant as well as those where both act.

Minimum controls:

For a filter or long-or-flat policy, fix the complete opportunity population
before comparing outcomes. Include both-act, candidate-only, control-only and
neither-act cases; flat decisions have zero net return and zero costs. Apply
the same execution and position rules and retain the denominator even when
one policy skips. A contrast conditional on both arms acting answers a
different question. M2-E10 now reports both its unchanged legacy paired
movement metric and a separate net diagnostic over all 24 clock hours; the
new diagnostic does not silently replace the original decision rule.

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
- Process execution (`execution_status`), candidate evaluation within the campaign (`evaluation_status`), and scientific evidence for each candidate (`evidence_status`). See the [reporting contract](CONTRACTS.md#g-reporting-contract).
- Positive net performance versus statistical significance; significance versus economic relevance.
- `INSUFFICIENT_EVIDENCE` as a legitimate, often rational outcome.
- A hypothesis being **false** versus a software test failing.

For technical stops, functional failures, missed benefit criteria and inconclusive results, apply the [short diagnosis template](DEVELOPMENT_PROCESS.md#diagnosis-in-existing-records) in the Research Journal attempt record or its linked evidence. Preserve the existing execution and evidence statuses separately. Link functional failures to the development Learning Card or incident review and exclude affected evidence from research decisions. Reassess it only after the correction and the evidence have both been verified.

Use English in reports, schemas, experiment metadata and CLI output. Results must be reproducible on the accepted Linux baseline.

### Research evidence handoff

When an experiment requires new software, Quant Research records the required capability, authorized data scope, fixed scientific constraints, and observable technical acceptance checks in the existing [Test Card](DEVELOPMENT_PROCESS.md#1-write-a-compact-test-card-before-implementation). Engineering selects the technical design within the approved scope. A specific technology is binding when a confirmed requirement or the registered comparison specifies it.

If an implementation constraint would change a predeclared scientific condition or invalidate the comparison, return the issue to Quant Research before dependent work proceeds. Quant Research proposes a revision and retains the original plan and any attempts under the [variant recording rules](#6-multiple-testing-and-research-selection). Route changes to confirmed requirements through [Requirements Engineering](requirements/AGENTS.md). Material changes follow the [existing approval rules](DEVELOPMENT_PROCESS.md#4-learn-and-decide).

Use **quant research mode** to plan or interpret an authorized experiment. Before a run, fix the research question, data scope, baseline and controls, costs, and decision rule in the existing experiment record. After the run, take the technical disposition and evidence references from Engineering or Verification, including the run IDs and any failed checks or limitations. Exclude evidence affected by a technical or functional failure until it has been verified after correction.

Assess the eligible evidence against the predeclared rule. Record the execution status, scientific finding and its uncertainty, and follow-up decision separately in the existing Research Journal attempt or its linked evidence. A replay of the same inputs can support technical reproducibility. The scientific claim still depends on the data, comparison and independence of the evidence. Send defects to Engineering and keep any new run or scope change subject to the applicable authorization and preflight. The [protected evaluation and confirmation rules](#4-out-of-sample-research-validation) continue to govern access and use.

## 10. Exposure and pre-run registration

Before an outcome campaign, register each scientific variant in the [exposure index](../evidence/exposure.json): ID, origin, data window, inputs/horizon/costs, candidate/control relation, fixed advancement and coverage rules, budget and Test Card reference. Count-only screens and manual selections that informed the rule also consume exposure. Keep attempts and platform replays distinct from variants and independent confirmation. Refresh the index and preserved evidence at acceptance; retain incomplete historical knowledge explicitly.

Commit and publish the fixed Test Card and definition separately before the first outcome run; record that revision in the receipt. A later commit does not retroactively prove preregistration, and publication does not make previously explored data independent. Changing a threshold, horizon or cost assumption creates a new registered variant. Sensitivity work needs its own counted plan.

Set minimum non-overlapping coverage and coverage across days/folds before interpreting economic results, with dependence and uncertainty explicit. Zero trades are a valid flat-policy result, not a profitability finding; a minimum count alone never establishes significance. Preserve M2-E14's existing thresholds. January 6 stays protected. Define any future independent confirmation scope and authorization before access under the existing protected-evaluation gate. Do not rotate holdouts to erase exposure or interpret literal authorization fields as observed read counts.

### Precision and claim admission

Before the next outcome campaign, including M2-E14, retain three reviewable
design checks against the frozen source: a known-answer null case that rejects
the historical biased price-drop control, a planted-effect positive case, and
an independent substantive review by someone other than the implementer.
Use the actual selection and evaluation path. A constant price series with no
events does not challenge control selection. Deterministic fixtures test known
answers; stochastic null studies require a separately budgeted error-rate
criterion rather than a promise of zero false alarms. AQRS-A08 supplies concrete
V1/V2 fixtures, not a universal design validator or a completed M2-E14 runner.
That runner must reject missing required design, precision or exposure records
before outcome access; its admission tests remain a prerequisite to execution.

Before an outcome run, state whether the intended decision needs a descriptive
engineering result or evidence about an effect. For the latter, predeclare the
effect scale, eligible population, uncertainty method and credible assumptions
about dispersion and independent units. Raw trade counts, non-overlap and dates
alone do not establish independence. The narrow existing holiday/weekend sample
does not establish regime stability; no broader-market conclusion follows.

`aqrs research precision --sd-bps 20 --effect-bps 2 --independent-units 18`
provides a conditional one-sided normal-mean planning calculation, with default
alpha 0.05 and power 0.8. These are explicit illustrative planning choices, not
an adopted confirmation test. The dispersion must refer to the chosen unit,
such as a paired observation or a day mean. The calculation estimates neither
dispersion nor dependence and does not calibrate multiple comparisons or the
joint M2-E14 gates. A favorable capacity flag never admits a campaign.

Judge planning by whether the declared decision can reasonably be informed
under justified assumptions, not by minimizing the number of inconclusive
results. Adequate power is not a guarantee of detection. Inability to afford a
decisive test justifies deferral of that claim, not rejection of the market.
Record uncertainty and temporal dependence before scientific interpretation;
position sizing at M5 is not a reason to postpone that obligation.

### Descriptive diagnostics and additional exposure

The existing evaluator adds average-tie Spearman association and prediction /
target mean and population standard deviation, both pooled and per fold. These
are descriptive views of the existing fixed-horizon predictions, including flat
decisions. Rank association measures monotonic ordering, not all information,
calibration, net value or causal effects. A constant vector or insufficient
observations yields a null coefficient with an explicit reason. Pooled results
must not hide opposing folds; counts are not independent sample sizes.

Every new diagnostic on previously used market dates is another recorded look,
even without a new model. Register each metric definition and its planned
aggregate/fold/horizon views before execution, bind the source, candidate,
attempt and data window, and retain the views on reruns. The evaluator emits
`diagnostic_exposure` entries; the report, SQLite metrics and evidence index
retain them. Five new metrics over two folds plus the aggregate create fifteen
view records, not fifteen independent observations or models. Synthetic checks
are engineering evidence; registering an unrun definition consumes no market
data. Record manual diagnostic looks as well. Do not silently recompute old
reports: raw prediction arrays are not currently archived, so recomputation
may require a new counted attempt and fits. Additional horizons or instruments
need a registered question and preflight, not an automatic diagnostic sweep.

Broaden time coverage or instruments only against a named missing source of
information. Instrument count does not establish independent breadth; document
synchronization, eligibility, common factors and dependence. Preserve the PCA
panel prerequisites. Before economic claims, qualify costs at relevant times
and sizes; passive fills require joint fill/outcome treatment under section 11.3
of the adopted design. A descriptive signal study may retain illustrative costs
with that limitation; it cannot claim realistic execution value.

For prospective confirmation, publish the frozen rule/code digests, cost and
execution assumptions, candidate family, future window, test and stop rules,
missing-data treatment and result-release plan before confirmation observations
exist. Keep an externally recorded publication receipt; a user-set commit date
alone is insufficient. Preserve every attempt and prevent outcome-driven edits
to that frozen version. Other development may continue separately. This proves
temporal ordering only; it does not waive M1-S, exposure accounting or the
existing protected-evaluation admission requirements.

Keep the movement-scale screen separate from conditional predictability,
forecast accuracy separate from trading activity, and economic effect size
separate from uncertainty. A longer horizon is a counted new variant, not a
way to establish predictability by passing the screen. Sparse or flat results
retain predictive diagnostics but support no economic claim. The raw one-bar
momentum reference is uncalibrated for a longer horizon; retain a suitable
matched predictor, such as M2-E14's one-feature Ridge, for a forecast claim.
Do not lower costs or thresholds merely to obtain trades. A nonnegative input
can have a signed linear association; the synthetic XOR check alone does not
require an interaction term in a real-market model.
