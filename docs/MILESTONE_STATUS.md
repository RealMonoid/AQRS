# AQRS — Milestone status and acceptance evidence

**Current status:** M0/v0.1 passed the local acceptance matrix on native Windows 11 and independent headless Ubuntu 24.04, each with Python 3.11 and 3.12.

Allowed milestone statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `ACCEPTED`. `ACCEPTED` is permitted only after satisfying the relevant `MILESTONE_DOD.md` tests and referencing auditable evidence here. Existing documents are not proof of completion.

| Milestone | Deliverable | Status | Evidence / run IDs | Blockers / unresolved deviations |
|---|---|---|---|---|
| M0 / v0.1 | Reproducible synthetic walking skeleton, **including Resource Governor and native Windows/Linux acceptance** | ACCEPTED | Four verified environments and paired runs below | Remote GitHub Actions execution pending |
| M1 / v0.2 | Real data and market feasibility | NOT_STARTED | — | Real market/provider not selected |
| M2 / v0.3 | Discovery and matched controls | NOT_STARTED | — | — |
| M3 / v0.4 | Adaptive research management | NOT_STARTED | — | — |
| M4 / v0.5 | Statistics and final-test candidate gates | NOT_STARTED | — | — |
| M5 / v0.6 | Net-cost/risk decisions and simulation | NOT_STARTED | — | — |
| M6 / v0.7 | Shadow/paper monitoring | NOT_STARTED | — | — |
| M7 / v0.8 | Operations and usability | NOT_STARTED | — | — |
| M8 / v0.9 | Integrated scientific beta and full evidence | NOT_STARTED | — | — |
| M9 / v1.0 | Locally deployable research product | NOT_STARTED | — | — |

## Current Build–Measure–Learn development loop

**Status:** M0-01 and M0-02 closed. No active development loop.

```text
Loop ID: M0-01
Milestone: M0/v0.1
Backward proof: deterministic UTC bars, causal features and exact label timing in purged folds.
Assumption: a research-only bar prefix suffices to build all fold features and labels.
Risk: critical. FTA-M0-A in RISK_REGISTER.md.
Prior ideas: IDEA-001 to IDEA-003 checked. No sweep or parallel development.
Baseline: documentation package with no runnable Python implementation.
Pass: stable fingerprint, future perturbation leaves prior features intact, invalid bars fail,
      horizon-3 uses open[t+1] to open[t+4], no label crosses its fold or holdout boundary.
Fail/stop: any future dependence, malformed data accepted, or empty fold treated as usable.
Budget: one focused session up to 15 minutes. Unit tests only, zero fits.
Incident: NOT_TRIGGERED.
```

M0-01 learning: `SUPPORTED / PERSEVERE`. The focused Windows test initially exited 1
with the market module absent, then exited 0 with 3 tests passing (0.35 s).
The next proof is a supervised two-candidate run with durable outcomes.

```text
Loop ID: M0-02
Milestone: M0/v0.1
Backward proof: CLI admits only bounded plans and produces auditable outcomes for both candidates.
Assumption: isolated sequential workers can enforce M0 budgets and preserve fair research evidence.
Risk: critical. FTA-M0-A, FTA-M0-B, cost and persistence controls in RISK_REGISTER.md.
Prior ideas: IDEA-001 to IDEA-003 checked. Fixed two-candidate schedule with no search.
Baseline: causal data path tested, with no research execution, governor or journal.
Pass: 75,000 fits rejected before work, strict unavailable memory rejected, blocking and RSS
      workers stopped, journal persists outcomes, and identical runs reproduce research metrics.
Fail/stop: any limit bypass, survivor, leakage, partial result counted as complete or lost attempt.
Budget: one focused session up to 45 minutes. Configured 120 s/trial and 300 s/campaign,
        at most 2 candidates, 1 seed, and 12 total fits including a bounded pilot.
Incident: M0-INC-01 and M0-INC-02 below.
```

### M0-02 acceptance evidence, 2026-11-06

Native Windows 11 Pro x86_64 build 26300 used a non-administrator account. Ubuntu
24.04.5 LTS x86_64 kernel 6.8.0-147-generic ran in a separate headless QEMU guest
with WHPX, as UID 1000 and with guest egress disabled. Each used a clean CPU-only
virtual environment. The Linux dependency installation used a local wheelhouse.

All commands below exited 0 in each of the four environments.

```text
python -m pip install -e ".[dev]"
python -m aqrs research plan --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m pytest -q
python -m ruff check .
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

| Environment | Python | Plan ID | Completed run IDs | First run wall seconds | Sampled peak MiB | Sampled CPU seconds |
|---|---|---|---|---:|---:|---:|
| Windows 11 | 3.12.12 | `d2191dc6291f4aa9a5a06fc4e0e0fb78` | `530f7957306743a3976df17c401277c2`, `3fc788772a8d45c68a8bab954889b65f` | 5.77 | 120.13 | 4.98 |
| Windows 11 | 3.11.14 | `be1dda1ec1854c4288f5ffa7aa8b1717` | `3a5020358d134fdc984cee23f97945f1`, `96809e464fbe437f8b5366f1cde1a123` | 5.42 | 118.70 | 4.58 |
| Ubuntu 24.04.5 | 3.12.3 | `24732f91dedd40a8bdcfe9f02830d569` | `baa9fb550c124fcc83c7318fc591b76b`, `072a7c0eb9334f069b844a21399cf488` | 3.46 | 122.56 | 3.02 |
| Ubuntu 24.04.5 | 3.11.14 | `cebea406ba7249a5af50d30e2fcf488b` | `95318570331540408b3965de81486667`, `fa352b62925b4cceb8ca0d54f940dd69` | 3.06 | 126.50 | 2.60 |

The Windows logs are `artifacts/windows-release-python{311,312}.txt`. The Ubuntu
logs are `artifacts/linux-m0/acceptance-release-python{311,312}.txt`. Each run
produced `dataset.csv`, `plan.json`, `report.json` and `report.md` under its
run ID. Find Windows runs and their SQLite journal under `artifacts/`, and the
Ubuntu equivalents under `artifacts/linux-m0/release-python{311,312}/`.
All campaigns completed two trials and seven fits, including one pilot.
SQLite integrity returned `ok` and both repeated trials in each environment
linked to the original evidence. Verified source fingerprint:
`2c8213e529e111c51f79e0db265da85245a0290510f30d2a926a3ecad1f91872`.

Both runs in each environment produced identical dataset bytes, research metrics,
fold intervals and holdout boundaries. Windows and Ubuntu fingerprints differ
with last-digit floating-point variation. In the Python 3.12 comparison, the
largest OHLC difference was about 1.1e-11. Timestamps, trade counts and decisions
matched. Both candidates recorded `INSUFFICIENT_EVIDENCE` on 2,988 OOS predictions,
made zero trades at the configured threshold and had higher MAE than the zero-return
control. The matched momentum control was negative net. The holdout was reserved.

The final suite passed 17 tests per environment. G01–G07 evidence includes the offline
CLI, 75,000-fit rejection before any fit, strict-memory rejection before launch,
sampled RSS termination, trial and campaign timeouts, process-tree and parent-loss
cleanup, durable timeout history, holdout perturbation and repeated-run accounting.
Windows used Job Objects. Linux used POSIX process groups and parent-pipe detection.
The 32 model entries and 19 infrastructure entries in the planning registry were retained.

**Incident M0-INC-01.** Initial integration review found that cancelling an active
candidate could still release the next candidate. Pilot cancellation was reported as a
preflight rejection. The scheduler did not treat cancellation as a terminal campaign
event. The correction propagates cancellation to remaining attempts and exit 130.
`test_cancellation_stops_remaining_candidates` verifies one supervisor call for the
cancelled candidate case and no candidate call after a cancelled pilot.

**Incident M0-INC-02.** During the first concurrent clean-environment verification,
a candidate and a test pilot each failed closed with a Windows `PermissionError`.
The exception site was not present in the initial journal reason. Transient sharing
around worker status files is a plausible cause. The watchdog now records the failing
operation and bounds Windows status-file rereads within the existing deadline. The
next full suite and both default campaigns passed. Track the site if the issue recurs.

**Learning:** `SUPPORTED / PERSEVERE` on the tested matrix. The next release check is the configured workflow on a shared GitHub revision. M1 remains outside the current authorization.

Previous substantive changes belong in the sole root `CHANGELOG.md` and version control; detailed loop evidence may live in GitHub issues or run artifacts. This is a **development** record, distinct from the financial research journal and scientific candidate approvals.

## Template for milestone acceptance record

```text
Milestone:
Status:
Commit/release:
Date (UTC):
Verified DoD criteria:
Commands actually run and exit codes:
Platform evidence (native Windows run and independent Linux run: OS/build/distro, architecture, Python, privileges, worker/memory modes):
Compute Governor evidence (preflight, fits, limits, timeout, RAM mode, stop reasons):
Run IDs / artifacts / dataset fingerprints:
Open critical bugs:
Deviations / ADRs:
Acceptance by:
Backward Development requirement → proof → minimum change:
Forward Execution commands and observed evidence:
FTA risk ID and critical negative tests (or why not applicable):
Postmortem incident ID and verified prevention (or NOT_TRIGGERED):
Rejected/deferred IDEA-### lookup and new decision (if any):
Build–Measure–Learn assumption, result and evidence:
Next smallest vertical increment:
```

**Important:** A research run's execution status is distinct from a software release gate. A well-tested negative-alpha campaign may meet a software gate.

## Model/tool registry (not yet implemented)

Planning sources: [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json). Registry `CORE`/`EVALUATE`/`CONDITIONAL`/`DEFERRED` labels are **planning decisions**, not release-pass results. M2 includes LightGBM and Isolation Forest pilots; other models receive documented decisions at their gates. The `model_registry_audit` occurs at M8. Status: `NOT_STARTED`.
