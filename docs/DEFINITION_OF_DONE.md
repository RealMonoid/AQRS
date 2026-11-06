# Definition of Done — AQRS v0.1 (M0)

**This document applies only to the first milestone.** Binding acceptance criteria for **all** development phases through v1.0 are in [`MILESTONE_DOD.md`](MILESTONE_DOD.md); the end-state vision is in [`PRODUCT_VISION.md`](PRODUCT_VISION.md). The current Codex task is to implement **only v0.1**.

This is the M0 acceptance checklist. The current evidence and open release gates are tracked in [`MILESTONE_STATUS.md`](MILESTONE_STATUS.md).

## 0. Development learning loops (required for the build process)

- [ ] The first M0 increment begins with a compact, falsifiable Test Card in `docs/MILESTONE_STATUS.md` or an existing issue: riskiest assumption, baseline, minimal test, predetermined success/failure criteria, development timebox and compute budget.
- [ ] The first M0 changes are planned **backward** from measurable acceptance outcomes to minimum contracts/components/tests, then implemented and tested **forward**. The evidence chain is recorded in the existing loop record.
- [ ] A **qualitative Fault Tree Analysis** is recorded for each of two critical M0 top events: future-data leakage falsely admitting alpha; a calibration campaign exceeding the Resource Governor's hard limits. Credible causal paths lead to observable negative tests. No invented event probabilities.
- [ ] Any actual critical failure or repeated serious defect receives a compact **postmortem** with root-cause uncertainty, timeline, repair, prevention test and a tracked follow-up. **Do not invent an incident** merely to satisfy this checkbox: if no incident occurs, document `NOT_TRIGGERED`.
- [ ] Before revisiting a discarded engineering approach, Codex checks the existing idea ledger (`docs/DECISIONS.md`). Consequential failed ideas are retained with evidence and conditions for reconsideration, without creating separate files.
- [ ] At least one M0 development loop ends with real command/test evidence, an explicit learning result (`SUPPORTED`, `REFUTED`, `INCONCLUSIVE`, or `BLOCKED`), and a clear `PERSEVERE`, `PIVOT`, `STOP`, or `DEFER` decision.
- [ ] Only one development experiment is actively built at a time; each is a small vertical slice, not a multi-feature batch. Expensive research tests are not repeatedly executed without justification.
- [ ] The current status and next smallest assumption are updated in the **existing** milestone-status file; no extra per-experiment documentation or tool subscriptions are created. See [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md).

## 1. Installation and execution

- [ ] `python -m pip install -e '.[dev]'` succeeds in a clean Python 3.11+ virtual environment with no API key or GPU.
- [ ] `python -m aqrs research run --config configs/research.yaml` runs the entire pipeline offline.
- [ ] `python -m aqrs research plan --config configs/research.yaml` shows planned trial/fit counts, estimated runtime, memory and active limits plus an explicit admit/reject outcome **without full training**.
- [ ] `python -m pytest -q` passes.
- [ ] `python -m ruff check .` passes.
- [ ] README documents **actually verified** commands, not intended functionality.
- [ ] Full model catalog and `configs/model_tool_registry.json` remain present, consistent and referenced. **Mentioning complex models does not mean v0.1 must install them.**
- [ ] Clean **native Windows** and independent **Linux** installation and the entire CLI/test sequence pass in CPU-only unprivileged environments (Linux headless). Record both OS versions/builds, Python versions, architectures and capabilities. WSL alone cannot satisfy the native Windows gate.
- [ ] **Permanent English-only policy:** all repository docs, future Codex additions/revisions, code comments, user-visible CLI/log/report text and structured output labels use English. `python scripts/check_language_policy.py --self-test` and `python scripts/check_language_policy.py` pass; modified prose receives manual review. Paths are portable and configurable. See `docs/LANGUAGE_POLICY.md`.
- [ ] **Documentation hygiene:** update canonical docs rather than creating duplicative version/date copies. Maintain exactly one `CHANGELOG.md` with a dated, concise record covering every added, modified, moved or deleted path; manually reconcile its file list with the actual changed-file list. Only retain old version/date details when they cannot interfere with operational behavior.

## 2. Complete vertical data flow

- [ ] Reproducible synthetic OHLCV dataset with seed, interval, scenario and dataset fingerprint.
- [ ] Data quality checks and causal features with correct warm-up.
- [ ] Reference horizon and availability follow `CONTRACTS.md`.
- [ ] At least **two** registered research candidates; Research Manager really selects them deterministically.
- [ ] Candidates and controls are fitted/evaluated on chronological research walk-forward folds.
- [ ] Training labels never extend across validation cutoffs; train-only transforms are tested.
- [ ] Final holdout is reserved and cannot alter research priority.
- [ ] Prediction results and subsequent decisions are reported separately.
- [ ] Trade fills occur **after** signal availability and modeled costs are charged.
- [ ] Include a predictive baseline, a trading baseline and a No-Trade comparison.
- [ ] SQLite Research Journal survives multiple runs, including negative and failed cases.
- [ ] Machine- and human-readable report includes gross/net values and limitations.

## 2a. Resource Governor — mandatory M0 DoD

- [ ] `configs/research.yaml` limits are read, validated and shown in the journal and report.
- [ ] Preflight counts candidates × folds × seeds/variants, **including appropriate baseline fits**, and makes a bounded pilot estimate or openly declared conservative bound.
- [ ] Plans exceeding limits stop **before** full training with `REJECTED_PREFLIGHT` or `BUDGET_EXHAUSTED`; no unbounded retry.
- [ ] Isolated worker/external watchdog **actually terminates** blocking model training on timeout; checking elapsed time afterward is inadequate.
- [ ] Memory policy is observed and enforced through a supported **Windows or Linux** mechanism appropriate to the active platform; if the required guarantee is unavailable the run fails visibly **before starting** (fail-closed). Sampled RSS alone is not presented as a hard kernel memory cap.
- [ ] Campaign wall time and trial/fit/seed/concurrency limits also bind scheduler-created follow-up work; no automatic budget escalation.
- [ ] Journal keeps resource execution states distinct from research evidence; timeout is not treated as alpha rejection.
- [ ] G01–G07 from [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md) are automatically tested; particularly, **do not execute** the 75,000-fit scenario.

## 3. Automated invariant tests

| Test ID | Required outcome |
|---|---|
| T01 | Identical seed/config reproduce market data and research metrics (excluding run IDs/timestamps/wall time). |
| T02 | OHLC invariants, unique timestamps, cadence and missing/nonfinite values are validated. |
| T03 | Modifying future bars does not change features of earlier bars. |
| T04 | Signal-bar features do not know `open[t+1]`, `close[t+1]` or any other future feature. |
| T05 | For `h=3`, entry is `open[t+1]`, exit `open[t+4]`; invalid tail labels are dropped. |
| T06 | Folds are chronological and purged/gapped where labels would overlap boundaries. |
| T07 | Scalers/models fit only on fold training data, never validation/holdout. |
| T08 | For **identical fixed trades/fills**, raising a positive cost cannot improve net PnL. This assertion need not hold when changed costs alter policy selection. |
| T09 | Prediction and trading controls use fair matching time spans, fills and costs. |
| T10 | A flat/long/short-derived simulated order executes only **after** its signal bar becomes available. |
| T11 | Journal retains two runs, candidates, variants, fold metrics and at least one failed/rejected case. |
| T12 | Research Manager cannot read final-holdout outcomes or set final-test-pass status automatically. |
| T13 | Completed negative net outcome is technically `COMPLETED`, never automatically “alpha confirmed.” |
| T14 | End-to-end test creates readable SQLite journal, `report.json`, `report.md`. |
| T15 | Preflight rejects a theoretical eight-year / 75,000-fit plan without running full training. |
| T16 | Blocking worker is terminated before a short configured timeout, and `TIMED_OUT` is journaled. |
| T17 | Memory guard is enforced through a tested supported mode, **or** unsupported required policy is rejected before fitting. |
| T18 | Budget violation never triggers automatic escalation, endless retries or independently double-counted restarts. |
| T19 | Full CLI/test sequence passes on **native Windows 10/11** (normal user, CPU-only) **and** independently on actual headless Linux (Ubuntu 24.04 LTS baseline), non-root, CPU-only; WSL cannot substitute for native Windows. |
| T20 | UTC/timezone, UTF-8 and paths with spaces work on both operating systems; no mandatory WSL, Docker, GUI, admin/root, cloud credentials or network at runtime. |
| T21 | All internal texts and serialized descriptions generated by v0.1 use English. |
| T22 | Worker cancellation, resource enforcement or explicit fail-closed preflight are tested independently on native Windows and Linux; no POSIX-only or Windows-only API leaks into the core. |
| T23 | Runtime/core uses no mandatory provider-specific API, WSL, container or external service; configurable artifacts and journal paths function on both OSes. |

## 4. Research outcome acceptance

- [ ] On the synthetic **null** scenario, the system may honestly report `INSUFFICIENT_EVIDENCE` or `REJECTED`; no forced-alpha exception path.
- [ ] Optional planted-signal scenario may test detection plumbing, without claiming real tradable advantage.
- [ ] Costs, data, baselines and split assumptions are in the report.
- [ ] Candidate/variant counts are retained; no hidden best-of-N search.
- [ ] No broker call or real-money order code in v0.1.

## 5. Required Codex completion report

Codex states:

1. Implemented and deliberately postponed components.
2. Commands **actually executed** and their exit statuses, including **native Windows and Linux environments**.
3. Paths to a generated dataset, SQLite journal and JSON/Markdown report.
4. Reproducibility and integrity checks, including any tests that did not pass.
5. Governor test results: preflight rejection, enforced timeout, memory mode and journal statuses.
6. Evidence that all changed file paths were listed in the sole `CHANGELOG.md` and redundant documentation was avoided.
7. The next **smallest** falsifiable assumption and executable vertical increment, with the observed Build–Measure–Learn result, not a wishlist of ten platform features.
8. The backward acceptance-to-test trace, risk grading, applicable FTA top events/negative tests, incident postmortem links (or `NOT_TRIGGERED`), and rejected-idea check.

**Acceptance means:** a complete, auditable research workflow with working resource limits on the tested **native Windows and Linux** platforms. **It does not mean:** profitable real-market alpha was found.
