# AQRS — Adaptive Quant Research System

**English-only repository policy (permanent):** All AQRS documentation and future Codex additions or revisions must be written in English. See [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md).

**Current status:** The M0/v0.1 synthetic research CLI is implemented. Platform evidence and release status are recorded in [`docs/MILESTONE_STATUS.md`](docs/MILESTONE_STATUS.md).

AQRS is designed as a local, CPU-friendly research platform for **short-horizon systematic trading**. Its goal is not impressive backtest graphics. It must discover potential *incremental predictive information* in market data, translate such information into plausible net-of-cost simulated decisions, and challenge apparent discoveries using independent controls. “No defensible tradable edge found” is a valid research result.

**Repository language: English. Local target: native Windows. Required secondary target: headless Linux. Future deployments: cloud-provider neutral, CPU-first.** See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

## Target product at v1.0

The final product is a **locally deployable alpha-research laboratory, not an autonomous live-money trader**. One researcher can run campaigns over legally usable, quality-controlled real market data; discover alpha candidates; measure incremental out-of-sample predictive and net economic value relative to condition-matched baselines; allocate research resources adaptively; freeze promising candidates for independent final checks; and monitor eligible candidates with **shadow/paper predictions** as new data arrive. The journal retains every variant, failure, cost assumption, decision and provenance.

- **Product vision / end state:** [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md)
- **All discussed models and tools, gates and status:** [`docs/MODEL_TOOL_CATALOG.md`](docs/MODEL_TOOL_CATALOG.md)
- **Fair model evaluation and integration rules:** [`docs/MODEL_EVALUATION_PROTOCOL.md`](docs/MODEL_EVALUATION_PROTOCOL.md)
- **Machine-readable model/tool planning registry (not an install list):** [`configs/model_tool_registry.json`](configs/model_tool_registry.json)
- **Measurable milestone DoD through v1.0:** [`docs/MILESTONE_DOD.md`](docs/MILESTONE_DOD.md)
- **Current milestones and evidence:** [`docs/MILESTONE_STATUS.md`](docs/MILESTONE_STATUS.md)
- **Incremental roadmap:** [`docs/ROADMAP.md`](docs/ROADMAP.md)
- **Risk and compute-budget policies:** [`docs/RISK_REGISTER.md`](docs/RISK_REGISTER.md), [`docs/RESOURCE_GOVERNOR.md`](docs/RESOURCE_GOVERNOR.md)
- **Permanent English-only documentation and Codex policy:** [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md)
- **Windows, Linux and cloud-neutral portability contract:** [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md)

## Start with Codex

Read [`AGENTS.md`](AGENTS.md), [`CODEX_START.md`](CODEX_START.md) and the current
[`docs/MILESTONE_STATUS.md`](docs/MILESTONE_STATUS.md). The original handoff archive and its
checksum manifest are historical inputs. The checked-out source and the current project documents
govern development.

## Documentation maintenance

**One canonical document per subject; one root [`CHANGELOG.md`](CHANGELOG.md).** Codex edits the current document in place, adds new documentation only when its distinct purpose is justified, and keeps prose concise and navigable. Every substantive change must have a dated entry listing **each changed file path**, including deletions and renames. Old version identifiers or dates belong in audit history or a necessary compatibility contract, never in duplicate document filenames or stale instructions. These rules apply to future milestones as well as v0.1; see [`AGENTS.md`](AGENTS.md).

## Product development: Lean Build–Measure–Learn

Codex must follow [`docs/DEVELOPMENT_PROCESS.md`](docs/DEVELOPMENT_PROCESS.md) for **software construction**, not confuse it with the alpha-research process implemented inside AQRS. Work one falsifiable, predeclared assumption at a time (WIP=1), build the smallest useful vertical slice, measure observed behavior and resource usage, and make an explicit continue/change/stop decision before the next increment. Use `docs/MILESTONE_STATUS.md` or an existing issue to record the current Test/Learning Card; keep the sole `CHANGELOG.md` for substantive file changes. Every meaningful increment plans **backward from the required evidence** and executes **forward** through a small tested slice. High-severity failure modes require a bounded Fault Tree Analysis before development; material incidents require a verified postmortem; consequential abandoned ideas remain searchable in `docs/DECISIONS.md`. Routine small fixes do not trigger a paperwork cascade. Free existing tools (Git, pytest, Ruff and Windows/Linux CI) are sufficient; no paid Lean software or additional tracking system is required.

## Reading order

1. `AGENTS.md` and `CODEX_START.md`
2. `docs/PRODUCT_VISION.md`, `docs/MILESTONE_DOD.md`, `docs/ROADMAP.md`
3. `docs/DEVELOPMENT_PROCESS.md`, `docs/PLATFORM_COMPATIBILITY.md`, `docs/RESOURCE_GOVERNOR.md`, `docs/RISK_REGISTER.md`
4. `docs/MODEL_TOOL_CATALOG.md`, `docs/MODEL_EVALUATION_PROTOCOL.md`, `configs/model_tool_registry.json`
5. `docs/RESEARCH_PROTOCOL.md`, `docs/CONTRACTS.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`
6. `docs/DEFINITION_OF_DONE.md` and `docs/MILESTONE_STATUS.md`
7. `docs/PROJECT_BRIEF.md`, `docs/CHAT_SYNTHESIS.md`, `docs/OPEN_QUESTIONS.md`

## v0.1 in one sentence

A single reproducible, bounded command runs **synthetic OHLCV → causal features → two candidates → early costs/controls → time-safe research folds → simulated long/short/flat policy → journal → report**, while keeping the final holdout outside research feedback.

M0 is **not** expected to discover real-world alpha. BTC-like five-minute bars are only an artificial example, not a selected trading market.

## Install and run v0.1

```bash
python -m pip install -e ".[dev]"
python -m aqrs research plan --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m pytest -q
python -m ruff check .
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

Use Python 3.11 or 3.12 in a clean virtual environment. Run the commands in **both native Windows and real Linux** for milestone acceptance. Native Windows PowerShell and a Windows/Ubuntu CI matrix are valid options; WSL does not substitute for the native Windows run. Manual verification must report the actual OS and Python environment. No API key, runtime network access, display server, broker, WSL, Docker or privileged runtime is required.

## Compute Budget First: avoid multi-year calibrations

AQRS treats compute budgets as **hard safety controls**, beginning with M0/v0.1. The Research Manager proposes what to investigate; a separate **Resource Governor** decides whether and for how long it may run. The default plan allows at most two research trials, 12 model fits, one seed and one parallel trial, with a 120-second trial timeout, 300-second campaign timeout and a 4-GiB sampled tree RSS stop threshold (see YAML; hardware-dependent defaults, not performance guarantees).

Preflight must count combinations of trials, fits, folds, seeds and baselines, estimate their cost from a bounded representative pilot, and reject foreseeable over-budget searches before starting them. An example with 75,000 fits at one hour per fit would require about **8.6 years of serial compute**; the governor must refuse it without executing the search. Inability to enforce a required resource limit is a clear failure/blocker, never silent permission to proceed.

The watchdog uses Windows Job Objects or Linux process groups for worker-tree termination.
The default `observed_rss` mode stops on sampled memory usage. Requests for `strict` memory
containment fail preflight. See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

`research plan` writes `plan.json` and normally fits one supervised pilot on synthetic matrix
inputs. `research run` writes `dataset.csv`, `plan.json`, `report.json` and `report.md` in a unique
run directory and keeps attempts in SQLite. Reports for preflight rejections contain no dataset or
research metrics. Exit codes are 0 for a completed run or admitted plan, 2 for an invalid config or
preflight rejection, 130 for cancellation and 1 for other execution failures.

Relative artifact and journal paths resolve against `project.path_base`, itself relative to the
configuration file. The supplied configuration resolves paths from the project root. An explicit
new run receives its own campaign budget and run ID. SQLite links previous attempts and identifies
reproduced evidence. The scheduler never restarts a failed trial automatically.

## Scientific operating principles

- Treat feature/label availability timestamps as part of the type contract; no lookahead.
- Validate using chronological research windows and a reserved final holdout.
- Count experiments and model-selection attempts; never tune on the final holdout.
- Measure net results with the same fills, fees, spread, slippage, position sizes and holding rules used for controls.
- Test for **incremental** signal value. A filter that simply reconstructs a trend-following strategy is not evidence for a new volume signal.
- Distinguish anomaly detection from alpha discovery: an unusual state is not a tradable edge.
- Separate prediction, decision policy, execution simulation, research selection and live/paper monitoring.
- Do not confuse scientific null results or resource-aborted jobs with software failures or claims about genuine alpha.
- Prefer transparent, simple methods until a more complex one earns inclusion via independent evidence.

## What is deliberately not chosen

There is no agreed production market, exchange, live instrument class, paid dataset, real trading-capital budget, GPU environment or broker connector. Do not invent one. These decisions remain in [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md). M0 operates on deterministic synthetic data only.

## Version policy

This handoff carries the prior scientific scope, model/tool registry and resource-governance decisions forward. The single [`CHANGELOG.md`](CHANGELOG.md) preserves historical changes and records all subsequent file edits. All AQRS-authored documents and every future Codex edit MUST remain in English; all milestones must pass their native Windows **and** Linux compatibility gates.
