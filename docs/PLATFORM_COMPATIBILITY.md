# Platform compatibility and deployment portability

**Binding from M0/v0.1.** AQRS is **developed and first run natively on Windows**, while **Linux is a required supported target** and deployment must remain **cloud-provider agnostic**. See [`MILESTONE_STATUS.md`](MILESTONE_STATUS.md) for the platforms actually verified.

## 1. Permanent English-only project policy

The canonical policy is [`LANGUAGE_POLICY.md`](LANGUAGE_POLICY.md). All repository documents, code/identifiers, comments, docstrings, configuration descriptions, CLI/help text, logs, research artifacts, experiment metadata and future Codex handoffs must remain in English. The user may communicate in German without introducing non-English repository files. Maintain UTC-aware ISO 8601 timestamps, UTF-8 and clearly labeled financial units. Run `python scripts/check_language_policy.py --self-test` and `python scripts/check_language_policy.py` at each documentation/release gate, plus manual review. Do not remove or weaken the language rule without explicit owner authorization.

## 2. Platform support matrix and honest release claims

| Environment | Requirement | Verification |
|---|---|---|
| **Native Windows 10/11 x86_64, Python 3.11/3.12, CPU** | **Primary local development and execution platform from M0**. No mandatory WSL, Docker, administrator rights or graphical interface for the CLI. | Run the full clean-install, CLI and test sequence in native Windows PowerShell or a native Windows CI runner. |
| **Ubuntu 24.04 LTS x86_64, Python 3.11/3.12, CPU** | **Required Linux compatibility target from M0**, headless, non-root during execution. | Run the same full acceptance suite in an actual Linux runner or server. WSL alone is not a substitute for native Windows verification. |
| Other mainstream Linux distributions / Linux servers | Designed for portability, not automatically certified. | Confirm dependencies, process controls and functional tests before listing as supported. |
| Hetzner, other VPS or cloud providers | **Provider-independent architecture**. No provider API, managed service, cloud account or container runtime required for M0 or the core research engine. | At M7/v0.8, demonstrate a reproducible headless deployment on a representative provider-neutral Linux VM; provider-specific recipes remain optional. |
| macOS, Linux ARM64 and other platforms | Potential future targets only; no guaranteed support at M0. | Add support only after dependency, execution-guard and CI verification. |
| Docker/containers, WSL, remote compute | Optional deployment and development conveniences, never M0 prerequisites. | If introduced, test separately and keep native Windows/Linux paths working. |

Record the actual OS build or distro, architecture, Python version, permissions and runtime capabilities for every platform acceptance. Passing a test under one OS does not imply it passes on another.

## 3. Portable code, paths and persistence

- Use pure/portable Python where reasonable and `pathlib.Path`; no fixed drive letters, POSIX-only paths, personal directories, current-working-directory assumptions or unsafe shell commands. Resolve configured paths relative to a documented base.
- Do not depend on a GUI, GPU, WSL, Docker, root/admin privileges, Bash, PowerShell scripts, systemd, POSIX signals or provider-specific SDKs in the **core runtime**.
- Use Python subprocess/process APIs with platform-specific supervision behind a small adapter. Keep research algorithms, contracts, journal and reporting independent of the OS and hosting provider.
- Support spaces and Unicode in paths, UTF-8 content, different path separators, case-sensitive/insensitive filesystems and Windows/POSIX filesystem permissions. Treat line endings portably; persist portable relative artifact references or structured URIs.
- Use atomic writes where practical and SQLite transactions for journal integrity; test permission denied, read-only storage, interrupted writes and controlled termination.
- All data and experiment times are UTC-aware; use monotonic clocks for budgets. Never use local wall time to infer market-event timing.

## 4. Installation and runtime conventions

- Package with `pyproject.toml` for normal Python virtual environments. Runtime must operate offline after dependencies are installed, with no API key, broker connection or hosting account.
- Use `python -m aqrs ...` and `python -m pip ...` as portable invocations. Virtual-environment activation differs across shells and must be documented accurately.
- Keep configuration (paths, budgets, logs, data locations, worker count) external to source. Do not bake in server addresses, home folders or cloud storage.
- Optional model families may have OS-dependent binary wheels; add them as optional extras after compatibility checks rather than making all model dependencies mandatory in M0.
- A server deployment must not require rewriting feature engineering, validation, research scheduling or journal formats. Cloud services and distributed workers, if ever added, sit behind interfaces and need separate scope/approval.

## 5. Worker, timeout and memory enforcement

- A watchdog must be able to stop a blocked training worker and its descendants on **both supported platforms**. A Python elapsed-time check after `fit()` is not enforcement. Isolate OS-specific supervision behind one documented adapter.
- **Windows:** use a tested Windows-native mechanism suitable for terminating worker trees and enforcing required limits, such as Windows Job Objects where available and configured. Do not assume POSIX process groups or `resource` exist. Running from a normal, non-admin account must be supported.
- **Linux:** use tested POSIX worker/process-group controls and an available, permitted memory mechanism (such as correctly configured delegated cgroup v2), as appropriate. Do not require root after prerequisites are installed.
- A sampled RSS reading is monitoring, **not** a strict kernel-backed RAM cap. `RLIMIT_AS` constrains virtual address space rather than resident RAM; do not equate them. Windows and Linux may need different enforcement capabilities.
- **Fail closed when a required guarantee is unavailable.** A run requiring strict memory containment must be rejected in preflight if the platform adapter cannot provide it. Never silently downgrade a hard cap to monitoring. If the documented M0 example cannot execute under a given capability set, report an honest blocker and provide a separately authorized, explicitly labeled bounded execution mode rather than bypassing the guard.
- **Current implementation.** The watchdog samples worker-tree RSS. `strict` memory requests are rejected before a pilot or trial starts. Windows attaches the interpreter to a kill-on-close Job Object before releasing it. Linux starts the interpreter in a dedicated process group. A closed supervisor pipe also signals the Linux worker to terminate its group. These guards cover trusted M0 workers and descendants in the job or process group.
- Campaign and trial budgets, timeout/cancellation, safe journal status and prohibition on automatic retrials are common semantics on both OSes; test them with artificial blocking and memory-pressure workers without endangering the host.

## 6. M0 acceptance on Windows **and** Linux

Use independent, native OS test runs (locally or in CI). The common command sequence, from the repository root in a clean Python environment, is:

```text
python -m pip install -e ".[dev]"
python -m aqrs research plan --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m pytest -q
python -m ruff check .
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

**Windows setup (PowerShell, native Windows):** `py -3.11 -m venv .venv`, then invoke `.venv\Scripts\python.exe` explicitly or activate the venv. **Linux setup (POSIX shell):** `python3 -m venv .venv`, then invoke `.venv/bin/python` explicitly or activate it. Never rely on Linux activation syntax in Windows documentation. Verify native Windows even if tests also pass in WSL. A future CI workflow should use a Windows + Ubuntu matrix, run the same functional contract tests and label any unavailable checks as blockers rather than silently skipping them.

**Required platform tests on both systems:** clean install, fully offline research run, paths with spaces/Unicode, UTC in a different local timezone, permission/write failures, no GUI, blocked-worker timeout with no orphan descendants, journal integrity, memory-policy enforcement or documented fail-closed behavior, and an accurate platform capability report. Run the native suite before M0 acceptance; no claim of passed tests until recorded in [`MILESTONE_STATUS.md`](MILESTONE_STATUS.md).

## 7. Future provider-neutral server deployment

At M1–M6, preserve cross-platform contracts for new data/models. At M7/v0.8, deliver a reproducible, headless Linux VM deployment guide usable on ordinary hosting providers (including Hetzner or other providers) without provider-specific calls; add configurable storage, restart/stop behavior, backups, logging and recovery tests. Containers may be offered as an **optional** path. At M8/M9 verify a clean native Windows install and a clean headless Linux install using representative datasets and enforced, finite compute budgets. Additional platforms/providers remain explicitly tested additions, not implicit promises.

**Rule:** Develop locally on Windows; validate on native Windows and Linux; remain independent of any cloud provider; extend the core through stable contracts rather than rewrites.
