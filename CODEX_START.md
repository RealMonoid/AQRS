# Codex start: AQRS project handoff

**English-only repository policy (permanent):** All documentation and all future Codex additions and revisions MUST be in English, without milestone or version exceptions. Read `docs/LANGUAGE_POLICY.md` first. Before reporting completion, execute `python scripts/check_language_policy.py --self-test` and `python scripts/check_language_policy.py`. Never weaken this rule without explicit owner authorization.

Start with [`docs/MILESTONE_STATUS.md`](docs/MILESTONE_STATUS.md) for current
acceptance evidence and the [canonical work plan](docs/MILESTONE_STATUS.md#experiment-queue).
Read pending rows in priority order and follow their links to the governing
cards, findings and deferrals. Check [project open questions](docs/OPEN_QUESTIONS.md)
and [open requirements questions](docs/requirements/OPEN_QUESTIONS.md) for
unresolved owner choices. Use the [dispatch rules](docs/DEVELOPMENT_PROCESS.md#experiment-queue)
to identify the next eligible action in scope. Recover the owner authorization,
completion boundary, reserved approvals and cumulative effort from the linked
card under the [readiness rules](docs/DEVELOPMENT_PROCESS.md#work-authorization-and-definition-of-ready).
If an eligible action is covered, start or resume it. Use
[next dispatch](docs/DEVELOPMENT_PROCESS.md#work-item-definition-of-done-and-next-dispatch)
after each completed item or blocker. Before stopping or requesting owner
input, apply the [permission-boundary check](docs/DEVELOPMENT_PROCESS.md#permission-boundary-before-stopping-or-asking-the-owner).
Apply
[completion reconciliation](docs/DEVELOPMENT_PROCESS.md#completion-reconciliation)
before reporting completion or handing off material work. The M0 brief below
remains a reference for the implemented baseline.

## Documentation and change control (mandatory)

For a quick view of how research moves from an observation or selected market
to a question, attempt, evidence and next decision, read the
[current research value stream](docs/ARCHITECTURE.md#current-research-value-stream).
It identifies the canonical records and explains how to verify and maintain
the consolidated exposure index without running research.

- Update existing canonical project files rather than adding versioned or date-stamped duplicates. New documents need a distinct, necessary purpose and must be linked from an existing index.
- Maintain **one and only one** `CHANGELOG.md` at the repository root. For every change, add a dated (`YYYY-MM-DD`), concise English entry listing **all** added, modified, renamed or deleted relative file paths (old and new paths for moves). Never create separate milestone or version changelogs.
- Keep dates and previous versions for history or compatibility **only when they do not interfere with functionality**, stable APIs or current instructions. Git history and the single changelog hold historical states; canonical docs describe the present state.
- Keep the documentation short and understandable; avoid redundant prose and stale versions. Before completion, verify that the actual changed-file list matches the changelog.

## Read in this order

1. `docs/LANGUAGE_POLICY.md`, `AGENTS.md` and `CHANGELOG.md`
2. `docs/PRODUCT_VISION.md` — end-state vision for v1.0
3. `docs/MILESTONE_DOD.md` — acceptance gates for all milestones
3a. **`docs/DEVELOPMENT_PROCESS.md` — binding Build–Measure–Learn method for every development increment**
4. `docs/MODEL_TOOL_CATALOG.md`, `docs/MODEL_EVALUATION_PROTOCOL.md` — the discussed models, decisions and fair tests
5. `configs/model_tool_registry.json` — structured planning registry; **not** an automatic install list
6. `docs/ROADMAP.md`, `docs/MILESTONE_STATUS.md`
7. `docs/PROJECT_BRIEF.md`, `docs/CHAT_SYNTHESIS.md`
8. `docs/DECISIONS.md`, `docs/ARCHITECTURE.md`
9. `docs/RESEARCH_PROTOCOL.md`, `docs/CONTRACTS.md`
10. `docs/RESOURCE_GOVERNOR.md`, `docs/RISK_REGISTER.md`
11. **`docs/PLATFORM_COMPATIBILITY.md`** — English, native Windows, Linux and cloud-neutral policies
12. `docs/DEFINITION_OF_DONE.md` — detailed M0 acceptance baseline
13. `docs/OPEN_QUESTIONS.md`

Treat these as **product and research-method constraints**, not an order to write more speculative design documents. Record justified deviations in `docs/DECISIONS.md`.

**Scope restriction:** Implement only increments covered by the current authorized work item or sequence. Follow the [dispatch rules](docs/DEVELOPMENT_PROCESS.md#experiment-queue) for queue work and use the milestone status to check start conditions. `EVALUATE` requires evidence at its assigned gate.

## Mandatory product-development feedback loop

For **each meaningful vertical increment**, use **Backward Development → Forward Execution** and follow [`docs/DEVELOPMENT_PROCESS.md`](docs/DEVELOPMENT_PROCESS.md): identify the riskiest assumption, record a compact **Test Card** before coding (hypothesis, baseline, evidence threshold, time/compute budget and stop rule), **BUILD** the smallest executable increment, **MEASURE** with targeted tests, and record a **Learning Card** with the actual outcome and explicit `PERSEVERE` / `PIVOT` / `STOP` / `DEFER` decision. **WIP limit: one active development experiment.** Use the current-loop section of `docs/MILESTONE_STATUS.md` or a single GitHub issue; do not create per-loop documentation files. Run broad tests at milestone gates, not after every inconsequential edit. A failed assumption can be a successful learning loop. For critical scientific correctness or protection boundaries, perform a **small Fault Tree Analysis before implementation** and derive preventive/detection tests; see `docs/RISK_REGISTER.md`. For material incidents or repeated failures, produce a concise, blameless **postmortem with a verified prevention action** in the existing milestone record/issue. Log consequential rejected or ill-conceived approaches in `docs/DECISIONS.md` with why they failed and conditions for reconsideration. Ordinary test failures do not require separate postmortems or documents.

The engineering loop, the internal alpha-discovery loop and the research Resource Governor have separate contracts. Update the single changelog for every substantive change.

## M0 baseline tasks

1. Set up a lightweight, installable Python package `aqrs` (Python 3.11+, CPU-only, native Windows and headless Linux compatible, no runtime network requirements). A normal Windows account must run it without WSL/admin privileges; a clean Linux virtual environment must run it without root or GUI.
2. Generate deterministic synthetic 5-minute OHLCV bars and test data quality, timestamp semantics and stable dataset fingerprints. Synthetic BTC-like data are a demo, **not** a chosen production market.
3. Compute causal features and a horizon-3 forward-return target using the exact event timing from `docs/CONTRACTS.md`: signal after close `t`, earliest fill `open[t+1]`, exit `open[t+4]`.
4. Define at least two registered research candidates: e.g. Ridge with lagged returns, and Ridge adding lagged relative volume and rolling volatility. No model zoo or exhaustive tuning.
5. Apply an **early economic plausibility/cost gate**; compare to a zero-return prediction and a simple trading baseline with identical fills, costs and position sizing.
6. Run deterministic chronological research walk-forward folds with label-overlap isolation and a final **reserved, feedback-inaccessible** holdout. Fit all transformations and models on fold training data only.
7. Implement an explicit simulated `long | short | flat` policy, controlled position overlap, configurable round-trip fees/spread/slippage and causal next-bar fills. No live order interface.
8. Implement a minimal deterministic Research Manager that registers and prioritizes the two candidates, invokes an authorized trial and records results and failures.
9. Implement a persistent SQLite Research Journal with separate `execution_status` and `evidence_status`, run/config/dataset identifiers, inputs, fold boundaries, costs, runtime and artifact references.
10. Produce machine-readable `report.json` and readable `report.md`. Clearly state that synthetic results are **not evidence of real alpha**.
11. Implement an **active Resource Governor in M0**. Count planned fits/trials/folds/seeds and benchmark estimated cost in bounded preflight. Reject implausible plans, enforce trial/campaign wall time and memory requirements in isolated workers, record stop reasons and prohibit automatic retries. See gates G01–G07 in `docs/RESOURCE_GOVERNOR.md`.
12. Add automated tests for timing/leakage, reproducibility, costs, journaling, baseline parity and Governor failures. Use **separate native Windows and Linux** tests or CI runners. Do not describe Windows behavior as best-effort or treat WSL as proof of native Windows compatibility.

## Required working commands

The M0 baseline uses these commands on **native Windows and native Linux**. Use each OS's documented virtual-environment setup:

```bash
python -m pip install -e ".[dev]"
python -m aqrs research plan --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m pytest -q
python -m ruff check .
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

The planning command must show planned fits/trials, estimated wall time/memory, active budgets and a clear allow/reject decision **without starting the full calibration**. The run command must create artifacts and return a truthful result.

## Model, tool and later milestone obligations

Do **not** delete catalog entries merely because they are unnecessary for v0.1. The registry tracks LightGBM, XGBoost, CatBoost, Isolation Forest, HDBSCAN, autoencoders, HMMs, PCA, neural sequence models, DeepLOB, PatchTST, financial NLP, optimization and RL alongside data/experiment tooling. They have different tasks and acceptance gates. Preserve `CORE`, `EVALUATE`, `CONDITIONAL`, `DEFERRED` states and document adopted/rejected/blocked decisions when each gate becomes due.

## Out of scope for v0.1

No real or paper broker, autonomous live trading, RL agent, transformer, giant hyperparameter sweep, Mabe-only tool, production dashboard, microservices, GPU/cloud dependency or all-models-at-once implementation. Keep a **provider-neutral future Linux-server deployment path** without building cloud infrastructure in M0. No mandatory profitable result.

## Priority when time or compute is limited

Keep the vertical slice **complete and honest** rather than broad and hollow. In order: timestamp and leakage correctness, active governor and safe termination, cost/benchmark parity, reproducible CLI, persistent journal and reports, tests, documentation. Do not silently skip a mandatory acceptance gate to report completion.

## Definition of Done

Use `docs/DEFINITION_OF_DONE.md` for the M0 tests and `docs/MILESTONE_DOD.md` for the whole product acceptance contract. Mark a milestone `ACCEPTED` in `docs/MILESTONE_STATUS.md` only after its gate is proven with actual commands, exit codes, run IDs and artifacts. Record Test Cards before implementation in the existing current-loop section or issue. A successfully executed **negative/null finding** is a valid software result. An interrupted or budgeted run is an execution event.

At the end of an authorized work item or sequence, report what exists, which applicable **native Windows and Linux** checks passed, the resource enforcement modes, any remaining blockers and the next smallest vertical increment.
