# AQRS English-only, Windows/Linux portable Codex handoff manifest

**Status:** Documents and configuration only. No `aqrs` application has been implemented by this handoff. Codex must build M0/v0.1 and perform **native Windows and independent Linux** execution tests.

## Entry points

1. Read `docs/LANGUAGE_POLICY.md` and `AGENTS.md` (permanent English-only policy, native Windows/Linux, research and compute rules).
2. Read `CODEX_START.md` (the only currently authorized implementation milestone).
3. Read `docs/PRODUCT_VISION.md`, `docs/MILESTONE_DOD.md` and `docs/DEVELOPMENT_PROCESS.md` (end state, acceptance gates and the mandatory development method).
4. Read `docs/PLATFORM_COMPATIBILITY.md` (English, native Windows/Linux and provider-neutral platform contract).
5. Use `CODEX_PROMPT.txt` as the opening development instruction in Codex.

## Included specification groups

- **Project context:** README, conversation synthesis, project brief, decisions, open questions, and the sole root `CHANGELOG.md`.
- **Scientific contracts:** research protocol, data/event/experiment contracts, architecture and risk register.
- **Models/tools:** Markdown catalog, adoption/evaluation protocol, structured JSON registry (32 method entries and 19 infrastructure entries).
- **Compute:** Resource Governor specification and configured bounded research defaults.
- **Delivery:** milestone roadmap, current and future definitions of done, status and acceptance-evidence template.
- **Development workflow:** binding [`docs/DEVELOPMENT_PROCESS.md`](docs/DEVELOPMENT_PROCESS.md) specifies risk-first Build–Measure–Learn, **Backward Development → Forward Execution**, Test/Learning Cards, WIP=1, small vertical slices, critical-risk Fault Tree Analysis, triggered postmortems and remembered rejected ideas; separate from financial alpha-research. No per-loop documentation sprawl.
- **Portability and language:** permanent English-only policy, language checker and GitHub CI gate, native Windows and headless Linux support, `.editorconfig` (UTF-8/LF), `.gitattributes` (LF).

## Mandatory change documentation

Codex must update canonical documents in place, not create dated/versioned copies. Maintain **exactly one** root `CHANGELOG.md`, with dated entries referencing every modified, added, renamed or removed file path. Preserve old versions and dates solely for non-disruptive history or necessary compatibility. Review file diffs against the changelog before closing any work.

## Mandatory English-only check

Run `python scripts/check_language_policy.py --self-test` and `python scripts/check_language_policy.py` on every documentation change. All future Codex revisions must comply; the automated detector is a guardrail, not a substitute for manual review.

## Archive verification (platform-independent)

From the extracted project root on Linux (or any shell with `sha256sum`):

```bash
sha256sum -c SHA256SUMS.txt
```

On native Windows, the same check can be done without Unix tools by running the following from PowerShell or a Windows terminal:

```powershell
python -c "import hashlib,pathlib,sys; rows=[line.split('  ',1) for line in pathlib.Path('SHA256SUMS.txt').read_text(encoding='utf-8').splitlines()]; failed=[path for digest,path in rows if not pathlib.Path(path).is_file() or hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()!=digest]; print('FAIL: '+', '.join(failed) if failed else 'PASS: matching hashes'); sys.exit(bool(failed))"
```

This verifies the handoff files, **not** that M0/v0.1 software exists or that any future algorithm is profitable.

## Compatibility baseline

- Native Windows 10/11 x86_64 is the primary local run target (normal user, CPU-only, no WSL); Ubuntu 24.04 LTS x86_64, Python 3.11/3.12 is the independent headless, non-root Linux test target.
- Portable `pathlib` paths, UTF-8, UTC-aware timestamps, no required GPU, WSL, Docker, cloud service or broker; cloud-provider-neutral Linux VM deployment is planned for a later milestone.
- Explicit process/timeout and truthful RAM enforcement. Do not call RSS polling a kernel-enforced hard memory cap.

## Long-term scope

Version 1.0 is a local adaptive alpha research laboratory with real data, discovery, matched controls, independent validation, adaptive budgeted experiments and shadow/paper monitoring. It is **not** a live real-money trading bot. Only M0/v0.1 is authorized now.
