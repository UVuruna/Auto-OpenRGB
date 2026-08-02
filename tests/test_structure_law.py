"""THE STRUCTURE LAW's guard — the god-file ratchet.

Root CLAUDE.md, Priority S / Rule #20 -> THE STRUCTURE LAW (owner decree
2026-07-29, SUPREME): every project carries a structure guard test that FAILS
the build when any file crosses the Violation threshold (~1,000 lines), except
files named in a RATCHET allowlist that may only SHRINK. Each entry documents
why it is tolerated today and which session owes the split. A file that heals
MUST leave the list — the second test enforces that.

The law exists because insistence without enforcement has failed repeatedly
elsewhere in this monorepo (PromptPainter's `gui.py` at 8,800 lines; DOMY
Watch's `defaults.py` at 3,498) — all flagged, all tolerated, because no test
failed. This one fails.

The RATCHET is EMPTY: the 2026-08-02 docs-migration inventory found no file
over ~420 lines (`setup/build.py`, the largest) anywhere in this project — no
god-files exist to tolerate.

Run: python -m pytest tests/test_structure_law.py
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 1000
SUFFIXES = (".py",)
EXCLUDED_DIR_NAMES = {
    ".venv", "venv", "__pycache__", ".git", ".claude", "UV",
    "dist", "build", "cert",
}

# THE RATCHET — may only SHRINK (THE STRUCTURE LAW, clause 3). Adding an entry
# requires the owner's explicit approval in that same session.
# Entry: posix-relative path -> (why it is tolerated, who owes the split).
RATCHET: dict[str, tuple[str, str]] = {}


def _source_files():
    for path in PROJECT_ROOT.rglob("*"):
        if path.suffix not in SUFFIXES or not path.is_file():
            continue
        if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
            continue
        yield path


def _line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def test_no_file_crosses_the_threshold_outside_the_ratchet():
    """No new god-file, ever: every source file over MAX_LINES must be a named,
    owner-approved ratchet entry — otherwise the build fails."""
    offenders = []
    for path in _source_files():
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        if rel in RATCHET:
            continue
        lines = _line_count(path)
        if lines > MAX_LINES:
            offenders.append(f"{rel} ({lines} lines)")
    assert not offenders, (
        "THE STRUCTURE LAW (root CLAUDE.md, Rule #20): these files crossed the "
        f"{MAX_LINES}-line violation threshold and are NOT in the ratchet: "
        + ", ".join(sorted(offenders))
        + ". Split by responsibility, or obtain the owner's explicit ratchet "
        "entry in this same session — never silently."
    )


def test_the_ratchet_only_shrinks():
    """A healed or vanished file must leave the list — the ratchet may never
    hold a file that no longer needs tolerating."""
    stale = []
    for rel in RATCHET:
        path = PROJECT_ROOT / rel
        if not path.exists():
            stale.append(f"{rel} (file no longer exists)")
        elif _line_count(path) <= MAX_LINES:
            stale.append(f"{rel} (healed — {_line_count(path)} lines)")
    assert not stale, (
        "THE STRUCTURE LAW ratchet must SHRINK: delete these entries — "
        + ", ".join(sorted(stale))
    )


def test_the_guard_is_actually_looking_at_this_project():
    """A guard that walks nothing passes forever. Pin that it sees the real
    source tree (core/, gui/, setup/, tests/, and the root-level scripts)."""
    names = {path.name for path in _source_files()}
    assert {"resolver.py", "hotkey_daemon.py", "main.py", "schedule.py",
            "main_window.py", "build.py"} <= names
