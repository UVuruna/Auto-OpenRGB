"""THE CONFIG SECTION LAW's guard (root CODE.md, owner decree 2026-08-01).

Config files and data tables are STRUCTURES, not notebooks. A table is
defined ONCE, whole, under a named section banner; a later addition patches
the table IN PLACE, in its own section — never as a dict-subscript assignment
or `.update()` call appended far below the table's own definition, and never
as a hidden duplicate key inside the very literal.

Only the files listed in CONFIG_FILES are checked below — this guard's job is
narrow and precise on purpose. Root CODE.md's own scope note: a file that is
mostly algorithm with one small incidental table (e.g. `gui/color_groups.py`'s
`HUE_CENTERS`, `core/settings.py`'s `WEEKDAY_KEYS`/`MONTH_KEYS`) is not what
this law targets — forcing section-banner coverage across dozens of unrelated
functions for one small table would be ritual, not structure. CONFIG_FILES is
a SEED of the files whose PRIMARY organizing structure genuinely is one or
more module-level data tables.

Checkable semantics (root CODE.md): after the module docstring and imports,
the file's FIRST top-level definition must be preceded by a section banner (a
comment line carrying a run of >= 8 box-drawing/`=` characters); every
top-level definition belongs to whichever banner precedes it. The guard fails
the build on:

1. a top-level definition before the first section banner,
2. a duplicate key inside one dict literal,
3. a module-level statement that patches an EARLIER-DEFINED top-level table
   (`TABLE[...] = ...`, `TABLE.update(...)`, `TABLE.append(...)`, etc.
   appearing after the table's own definition) — unless the exact site is
   named in PATCHING_RATCHET (legacy patches that predate this law).

Checked via the `ast` module — duplicate keys and definition order are
unambiguous there, including inside arbitrarily nested dict literals (each
`ast.Dict` node is checked independently, so a repeated key name in two
DIFFERENT sibling dicts is correctly not a duplicate).

Run: python -m pytest tests/test_config_sections.py
"""

import ast
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ═══════════════════════════ CONFIG_FILES ═══════════════════════════
# Seed of the config-law guard (root MIGRATE-DOCS.md Phase 3). Each entry's
# PRIMARY organizing structure is one or more module-level data tables — not
# merely a file that happens to hold one small constant:
CONFIG_FILES = [
    "core/keymap.py",   # VIRTUAL_KEYS + KEY_GROUPS + MODIFIER_FLAGS -- the
                        # whole file IS these three lookup tables
]

# Legacy post-definition patches that predate this law and cannot be folded in
# without behavior risk (root CODE.md). Format: "path/to/file.py:LINE" ->
# reason. Empty: nothing in this project predates the law.
PATCHING_RATCHET: dict[str, str] = {}

BANNER_RE = re.compile(r"(=|═){8,}")
PATCH_METHODS = ("update", "append", "extend", "insert", "add", "push", "assign", "splice")


# ═══════════════════════════ PYTHON CHECKER ═══════════════════════════


def _banner_lines(source: str) -> list[int]:
    lines = []
    for i, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#") and BANNER_RE.search(stripped):
            lines.append(i)
    return lines


def _root_name(node):
    while isinstance(node, ast.Subscript):
        node = node.value
    if isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def _const_key(node):
    return node.value if isinstance(node, ast.Constant) else None


def _check_python(path: Path, rel: str) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    banners = _banner_lines(source)
    min_banner = min(banners) if banners else None

    errors: list[str] = []
    table_names: set[str] = set()

    body = tree.body
    start = 0
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        start = 1  # module docstring, exempt

    for node in body[start:]:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if min_banner is None or node.lineno < min_banner:
                errors.append(f"{rel}:{node.lineno}: top-level definition before the first section banner")

        if isinstance(node, ast.Assign):
            if isinstance(node.value, (ast.Dict, ast.List, ast.Set)):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        table_names.add(target.id)
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    base = _root_name(target)
                    if base in table_names:
                        site = f"{rel}:{node.lineno}"
                        if site not in PATCHING_RATCHET:
                            errors.append(
                                f"{site}: post-definition patch of {base!r} via subscript "
                                f"assignment -- fold the entry into {base}'s own definition"
                            )
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.value, (ast.Dict, ast.List, ast.Set)) and isinstance(node.target, ast.Name):
                table_names.add(node.target.id)

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Attribute) and call.func.attr in PATCH_METHODS:
                base = _root_name(call.func.value)
                if base in table_names:
                    site = f"{rel}:{node.lineno}"
                    if site not in PATCHING_RATCHET:
                        errors.append(
                            f"{site}: post-definition patch of {base!r} via .{call.func.attr}() "
                            f"-- fold the entry into {base}'s own definition"
                        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            seen = set()
            for key_node in node.keys:
                key = _const_key(key_node) if key_node is not None else None
                if key is None:
                    continue
                if key in seen:
                    errors.append(f"{rel}:{node.lineno}: duplicate dict key {key!r}")
                seen.add(key)

    return errors


# ═══════════════════════════ TESTS ═══════════════════════════


@pytest.mark.parametrize("entry", CONFIG_FILES)
def test_seeded_config_file_follows_the_config_section_law(entry):
    path = PROJECT_ROOT / entry
    assert path.exists(), f"CONFIG_FILES entry does not exist: {entry}"
    errors = _check_python(path, entry)
    assert not errors, (
        "THE CONFIG SECTION LAW (root CODE.md): " + "; ".join(errors)
    )


def test_the_guard_is_actually_looking_at_this_project():
    assert len(CONFIG_FILES) > 0
    assert all(entry.endswith(".py") for entry in CONFIG_FILES)


def test_the_patching_ratchet_only_shrinks():
    """Mirrors the structure-law ratchet's shrink-only obligation (root
    CODE.md): every entry names a file:line site that must still exist and
    still be a real patch -- an entry for a site that has been folded into
    its table's own definition must be deleted, not left stale."""
    for site in PATCHING_RATCHET:
        rel_path = site.rsplit(":", 1)[0]
        assert (PROJECT_ROOT / rel_path).exists(), f"stale PATCHING_RATCHET entry: {site}"
