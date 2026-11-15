# AQRS — Adaptive Quant Research System

**English-only repository policy (permanent):** All AQRS documentation and future Codex additions or revisions must be written in English. See [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md).

**Current status:** M0/v0.1 and M1/v0.2 retain their historical acceptance. The offline CLI currently admits the common synthetic engineering workflow. FR-005 blocks the older Binance Spot research and [data preparation entries](#prepare-broader-spot-datasets) pending their own study-admission qualification. Their implementation and evidence remain preserved. See the [milestone status](docs/MILESTONE_STATUS.md) for the verified scope and platform evidence.

AQRS's product is a reproducible, automated quant research workflow that learns
about its own procedures and generalizes justified improvements. Bitcoin and
other market studies are interchangeable tests of that workflow. The eventual
research scope remains short-horizon systematic trading, with separate predictive,
economic and independent evidence. A useful workflow improvement does not require
a profitable market finding.

**Current owner instruction:** new research runs remain stopped. The first
[structured selection format](docs/CONTRACTS.md#f3-structured-next-question-selection-format-only)
and [five public examples](examples/research_selection_cases.json) specify the
next-question interface only. There is no selector implementation or independent
selection-quality result. The [authorized implementation sequence](docs/MILESTONE_STATUS.md#experiment-queue)
starts with workflow questions, central attempt accounting and general data locks.

**Repository language: English. Local target: native Windows. Required secondary target: headless Linux. Future deployments: cloud-provider neutral, CPU-first.** See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

**FR-005 start gate:** the common command accepts structured synthetic study
requests for `bar_reversal` and `volume_movement`. See the six required `study`
fields in `configs/research.yaml`: a question, matching rule, minimum accuracy
advantage over the stronger control, and actions for all three outcomes.
Before reading submitted data, `research run` checks 256 synthetic series with
quiet/volatile phases using the actual study scorer; at least 80% must detect
the minimum effect. A rejection reports the observed rate and prospective
extent guidance. It never silently extends the requested study. `research plan`
remains declarative. See the [contract](docs/CONTRACTS.md#f4-fr-005-study-admission).

The simulation runs under existing resource limits and evaluates detectability
conditional on its stated assumptions. It does not judge the meaning of the
question or authorize market research. Declared outcome actions are reported;
they do not authorize automatic follow-on experiments or arbitrary commands.
Legacy E14/E18, E19, E22, supervised/Isolation Forest pilots, E15, blind-search
and Spot acquisition/replay entries remain `BLOCKED_FR005_QUALIFICATION`.
Their algorithms and historical evidence remain preserved. Existing global
variant bookings stay in place; old checkout/worktree journals are not imported.

## Target product at v1.0

The owner-authorized [M2-E22 study](docs/MILESTONE_ARCHIVE.md#m2-e22-test-card-predictive-first-spot-reversal)
tests a fixed 30-minute Spot reversal against both constant directions on
365 evaluation days after 91 training days. Prediction is measured before
any cost or trading gate. September–October 2026 and January 6 remain
[locked](docs/RESEARCH_PROTOCOL.md#owner-data-authorization-and-fixed-holdout).
The historical `python -m aqrs.predictive_spot --smoke NEW_OUTPUT` used synthetic
data only; FR-005 now blocks this unqualified legacy entry. The single market attempt used `--run PUBLISHED_SHA` after source-bound
registration, publication and verification; it refuses an existing output.
The [completed study](docs/MILESTONE_ARCHIVE.md#m2-e22-learning-card-prediction-before-costs)
passed the predictive screen but lost under the fixed illustrative costs.
Artifacts are under `artifacts/m2-e22/run-01/` (report, journal, raw archive
checksums and recoverable source). D01's legacy preparation scope is unchanged.

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

Start with [`AGENTS.md`](AGENTS.md), [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md)
and the short current [`docs/MILESTONE_STATUS.md`](docs/MILESTONE_STATUS.md).
Use [`CODEX_START.md`](CODEX_START.md) and relevant subject documents for orientation.
The [milestone archive](docs/MILESTONE_ARCHIVE.md) and `CHANGELOG.md` are
lookup-only for specific historical questions, not mandatory reading before changes.
The original handoff archive and its
checksum manifest are historical inputs. The checked-out source and the current project documents
govern development.
Codex uses the recorded owner authorization and the
[work-item lifecycle](docs/DEVELOPMENT_PROCESS.md#work-authorization-and-definition-of-ready)
to complete necessary steps and pull the next eligible covered queue item.

## Preserved M2-E19 volatility regime pilot

The [registered pilot](docs/MILESTONE_ARCHIVE.md#m2-e19-test-card-volatility-regime-filter)
used only the ten qualified M2-E18 BTCUSDT Spot archives. The completed
comparison remains `INCONCLUSIVE / DEFER`; integration does not authorize
another count or model run. The historical `--archives` and `--output`
entry and its coverage-first implementation are preserved but blocked pending
FR-005 qualification; old admission receipts cannot reopen them.

The conditional comparison requires the published, clean reviewed revision,
the qualifying count, a matching review receipt supplied with `--admission`,
and the pilot-local `hmmlearn==0.3.3` dependency. Use a new output directory
for the comparison. A non-root Ubuntu replay also requires the qualifying
Windows report supplied with `--windows-report`. The pilot uses the existing
simulator and the original illustrative costs.

## Repository map

| Find | Location |
|---|---|
| Agent instructions and onboarding | [AGENTS.md](AGENTS.md) and [CODEX_START.md](CODEX_START.md) |
| Research value stream: origin, attempts, evidence and learning | [Current workflow and exposure maintenance](docs/ARCHITECTURE.md#current-research-value-stream) |
| Requirements engineering and confirmed requirements | [Requirements Engineer](docs/requirements/AGENTS.md) and [requirements register](docs/requirements/REQUIREMENTS.md) |
| Current milestone, experiment queue, and development evidence | [MILESTONE_STATUS.md](docs/MILESTONE_STATUS.md) |
| Milestone acceptance criteria | [MILESTONE_DOD.md](docs/MILESTONE_DOD.md) |
| Decisions, open questions, and file changes | [DECISIONS.md](docs/DECISIONS.md), [OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md), and [CHANGELOG.md](CHANGELOG.md) |
| Development process and research rules | [DEVELOPMENT_PROCESS.md](docs/DEVELOPMENT_PROCESS.md) and [RESEARCH_PROTOCOL.md](docs/RESEARCH_PROTOCOL.md) |
| Work-order checks and material sequencing decisions | [SEQUENCE_PREFLIGHT.md](docs/SEQUENCE_PREFLIGHT.md) |
| Python code and component responsibilities | [src/aqrs/](src/aqrs/) and [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Run settings and model registry | [configs/](configs/) |
| Tests, maintenance checks, and CI | [tests/](tests/), [scripts/](scripts/), and [.github/workflows/](.github/workflows/) |
| Local run inputs and evidence | The run configuration sets the report and Research Journal paths, which default to `artifacts/`. All project copies use the variant ledger at `~/.aqrs/variant-ledger.sqlite3`. The run output and report show `variant_ledger_created` when the ledger is initialized. Find study evidence from its entry in [MILESTONE_STATUS.md](docs/MILESTONE_STATUS.md). |

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
For the archived pilot, use [January 5, 2026](docs/MILESTONE_ARCHIVE.md#m1-e02-learning-card-binance-btcusdt-spot-2026-11-08).
With the dependencies above installed, run the offline importer into a new directory
under an existing parent:

```bash
python -m aqrs.binance_spot_pilot --day 2026-01-05 --archive BTCUSDT-1m-2026-01-05.zip --checksum BTCUSDT-1m-2026-01-05.zip.CHECKSUM --output btcusdt-import
```

The importer validates the checksum and all 1,440 UTC minute intervals before writing
`dataset.csv` and `import_report.json`. Keep the source and output local for this
non-commercial technical pilot.

## Prepare or run the synthetic blind diagnostic

[AQRS-B01](docs/MILESTONE_ARCHIVE.md#aqrs-b01-test-card-external-synthetic-blind-search-preparation)
is an owner-gated, external-synthetic diagnostic. Its
[delivery contract](docs/CONTRACTS.md#a2-external-synthetic-blind-test-input-aqrs-b01)
and [fixed procedure](docs/RESEARCH_PROTOCOL.md#11-aqrs-b01-frozen-blind-search-procedure)
define the entire search. It never downloads data or reads the protected day.
Delivery does not authorize search. Global Governor settings are unchanged.
The CSV may include validated minute buy volume, sell volume and trade count.
Each supplied activity field activates two fixed order-flow rules in the
24-slot search. Absent fields select the predefined OHLCV fallback rules.
The [machine-readable evidence table](docs/RESEARCH_PROTOCOL.md#11-aqrs-b01-frozen-blind-search-procedure)
lists the published ledger and local files. Preflight estimates 129 MiB of
run storage per dataset in addition to the input CSVs.

The single open rehearsal has a separate generated input and a two-trial budget:

```text
python -m aqrs.blind_search register-open
```

This qualifies the known fixture, charges six quantile calibrations and writes
the candidate entries under `evidence/blind/AQRS-B01-OPEN/`, with no outcome
measurements. Commit and push both registration files and the bound source to
`codex/aqrs-b01-blind-preparation`, then execute with that exact remote revision:

```text
python -m aqrs.blind_search execute --published-revision FULL_COMMIT_SHA
```

The runner verifies the remote revision, exact registration and source before
releasing any candidate worker. A reserved or existing attempt cannot rerun.
The supervisor enforces worker deadlines and sampled RSS, not a strict RAM cap.
Git subprocesses have finite timeouts; publication and final receipt I/O are
outside worker deadlines. No network payload is downloaded. Use `[skip ci]`
publication messages while the owner's no-download restriction applies.

For a later authorized external run, the owner must explicitly supply data,
approve the 24-trial exception and start each named dataset attempt. Record that
instruction in a local JSON under `artifacts/blind-test/` with exactly
`owner_start_approved=true`, `approved_trials=24`, `trial_count_exception=true`,
`plan_sha256`, `dataset_id`, `dataset_sha256`, `attempt_id`,
`max_wall_seconds` (at most 300), and the nonempty English `owner_instruction`.
This is an auditable operator authorization record, not cryptographic identity
verification; Codex must not fabricate approval. Approve the aggregate dataset
count and budget before multiple individual runs. Use the same arguments for
`claim`, `register`, and `close` for that dataset:

```text
python -m aqrs.blind_search claim --attempt AQRS-B01-D001 --dataset-id D001 --dataset-sha256 DATASET_SHA256 --authorization artifacts/blind-test/D001-authorization.json
python -m aqrs.blind_search register --attempt AQRS-B01-D001 --dataset-id D001 --dataset-sha256 DATASET_SHA256 --authorization artifacts/blind-test/D001-authorization.json
python -m aqrs.blind_search execute --attempt AQRS-B01-D001 --published-revision REGISTRATION_COMMIT --authorization artifacts/blind-test/D001-authorization.json
python -m aqrs.blind_search close --attempt AQRS-B01-D001 --dataset-id D001 --dataset-sha256 DATASET_SHA256 --authorization artifacts/blind-test/D001-authorization.json
```

Run one command at a time. After `claim`, commit and push only the printed
`D001-start.json`. After `register`, commit and push its registration and
pending ledger, and use that full commit in `execute`. After `close`, commit
and push the three printed verdict, summary and gap files together before
opening the next dataset. Keep the local ownership token in the same workspace.
An incomplete controlled run can close as `NOT_EVALUABLE`. A hard stop with no
terminal receipt leaves the sequence blocked for owner review. A correction is
recorded with `correct --dataset-id D001 --note "English explanation"` between
datasets and published as its own new file.

To verify any two recorded candidates, use the full published verdict commit:

```text
python -m aqrs.blind_search replay --dataset-id D001 --published-revision VERDICT_COMMIT --candidate S01 --candidate P01
```

The expected values are the named candidate rows in `report.json#/results`.
Replay prints `expected`, `recomputed`, and `matches=true` for both on success.
Substitute any two measured candidate identifiers. Required files and field
definitions are in the [evidence dictionary](docs/CONTRACTS.md#aqrs-b01-evidence-field-dictionary).

Outputs are under `artifacts/aqrs-b01/runs/ATTEMPT/`: JSON/Markdown report,
SQLite journal, per-candidate result and full opportunity/event CSV with hashes.
All results remain synthetic and never count as market evidence. A partial
execution is distinguishable from a completed no-finding result.

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
automatically independent evidence. See [AQRS-D01](docs/MILESTONE_ARCHIVE.md#aqrs-d01-test-card-free-spot-data-expansion)
for the fixed acquisition budget and verification status.

## Historical M1 pilot: BTCUSDT spot campaign

FR-005 currently blocks this market entry pending scientific qualification.
The following configuration and evidence describe the completed historical run.

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
budget. Current `research plan` is declarative and performs no fit.
See the [M1-E04 Test Card](docs/MILESTONE_ARCHIVE.md#m1-e04-test-card-first-real-data-campaign-2026-11-08)
for the cost assumptions and evidence boundary. The archived 15-minute screen skipped candidate fits and simulation. The current CLI reports this outcome as `evaluation_status=SCREENED_OUT`. For the accepted 30-minute workflow use the [M1-E11 replay record and its frozen configuration](docs/MILESTONE_ARCHIVE.md#m1-e11-learning-card-and-m1-acceptance-2026-11-09).

## Preserved M2-E14 and M2-E18 discovery comparisons

Exercise the retained comparison and admission code with synthetic fixtures:

```bash
python -m pytest -q tests/test_m2_e14.py tests/test_m2_e19.py
```

The historical entry writes an attempt journal, recoverable execution source, machine
report and short Markdown report. The market entry requires the verified
published revision and an exact admission record for the registered ten
BTCUSDT Spot days. An Ubuntu market replay also requires the valid Windows
report bound by digest. See the [Test Card](docs/MILESTONE_ARCHIVE.md#m2-e14-guarded-campaign-entry-test-card)
for eligibility, the shared Governor plan and the descriptive claim.

Select `--campaign M2-E18` to exercise the same entry with the fixed
December 1–10, 2025 AQRS-D01 scope. Its market preparation also verifies
the D01 archive and checksum digests and the M2-E17 training-prefix
fingerprint. See the [M2-E18 Test Card](docs/MILESTONE_ARCHIVE.md#m2-e18-guarded-campaign-entry-test-card).
Both campaigns are closed. Current completed registration records deliberately
reject fresh admission. The tests stage digest-bound historical registrations
in temporary directories; they do not reset the canonical exposure index.

## Compute Budget First: avoid multi-year calibrations

AQRS treats compute budgets as **hard safety controls**, beginning with M0/v0.1. The Research Manager proposes what to investigate; a separate **Resource Governor** decides whether and for how long it may run. The default plan allows at most two research trials, 12 model fits, one seed and one parallel trial, with a 120-second trial timeout, 300-second campaign timeout and a 4-GiB sampled tree RSS stop threshold (see YAML; hardware-dependent defaults, not performance guarantees).

Preflight must count combinations of trials, fits, folds, seeds and baselines, estimate their cost from a bounded representative pilot, and reject foreseeable over-budget searches before starting them. An example with 75,000 fits at one hour per fit would require about **8.6 years of serial compute**; the governor must refuse it without executing the search. Inability to enforce a required resource limit is a clear failure/blocker, never silent permission to proceed.

The watchdog uses Windows Job Objects or Linux process groups for worker-tree termination.
The default `observed_rss` mode stops on sampled memory usage. Requests for `strict` memory
containment fail preflight. See [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

`research plan` writes `plan.json` without study-data access or a timing fit;
its estimates do not authorize execution. An admitted `research run` performs
its bounded timing pilot when configured, writes `dataset.csv`, `plan.json`,
`report.json` and `report.md` in a unique
run directory and keeps attempts in SQLite. Reports for preflight rejections contain no dataset or
research metrics. Exit codes are 0 for a completed run or admitted plan, 2 for an invalid config or
preflight rejection, 130 for cancellation and 1 for other execution failures.

For a synthetic next-bar comparison, set the candidate's `model` to
`volume_movement` and `horizon_bars` to 1. It compares completed-bar volume
with the training volume median and predicts whether the next bar's absolute
open-to-close return exceeds its training median. Values equal to a median are
in the lower group. The report compares the rule with always above and always
below using the same daily bounds as `bar_reversal`.
The `volume_movement` result is `VOLUME_MOVEMENT_ADVANTAGE`,
`NO_VOLUME_MOVEMENT_ADVANTAGE`, or `INCONCLUSIVE`.

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

The [versioned exposure index](evidence/exposure.json) distinguishes reconstructed variants, individual attempts, count-only screens and synthetic checks. Unknown historical exposure remains explicit; these are not independent discoveries. The [frozen configurations](evidence/configurations.json), [digest manifest](evidence/manifest.json) and `evidence/acceptance.zip` preserve historical acceptance records. Eight scripts under `evidence/historical/` are immutable reference inputs, not supported campaign entrypoints. See the [AQRS-A06 Learning Card](docs/MILESTONE_ARCHIVE.md#aqrs-a06-learning-card-audit-controls-and-recoverable-evidence) and [durable verification record](evidence/aqrs-a06-verification.json) for four-job CI, remote-restoration proof and limitations.

Verify with `python scripts/evidence_archive.py --verify`. Add `--restore <new-directory>` to restore; extraction refuses an existing destination and unsafe or nonportable member names. SQLite backup snapshots preserve committed WAL records. Restoration proves integrity and journal readability, not historical preregistration or missing source linkage. Keep a verified copy outside the local disk; the configured Git remote carries the versioned bundle. The repository was public when checked on 2026-11-14; local research scope does not imply private repository access. Refresh evidence and exposure records before accepting a new campaign.

For the complete bound exposure inventory, run `python scripts/evidence_archive.py
--verify-exposure`. Use `--consolidate-exposure` after adding a verified archive
source to the existing index. This performs no research and preserves manual
screens. The [value-stream overview](docs/ARCHITECTURE.md#exposure-maintenance-and-interpretation)
explains registration links, diagnostic counts, legacy gaps and the distinction
between replay and independent confirmation.

For source-bound supervised receipts, use `python scripts/evidence_archive.py
--verify-supervised-replay WINDOWS_DIR [UBUNTU_DIR] --source-revision COMMIT`.
The Windows-only check verifies the completed receipt before the conditional
Ubuntu replay. Providing both directories also compares their data and results.
See the [supervised replay scope](docs/OPEN_QUESTIONS.md#m2-supervised-pilot-replay).

`python -B -m scripts.m2_e15_count plan` checks the fixed count budget
without opening market files. The matching `run` used the one authorized
BTCUSDT development count. Its local output directory reserves the attempt.
The [M2-E15 result](docs/MILESTONE_ARCHIVE.md#m2-e15-learning-card-state-persistence-count)
links the preserved evidence and the scope of any follow-up.

Verify the named campaign archives and their
report digests with these read-only commands.

```sh
python scripts/evidence_archive.py --verify --campaign M2-E14
python scripts/evidence_archive.py --verify --campaign M2-E18
```

For E18, add `--replay-revision <revision>` to check the Windows report bytes
stored in a locally available Git revision. The replay correction `1eebbfa`
matches the receipt. Its parent `1eebbfa^` fails the digest check. The
campaign mode rejects `--build` and `--restore`.

Core report schema `2` adds recoverable source, available Git identity, environment versions and explicit zero-cost flags. Workers execute the archived source. Package version `0.1.0` remains a compatibility label, not an execution identity or milestone status. Old reports remain unchanged legacy records.

The core deadline covers supervised input validation/staging, timing fits and candidate workers. Configuration loading, source snapshots, SQLite/report persistence and cleanup are control-plane work outside that hard compute boundary; elapsed setup is checked before admission. This is not an OS deadline for arbitrary filesystem I/O. Pilots validate approved Governor settings and retain frozen costs; their parent-side archive/report I/O still has no hard external timeout. Strict RAM containment remains unsupported and is rejected. Supported estimator/calibration calls reserve fits before starting. A new manual campaign still needs its separately authorized budget.

LightGBM 4.6.0 is an optional runtime extra (`pip install -e ".[supervised]"`) and is included in the development extra for its real synthetic integration test. The core install does not require it. A completed economic screen uses `evaluation_status=SCREENED_OUT` and `execution_status=COMPLETED`; development screens retain `evidence_status=INSUFFICIENT_EVIDENCE`.

## Version policy

This handoff carries the prior scientific scope, model/tool registry and resource-governance decisions forward. The single [`CHANGELOG.md`](CHANGELOG.md) preserves historical changes and records all subsequent file edits. All AQRS-authored documents and every future Codex edit MUST remain in English; all milestones must pass their native Windows **and** Linux compatibility gates.
