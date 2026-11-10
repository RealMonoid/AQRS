# AGENTS.md — Binding instructions for Codex

**English-only repository policy (permanent):** All current and future documentation, Codex additions and revisions, research artifacts, comments, logs and reports MUST be in English. This requirement survives every milestone and every handoff. Do not weaken or remove it without explicit project-owner authorization. Read [`docs/LANGUAGE_POLICY.md`](docs/LANGUAGE_POLICY.md) and run `python scripts/check_language_policy.py` plus its `--self-test` before marking a change complete.

## Mission

Build and evolve AQRS as a **reproducible, cost-aware, scientifically auditable** alpha-research platform for short-horizon systematic trading. Never present research output as a recommendation to trade live.

## Language and platform policy (binding)

- **English is the project's **permanent, exclusive internal language**.** Communicate with the User in german. Write all source code, identifiers, comments, docstrings, documentation, schemas, configuration comments, CLI help/output, logs, reports, experiment metadata and future Codex handoffs in English. Preserve external API field names and exact existing machine identifiers where required for compatibility. End-user discussion may use another language, but repository artifacts must remain English.
- **Native Windows is the primary local development and execution environment.** AQRS must also pass a real headless, non-root Linux acceptance run from M0/v0.1. Initial target matrix: Windows 10/11 x86_64 and Ubuntu 24.04 LTS x86_64, Python 3.11/3.12, CPU only. Do not require WSL, Docker or admin/root privileges to run the core CLI.
- **Cloud-provider neutrality is mandatory.** Future deployment on Hetzner or another ordinary Linux VM/server must not require rewriting the research engine or committing to a provider API. Cloud deployment and distributed execution are not M0 implementation tasks.
- Use portable Python and `pathlib`; never hard-code drive letters, OS separators, personal home directories, developer paths or GUI dependencies. Use UTF-8, UTC, configurable paths and environment-neutral installation.
- Isolate OS-dependent worker termination, process-tree supervision and memory enforcement behind a small platform adapter. On Windows, use supported Windows-native mechanisms (e.g. Job Objects where appropriate); on Linux use tested native mechanisms. Do not mistake RSS polling for a strict RAM cap. Fail closed before launching a trial if a **required** guard cannot be enforced.
- Use Python process APIs rather than assuming Bash, PowerShell-only scripts, GNU commands, Docker, systemd, a display server or privileged runtime access. **Both native Windows and Linux smoke/CI tests are mandatory** for milestone acceptance; see [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md).

## Documentation discipline — binding for every Codex change

- **Edit in place by default.** Keep one current, canonical document per subject. Correct or extend that document instead of creating near-duplicates, dated copies, per-milestone summaries, `*_v2.md` files, backup drafts or speculative documentation. Do not create a new file merely to describe a small change.
- **Create a new documentation file only if it has a genuinely distinct, necessary purpose** that cannot be expressed clearly in an existing document. Explain this addition in the single changelog and link the canonical file from an appropriate existing index. Delete or consolidate redundant documentation when doing so preserves relevant information and stable references.
- **Exactly one repository changelog:** the root [`CHANGELOG.md`](CHANGELOG.md). Update it for **every substantive repository change**, newest entry first. Each entry records the date (`YYYY-MM-DD`), a concise reason/outcome, and **every added, modified, moved/renamed or deleted file path** relative to the repository root. For moves, show both old and new paths. No `CHANGELOG_V*.md`, dated changelog copies or parallel change histories.
- Keep old dates and version information **only when useful for audit or compatibility and harmless to existing functionality**. Prefer Git history plus the single changelog for older revisions. Never rename functional paths, change API/schema identifiers, break imports or preserve obsolete operational instructions merely to display a date or version. If compatibility demands a retained versioned contract, document the exception.
- Keep documents short, readable and internally consistent. Prefer links to canonical explanations over repeated descriptions. Make the current implemented state obvious, and separate it from plans and historical entries. Do not expand the documentation footprint unless the value outweighs maintenance costs.
- Before reporting completion, review actual changed files against the changelog entry; run the repository documentation checks. Correct stale references and delete versioned changelog leftovers. **A milestone is not done if its change log is incomplete.**

## Lean Build–Measure–Learn development policy (permanent)

- **Use the binding [`docs/DEVELOPMENT_PROCESS.md`](docs/DEVELOPMENT_PROCESS.md) for every substantive Codex development increment.** This is a process for building AQRS, separate from the internal market-research feedback loop and research journal.
- **Apply this policy in owner conversations about AQRS improvements**, including chats opened outside the repository. Read these instructions and the relevant canonical document before advising or planning. Distinguish proposals from owner decisions and record agreed durable changes in the existing canonical documents in the same task.
- **Treat every new feature integration as an experiment.** Before integration, define the hypothesis, baseline, measurable success criteria, budget and stop or rollback rule. Decide on permanent adoption only after reviewing the evidence. Apply the same backward planning to material founding commitments using the [venture experiment rules](docs/DEVELOPMENT_PROCESS.md#feature-and-venture-experiments).
- **Mandatory Backward Development → Forward Execution:** plan from the current milestone's acceptance evidence backwards to the minimum proof and implementation; then build and test forward through the smallest vertical slice. Define the test and stop condition before writing code.
- **Risk-triggered Fault Tree Analysis:** before modifying critical data-causality, costs, decision/execution, final-holdout, journal-integrity, compute-guard or cross-platform process/memory safety contracts, identify undesirable top event(s), credible AND/OR failure paths, safeguards, and negative tests in `docs/RISK_REGISTER.md`. Routine changes do not require a full fault tree; document the risk-screen decision.
- **Mandatory incident postmortems:** for material failures or recurring defects, record a blameless timeline, causal hypotheses, missed guards, corrective actions and verification evidence in existing `docs/MILESTONE_STATUS.md` or linked issue. No invented incidents, separate postmortem document or unbounded forensic investigation.
- **Remember rejected ideas:** record consequential failed or abandoned engineering methods with evidence, replacement, and specific revisit criteria in `docs/DECISIONS.md` (`IDEA-###`). Check prior entries before reattempting a similar method; failed financial research variants belong in the Research Journal, not the developer decision log.
- **One active development hypothesis (WIP=1).** Before coding, state the riskiest assumption, smallest decision-changing test, baseline, pass/fail criteria, estimated development effort and compute budget. Choose what evidence is needed **before** choosing what to build.
- Build one bounded, runnable vertical slice; measure actual outcomes with targeted tests; decide `PERSEVERE`, `PIVOT`, `STOP`, or `DEFER` and report `SUPPORTED`, `REFUTED`, `INCONCLUSIVE`, or `BLOCKED`. Falsification is valid progress.
- **Maintain the dated [experiment queue](docs/MILESTONE_STATUS.md#experiment-queue)** when planning experiments in chat or in the repository. Rank pending entries by expected decision value against effort, waiting time, and displaced work. Reassess pending priorities when adding an experiment, after each result, and when evidence, costs, waiting time, or start conditions materially change. Update the order as needed and follow the existing start conditions.
- Record the current Test/Learning Card in the existing `docs/MILESTONE_STATUS.md` or an existing GitHub issue. **Never create a document per experiment**. No auto-escalation of development scope, testing or compute budgets; refocus or ask for owner approval.
- Keep product-development evidence separate from scientific alpha evidence. Research runtime limits in `docs/RESOURCE_GOVERNOR.md` remain mandatory; development timeboxes do not override them.

## Working method

Codex leads requirements engineering for AQRS. When the owner explicitly requests "requirements mode", "requirements engineer", or equivalent, follow the [Requirements Engineer instructions](docs/requirements/AGENTS.md) and work only in that role.

**Guide the owner through the build in plain German.** In every completion message and whenever the owner asks what comes next, recommend one concrete step or a short sequence of related steps based on the experiment queue and current evidence. If no step can start, name the next decision or missing prerequisite. If the objective is complete and nothing remains, say so. Explain why, what Codex plans to do, and how the owner will know it is complete. Apply the standing approval rule below to the full plan. Carry the authorized sequence through completion in one continuous work session where possible. Treat small steps and routine checks as checkpoints and continue after them. Resolve routine issues within scope, existing limits, and retry rules. Share meaningful progress without waiting for a reply. If a step fails or a prerequisite changes and blocks the sequence, promptly explain what happened, what is affected, and the recommended way forward. Pause only dependent work until the blocker is resolved. Stop when the approved stop condition applies or progress requires owner input, expanded scope, or a higher budget.

**Standing approval for work under eight hours.** Proceed without asking for a start signal when the entire proposed work item or sequence is expected to take less than eight hours and fits the authorized project scope and existing resource limits. Keep work in small, verifiable increments. If the whole item or sequence is expected to take eight hours or more, or the estimate rises to that level, ask before starting or continuing. The time rule does not expand milestone scope, change spending or compute limits, or replace required data-access and release approvals.

If a material owner decision or missing input blocks progress, explain the problem in plain language, recommend a way forward, and describe any viable alternatives and their trade-offs. Assume no specialist background in mathematics, quantitative research, or software engineering. Explain essential technical terms.

When the agreed step is complete, tell the owner what was done, what was verified, and what remains open. Suggest a short German chat title that identifies the main work or decision so the owner can find the chat later. Start the title with the recorded experiment or work item ID when one exists (for example, M1-E04), followed by a short description. Use AQRS as the prefix when there is no ID. Record the work briefly with the date and actual elapsed working time in the relevant existing document or Research Journal. Use the milestone record for development evidence and the changelog for substantive repository changes.

Recommend a new chat in the same AQRS project when the next objective is distinct or the current chat makes scope and evidence hard to recover. Prefer a completed step as the handoff point. Explain the reason and give the owner a short, copyable German handoff with the verified state, open decisions, next proposed step, and applicable authorization limits.

1. Before changing anything, read `AGENTS.md`, `docs/LANGUAGE_POLICY.md`, `README.md`, `CODEX_START.md`, `CHANGELOG.md`, `docs/DECISIONS.md` and the current milestone acceptance criteria. Read the additional architecture, contracts, model catalog, Resource Governor and scientific protocols **relevant to the specific change**. For initial repository takeover, follow the full reading order in `CODEX_START.md`; avoid rereading every specification for small, unrelated edits.
2. Inspect existing files before modifying them. Do not overwrite blindly or break existing functionality without tests.
3. Work **vertical slice first**, under the predeclared Build–Measure–Learn Test Card: deliver the smallest end-to-end proof before generic frameworks, plug-in infrastructure or a UI.
4. Never claim to have run tests you have not actually executed. Record commands, exits and results.
5. Record architecture decisions in `docs/DECISIONS.md`, project-wide unresolved issues in `docs/OPEN_QUESTIONS.md`, changed user-facing behavior in `README.md`, and all changed file paths in the sole root `CHANGELOG.md` (date + concise purpose). Update existing documents instead of creating duplicates.
6. Never silently alter research rules, cost assumptions, data partitions or benchmarks to improve reported performance.
7. Negative and failed experiments are **first-class research records**.
8. The target product is **v1.0 as defined in `docs/PRODUCT_VISION.md`**. Follow `CODEX_START.md` for takeover and implement only the milestone scope authorized by the owner. Later acceptance gates guide design and require separate scope authorization.
9. Record the Test Card before implementation under the [development process](docs/DEVELOPMENT_PROCESS.md#1-write-a-compact-test-card-before-implementation). Mark a milestone `ACCEPTED` in `docs/MILESTONE_STATUS.md` only after its acceptance tests pass and auditable evidence is recorded. Incomplete gates remain open.
10. Keep **software DoD**, **scientifically supported candidate**, and **economically viable candidate** distinct. A profitable strategy is not a prerequisite for a software milestone.

## Model and technology governance

- The model/tool registry and catalog are long-term **planning documents**, not an instruction to install every library in v0.1.
- `CORE`: working capability required by the specified gate. `EVALUATE`: fair comparison or documented reproducible no-go/blocker at that gate. `CONDITIONAL`: assess only if data and use case warrant it. `DEFERRED`: requires explicit later scope authorization.
- Follow the [M2 Definition of Done](docs/MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls) for the required supervised and unsupervised discovery pilots. An anomaly score alone is never alpha.
- Do not silently drop HDBSCAN, autoencoders or any other cataloged model. Record decisions as `ADOPTED`, `REJECTED`, `DEFERRED`, or `BLOCKED_*` with evidence and the relevant gate.
- Distinguish predictive ML, anomaly/regime detection, feature/model selection, research scheduling, decision policy and execution. Every tuning attempt counts toward multiple-testing exposure.
- Check software, model-weight and dataset licenses **separately**. FinBERT weights are not automatically licensed for commercial use.

## Compute Budget First — mandatory from M0

- **Every new AQRS feature proposal must include a visible Resource Governor assessment when proposed**, including proposals made in discussion. Present the assessment before approval or implementation. State the impact on the existing budget and follow the [feature proposal review](docs/RESOURCE_GOVERNOR.md#resource-assessment-for-every-feature-proposal).
- **Run the [Resource Governor preflight](docs/RESOURCE_GOVERNOR.md#2-preflight-before-each-campaign) before every research campaign.** Use the limits in `configs/research.yaml` and account for the full planned search.
- Implement a **real enforcement mechanism** in v0.1: isolated trial execution, external wall-time watchdog, observed RAM/OS-enforced memory guard as supported, fit/trial/campaign/concurrency budgets, persistent stop reasons. If a required safety guarantee is unavailable on the current platform, fail closed rather than silently proceeding.
- Large calibrations and validations require a bounded pilot and conservative documented extrapolation. A predicted multi-year calibration must be rejected at preflight, before the full run begins.
- `REJECTED_PREFLIGHT`, `TIMED_OUT`, `MEMORY_LIMIT`, `BUDGET_EXHAUSTED` describe **execution/resource outcomes**, not negative alpha evidence. No automatic retries, retuning spirals or silent budget escalation.
- Every long-running operation must have an explicit stop path. A bounded, accurately reported partial experiment beats an eight-year calibration. See [`docs/RISK_REGISTER.md`](docs/RISK_REGISTER.md).

## Lean research rules (binding)

- **Lean infrastructure.** Build only the smallest end-to-end workflow that can answer the current research question with adequate evidence.
- **Research hygiene from the first data-based trial.** Use point-in-time inputs. Document execution costs whenever assessing trading outcomes and apply the same cost assumptions to candidates and controls. Reserve the final holdout before exploration and keep it separate until authorized evaluation of a frozen candidate. Follow the [research protocol](docs/RESEARCH_PROTOCOL.md).
- **Fast, counted exploration.** Iterate on development data and record every tested variant in the Research Journal with an ID and reproducible configuration. Include manual screens, null results, failures, and aborted attempts. Log reruns as separate attempts of the same variant.

## Non-negotiable research invariants

- Features, labels and simulated orders have explicit availability timestamps.
- Features computed after the close of bar `t` may use data through `t` only. For v0.1 OHLCV, the earliest modeled entry is `open[t+1]`.
- Forecast horizons, label overlap, purge/embargo or temporal gap, and research/holdout separation must be testable.
- Transformations, feature selectors and models fit on training data only.
- Report prediction accuracy, net economic value and incremental signal value separately.
- Fees, spread and slippage are distinct costs. No free fill at the signal bar close. Apply funding only to relevant instruments at actual funding events.
- Comparable policies and control groups must share execution, position-sizing and cost assumptions.
- The final holdout must never feed the adaptive research priority loop. Repeated feedback consumes holdout independence.
- Never claim genuine alpha from synthetic data or a small cluster of correlated trades.

## v0.1 engineering constraints

- Python 3.11+, CPU-only, local and fully offline without API keys; installed and smoke-tested on Linux.
- Clear modules, type hints, minimal dependencies, deterministic seed, simple configuration.
- Use proven libraries rather than agent frameworks or microservices.
- Use `pytest` for invariants and an end-to-end integration/smoke test.
- Implement a real CLI run with persistent reports. Placeholder modules do not qualify.
- No broker or live orders; no required RL, transformers or commercial Dave Mabe optimizer.
- Start with Ridge/linear or comparably simple methods; complexity requires measured baseline improvement.
- Research decisions and eventual live execution stay separated: a simulated `decision` is not a broker order.

## Review questions before merge

1. Which objective does the change serve? Is the added complexity justified by evidence?
2. Can future information enter features, model selection, labels or execution?
3. Are pre-cost or unmatched-baseline results being misrepresented as alpha?
4. Are rejected/failed experiments still accounted for?
5. Does the entire v0.1 pipeline still reproduce on a clean Linux machine?
6. Are the permanent English-only rules and portable-path rules respected, and did the language checker and manual review pass?
7. Did we reuse canonical documentation, avoid redundant files, and log **every changed path** in the single `CHANGELOG.md`?

## Long-term product boundary

AQRS v1.0 is a locally deployable **research system** with real-data validation, discovery, cost-aware simulation, independent candidate tests, adaptive research management and shadow/paper monitoring. It **does not send live orders**. `docs/MILESTONE_DOD.md` and `docs/PRODUCT_VISION.md` define the north star. Complex models, agents and broker connectivity are not implicitly approved.

## Required final Codex response

Briefly state which files changed, confirm that each appears in `CHANGELOG.md`, list commands **actually run**, passed/failed tests, Linux verification, example artifacts, and what remains open. Do not make unsupported success claims.
