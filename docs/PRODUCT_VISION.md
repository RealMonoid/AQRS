# AQRS — Product vision and desired v1.0 end state

**Permanent language rule:** AQRS documentation, research outputs and every future Codex addition or revision are English-only. See [`LANGUAGE_POLICY.md`](LANGUAGE_POLICY.md). This is a product-wide acceptance requirement.

**Status:** Binding north-star product specification. This is **not** an instruction to implement every future feature during v0.1. See [`MILESTONE_DOD.md`](MILESTONE_DOD.md) for separately accepted increments and acceptance criteria.

## 1. What we ultimately intend to build

**AQRS is a locally usable, resource-bounded, scientifically controlled research instrument for short-horizon systematic trading, built first for native Windows with verified Linux portability and no cloud-provider lock-in.** One researcher can use legally acquired market data to discover previously unspecified predictive structures, test their net economic feasibility, challenge alternative explanations, allocate research resources deliberately, and monitor reviewed candidates on new observations.

The primary output is an **auditable research decision**, not automatic buy/sell advice: *reject, defer, investigate, accept as a research finding, submit a frozen version for one controlled final review, observe in shadow/paper mode, pause, retire*.

**v1.0 is a functioning alpha-research platform, not live trading software and not a profitability guarantee.** It is a perfectly valid product outcome if **no candidate survives** plausible costs and strong controls.

## 2. The experience from a user's perspective

By v1.0, a single user can operate AQRS locally through a CLI (with an optional simple read-only interface):

1. **Select a research universe:** market, venue, instrument, data availability, candidate horizons, budgets and cost assumptions. Every real instrument has a documented data/trading contract. Old data from 2003 are not presumed predictive for today's intraday market.
2. **Audit data:** coverage, timestamps, gaps, unusual observations, market sessions, corporate actions/contract rollovers where relevant, licenses and provenance. Invalid inputs block affected experiments.
3. **Launch a bounded campaign:** hypothesis-driven and data-driven methods search for **incremental conditional predictive information**. Unusual observations alone do not equal alpha.
4. **Follow the evidence trail:** every candidate has an immutable ID, feature availability timestamps, prediction horizon, cost model, baselines, matched controls, chronological research folds, variant counts and evidence status.
5. **Allocate research fairly:** the Research Manager does not rank candidates by prettiest historical backtest. It considers compute effort, uncertainty, independent research-validation evidence and a modest exploration budget. Deferred families can be revisited.
6. **Make forward-looking decisions:** forecasting and trading policy are separate. A cost/risk rule may choose *long, short, flat or wait*. Current position, turnover, exposure, liquidity and execution assumptions matter; there is no obligation to trade.
7. **Freeze and assess candidates:** after a documented research process, an immutable candidate version may be submitted to a **controlled independent final test**. Final data never flow back into ongoing model selection or scheduler rewards. **Many different final candidates** can collectively overuse the same holdout; therefore access must be tracked globally across campaigns and repeated usage must not be treated as new independent evidence.
8. **Monitor candidates:** accepted candidates first run as shadow/paper forecasts and simulated decisions over fresh data. Monitor predictive quality, net results, costs and risk separately. Predefined rules determine *continue, pause, investigate or retire*.
9. **Reproduce and audit:** a report links the research question to data versions, source code, trials, controls, negative tests and final decisions. A repeated run with identical inputs reproduces the essential numerical results.

### Example of future CLI experience (**not commands already implemented**)

```bash
# Illustrative future commands only; not the v0.1 CLI contract.
aqrs data audit --dataset venue_asset_5m
aqrs research campaign --config configs/campaign_example.yaml
aqrs research status --campaign CAMP-001
aqrs candidate show CAND-042
aqrs candidate freeze CAND-042 --version 3
aqrs candidate evaluate-final CAND-042 --version 3
aqrs paper monitor --candidate CAND-042:v3
aqrs report export --campaign CAMP-001
```

The final CLI may have different spelling but must enable these workflows without changing source code. v1.0 has no `live trade` command.

## 3. Long-term architecture: two separate feedback loops

```text
        Research goal, approved compute, data/market contracts
                               |
                   Backward Planning / Feasibility
                               |
                Research families + Candidate Registry
                               |
                Adaptive Research Manager (revisitable)
                               |
                  Resource Governor (preflight + run)
                               |
                 Staged tests / Forward Research Execution
                               |
          +--------------------+--------------------+
          |                    |                    |
     Alpha Discovery    Baselines & Ablations   Cost, execution,
          |                    |                and risk estimates
          +--------------------+--------------------+
                               |
                       Research Walk-Forward
                               |
                     Versioned Evidence Report
                               |
                     Research Decision / Journal
                               |
                       RESEARCH FEEDBACK ONLY
                               |
                        Research Manager

            --- human approval + immutable candidate freeze ---
                               |
                    Separate FINAL HOLDOUT gate
                               |
                       Shadow/Paper Monitoring
                               |
                    Drift / Cost / Regime / Risk
                               |
                        Pause / Review / Retire
                            (monitoring loop)

              No broker or real order routing in v1.0.
```

**Responsibility boundaries:**

- **Alpha Discovery:** finds possible predictive structures from market mechanisms or statistical models. Isolation Forest is optional; rarity is not an alpha claim.
- **Research Management:** plans, selects and budgets studies; learns only from permitted research feedback, never repeated final-holdout tests.
- **Validation & Scientific Controls:** enforces causality and time partitions, measures selection bias and tests incremental information against simple and matched comparison strategies.
- **Economic Decision & Execution Simulation:** weighs net value, uncertainty, risk budgets, no-trade, execution cost and executability. Accuracy is not PnL.
- **Alpha Monitoring:** on new data, separates *predictive drift, execution-cost deterioration, risk deterioration and possible alpha decay*. A single drawdown does not prove decay.
- **Research Journal & Provenance:** complete, reproducible history of data, code, parameters, model definitions, tests, decisions and negative findings.
- **Resource Governor:** protects the human user's finite compute budget independently of a research idea's apparent attractiveness, before and during heavy work.

## 3a. Model and tool strategy

AQRS must be neither a LightGBM-only application nor an uncontrolled model zoo. All model families discussed in planning are represented in [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json): supervised ML (LightGBM/XGBoost/CatBoost), anomaly/regime models (Isolation Forest, **HDBSCAN, autoencoders**, PCA, HMM, GMM, K-Means), deep time series/LOB (LSTM, TCN, TFT, PatchTST, DeepLOB), FinBERT and language models, GNN, decision optimization, research scheduling and consciously deferred RL algorithms.

**Product goal by v1.0:** at least one genuinely functioning supervised and one unsupervised discovery variant are wired into the research process and tested fairly against relevant controls. LightGBM and Isolation Forest are the preferred first pilots from v0.3. HDBSCAN and autoencoders must be explicitly considered and given either a documented bounded pilot or defensible no-go/blocker status. **Integrating all models is not a product requirement.** Follow [`MODEL_EVALUATION_PROTOCOL.md`](MODEL_EVALUATION_PROTOCOL.md); users must be able to inspect the decisions through the journal/model audit.

## 4. Scientific reliability

An apparently positive backtest is not automatically valuable. AQRS must challenge a candidate's incremental contribution:

- Forecasting gain **against** trivial null/linear-model baseline.
- Net economic value **after** fees, spread, slippage and applicable instrument-specific costs, including stress tests.
- **Condition-matched controls:** if a volume condition works only in downtrends, test against downtrend-only shorts.
- Valid time-series evaluation, with purge/embargo where labels overlap and train-only fitting of transformations.
- Multiple attempted families/features/windows/parameters counted; null and negative results remain visible.
- Uncertainty and observation dependence: numerous correlated trades are not numerous independent pieces of evidence.
- Final holdout **not** a repeatedly queried score server. Only frozen, documented candidates receive controlled access.

## 5. Why this system might deliver research value

Its value does **not** follow from free models alone. Potential edge sources include more effective use of known information, small-capacity niches, better specialized data, persistent market mechanisms, superior execution, and disciplined falsification. Research areas lacking plausible economics are not automatically banned forever, but may be cheaply screened or deprioritized.

The project does not optimize `experiments_per_hour`. It aims for **validated findings per research budget**, with false-discovery, selection-bias and cost accounting. No 99% failure-rate assumption is built in.

## 6. What “complete” means

Acceptance of **v1.0** means one user can reproducibly run the full research-and-monitoring workflow on at least one real, documented and lawfully sourced historical dataset. **It does not mean** a profitable live-money strategy has been found.

Binding, testable acceptance criteria are in `docs/MILESTONE_DOD.md` under M9/v1.0. Key quality limits:

1. **No lookahead or label leakage**, demonstrated with adversarial automated tests.
2. **Correct costs and execution modeling**, checked against manually verified examples and stress scenarios.
3. **Reproducibility:** fixed data/code/seeds/config reproduce principal research metrics.
4. **Search auditability:** every variant, negative result, reject, failure, ranking decision and provenance is inspectable.
5. **Independent final check:** research and final data/access permissions are distinct; final tests logged and never retroactively optimized.
6. **Controlled adaptation:** a scheduler must be evaluated transparently against static prioritization on reproducible research tasks. If no incremental value is shown, keep the deterministic method.
7. **Shadow/paper validation:** fresh signals, simulated decisions, costs, risk and monitor states are logged without a live broker. Pause and resume are deterministic and testable.
8. **Clear safety boundary:** no real-money orders, autonomous broker actions or unsupported profit promises.
9. **Cross-platform execution:** install, run and test on a native Windows machine **and** a clean headless Linux environment, with truthful OS-specific resource enforcement and portable auditable artifacts. Windows is primary locally; cloud hosting is optional and provider-neutral. All internal artifacts and CLI messages are English.

## 7. Deliberately not fixed

- No guaranteed profit or fixed Sharpe/return threshold as a **software acceptance criterion**.
- No preselected asset class, exchange, API or mandatory commercial data source. Market/data choice at v0.2 follows economic feasibility, quality and access review.
- No rigid `spread > 0.05%` / `holding period < 15 min` prohibition.
- No RL, transformer, Mabe optimizer or LLM agent as a compulsory product component. Added complexity is a hypothesis to test, not an objective.
- No automated live-money execution. That would be a **separate product** requiring explicit authorization, safety requirements and its own DoD.

## Compute and research budgets as product capabilities

AQRS v1.0 must research in a **bounded, controlled** manner on a mid-range PC even if the budget is far smaller than the theoretical search space. Users must never learn *after* launching that a proposed calibration needs years. The **Resource Governor belongs to the core architecture from v0.1**: preflight fit/trial/seed/fold counting and wall-time estimate, hard campaign/time/memory policies, active worker stopping and full journal trace. Adaptive scheduling only allocates approved capacity. Budget exhaustion is not a negative alpha result. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md).

The system should be able to explain immediately: **Which studies were proposed? What were they projected to cost? Which were accepted, rejected, stopped or deferred, and why?** Statistical validation itself is budgeted; no endless recalibration. Risks: [`RISK_REGISTER.md`](RISK_REGISTER.md).

## Windows, Linux, cloud neutrality and English as product properties

**English** is the permanent internal language of schemas, code, logs, reports, model cards, journal metadata and Codex instructions. **Windows is the initial native local operating environment**; headless **Linux is an equally release-tested supported target** from v0.1. No WSL, Docker, admin/root, GPU or managed cloud service is a prerequisite for local research. The core remains hosting-neutral so that a future Hetzner or another provider's Linux VM can use the same research code with different installation and configuration. Provider-specific deployment and additional CPU architectures require their own tests and are not promised by M0. Keep process/memory enforcement OS-specific and explicit. See [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## 8. Acceptance documents and current status

- `docs/MILESTONE_DOD.md`: binding DoD for **all** planned milestones through v1.0.
- `docs/DEFINITION_OF_DONE.md`: exact tests **only for v0.1**.
- `docs/ROADMAP.md`: order, dependencies and incremental scope.
- `docs/DECISIONS.md`: accepted and revisable architecture decisions.
- `docs/OPEN_QUESTIONS.md`: choices not invented, including real trading/data arrangements.
- `docs/PLATFORM_COMPATIBILITY.md`: English language, native Windows/Linux acceptance and provider-neutral deployment contract.

**Current state:** specifications and handoff, no software implementation or accepted milestone.
