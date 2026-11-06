# Changelog

The **only** changelog in this repository. Entries are in English, newest first, and include the date (`YYYY-MM-DD`), purpose and every added, modified, moved or deleted file path. Keep older entries here, not in separate `CHANGELOG_V*.md` files. Historical version labels below document prior handoffs; they do not govern runtime behavior or replace current specifications.

## 2026-11-06 — Upgrade the M0 workflow actions to Node.js 24

Update checkout, Python setup and artifact upload to releases that declare
Node.js 24. Track the hosted matrix and warning check in the milestone record.

**Paths**

- `.github/workflows/docs-language.yml`
- `CHANGELOG.md`
- `docs/MILESTONE_STATUS.md`

## 2026-11-06 — Record GitHub Actions acceptance for M0

Record the successful Windows and Ubuntu matrix on Python 3.11 and 3.12, with job
links, campaign IDs and verified artifact evidence.

**Paths**

- `CHANGELOG.md`
- `docs/MILESTONE_STATUS.md`

## 2026-11-06 — Implement the M0 synthetic walking skeleton

Add the installable offline CLI, causal synthetic research folds, two Ridge candidates,
matched controls, native worker supervision, persistent attempt history and audit reports.
Extend the existing CI workflow to exercise the Windows and Ubuntu acceptance commands.
Record run evidence and remaining release gates in the canonical milestone status.

**Paths**

- `.github/workflows/docs-language.yml`
- `CHANGELOG.md`
- `CODEX_START.md`
- `README.md`
- `configs/research.yaml`
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/DECISIONS.md`
- `docs/DEFINITION_OF_DONE.md`
- `docs/MILESTONE_STATUS.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/PLATFORM_COMPATIBILITY.md`
- `docs/RESOURCE_GOVERNOR.md`
- `docs/RISK_REGISTER.md`
- `pyproject.toml`
- `src/aqrs/__init__.py`
- `src/aqrs/__main__.py`
- `src/aqrs/config.py`
- `src/aqrs/evaluation.py`
- `src/aqrs/governor.py`
- `src/aqrs/journal.py`
- `src/aqrs/market.py`
- `src/aqrs/planning.py`
- `src/aqrs/platform_guard.py`
- `src/aqrs/research.py`
- `src/aqrs/storage.py`
- `src/aqrs/worker.py`
- `tests/test_cli.py`
- `tests/test_evaluation.py`
- `tests/test_governor.py`
- `tests/test_market.py`

## 2026-11-06 — Native Windows first, verified Linux support and provider-neutral deployment

**Purpose:** Correct the operating-system assumption to match the owner's actual environment. AQRS runs initially on **native Windows**; **Linux remains a required, independently verified target**. Keep the research engine cloud-provider neutral for later Hetzner or other Linux VM deployments, without creating hosting infrastructure during M0. Make OS-specific process/memory guards explicit and enforceable or fail closed. The English-only repository policy and single-changelog rule remain unchanged. The existing v0.1 scientific requirements, compute limits and model roadmap are retained.

**Changed paths:**
- `.github/workflows/docs-language.yml`
- `AGENTS.md`
- `CHANGELOG.md`
- `CODEX_PROMPT.txt`
- `CODEX_START.md`
- `HANDOFF_MANIFEST.md`
- `README.md`
- `SHA256SUMS.txt`
- `docs/ARCHITECTURE.md`
- `docs/CHAT_SYNTHESIS.md`
- `docs/CONTRACTS.md`
- `docs/DECISIONS.md`
- `docs/DEFINITION_OF_DONE.md`
- `docs/DEVELOPMENT_PROCESS.md`
- `docs/MILESTONE_DOD.md`
- `docs/MILESTONE_STATUS.md`
- `docs/MODEL_EVALUATION_PROTOCOL.md`
- `docs/MODEL_TOOL_CATALOG.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/PLATFORM_COMPATIBILITY.md`
- `docs/PRODUCT_VISION.md`
- `docs/PROJECT_BRIEF.md`
- `docs/RESOURCE_GOVERNOR.md`
- `docs/RISK_REGISTER.md`
- `docs/ROADMAP.md`

**Verification:** Language-policy self-test, full English document audit, internal link check, package checksum verification, and ZIP integrity checks; cross-platform application execution remains pending Codex implementation.

---

## 2026-11-06 — Binding backward development, fault-tree risk gates and incident learning

**Purpose:** Make Codex's software construction follow backward acceptance planning then forward evidence-driven implementation. Add qualitative Fault Tree Analysis before critical scientific/operational boundary changes, blameless postmortems for material/repeated incidents, and a compact searchable ledger of consequential rejected ideas. Keep Build–Measure–Learn, WIP=1, hard compute budgets, Linux/English requirements and one canonical changelog. No new per-incident or per-idea documentation files.

**Changed paths:**
- `AGENTS.md`
- `CHANGELOG.md`
- `CODEX_PROMPT.txt`
- `CODEX_START.md`
- `HANDOFF_MANIFEST.md`
- `README.md`
- `SHA256SUMS.txt`
- `docs/DECISIONS.md`
- `docs/DEFINITION_OF_DONE.md`
- `docs/DEVELOPMENT_PROCESS.md`
- `docs/MILESTONE_DOD.md`
- `docs/MILESTONE_STATUS.md`
- `docs/RISK_REGISTER.md`
- `docs/ROADMAP.md`

**Verification:** Documentation/language/link checks and archive integrity run on this handoff package. These are specifications only: no AQRS application has been implemented or Linux runtime acceptance claimed.

---

## 2026-11-06 — Lean Build–Measure–Learn development workflow

**Purpose:** Apply Lean Startup principles to **Codex's software construction process**, separately from AQRS's internal alpha-research loop. Require risk-first Test Cards, small vertical slices, measured Learning Cards, WIP=1, budgeted work, explicit continue/pivot/stop/defer decisions and minimal innovation accounting. Preserve permanent English-only documentation, headless Linux support, the mandatory Resource Governor and the single-changelog policy. Avoid paid Lean tools or an additional project-management system.

**Changed paths:**
- `AGENTS.md`
- `CHANGELOG.md`
- `CODEX_PROMPT.txt`
- `CODEX_START.md`
- `HANDOFF_MANIFEST.md`
- `README.md`
- `SHA256SUMS.txt`
- `docs/DECISIONS.md`
- `docs/DEFINITION_OF_DONE.md`
- `docs/DEVELOPMENT_PROCESS.md` — **new** canonical build-process document.
- `docs/MILESTONE_DOD.md`
- `docs/MILESTONE_STATUS.md`
- `docs/ROADMAP.md`

**Verification:** Language-policy check and self-test, document links, changelog path coverage, manifests, and archive integrity. This remains a documentation handoff; no running AQRS application is claimed.

---

## 2026-11-06 — Documentation consolidation and long-term file governance

**Decision:** Maintain one canonical document per subject and exactly one repository changelog. Revise existing documents instead of creating dated or versioned duplicates. Historical dates/versions are permitted only as non-disruptive audit metadata or necessary backward-compatible contracts. The root changelog must list all changed files, including added, deleted and renamed paths; the current documentation must stay readable, concise and accurate.

**Modified files:**

- `AGENTS.md` — binding file-creation and documentation discipline, pre-merge review.
- `CODEX_START.md` — mandatory one-changelog and in-place-edit instruction.
- `CODEX_PROMPT.txt` — restates policy in the Codex handoff.
- `README.md` — current documentation maintenance guidance; replaces version-specific changelog link.
- `docs/DECISIONS.md` — ADR-036 documents the long-term decision.
- `docs/LANGUAGE_POLICY.md` — aligns the permanent English policy with one canonical changelog.
- `docs/MILESTONE_DOD.md` — universal documentation and path-coverage gate.
- `docs/DEFINITION_OF_DONE.md` — v0.1 documentation acceptance and completion report.
- `HANDOFF_MANIFEST.md` — references the single changelog and updated maintenance rules.
- `scripts/check_language_policy.py` — detects parallel/versioned changelogs in the documentation audit.
- `SHA256SUMS.txt` — regenerated integrity inventory (packaging output, not a runtime dependency).

**Consolidated history:**

- Added `CHANGELOG.md` (this file) as the sole canonical changelog.
- Removed `CHANGELOG_V3.md`, `CHANGELOG_V4.md`, `CHANGELOG_V5.md`, `CHANGELOG_V6.md` after preserving their complete text below.

**Verification:** language-policy checker and self-test, single-changelog guard, internal Markdown references, checksums and archive integrity. No AQRS application code or live trading functionality was modified in this documentation-only handoff.

---

## 2026-11-06 — Previous handoff v6: AQRS handoff v6 — permanent English-only documentation and Codex policy

### Change requested by the project owner

English is now the **explicit, binding, permanent internal language** for all AQRS documents and every future addition or revision by Codex or any other contributor. The rule applies beyond the current handoff, beyond v0.1 and beyond v1.0. External conversation language does not change repository language.

### Implementation

- Added `docs/LANGUAGE_POLICY.md` as the normative repository-wide policy and translation workflow.
- Strengthened `AGENTS.md`, `CODEX_START.md`, `CODEX_PROMPT.txt`, `README.md`, `docs/PLATFORM_COMPATIBILITY.md`, `docs/MILESTONE_DOD.md`, `docs/DEFINITION_OF_DONE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md` and `docs/PRODUCT_VISION.md`.
- Added the cross-platform, dependency-free `scripts/check_language_policy.py`, including a self-test and checks that core policy declarations remain present.
- Added `.github/workflows/docs-language.yml` for automated checks on pushes and pull requests, with mandatory manual review for text the heuristic cannot reliably classify.
- Regenerated the archive manifest and file checksums. All original scientific, model-selection, Linux and Resource Governor requirements remain unchanged.

### Important limitation

The language checker detects likely violations but is not a perfect natural-language classifier. It cannot guarantee every short phrase or future generated output is English. Codex must also review every changed document and generated prose artifact before milestone acceptance.

---

## 2026-11-06 — Previous handoff v5: AQRS handoff v5 — English research language and Linux-first compatibility

**Date:** November 6, 2026.

### New binding decisions

1. English is the canonical language for all internal research artifacts: documentation, code comments, identifiers, command output, reports, structured metadata, logs and future Codex instructions.
2. Linux is an explicitly supported, tested target beginning in M0/v0.1. Initial acceptance baseline: headless Ubuntu 24.04 LTS x86_64, Python 3.11/3.12, CPU-only, no GUI or runtime root privileges.
3. Portability is an architectural constraint: use `pathlib`, virtual environments, ISO 8601 UTC, UTF-8, no hardcoded user-specific paths or external runtime services.
4. The Resource Governor's OS-level enforcement promises must be honest and tested. RAM polling is not a kernel hard cap. Fail closed on an unavailable required guarantee.
5. All milestone gates, including M0 and final M9/v1.0, must provide actual Linux test evidence rather than only nominal Python compatibility.

### Changes

- Translated the full v4 documentation set, Codex start/prompt, configuration comments and model/tool registry descriptions to English while retaining research requirements and stable machine identifiers.
- Added [`docs/PLATFORM_COMPATIBILITY.md`](docs/PLATFORM_COMPATIBILITY.md) and extended `AGENTS.md`, the milestone acceptance rules, architecture, research contracts, Resource Governor and roadmap.
- Preserved the v4 model catalog, alpha-research goals, resource budgets and no-live-trading boundary. No research strategy or real-market result is claimed.

### Status

This is a handoff specification. Python implementation and Linux execution are **future work for Codex**, not done by translation of the documents.

---

## 2026-11-06 — Previous handoff v4: AQRS handoff v4 — Compute Budget First (November 6, 2026)

### Motivation

An earlier research framework reportedly produced a calibration estimate of **eight years**. Accordingly, compute budgeting became a binding **software requirement beginning with v0.1**, not an optional operational aspiration.

### Added

- `docs/RESOURCE_GOVERNOR.md`: architecture, technical constraints, default budgets, lifecycle, preflight, active worker/memory controls and acceptance tests G01–G07.
- `docs/RISK_REGISTER.md`: three scientific/economic and three technical failure risks with mitigations and milestone linkage.
- `configs/research.yaml`: configurable `resource_governor` limits.

### Updated obligations

- `AGENTS.md`, `CODEX_START.md`, `CODEX_PROMPT.txt`, `README.md`, `docs/DEFINITION_OF_DONE.md`, `docs/MILESTONE_DOD.md` (M0–M9), `docs/CONTRACTS.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, `docs/PRODUCT_VISION.md`, `docs/RESEARCH_PROTOCOL.md`, `docs/MODEL_EVALUATION_PROTOCOL.md`, `docs/MODEL_TOOL_CATALOG.md` and milestone status were revised to reflect bounded execution and resource accounting.
- M0 must reject a multi-year fit plan **before execution**, demonstrate actual worker timeouts and avoid automatic retraining loops.
- Resource termination is an execution outcome, not a statistically negative alpha finding.

---

## 2026-11-06 — Previous handoff v3: Changes relative to AQRS handoff v2 (November 6, 2026)

**Reason:** The model and software-tool catalog was incomplete and did not clearly direct Codex's future work.

### Added documents

- `docs/MODEL_TOOL_CATALOG.md`: 32 named models/methods and 19 engineering/infrastructure tools, including role, library/project, earliest gate, baseline and adoption status.
- `docs/MODEL_EVALUATION_PROTOCOL.md`: model cards, fair baselines, train-only fitting, cost/resource checks, decision statuses and acceptance tests.
- `configs/model_tool_registry.json`: machine-readable **planning registry**, not runtime dependency installation or evidence of working implementations.

### Updated commitments

- **v0.1** remains a lean, CPU-only walking skeleton, with no forced model zoo.
- **v0.3:** conduct reproducible supervised (LightGBM) and unsupervised (Isolation Forest) discovery pilots. Record a documented pilot, blocker or no-go decision for XGBoost, HDBSCAN, autoencoders, PCA and Random Forest.
- **v0.9/v1.0:** every registry entry must have a defensible final decision status. End-to-end demonstrations must include at least one functioning supervised and one functioning unsupervised discovery route, without any profitability requirement.
- Choose models based on incremental independent results, data quality, licensing and resource constraints, not a fashionable architecture.
