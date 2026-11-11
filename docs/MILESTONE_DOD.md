# AQRS — Milestones and Definitions of Done from v0.1 to v1.0

**Status:** Binding target and acceptance specification for Codex. **No milestone has been implemented or accepted solely because this file exists.**

**Current scope:** Use `MILESTONE_STATUS.md` for accepted gates and the experiment queue. Implement only the smallest owner-authorized vertical increment with its own tests and evidence gate.

## 0. Three different meanings of “done”

1. **Technically complete:** the workflow runs reliably, is tested, reproducible, documented and auditable.
2. **Scientifically supported:** the claimed relationship survives prespecified comparisons and suitable independent testing; this can result in a **null/negative finding**.
3. **Economically interesting:** a particular policy demonstrates adequately robust net value under credible execution, risk and cost assumptions. This judgment depends on time and market, and is never a permanent property of the software.

**AQRS can be technically complete without a single economically viable signal.** Positive returns, a fixed Sharpe threshold or a desired win rate are **not release gates**. Positive alpha claims require a **separate evidence-based candidate admission process**.

### Universal DoD for every milestone (all items mandatory)

**Lean software-development contract:** For every substantive vertical increment, follow [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md). Before implementation, predeclare one critical assumption, a discriminating minimal test, evidence threshold, baseline, time/compute budget and stop rule. After implementation, record observed evidence and a `PERSEVERE`/`PIVOT`/`STOP`/`DEFER` decision. **One active development experiment at a time.** Log the current loop in the existing milestone status or issue; do not add a new document for every loop. A refuted/inconclusive hypothesis is not a reason for endless rework or automatic budget expansion. The feedback loop must never contaminate final-holdout research.


**English-only repository policy (permanent):** New and edited documentation, Codex-created files, comments, reports and research artifacts MUST remain in English for every milestone. Read `docs/LANGUAGE_POLICY.md`; run `python scripts/check_language_policy.py --self-test` and `python scripts/check_language_policy.py`, and manually review modified prose. A failed language gate blocks milestone acceptance.

- [ ] **Build–Measure–Learn evidence:** at least one closed Test Card → small build → measured outcome → Learning Card per meaningful milestone increment; outcome and next decision recorded in the existing milestone status or linked issue. No unbounded parallel work or undisclosed repeats.
- [ ] **Backward Development → Forward Execution:** objective, independent acceptance evidence, minimum change and tests are traced backward *before coding*, then forward-built and measured in a bounded vertical slice. Actual acceptance tests match the precommitted criteria.
- [ ] **Risk-based FTA:** critical data-causality, cost/fill, holdout, resource, journal or platform failure modes have a compact top-event/AND–OR/path-to-test review in the existing `RISK_REGISTER.md`; routine changes have an explicit no-FTA risk rationale. Missing critical prevention/regression tests block acceptance.
- [ ] **Incident and failure learning:** material/recurrent incidents receive concise postmortems with evidence and verified recurrence prevention in the existing milestone record/issue; consequential discarded engineering ideas are preserved in `DECISIONS.md` with revisit criteria. No fake incidents or duplicated postmortem files.
- [ ] Working implementation, not empty placeholders, architecture-only text or fake success messages.
- [ ] A documented end-to-end run of the pipeline available to date continues to work.
- [ ] New critical components have automated positive, negative, boundary and at least one adversarial invariant test.
- [ ] Tests and lint are **actually executed**; exits, problems and example artifacts appear in the completion report.
- [ ] No silent change to data/event timing, costs, research rules, benchmarks or final-holdout separation.
- [ ] Dataset, configuration, seed, code/version, candidate version and observed results are traceable.
- [ ] Null findings, failures and deferrals are logged just as successes are; all tested variants remain countable.
- [ ] Every new algorithm has appropriate simple baselines and a benefit criterion fixed before comparison.
- [ ] **Compute-budget preflight** counts planned models/trials/fits/folds/seeds and reports estimated wall time, RAM and approved limits; an active Governor enforces limits and records termination. Tests: `RESOURCE_GOVERNOR.md`.
- [ ] README, `ARCHITECTURE.md`, `DECISIONS.md`, research protocol and changed contracts describe **implemented** behavior rather than intentions.
- [ ] No real-money order or unapproved broker write permissions; access to a new data source is not trading authorization.
- [ ] Milestone has explicit `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED` or `ACCEPTED`; missing tests never imply acceptance.
- [ ] Documentation, code comments, experiment metadata, logs and reports are in **English**; avoid language drift across new artifacts.
- [ ] Documentation is **lean and current**: canonical files edited in place, no needless duplicate or date/version-suffixed documents; exactly one root `CHANGELOG.md` lists the date, reason and **every changed file path** (including added/deleted/renamed paths). Dates/old versions do not disrupt active contracts or functionality. Check coverage against the actual diff.
- [ ] Fresh **native Windows** and independent **headless Linux**, CPU-only execution are demonstrably supported. Record OS/build or distro, architecture, Python, permissions and resource enforcement capabilities for each; portable paths and UTC are tested.

**Release rule:** A milestone is accepted only after its gate passes, evidence (test log, run ID and artifacts) is recorded, and a human-readable acceptance review is made. Optional/rejected models may remain absent when no incremental value is demonstrated.

---

## M0 — v0.1: Walking Skeleton

**Goal:** demonstrate on an ordinary CPU computer a complete, fully offline, reproducible research path, without asserting genuine market alpha.

**Deliverables:** synthetic OHLCV; quality checks; causal features; at least two candidates; early economic cost gate; simple forecast/trading/No-Trade baselines; chronological walk-forward research folds; separate long/short/flat decision with next-bar execution; SQLite journal; JSON/Markdown report; CLI; **enforced Resource Governor with preflight, timeout, memory, trial and fit limits**; tests and portable Windows/Linux packaging.

**Gate:** The numbered checklist in [`docs/DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md) is the detailed binding M0 specification. Additionally `docs/MODEL_TOOL_CATALOG.md` and `configs/model_tool_registry.json` must be consistent, readable and versioned; no advanced model is installed merely because it is cataloged.

**Pre-build risk proof:** M0 documents two compact qualitative FTAs: (a) a future-information leak can falsely admit a signal and (b) an over-budget campaign starts or continues despite planned limits. Associate each material path with a specific test or guard. A rejected over-budget plan is a *prevention success*, not an invented incident. A triggered material failure requires a postmortem before release acceptance.

**Acceptance evidence:** installation and `research plan` CLI, refusal of oversize plan, **actual blocked-worker termination, safe memory-enforcement/fail-closed test**, full CLI research run, pytest and lint exits, `report.json`, `report.md`, persistent SQLite journal, second reproducible run and negative/failure records. Test on **native Windows and headless Linux** separately, without runtime administrator/root privileges or GPU.

**Explicitly excluded:** real market data, brokers, RL, transformers, profitable-real-backtest claims, autonomous agents, a full platform UI.

---

## M1 — v0.2: Real market data and market feasibility

**Goal:** correctly process a **deliberately selected real market**, without converting bad data into spurious alpha.

**Deliverables:** adapter for at least **one** lawfully accessible historical source; versioned data manifest; documented venue/instrument/time semantics; quality checks for timestamps, timezone, duplicates, missing bars, sessions/halts, prices/volume and applicable splits/corporate actions/rollovers/funding events; documented market/data-cost suitability.

**Definition of Done:**

- [ ] One real dataset can be imported and stored locally with reproducible results; provenance, use/license terms, retrieval date, symbol and source version are recorded.
- [ ] Reproducible data-quality report covers coverage, gaps, duplicates, out-of-order records and invalid prices/values; at least one intentionally damaged dataset is rejected or quarantined visibly.
- [ ] Timezone, trading-session and instrument semantics are specified in a `MarketDataContract` or comparable structure.
- [ ] Synthetic and real adapters fulfill the same research-data interface; the v0.1 analysis modules run on the real source **without source-code modifications**.
- [ ] Real-market costs/fill assumptions are labeled *estimated*, *measured* or *unknown* rather than treated as guaranteed.
- [ ] Inadequate coverage or unsuitable horizons are surfaced as research risks, not silently interpolated away.
- [ ] At least one end-to-end run on **real historical data** is archived. Negative findings are accepted.
- [ ] The first archived real-data run records separate elapsed times for import, feature calculation, and execution simulation within its approved budget. If measurements identify repeated feature calculation as a bottleneck, evaluate computing shared causal features once per run. Verify equivalent outputs, preserved fold and holdout boundaries, and lower elapsed time before adopting reuse.
- [ ] Before DeepLOB/FinBERT/GNN or other input-specific pilots, a catalog prereq audit documents whether order-book/text/multi-asset data, licenses and correct timestamps exist. Missing input leads to `BLOCKED_DATA`, not invented observations.
- [ ] Clean native Windows and headless Linux runs persist the real-data artifacts and respects ordinary CPU/memory budgets.

**Continuation gate:** valid real-market data and time contract for at least one research market; **no alpha claim required**.

---

## M2 — v0.3: Alpha Discovery with genuine controls

**Goal:** develop testable candidates from both research questions and data-driven search, **not only optimized backtest configurations**.

**Deliverables:** candidate registry with hypothesis/target and mechanism or exploratory origin; at least two **different** small research families (e.g. rule-based event study and supervised predictive feature study); basic statistical/ML baselines; initial ranking/feature analysis; ablations and condition-matched controls; early net-cost tests.

**Definition of Done:**

- [ ] One campaign generates at least two versioned, interpretable alpha **candidates** from real data, even if they are all rejected.
- [ ] **LightGBM supervised challenger** and **Isolation Forest unsupervised hypothesis generator** each have a reproducible bounded pilot compared with a simple baseline; anomaly score is not alpha. A genuine blocker keeps the gate `BLOCKED`, never fakes a pass.
- [ ] **XGBoost, HDBSCAN, PCA, autoencoders and Random Forest** have model cards and either a fair bounded pilot or an explicit `BLOCKED_*`/`DEFERRED`/`REJECTED` decision with objective rationale/revisit trigger. CatBoost, GMM, K-Means, HMM and other `CONDITIONAL` entries stay registered without compulsory adoption.
- [ ] Each candidate records whether its hypothesis was preregistered or discovered from data, as well as horizon, inputs and their availability timestamps.
- [ ] Each new signal records the observable event or decision condition, its detection rule and its observation cadence under the [research protocol](RESEARCH_PROTOCOL.md#define-new-signals-around-the-event-under-study).
- [ ] The rule-based event study demonstrates a [bounded screen](RESEARCH_PROTOCOL.md#lean-research-funnel) with matched controls, early cost estimates, and a recorded advance, defer, or stop decision.
- [ ] Forecast value is compared with a trivial predictor and suitable simple model baseline on the same chronological research folds.
- [ ] Descriptive signal diagnostics include flat policies and separate fold views; every new diagnostic on reused data is recorded as additional exposure. Before outcome access, verify the biased-design self-test, planted-effect check, justified precision plan and independent substantive review under the [admission protocol](RESEARCH_PROTOCOL.md#precision-and-claim-admission). Synthetic checks do not establish market evidence.
- [ ] A candidate→decision control demonstrates that apparent value is not simply a known market filter; e.g. volume+downtrend against downtrend alone.
- [ ] At least one negative control (e.g. time/block-preserving placebo or condition-matched random entry) can identify a deliberately misleading correlation.
- [ ] Costs, turnover, effective independent event count and tried-variant count are visible per candidate.
- [ ] Adversarial causal tests show future observations cannot alter earlier features/decisions.
- [ ] Null/negative data run without forced positive selection; a planted synthetic effect can be distinguished from the null as a **software positive-control test**, without claiming real-market profits.
- [ ] The supervised/unsupervised pilots install and execute under their declared Windows/Linux/CPU/memory budget or are transparently blocked with evidence.

**Continuation gate:** discovery and matched controls work reproducibly; **no promise of finding a profitable real-world candidate**.

---

## M3 — v0.4: Adaptive, budget-aware research management

**Governor expansion:** M0's hard limits now apply centrally to every research family and adaptive scheduler. Adaptive policies may allocate budgets but **never increase them autonomously**. Compare against deterministic scheduling under the same resources.

**Goal:** select and justify which experiments receive the next available compute budget.

**Deliverables:** research-family registry, candidate queue, effort/cost model (CPU, data acquisition if relevant, attempt counts), explainable priority, cheap→expensive stages, exploration reserve and reversible deferrals/reactivation. Only permitted **research feedback** is used.

**Definition of Done:**

- [ ] User sets a finite campaign budget; studies stop predictably at exhaustion rather than running until all possible hypotheses are tried.
- [ ] At least three research families are managed. Each priority choice records its reasoning and admissible time-bounded evidence.
- [ ] An unsuccessful family can be `DEFERRED`; new data, changed economics or exploration allocation can reactivate it. No arbitrary permanent blacklist.
- [ ] Candidate/variant counts, aborted attempts and resource consumption remain visible in the journal.
- [ ] Controlled replay demonstrates reproducible priority/stop/registration decisions under identical inputs.
- [ ] Evaluate Successive Halving or comparable staged screening against a fixed equal-budget approach, considering regime and selection bias. Optuna/bandits remain optional if they add no demonstrated value.
- [ ] A **simple static scheduler** is the comparison. Evaluate adaptation on compute cost, quality of allowable research findings, exploration coverage and selection distortion.
- [ ] If reliable improvement is absent, keep **deterministic** scheduling as production default. Bandits/Bayesian Optimization are not mandatory.
- [ ] Automated test proves scheduler cannot access or reward itself on final-holdout outcomes.
- [ ] Resource controls continue to work on supported Windows/Linux worker processes, including rejected expensive scheduling plans.

**Continuation gate:** bounded, explainable research with correct feedback separation, **not** maximum tests per hour.

---

## M4 — v0.5: Rigorous statistics and independent candidate admission

**Validation budget:** Nested CV, bootstrap, permutation, seeds, cost and regime stress must be planned as explicit fits/simulations, not launched as an unapproved Cartesian product. Exhaustion means `INSUFFICIENT_EVIDENCE`, not endless extra tests.

**Goal:** explicitly control uncertainty, data snooping, time dependence and multiple comparisons; technically separate **research selection** from a **controlled final evaluation**.

**Deliverables:** immutable candidate freeze with dataset/code/config/model hashes; purged/embargoed walk-forward or nested validation where warranted; meaningful uncertainty intervals (e.g. block bootstrap); multiple-testing/reality-check method appropriate to the hypotheses; condition-matched placebos; final gate and audited access.

**Definition of Done:**

- [ ] A candidate can be frozen into an **immutable version**. Features, model, policy, costs and selection criterion are locked **before** final evaluation.
- [ ] Final testing is isolated from the normal scheduler. Holdout access is tracked **across candidates and campaigns**, because evaluating many different finalists on one set consumes independence. Repeated access cannot count as new evidence or feed later optimization.
- [ ] Each protected campaign has an approved [confirmation budget](RESEARCH_PROTOCOL.md#4-out-of-sample-research-validation) before it starts. Demonstrate rejection of incomplete plans, out-of-plan requests and exhausted slot budgets before protected data access.
- [ ] Before any real protected evaluation, pass the M1-S security acceptance in the [adopted adaptive research design](ADAPTIVE_QUANT_RESEARCH_PROPOSAL.md#m1-s-technical-isolation-and-sealed-evaluation). Use synthetic secrets in the actual isolated test environment. Verify the external authority boundary, time-limited inputs to candidate code, controlled result release and exposure tracking with SEC01–SEC24. Without verified isolation, keep protected evaluation synthetic and report `ISOLATION_NOT_VERIFIED`. M1 source and import feasibility work can use authorized development data.
- [ ] Adversarial tests show purging/embargo and train-only fit prevent target overlap, preprocessing or feature knowledge leaking into OOS periods.
- [ ] Uncertainty handles serial dependence; effective independent sample size, blocks or market episodes are documented.
- [ ] Registry/trial count includes attempted LightGBM, XGBoost, autoencoder, HDBSCAN and other variants, not just winners.
- [ ] Implement a **precommitted multiple-testing control** suited to the number/type of comparisons, verified against null/control data. Not every statistical technique must be implemented, but the selected one must be justified and tested.
- [ ] On known synthetic null processes, assess false-positive behavior against a **predefined** significance target and documented Monte Carlo tolerance. Perfect zero false positives are not required.
- [ ] End-to-end example demonstrates both passing and rejected/inconclusive scientific statuses, without real-profit claims.
- [ ] Failed final test does not trigger covert retuning on the same final observations. Further work becomes a **new research hypothesis** requiring new independent later evidence.
- [ ] All statistical resampling work is Resource-Governor-bounded and reproducible on Windows and Linux.

**Continuation gate:** candidate can be examined and rejected without exhausting the independent test set; **holdout consumption is audited**.

---

## M5 — v0.6: Cost-, risk- and decision-aware trading policy

**Goal:** determine whether a forecast actually justifies a trade **under realistic constraints**, rather than mapping every positive directional prediction to a buy.

**Deliverables:** separate decision policy; flat/wait as real alternatives; exposure and risk limits; predicted net benefit including turnover; existing positions; market/time/size-aware costs where data permit; stress-tested execution simulation and incremental cost/risk ablations.

**Definition of Done:**

- [ ] For the same forecasts, reproducibly distinguish **Long, Short and Flat** using documented costs, risks and current position constraints.
- [ ] Decisions use prices/estimates available at that moment; fill rules and possible nonexecution are transparent in the chosen simulator.
- [ ] Position, turnover, entry/exit, exposure and all applicable costs appear separately in the trade/decision ledger. Perpetual funding is event-time-based, not a flat fee on every 15-minute trade.
- [ ] At least one independent hand-calculated test and adverse scenarios (higher spread/slippage, worse fills, illiquidity) match the simulator or show explicitly justified conservatism.
- [ ] Minimum risk controls: position caps, exposure budget, drawdown monitoring and safe `flat`/`pause` action. Limits are configurable, not arbitrary permanent constants.
- [ ] Qualify market/time/size-specific cost assumptions against available observations and conservative stress cases. Passive-order claims address fills and subsequent outcomes jointly; lack of suitable quotes or depth remains an explicit limitation.
- [ ] Active policies are compared with `no-trade` and a simple policy under matching cost and risk conditions. Complexity must justify itself incrementally.
- [ ] Reports separate forecast quality, simulated realized gross/net PnL, execution costs, risk and uncertainty. Simulated fills are not guaranteed actual fills.
- [ ] Native Windows and Linux headless execution remain reproducible and within approved resource limits.

**Continuation gate:** transparent, testable net-value and risk decisions; **no broker**.

---

## M6 — v0.7: Shadow/paper monitoring and alpha lifecycle

**Recalibration guard:** monitoring may pause or request review, but never automatically retrain recursively without a new registered candidate version, authorization and compute budget.

**Goal:** after research/final evaluation, track, pause and retire a frozen candidate on **new** data without real money.

**Deliverables:** read-only incoming observations (live, delayed or incrementally delivered), forecast and paper-trade ledgers, predicted-versus-observed reports, signal quality/cost/liquidity/risk monitoring, lifecycle statuses and precommitted pause/review/retire rules.

**Definition of Done:**

- [ ] A **frozen** candidate processes only fresh real observations available at each moment, recording each forecast with `generated_at` and `available_at`.
- [ ] Shadow/paper decisions can be compared with later realized outcomes; parameters/model cannot silently change during monitoring.
- [ ] Backtest and shadow processing reuse the same frozen signal and decision functions. Batch and incremental replay of identical timestamped observations produce matching decisions; test warm-up, missing/duplicate data and restart behavior before fresh-data monitoring.
- [ ] Monitoring distinguishes at least four cause families: prediction/calibration drift, cost/spread deterioration, regime/data shift, and risk/drawdown deterioration. An alert does not automatically prove “alpha decay.”
- [ ] Predefined `WATCH`, `PAUSE`, `REVIEW`, `RETIRE` and controlled-resume transitions have recorded rationale.
- [ ] Simulated normal operation, gradual drift, abrupt cost changes and data outages trigger expected states; missing data do not generate fake trades.
- [ ] Incoming shadow/paper data are not retroactively labeled as old unconsumed final holdout. Retuned candidate gets a new version and fresh independent review.
- [ ] No broker write connection or real-money order route. “Paper” means simulation or read-only observation.
- [ ] Process can run/restart headlessly on Windows and Linux without autonomous retry/calibration loops or duplicated experiment evidence.

**Continuation gate:** independently monitored candidates can be paused/retired reliably. If no real candidate qualifies for paper monitoring, a clearly labeled test candidate may demonstrate the software lifecycle.

---

## M7 — v0.8: Operations, resource management and usability

**Operational expansion:** measured hardware profiles, preflight prediction accuracy, controlled process termination, resume without counting duplicated trials and memory-efficient reporting are verified on the native Windows reference PC and a headless Linux deployment target.

**Goal:** one technically capable user can operate and audit campaigns on a native Windows mid-range PC or a provider-neutral Linux server without source-code changes for routine actions.

**Deliverables:** stable CLI for market/campaign/candidate/journal/report workflows; clear statuses/errors; validated configuration; logging; interruption/resume handling; bounded RAM/runtime; local storage; evidence export; optional small read-only viewer, **not a dashboard requirement**.

**Definition of Done:**

- [ ] Fresh install from documented dependencies works without proprietary account, GPU or mandatory cloud.
- [ ] Start/status/results, freeze, final-test gate, journal export and monitoring are available through documented CLI without editing code.
- [ ] Controlled abort/restart preserves journal and **does not silently count repeats as independent findings**.
- [ ] Maximum measured wall/CPU/RAM and preflight estimate error are reported under a documented reference budget; no unsupported speed/hardware promise.
- [ ] Logs/reports retain reproducible version/data references; feed, model or report failures cause visible states instead of fabricated results.
- [ ] Read-only feed credentials (if any) do not appear in Git, logs or reports; broker write credentials are not permitted.
- [ ] Operations guidance describes complete research/review workflow and troubleshooting on fresh native Windows and Linux machines.
- [ ] Provider-neutral Linux server instructions cover virtualenv, configurable storage, OS process supervision, restart, backup/restore and an optional container path (Hetzner or any comparable VM). No mandatory cloud SDK or container runtime. Container runtime remains optional.
- [ ] English CLI help, diagnostics and reporting; no GUI or root requirement in normal operation.

**Continuation gate:** a documented, reliable local research tool for one technically capable user.

---

## M8 — v0.9: Integrated scientific beta / end-to-end evidence

**Resource negative test:** an intentionally proposed multi-year calibration is rejected in preflight before fitting; timeout/RAM/validation budgets and retry guard are checked in an integration run.

**Goal:** verify the **entire research lifecycle**, not just modules, under controlled end-to-end scenarios.

**Deliverables:** integrated regression tests, simulated negative/positive/shifting regimes, complete real-data campaigns, freeze/final/monitor lifecycle tests, data/decision boundary audit and updated documentation.

**Definition of Done:**

- [ ] At least **three reproducible demo campaigns** run: (a) synthetic null without forcing alpha, (b) labeled synthetic planted signal as a positive control, (c) real historical market with no required profitable result.
- [ ] One fully documented campaign shows *data → discovery → priority → costs/controls → validation → journal → candidate status*.
- [ ] Constructed technical test drives a candidate through *freeze → final gate → paper/shadow monitoring → pause/review*, without claiming genuine market alpha.
- [ ] All adversarial tests for temporal leakage, multiple-test selection bias, incorrect costs, data gaps and prohibited final-holdout feedback pass.
- [ ] A `model_registry_audit.json` (or equivalent journal export) includes a `ADOPTED`/`REJECTED`/`DEFERRED`/`BLOCKED_*` decision, gate, rationale and optional pilot ID for **every** entry in `configs/model_tool_registry.json`; no silent omission.
- [ ] At least one supervised (e.g. LightGBM) and one unsupervised (e.g. Isolation Forest) discovery variant **actually execute** under the supported data contract. Unsupervised output is tested for incremental prediction, not relabeled alpha.
- [ ] Default research-priority approach is transparently evaluated against simpler static allocation; unproven adaptive methods remain optional.
- [ ] An external reader can reconstruct **which** variants were tested, **why** they were rejected, **what** data each model saw and **which** independent tests have been consumed.
- [ ] No unresolved critical bugs capable of corrupting PnL, availability, costs, holdout separation or journal history. Noncritical issues are documented.
- [ ] Full native Windows and headless Linux clean-machine, unprivileged run demonstrates valid resource preflight, worker termination, reports and portable artifact paths.

**Continuation gate:** integrated, tested real-data research/monitoring workflow with credible scientific provenance.

---

## M9 — v1.0: Locally deployable Adaptive Quant Research System

**Binding boundary:** no unbounded calibration/reoptimization. User-set budgets, real-time resource status and auditable stop/defer decisions are core product capabilities.

**Goal:** a single user, without a participating developer, can design and run **new** real-data campaigns, decide what deserves further study, independently evaluate frozen candidates and paper-monitor them on new data.

### Product Definition of Done (all mandatory)

- [ ] **End-to-end:** gates M0–M8 are `ACCEPTED`; users can configure and run a new campaign from the documentation and CLI.
- [ ] **Real data:** at least one documented, legally usable market/instrument data contract; audit and data-versioning run without manual code patches.
- [ ] **Models/tools:** catalog/registry complete and reviewed; at least one supervised and one unsupervised discovery workflow run. Unadopted models (including autoencoders, HDBSCAN, DeepLOB, transformers) have explicit documented gate/status decisions.
- [ ] **Discovery:** hypothesis-driven **and** data-driven candidate families share the same research interface; every candidate is versioned, testable and allowed to fail.
- [ ] **Costs/risk/decision:** forecasting, net opportunity, current position, cost/risk policy and simulated fills are separate. `flat` and `pause` are first-class actions.
- [ ] **Validation:** chronological and appropriately purged folds, matched controls and a one-time audited final test are technically/procedurally isolated; search correction accounts for multiple tests and dependence.
- [ ] **Research Manager:** finite experiment budgets, revisitable priorities, exploration reserve and full attempt counter work. Adaptive selection is evaluated against a fixed baseline rather than asserted better.
- [ ] **Monitoring:** at least one technically demonstrated shadow/paper lifecycle with forecast/cost/risk drift states and predefined pause; no broker write operations.
- [ ] **Journal:** provenance, model/policy versions, all attempts and failures, costs, research choices, holdout consumption and monitoring states are continuously auditable.
- [ ] **Reproducibility:** install, null, planted-positive-control and real-data campaigns reproduce their essential metrics in a documented CPU environment.
- [ ] **Quality/safety:** critical adversarial tests pass; observed resource consumption fits declared single-machine budgets; no accidental broker permissions or alpha guarantees.
- [ ] **Windows/Linux and English:** fresh native Windows and independent non-root headless Linux setups pass complete CLI/tests; stored artifacts survive restart and path changes; logs/reports/CLI/documentation remain English; OS-level memory/timeout behavior is accurately documented and enforced or blocked.
- [ ] **User guidance:** README, architecture, data/research contracts, examples, operations guide, limitations and release notes match the code.
- [ ] **Acceptance evidence:** v1.0 release bundle contains actual test logs, demo run IDs, real-data campaign (even when no alpha found), accepted gates, residual risks and deferred features.

**Final result:** *A working research product capable of finding, falsifying, prioritizing, independently evaluating and paper-monitoring alpha candidates without risking real capital.* **Not:** *a guaranteed money machine*.

---

## 10. Candidate gates (independent of software releases)

AQRS can be v1.0 even when all alpha candidates fail. That is intentional. Each candidate has its **own** lifecycle:

| Candidate status | Entry condition | Allowed next action |
|---|---|---|
| `IDEA` | Research question, data and horizon recorded | Cheap feasibility screen |
| `SCREENED` | Data, cost and first baseline are plausible | Research validation |
| `RESEARCH_TESTED` | Research folds/controls logged including negative results | Reject, deepen, or freeze |
| `FROZEN` | Model, features, policy, costs, selection criterion and version fixed | Single independent final evaluation |
| `FINAL_EVALUATED` | Final test run and dataset access consumption logged | Reject or, if eligible, paper monitoring |
| `PAPER_MONITORED` | Fresh data without real money; predictions/decisions/outcomes logged | Watch, pause, review |
| `PAUSED` / `RETIRED` | Precommitted rule or substantiated observation | Do not trade; possibly new research ID/version |

`RESEARCH_TESTED` and `FINAL_EVALUATED` do **not** mean “profitable.” Keep lifecycle status and evidence verdict separate.

**Necessary checks before a positive alpha claim:** incremental value beyond suitable baselines and condition-matched controls; conservative net economics; meaningful effective sample size; independent time periods; accounting for all selection attempts; plausible market mechanism or documented uncertainty; cost/regime robustness; no repeated optimization against final test. If unmet, reject or mark inconclusive; **do not “rescue” the hypothesis with endless extra filters**.

## 11. Project governance and change control

- **Authorization:** Use the milestone status for completed gates and experiment start conditions. Future gates guide extension points and deferred decisions.
- **After every gate:** choose the next smallest complete vertical increment. No obligation to deploy all cataloged models if simpler methods achieve the same scientifically supported function.
- **Changes:** substantive alternatives require a recorded ADR with rationale, risks, baseline and revised acceptance test. Never secretly move the goalposts to pass tests.
- **Blockers:** dataset licenses, real venue rules and execution contracts cannot be invented. Real-data gates stay `BLOCKED` if real inputs are missing; synthetic examples prove technical plumbing but not those gates.
- **Optional post-v1.0:** live order execution would be a **new, explicitly authorized product** with its own safety, financial and operational requirements, separate from this roadmap.
- **Language/platform:** future Codex changes remain English, native-Windows- and Linux-compatible by design, and provider neutral. Treat a failed Windows or Linux acceptance gate as open work, never as a minor cosmetic issue.
