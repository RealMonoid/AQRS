#!/usr/bin/env python3
"""Check the permanent English-only documentation policy (stdlib only).

This is a conservative heuristic, not a language classifier. Manual review remains
mandatory for every changed AQRS artifact.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".yaml", ".yml", ".json"}
SKIP_DIRS = {".git", ".venv", "venv", "build", "dist", "artifacts", "outputs", "__pycache__"}
POLICY_DECLARATIONS = {
    "AGENTS.md": "English-only repository policy (permanent)",
    "CODEX_START.md": "English-only repository policy (permanent)",
    "docs/LANGUAGE_POLICY.md": "Permanent English-only language policy",
}
GERMAN_TERMS = set((
    "aber alle als also auch auf aus bekommen bevor bei bereits bis bleibt bitte damit danach "
    "dann dass dein deine deiner dem den dennoch der deren diese dieser dieses diesen dir doch "
    "durch dürfen ein eine einer eines endlich ergebnis ergebnisse erstellen erst falls finden "
    "für gegen haben hier immer kann keine keinen können mit muss müssen nach nicht nur "
    "oder prüfen schritt sein sollte sollen sowie statt trotzdem und unser unsere werden "
    "wichtig wenn wieder wird wir wurden wurde wobei zusätzlich zwischen zusammen"
).split())
GERMAN_HEADINGS = set((
    "einleitung zusammenfassung ergebnisse anforderungen entscheidungen voraussetzungen "
    "entwicklungsauftrag beispiele beispiel schlussfolgerung ausblick übergabe inhalt"
).split())
WORD = re.compile(r"[a-zA-ZäöüÄÖÜß]+")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")


def german_issue(line: str) -> bool:
    """Flag likely German explanatory prose, avoiding isolated names/identifiers."""
    cleaned = URL.sub("", INLINE_CODE.sub("", line)).strip()
    cleaned = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|#+\s*)", "", cleaned)
    words = [word.lower() for word in WORD.findall(cleaned)]
    if not words:
        return False
    if words[0] in GERMAN_HEADINGS and len(words) <= 9:
        return True
    marked = sum(word in GERMAN_TERMS for word in words)
    has_diacritic = bool(re.search("[äöüÄÖÜß]", cleaned))
    return marked >= 3 or (marked >= 2 and has_diacritic)


def collect_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def audit(root: Path) -> tuple[int, list[str]]:
    issues: list[str] = []
    for relative, marker in POLICY_DECLARATIONS.items():
        path = root / relative
        if not path.is_file() or marker not in path.read_text(encoding="utf-8"):
            issues.append(f"{relative}: required binding language policy is missing")
    # Keep documentation history in one canonical, version-neutral file.
    if not (root / "CHANGELOG.md").is_file():
        issues.append("CHANGELOG.md: required canonical changelog is missing")
    for path in sorted(root.glob("CHANGELOG*")):
        if path.name != "CHANGELOG.md" and path.is_file():
            issues.append(f"{path.name}: duplicate/versioned changelog is prohibited")
    checked = 0
    for path in collect_files(root):
        checked += 1
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeError:
            issues.append(f"{path.relative_to(root)}: not readable as UTF-8")
            continue
        for number, line in enumerate(lines, 1):
            if german_issue(line):
                issues.append(f"{path.relative_to(root)}:{number}: review likely non-English prose")
    return checked, issues


def self_test():
    assert german_issue("Diese Dokumente müssen immer auf Englisch geschrieben werden.")
    assert german_issue("Wir prüfen die Hypothesen und erstellen neue Berichte.")
    assert german_issue("# Anforderungen")
    assert not german_issue("All project documentation and future Codex edits must be written in English.")
    assert not german_issue("The model and research journal are versioned and auditable.")
    assert not german_issue("The paper cites Müller and discusses out-of-sample model selection.")
    print("Language-policy checker self-test passed.")


def main():
    parser = argparse.ArgumentParser(description="Audit AQRS documentation for English-only policy violations.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to inspect")
    parser.add_argument("--self-test", action="store_true", help="Run detector examples before auditing")
    arguments = parser.parse_args()
    if arguments.self_test:
        self_test()
    root = arguments.root.resolve()
    count, issues = audit(root)
    if issues:
        print(f"FAIL: {len(issues)} possible language-policy violations in {count} checked files:")
        for issue in issues:
            print(f"  {issue}")
        raise SystemExit(1)
    print(f"PASS: checked {count} documentation/configuration files; no obvious German prose detected.")
    print("Manual review remains mandatory; this heuristic is not proof of English-only text.")


if __name__ == "__main__":
    main()
