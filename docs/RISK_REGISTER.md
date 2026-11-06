# AQRS — Project risks and mitigations

**Status:** Qualitative risk hypotheses, not claimed empirically measured probabilities. Reassess priorities after milestones and when new evidence arrives. The previously discussed “99% failure rate” is **not** an established AQRS metric. R-01 through R-06 are the six original research/compute risks; R-07 adds cross-platform portability.

| ID | Category | Failure mode | Early warning | Mitigation / stop criterion | Acceptance gate |
|---|---|---|---|---|---|
| R-01 | Research economics | No after-cost economically exploitable alpha exists in the investigated data. | Predictors fail matched/zero/momentum controls; net edge is below realistic costs. | Stop tuning; revisit market/data hypothesis. “No alpha” is a legitimate software output. | M1–M5 |
| R-02 | Scientific validity | Research Manager prioritizes lucky correlations and generates false alpha. | Excellent in-sample results, weak OOS performance, many variants, low effective count of independent events. | Count trials, matched controls, train-only fits, chronological folds, multiple-testing control and isolated holdout. | M0, M2, M4 |
| R-03 | Data and execution | Data, timestamps or cost model do not resemble actual executability. | Unexplained volume spikes, missing bars, optimistic next-bar fills, changing spreads/slippage. | Source/license audit, market/venue contract, time-aware costs and execution stress; `INSUFFICIENT_EVIDENCE` on unreliable inputs. | M0, M1, M5 |
| R-04 | Compute explosion | Cartesian model/parameter/fold/seed searches run for months or years. | Exploding fit count, large preflight estimates, unbounded grids. | Resource Governor with fit/trial/wall/RAM/campaign limits and bounded pilot; reject in preflight. | **M0**, M3 |
| R-05 | Validation explosion | Nested CV, bootstrap, permutation, cost and regime variants multiply uncontrollably. | Validation consumes more than authorized campaign budget; final holdout queried repeatedly. | Cheap staged screens first, explicit statistical-validation budget, report insufficient evidence rather than running indefinitely. | M3, M4 |
| R-06 | Recalibration loop | Retuning, restart and retesting recur after every miss. | Growing retrain chains, repeated trial IDs, no terminal state. | Terminal statuses, `auto_retry_count=0` at M0, no unapproved budget increases/restarts, controlled pause. | **M0**, M3, M6 |
| R-07 | Platform portability | Core implementation works on the developer's Windows PC but fails on a Linux VM (or vice versa); resource guards become no-ops. | OS-only imports, shell-specific paths, runtime WSL/Docker requirement, worker grandchildren survive cancellation, missing RAM guard. | Native Windows and independent Linux CI/run gates, portable paths, platform adapter with capability preflight, honest fail-closed status; provider-neutral deployment audit at M7. | M0, M7, M8–M9 |

## Keep business and technical outcomes separate

A failed/no-alpha research hypothesis is **not** a software failure if its test was implemented and executed correctly. Conversely, clean code and a completed backtest are **not** scientific validation. A resource-aborted trial cannot be used as evidence for or against alpha.

## Research management, not rigid bans

Repeated failures may lower a research family's priority, but a changing market, improved data or cost structure can justify reconsideration. No universal prohibition such as “never research sub-15-minute signals when average spread exceeds 0.05%” is authorized; feasibility depends on the *net conditional edge* and specific execution assumptions.

## Procedure for a new risk

Assign an ID, owner, observable trigger, budget/stop rule, proposed test and affected milestone; add it to this registry and the relevant release gate. Record evidence rather than inventing precision. If the risk requires a changed norm, add an ADR to `DECISIONS.md`.

## Mandatory Fault Tree Analysis (FTA) for critical development changes

Fault trees here are **qualitative engineering guards**, not numeric failure-probability predictions. They are written before implementation when a critical contract changes and rechecked after a material incident. The source of truth for thresholds is [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md). Codex keeps FTA findings **in this existing risk register** and links the active Test Card rather than generating separate fault-tree documents.

| Top event | Illustrative credible top-level causal paths (refine against implementation) | Required control / observable negative test | Linked risks |
|---|---|---|---|
| **FTA-M0-A: falsely admitted alpha due to future knowledge** | Future-derived feature **OR** overlap-contaminated training label **OR** future-fit transform **OR** final-holdout feedback used to select a candidate. | Future-bar perturbation must not alter earlier features; purged folds, train-only transforms and holdout access-control tests must fail closed on planted leakage. | R-02, R-03 |
| **FTA-M0-B: over-budget campaign launched or allowed to continue** | Missing/inaccurate preflight **OR** worker timeout not actually enforced **OR** memory guard unavailable but bypassed **OR** a retry loop independently launches more work. | Extreme 75,000-fit plan rejected before fitting; worker killed on timeout; unsupported required RAM protection blocks launch; no automatic budget escalation or retries. | R-04, R-05, R-06 |

Actual logical AND dependencies and minimal single-point paths should be derived when the relevant implementation exists, not confidently invented in advance. If a control failure is found, the linked milestone remains blocked until the protective regression test passes. Postmortems for significant incidents follow the existing milestone record / issue workflow, with prevention steps and recheck criteria.

### M0 implementation controls

- **FTA-M0-A.** A false admission can follow an offline leak (future input OR an out-of-window label OR a transform fitted outside training) AND reuse of the contaminated result as evidence. A separate path is a holdout value entering model selection or evaluation. Build features from trailing bars only, physically cut off the holdout before labeling, enforce strict exit-before-boundary inequalities, and pass only training slices to fitting. Perturb future bars, check exact open indices, test a holdout mutation against research rows, and inspect fitted training statistics. Keep synthetic evidence inconclusive.
- **FTA-M0-B.** Over-budget work can start if preflight miscounts fits OR permits unsupported containment. A running trial can escape limits if the watchdog fails OR descendants outlive termination OR a required memory mode is bypassed. Repeated launches also require a failed attempt AND an unguarded retry or duplicate reservation. Reject extreme fit counts and unsupported memory modes, gate worker entry until supervision attaches, test blocking and memory-pressure workers with descendants, and check the persistent attempt ledger for retry/identity behavior.
- **M0 cost and persistence risks.** An early fill, missing cost component or unequal control policy can fabricate economic value. Test fixed trades with increased costs, matching controls and exact fill indices. A crash between reservation and result can erase a failure or duplicate evidence if the scheduler relaunches it. Reserve in SQLite before worker entry, update terminal status transactionally, preserve nonterminal interrupted records and use a stable evidence key. Exercise rejection, timeout and repeat campaigns.
