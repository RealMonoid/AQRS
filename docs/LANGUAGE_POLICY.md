# Permanent English-only language policy

**Status: binding, repository-wide and ongoing.** This rule applies to all existing project documentation and to every future addition, revision, generated document and Codex development session. It is not limited to the initial handoff, v0.1 or the current milestone. Changing or relaxing it requires an explicit decision by the project owner; Codex must not make that decision independently.

## Required language

All prose created or maintained as part of AQRS must be **English only**. This includes:

- `README.md`, `AGENTS.md`, architecture decisions, specifications, the sole `CHANGELOG.md`, milestone records, research notes, templates, examples, prompts and future handoff packages;
- source-code comments, docstrings, explanatory identifiers, tests and their failure messages;
- YAML/JSON configuration descriptions and comments, SQL descriptions and schema documentation;
- CLI help, diagnostics, logs, reports, notebooks, plots, journal annotations and machine-generated research summaries;
- documentation added or revised by Codex, other agents, maintainers or automated generators.

Project-owner conversations may be in another language. **Do not copy non-English conversation text into repository prose.** Translate and synthesize it into English before writing or updating a file. When importing external materials, distinguish raw source data from AQRS-authored prose. Preserve required proper names, fixed external API identifiers, source titles and legally necessary quotations without translating identifiers incorrectly; the surrounding explanation still must be in English.

## Codex obligations for every change

1. Read this file and `AGENTS.md` before changing anything.
2. Write all new or modified project prose in English, including headings, tables, comments, status notes, release notes and generated output templates.
3. When editing an existing document, retain or normalize its English prose. Never introduce translated-back or mixed-language sections.
4. If a supplied instruction or reference uses a different language, respond to the user conversationally as appropriate but write all repository artifacts in English.
5. Before reporting a milestone or change complete, execute `python scripts/check_language_policy.py` and the self-test command; also review affected prose manually. Record the command results in the Codex completion report.
6. If an imported document is not in English, translate it before merging it into the normative documentation set. If translation cannot be completed, mark the work as blocked rather than silently committing non-English documentation.
7. Do not remove, weaken or bypass the policy, its checker or the CI gate without an explicit, documented decision from the project owner.

## Automated enforcement and limits

The repository includes a dependency-free, cross-platform check:

```bash
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

The check audits Markdown/text documentation and human-readable configuration text for likely non-English (especially German) passages and verifies that the key policy declarations remain present. `.github/workflows/docs-language.yml` runs the same check on GitHub pushes and pull requests. Keep the check active as the repository grows, including Linux and headless execution.

**Important:** A lightweight language heuristic cannot prove that every sentence is English, particularly short headings or code comments. Codex and reviewers remain responsible for checking every modified artifact. Passing the checker is necessary, not sufficient.

## Documentation footprint and history

The documentation repository keeps **one up-to-date canonical file per distinct purpose** and only one root `CHANGELOG.md`. All dated entries, renamed or removed file paths and historical change descriptions belong in that changelog, not in multiple version-suffixed or dated copies. Translate and edit existing files in place; only add a new documentation file for a separately justified need. Retain old versions and dates for history or backward compatibility only if they do not interfere with active functionality, stable references or accurate current instructions. All changelog entries are in English and identify every changed file path. See `AGENTS.md`.

## Acceptance

The language rule is part of the **universal Definition of Done for every milestone through v1.0 and beyond**. A milestone cannot be accepted if its new or edited documentation, Codex additions, reports or code explanations violate this rule, even when its numerical tests pass.
