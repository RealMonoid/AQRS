# AQRS — Incremental roadmap to version 1.0

**Detailed acceptance:** [`MILESTONE_DOD.md`](MILESTONE_DOD.md). **Model and tool evaluation gates:** [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md), [`MODEL_EVALUATION_PROTOCOL.md`](MODEL_EVALUATION_PROTOCOL.md). **Final vision:** [`PRODUCT_VISION.md`](PRODUCT_VISION.md). **Actual status:** [`MILESTONE_STATUS.md`](MILESTONE_STATUS.md). Current v0.1-specific DoD: [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md).

## Development process for every gate

All milestones are delivered through small, **risk-first Build–Measure–Learn loops** defined in [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md). Codex must work backward from the current measurable release gate, implement and verify forward, use bounded Fault Tree Analysis for critical risks, and perform blameless postmortems only after material/repeated incidents. Retain consequential failed ideas with evidence in the existing `DECISIONS.md` ledger. Codex must predefine the test and success/failure evidence, build only the smallest increment needed, measure it on the relevant Windows/Linux test environment, and explicitly decide whether to continue, pivot, stop or defer. **WIP=1 active development experiment**; no obligation to install Lean Startup SaaS or implement all future milestone features. Keep cards in the existing status/issue and changed paths in the one root changelog.

## Principle

Use **Lean Startup / Walking Skeleton**. Every milestone extends an end-to-end working research path. No big-bang implementation, promised completion times or feature expansion without scientific or engineering benefit. Use the [experiment queue](MILESTONE_STATUS.md#experiment-queue) and recorded owner authorization to select the next eligible increment. The permanent English-only policy in `docs/LANGUAGE_POLICY.md` binds every future Codex addition/revision and every release. Native Windows and Linux are tested platforms at each release. The language check and manual review are required at every milestone gate.

| Gate | Version | New capability | Core acceptance |
|---|---|---|---|
| **M0** | **v0.1** | Offline synthetic data → features → candidates → cost/controls → time-safe folds → decisions → journal/report, with Resource Governor | Reproducible native Windows **and** Linux CLI walking skeleton with automated tests |
| **M1** | v0.2 | Real market data and market feasibility | Audited real data/instrument contract and real historical research run |
| **M2** | v0.3 | Hypothesis- and data-driven discovery | Versioned candidates, matched control tests and **LightGBM/Isolation Forest pilots**; HDBSCAN/autoencoder/XGBoost evaluated or explicitly blocked |
| **M3** | v0.4 | Budgeted adaptive research management | Explainable, revisitable priorities, exploration and comparison with fixed allocation; Governor-integrated scheduling |
| **M4** | v0.5 | Scientific candidate admission | Statistical independence controls, multiple-testing treatment and frozen candidate/final-test audit |
| **M5** | v0.6 | Cost-, risk- and decision-aware policy | Trade/size/no-trade choices with documented cost/risk alternatives; realistic execution simulation |
| **M6** | v0.7 | Shadow/paper monitoring and alpha lifecycle | New observations, drift decomposition and precommitted pause/review actions |
| **M7** | v0.8 | Operations and usability | Repeatable Windows operation plus provider-neutral Linux-server deployment, budget/memory/timeout observability, recoverable runs and operator CLI |
| **M8** | v0.9 | Integrated scientific beta | End-to-end real-data evidence, failure cases, reproducibility and model registry audit |
| **M9** | v1.0 | Deployable local adaptive quant research system | Full product acceptance across science, software, governance, Windows/Linux, portability and documentation |

## What a v1.0 user can actually do

In a local shell, the user configures a supported dataset, launches a bounded research campaign, sees the Discovery findings and matched controls, inspects why experiments were selected and how much they cost, freezes a candidate for an independent final test and monitors it on new data in shadow/paper mode. They can retrieve the history of every candidate and its rejected variants. The application does not send broker orders or promise profitability.

## Resource governance and long-running dead ends

The Resource Governor is a release-critical control **from M0**, not a late operations enhancement. Preflight counts fits/trials/folds/seeds, runs a bounded representative pilot or conservative estimate, rejects obviously over-budget searches, enforces timeout and memory policy, journals resource outcomes and forbids retry/budget escalation loops.

- **M0:** real governor, failure tests G01–G07, including rejection of an eight-year/75,000-fit hypothetical plan before execution.
- **M1–M2:** data source/model family cost estimates and early feasibility gates.
- **M3:** multi-stage adaptive budget allocation; avoid turning Successive Halving into another huge sweep.
- **M4:** time-budget the statistical validation layer, including bootstrap/permutation and stress variants.
- **M6–M7:** prevent monitoring/recalibration loops and test safe recoverability on native Windows and a generic Linux server.
- **M8–M9:** demonstrably bounded end-to-end beta and independent clean Windows/Linux installation tests.

**The priority metric is not models trained per second. It is the rate of independently supported research findings within a finite budget.**

## Model, tool and mandatory evaluation gates

Use the complete [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and its structured registry. `CORE` means operational by the gate, `EVALUATE` means fair test or documented blocker decision, `CONDITIONAL` depends on fit/data and `DEFERRED` stays out of scope. M2 explicitly introduces the LightGBM and Isolation Forest pilots. HDBSCAN, autoencoders, PCA, XGBoost and Random Forest get explicit evaluated/blocked decisions, not forced adoption. By M8/M9 all catalog entries must be audited and traceable; both supervised and unsupervised discovery paths must function in the supported environment.

## Windows, Linux, cloud-neutral and language gates

**M0:** native Windows CPU clean-install + run + tests (normal user, no WSL), and independent headless non-root Linux CPU clean-install + run + tests; actual worker timeout/memory-capability or fail-closed evidence, English output, portable paths.
**M1–M6:** every new data/model/monitoring component preserves both Windows and Linux baselines without unavoidable GUI, GPU, cloud or container prerequisites.
**M7:** publish repeatable Windows local operations and provider-neutral headless Linux VM/server deployment (Hetzner or any comparable provider); process restart, artifact backup/restore and logs are tested; containers remain optional.
**M8/M9:** full clean-machine native Windows and headless Linux validation with pinned versions, representative real-data pipeline, enforced bounded compute and explicit OS-specific evidence.

See [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## Product boundary

v1.0 is a **local scientific research platform**, not a live-money trading bot. Broker integration, hands-off execution, distributed infrastructure and RL execution are separate projects requiring explicit authorization and scientific rationale.
