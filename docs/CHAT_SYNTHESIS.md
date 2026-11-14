# Conversation synthesis and handoff context

**Source:** the full conversation visible at handoff. This document conveys **product decisions rather than a verbatim transcript**. Where an earlier suggestion was corrected, narrowed or rejected later, the later and more critical conclusion governs.

## Added clarification: all discussed model/tools must remain cataloged

The v2 handoff mentioned model families only as scattered examples. The owner explicitly requested a **complete model/tool catalog**, now maintained in [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md), [`MODEL_EVALUATION_PROTOCOL.md`](MODEL_EVALUATION_PROTOCOL.md), and [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json). This is **not** an instruction to implement every algorithm. LightGBM and Isolation Forest are selected as distinct v0.3 pilots. HDBSCAN, autoencoders, XGBoost and other methods must receive documented evaluations or evidence-backed blocker decisions. v0.1 remains a small walking skeleton.

## Original research question

The discussion began with how machine-learning models are used in quantitative trading. Considered models included XGBoost, LightGBM, CatBoost, time-series transformers, DeepLOB and other order-book models, language models, clustering/anomaly detection and reinforcement learning. Main conclusion: **architectural sophistication is not equivalent to financially valuable predictive power**. Many open-source models run on a mid-range CPU computer. High-quality data and actual market execution economics are harder problems.

## Major course corrections

1. **Trading is not the same as long-term investing.** The project targets short-horizon tradability, microstructure, realistic forecast horizons and execution. Historical equity-factor or quarterly-report examples do not substitute for intraday alpha research.
2. **Anomaly ≠ alpha.** Isolation Forest identifies unusual states, not necessarily forecasts or strategies. Start by measuring **conditional incremental predictive value** against baselines. Unsupervised anomaly discovery is one optional path.
3. **A hypothesis need not precede all exploration.** Data-driven discovery may generate a hypothesis, but independent untouched data must test it. The discovery data cannot also be independent proof.
4. **Dave Mabe: Backtest Wide, Trade Narrow / Columns.** Can generate practical rule filters from a broad trade set. The starting idea need not already be optimally profitable, but aggressively filtering a bad or random base signal is overfitting-prone. The owner knows Mabe's approach from a podcast but has **no preference for it**. Decision: do not require Mabe's optimizer. Later compare transparent threshold/decision-tree filters fairly with ordinary ML such as LightGBM.
5. **Screen costs early.** Spread, fees, slippage and adverse selection can dominate very short holding periods. Funding applies only for instruments and actual funding events. Venue quality, wash-trading exposure and execution assumptions matter.
6. **The filter may be the real signal.** “Volume condition + downtrend” must beat “short during downtrends without the volume condition.” Matched controls and ablations are essential.
7. **Multiple testing is a major threat.** Hypotheses, windows, thresholds and architectures multiply false apparent wins. Journal every attempt; use chronological walk-forward, label-overlap gaps, reserved holdout and awareness that correlated trades are not independent observations.
8. **Decision-theoretic framing matters more than raw price prediction.** Expected net value, risk, current positions and alternatives (trade, wait, do nothing) influence decisions. A simple v0.1 policy is enough; RL requires an unusually credible simulator and is not a default.
9. **Alpha decay is a hypothesis, not automatic diagnosis.** Competition and structural change can destroy genuine past edges, but many supposedly decayed effects were never real. Long-term Discovery and Monitoring loops stay separate.
10. **Old historical data are contextual.** Data from 2003 can illuminate mechanisms/stress regimes, but cannot alone prove a short-lived strategy remains viable now. Prioritize recent regimes where relevant; do not ban old data categorically.
11. **Market/data selection matters.** Advantage may come from niche capacity, unusual data, better analysis or execution. An algorithm cannot create alpha out of arbitrary generic data. Review data quality, venue, capacity and costs before expensive research.
12. **Shrink the search space adaptively, not with rigid exclusions.** The proposed ban on sub-15-minute strategies where average spread exceeded 0.05% was **rejected**: spread without expected move, liquidity and execution is not enough. Use reversible, explained prioritization and preserve some exploratory budget.
13. **Backward Planning + Forward Execution + Adaptive Research Management + Research Journal** was accepted. Classical rule-engine Backward Chaining is not required. Begin with deterministic workflows; consider bandits/Bayesian Optimization only when they show incremental benefit.
14. **Lean Startup / Walking Skeleton** is the development approach: build v0.1 now rather than spending months on speculative architecture.

## Resulting product

An adaptive alpha-research environment with two long-term loops:

- **Discovery:** propose candidate hypotheses; test economic and statistical value; challenge baselines and alternative explanations; allocate research time with measured evidence.
- **Monitoring (later):** observe accepted signals for predictive drift, worse execution, risk and potential decay; use predefined pause/review criteria.

Both flows write to a persistent journal. The Research Manager learns only from permitted research feedback, never from repeated peeks at an allegedly untouched final holdout.

## What v0.1 explicitly demonstrates

A small reproducible **vertical slice**: synthetic market bars → causal features → two or more candidates → early cost/plausibility checks → prediction/trading controls → chronological research folds → simple decisions/backtest → journal → report. CPU-local with tests. This demonstrates **software and methodological correctness**, not a profitable real-market edge.

## Unsupported assumptions to avoid

- No fixed “99% failure rate” as a measured fact.
- No universal claim that high volume implies wide spreads.
- No unconditional funding charge on every 15-minute perpetual position.
- No promise that “AI finds alpha” or “transformers beat LightGBM.”
- No assumption that a once-published trading effect remains profitable today.
- No invented production market, provider, broker or trading account.
- No mandatory 2003-to-present dataset for modern intraday signals.

## Working arrangement

The owner intends to continue development **in Codex rather than this chat**. `CODEX_START.md` is the current implementation assignment; `AGENTS.md` and this document give future sessions their context. After reading, Codex should implement, run real tests and document evidence rather than merely restating a plan.

## Handoff clarification: full product DoD

After the initial handoff, the owner required both a precise **v1.0 end-state** and an objectively testable DoD for **every milestone**, not only v0.1. Consequently the package added `PRODUCT_VISION.md`, `MILESTONE_DOD.md` and `MILESTONE_STATUS.md` and refined `ROADMAP.md`. Target: a **local research laboratory by v1.0** covering real data, hypothesis/data discovery, matched controls, adaptive research allocation, independent candidate review and paper monitoring, **without autonomous real-money orders**. Codex must implement v0.1 first; later gates are separately accepted vertical increments.

## Project review: compute limits and six failure modes (v4)

The owner reported that a previous framework projected an **eight-year calibration** and failed as a project. The agreed response is a *working v0.1 Resource Governor* with preflight counts for trial/fit/fold/seed combinations, reasoned runtime/RAM estimates, explicit limits and actual interruption. There are **no** automatic budget increases or unbounded retuning/retry loops. Milestone tests include refusal of absurd plans, actual timeouts, memory checks and journal preservation. Three scientific/economic risks are: no viable net alpha, overfitting/data snooping, and unreliable market data/execution. Three technical risks: combinatorial optimization, validation explosion and infinite recalibration. Details: [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md), [`RISK_REGISTER.md`](RISK_REGISTER.md).

## Platform decision: native Windows first, portable Linux and cloud-neutral

English remains the **permanent internal language** for documentation, code comments, reports, metadata and Codex handoffs. The owner will **develop and run AQRS on a native Windows PC**. Linux compatibility remains a separately tested release requirement (initially headless, non-root Ubuntu 24.04 LTS x86_64, Python 3.11/3.12, CPU-only). The core must stay independent of future hosting choices, including Hetzner or other providers. No WSL, Docker, admin/root privileges or cloud account is required for the local application. Keep OS-specific resource guards isolated and honestly tested. See [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).
