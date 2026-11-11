# AQRS — Adaptive Quant Research System

**English-only repository policy (permanent):** All AQRS documentation and future Codex additions or revisions must be written in English. See [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md).

**Current status:** M0/v0.1 and M1/v0.2 are accepted. The offline CLI supports the synthetic baseline and the bounded Binance BTCUSDT spot workflow for local, personal, non-production research. A separate [Spot data preparation entry](#prepare-broader-spot-datasets) now qualifies bounded multi-day inputs for two symbols and retains activity fields. See the [milestone status](docs/MILESTONE_STATUS.md) for the verified scope and platform evidence.

AQRS is designed as a local, CPU-friendly research platform for **short-horizon systematic trading**. Its goal is not impressive backtest graphics. It must discover potential *incremental predictive information* in market data, translate such information into plausible net-of-cost simulated decisions, and challenge apparent discoveries using independent controls. “No defensible tradable edge found” is a valid research result.

**Repository language: English. Local target: native Windows. Required secondary target: headless Linux. Future deployments: cloud-provider neutral, CPU-first.** See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

## Target product at v1.0

The final product is a **locally deployable alpha-research laboratory, not an autonomous live-money trader**. One researcher can run campaigns over quality-controlled real market data; discover alpha candidates; measure incremental out-of-sample predictive and net economic value relative to condition-matched baselines; allocate research resources adaptively; freeze promising candidates for independent final checks; and monitor eligible candidates with **shadow/paper predictions** as new data arrive. The journal retains every variant, failure, cost assumption, decision and provenance.

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

## Repository map

| Find | Location |
|---|---|
| Agent instructions and onboarding | [AGENTS.md](AGENTS.md) and [CODEX_START.md](CODEX_START.md) |
| Requirements engineering and confirmed requirements | [Requirements Engineer](docs/requirements/AGENTS.md) and [requirements register](docs/requirements/REQUIREMENTS.md) |
| Current milestone, experiment queue, and development evidence | [MILESTONE_STATUS.md](docs/MILESTONE_STATUS.md) |
| Milestone acceptance criteria | [MILESTONE_DOD.md](docs/MILESTONE_DOD.md) |
| Decisions, open questions, and file changes | [DECISIONS.md](docs/DECISIONS.md), [OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md), and [CHANGELOG.md](CHANGELOG.md) |
| Development process and research rules | [DEVELOPMENT_PROCESS.md](docs/DEVELOPMENT_PROCESS.md) and [RESEARCH_PROTOCOL.md](docs/RESEARCH_PROTOCOL.md) |
| Python code and component responsibilities | [src/aqrs/](src/aqrs/) and [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Run settings and model registry | [configs/](configs/) |
| Tests, maintenance checks, and CI | [tests/](tests/), [scripts/](scripts/), and [.github/workflows/](.github/workflows/) |
| Local run inputs and evidence | The run configuration sets the paths. Defaults use `artifacts/` for reports and the SQLite Research Journal. Git ignores these outputs. Find evidence for a specific experiment from its entry in [MILESTONE_STATUS.md](docs/MILESTONE_STATUS.md). |

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

## M1 pilot: import one Binance BTCUSDT spot day

Use a local Binance Vision daily one-minute ZIP and its matching `.CHECKSUM` file.
For the archived pilot, use [January 5, 2026](docs/MILESTONE_STATUS.md#m1-e02-learning-card-binance-btcusdt-spot-2026-11-08).
With the dependencies above installed, run the offline importer into a new directory
under an existing parent:

```bash
python -m aqrs.binance_spot_pilot --day 2026-01-05 --archive BTCUSDT-1m-2026-01-05.zip --checksum BTCUSDT-1m-2026-01-05.zip.CHECKSUM --output btcusdt-import
```

The importer validates the checksum and all 1,440 UTC minute intervals before writing
`dataset.csv` and `import_report.json`. Keep the source and output local for this
non-commercial technical pilot.

## Prepare broader Spot datasets

For broader **data preparation**, the optional Spot dataset entry qualifies one
or two explicitly selected symbols over up to 31 contiguous UTC days. The checked-in
scope is BTCUSDT and ETHUSDT, December 1–24, 2025. This prepares development data;
it does not run a research campaign or change M1's fixed campaign input.

```bash
python -m aqrs.spot_dataset plan --scope configs/spot_data.json
python -m aqrs.spot_dataset acquire --scope configs/spot_data.json --output artifacts/spot-data
```

`acquire` is the explicit online action. For already available ZIP/checksum pairs,
use `qualify --scope configs/spot_data.json --archive-dir <directory> --output <new-directory>`.
The existing `configs/research.yaml` supplies Governor settings; `--config` can
select another validated research configuration with equal or tighter limits.
Each instrument receives its own `dataset.csv`, `activity.csv` and `manifest.json`.
Activity retains quote volume, trade count and taker-buy base/quote volume, available
only at bar close. The top-level `report.json` records the frozen plan, source,
per-worker outcome and observed resources. Failed or partial attempts remain explicit;
an existing output directory is never overwritten. More than one symbol is not
automatically independent evidence. See [AQRS-D01](docs/MILESTONE_STATUS.md#aqrs-d01-test-card-free-spot-data-expansion)
for the fixed acquisition budget and verification status.

## M1 pilot: run the BTCUSDT spot campaign

Place the verified January 5 archive and its checksum in `artifacts/m1-e02/`.
Run the original M1-E04 15-minute economic screen from the project root with a fresh output location or pilot journal:

```bash
python -m aqrs research run --config configs/m1-e04.yaml
```

The offline campaign validates the source before any fit and reuses the synthetic
workflow's analysis and watchdog. The M1 campaign admits only January 5. The January 6 reservation is fixed, and the spot importer rejects that date before opening an archive.
The run writes `data_manifest.json`, `plan.json`, `report.json`, `report.md` and,
when admitted, `dataset.csv` under its run ID in `artifacts/m1-e04/`. Attempts
are stored in the pilot's SQLite journal. Use the run command alone for this
budget because `research plan` performs a separate synthetic preflight fit.
See the [M1-E04 Test Card](docs/MILESTONE_STATUS.md#m1-e04-test-card-first-real-data-campaign-2026-11-08)
for the cost assumptions and evidence boundary. The archived 15-minute screen skipped candidate fits and simulation. The current CLI reports this outcome as `evaluation_status=SCREENED_OUT`. For the accepted 30-minute workflow use the [M1-E11 replay record and its frozen configuration](docs/MILESTONE_STATUS.md#m1-e11-learning-card-and-m1-acceptance-2026-11-09).

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

## Auditable evidence and execution boundaries

Current reports explicitly label zero/single-trade results, the limited meaning
of the movement-scale screen and the uncalibrated momentum reference. The
Isolation Forest report retains its legacy paired metric and adds all-hour
net policy differences including skipped opportunities. No higher evidence
status follows from these diagnostics.

Prediction reports also show descriptive Spearman rank association and forecast /
target dispersion, overall and for each existing chronological fold, including
when the policy takes no trades. Undefined association is labeled explicitly.
No significance, stable edge or profitability follows. Each new diagnostic view
is recorded in `diagnostic_exposure` and the journal; reruns retain their own
views. The training cost screen still stops before prediction when it fails.
See the [diagnostic and exposure rules](docs/RESEARCH_PROTOCOL.md#descriptive-diagnostics-and-additional-exposure).
The [AQRS-A08 verification receipt](evidence/aqrs-a08-verification.json) records
the synthetic examples, independent review and four passing Windows/Linux jobs.

For a data-free precision planning example, run:

```bash
python -m aqrs research precision --sd-bps 20 --effect-bps 2 --independent-units 18
```

The calculation reports assumptions and required independent units, with no
fits, market access or campaign side effects. Its normal approximation is not
a significance test or an estimate of actual market dependence. See the
[claim admission rules](docs/RESEARCH_PROTOCOL.md#precision-and-claim-admission).
The corrected count-only API is `aqrs.events.scan(validated_minute_closes)`
under `PRICE_DROP_V2`; historical V1 counts must not qualify an outcome study.
There is no new real-data count runner in this increment.
The [AQRS-A07 verification record](evidence/aqrs-a07-verification.json) retains
the synthetic example, regression results, independent review and CI evidence.

The [versioned exposure index](evidence/exposure.json) distinguishes reconstructed variants, individual attempts, count-only screens and synthetic checks. Unknown historical exposure remains explicit; these are not independent discoveries. The [frozen configurations](evidence/configurations.json), [digest manifest](evidence/manifest.json) and `evidence/acceptance.zip` preserve historical acceptance records. Eight scripts under `evidence/historical/` are immutable reference inputs, not supported campaign entrypoints. See the [AQRS-A06 Learning Card](docs/MILESTONE_STATUS.md#aqrs-a06-learning-card-audit-controls-and-recoverable-evidence) and [durable verification record](evidence/aqrs-a06-verification.json) for four-job CI, remote-restoration proof and limitations.

Verify with `python scripts/evidence_archive.py --verify`. Add `--restore <new-directory>` to restore; extraction refuses an existing destination and unsafe or nonportable member names. SQLite backup snapshots preserve committed WAL records. Restoration proves integrity and journal readability, not historical preregistration or missing source linkage. Keep a verified copy outside the local disk; the private Git remote carries the versioned bundle. Refresh evidence and exposure records before accepting a new campaign.

Core report schema `2` adds recoverable source, available Git identity, environment versions and explicit zero-cost flags. Workers execute the archived source. Package version `0.1.0` remains a compatibility label, not an execution identity or milestone status. Old reports remain unchanged legacy records.

The core deadline covers supervised input validation/staging, timing fits and candidate workers. Configuration loading, source snapshots, SQLite/report persistence and cleanup are control-plane work outside that hard compute boundary; elapsed setup is checked before admission. This is not an OS deadline for arbitrary filesystem I/O. Pilots validate approved Governor settings and retain frozen costs; their parent-side archive/report I/O still has no hard external timeout. Strict RAM containment remains unsupported and is rejected. Supported estimator/calibration calls reserve fits before starting. A new manual campaign still needs its separately authorized budget.

LightGBM 4.6.0 is an optional runtime extra (`pip install -e ".[supervised]"`) and is included in the development extra for its real synthetic integration test. The core install does not require it. A completed economic screen uses `evaluation_status=SCREENED_OUT` and `execution_status=COMPLETED`; development screens retain `evidence_status=INSUFFICIENT_EVIDENCE`.

## Version policy

This handoff carries the prior scientific scope, model/tool registry and resource-governance decisions forward. The single [`CHANGELOG.md`](CHANGELOG.md) preserves historical changes and records all subsequent file edits. All AQRS-authored documents and every future Codex edit MUST remain in English; all milestones must pass their native Windows **and** Linux compatibility gates.
