# Product Brief — Adaptive Quant Research System

## Problem

Retail quantitative traders can run many ML models for free, but model quality is not automatically a tradable competitive advantage. In competitive markets many apparent strategies are overfit, unprofitable after realistic costs or already decayed. Without statistical discipline, automated discovery tends to produce more false discoveries, not more usable strategies.

## End product and milestones

The **v1.0 target** is in [`PRODUCT_VISION.md`](PRODUCT_VISION.md): one researcher runs a local integrated pipeline for real data, alpha discovery, falsification, adaptive research allocation, independent candidate testing, and shadow/paper monitoring, without broker orders. Binding definitions of done for **every** milestone are in [`MILESTONE_DOD.md`](MILESTONE_DOD.md). Codex's first assignment remains limited to v0.1.

## Model and tool planning

Every discussed model family—LightGBM, XGBoost, CatBoost, Isolation Forest, autoencoders, HDBSCAN, HMM, PCA, DeepLOB, PatchTST, LSTM/TCN, FinBERT, RL and others—is cataloged with its intended role, Python library, prerequisites, earliest gate and decision status in [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json). Adoption follows [`MODEL_EVALUATION_PROTOCOL.md`](MODEL_EVALUATION_PROTOCOL.md), not hype. **v0.1 stays deliberately minimal.**

## Goal

Build a **local, data-driven research platform for short-horizon trading** that searches for reproducible and economically meaningful predictive structures, challenges them against control hypotheses, and increasingly prioritizes research using recorded evidence.

Its primary value is faster, cheaper and more scientifically credible **falsification** of alpha ideas. The software may be functioning correctly even when it finds no profitable idea.

## Intended user and constraints

- Initially one technically curious retail quant researcher.
- Ordinary mid-range PC, CPU-first, limited data and compute budget.
- Focus on **trading** and short-to-medium intraday horizons, not long-term portfolio investment.
- No production venue, instrument, provider or precise live timeframe has been selected.
- BTC/five-minute/fifteen-minute bars and opening gaps were **illustrative examples**, not an agreed trading strategy.
- English is the permanent internal research language; **native Windows is the primary local platform** and **headless Linux is a required separately tested platform** from v0.1. Cloud provider selection remains open and must not be embedded in core code.

## Keep concepts distinct

1. **Rarity/anomaly:** a market state is unusual; this is not alpha by itself.
2. **Predictive structure:** state `X_t` adds predictive value about `Y_{t+h}` relative to a meaningful baseline.
3. **Economic opportunity:** the incremental effect is big enough under plausible fills, cost, size and risk constraints.
4. **Trading policy:** a decision rule considers expected net value, costs, risk, current state and alternatives such as trade/wait/no-trade.
5. **Validated alpha:** incremental, repeated value relative to suitable controls in independent periods under credible market assumptions; not a promise of future profits.

Do not require anomaly detection as the first research stage. It may generate future hypotheses but does not replace a predictive and economic test.

## Target architecture

**Backward Planning → Hypothesis/Data Discovery → Adaptive Research Manager → Resource Governor → Bounded Forward Execution → Scientific Validation → Persistent Research Journal → Feedback**.

At the final product stage, an independent **Alpha Monitoring** loop tracks accepted signals on new data. Research selection uses eligible research evidence only, not the reserved final holdout.

## Specific success criteria

- One reproducible command runs the full research pipeline and records all attempts, including failures.
- Explicit event timing blocks lookahead and prevents training-label overlap across boundaries.
- Costs appear in early screening and realistic backtests; predictive quality is distinct from economic usefulness.
- Matched controls and ablations challenge claims of incremental edge.
- Research budgets are transparent, enforced and audited before and during runs.
- The final v1.0 product operates on real, quality-controlled data, supports candidate lifecycle/monitoring, and does not send real-money broker orders.
- A negative or inconclusive result is accepted and honestly reported.

## Minimum-complexity principle

A new model, optimizer, dashboard or orchestration framework must justify itself against a simpler approach under a comparable scientific and resource budget. Prefer deterministic rules and transparent statistics first; only add bandits, sophisticated optimization or neural methods after evidence of incremental benefit.

## Not goals for v0.1

No real-market alpha claim, no broker, no autonomous live execution, no RL, no big transformer, no mandatory Dave Mabe commercial optimizer, no production dashboard, no microservices and no unlimited model zoo.

## Addendum: research throughput must not become an endless search (v4)

An earlier research framework reportedly projected **eight years of calibration**. Therefore v0.1 must implement an **active Resource Governor** with bounded preflight estimates, explicit trial/fit/fold/seed/campaign budgets, enforced worker timeouts, defensible memory behavior and truthful terminal statuses. The Research Manager allocates *within* a budget and must never inflate it automatically. No unbounded retune/retry loop. Budget rejection is not scientific rejection. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md) and [`RISK_REGISTER.md`](RISK_REGISTER.md).

## Platform portability and permanent English requirement

English is mandatory for all internal artifacts. AQRS begins on native Windows, must also pass actual headless Linux tests, and remains cloud-provider agnostic for future Hetzner/other server deployments. Use portable paths, unprivileged CPU execution, UTC, OS-adapted worker/resource guards and safe persistence. Linux server-specific deployment instructions follow in a later milestone; no container or cloud provider is required for M0. See [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).
