#!/usr/bin/env python3
"""Regenerates INDEX.md from the snapshotted skills.

The description field is the whole point of the table. It is the only thing
that decides whether a skill loads at all, so seeing all of them side by side
is what makes overlaps visible: two skills claiming the same kind of request
will compete silently otherwise.

Usage:  python3 scripts/build-index.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_DESC = 300


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def field(fm: str, name: str) -> str:
    """Reads a scalar frontmatter field, folding YAML block scalars to one line."""
    m = re.search(
        rf"^{name}:\s*([>|][-+]?)?\s*\n?((?:(?:  +.*|.*)\n?)*?)(?=^\w+:|\Z)", fm, re.M
    )
    return " ".join(m.group(2).split()) if m else ""


def main() -> None:
    rows = []
    for d in sorted(SKILLS.iterdir()):
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        desc = field(frontmatter(text), "description")
        n_files = sum(1 for p in d.rglob("*") if p.is_file())
        # stat, not len(text): the column is bytes, and most of these files are
        # Hebrew, where one character is two or three UTF-8 bytes.
        rows.append((d.name, desc, n_files, skill_md.stat().st_size))

    lines = [
        "# אינדקס סקילים",
        "",
        f"{len(rows)} סקילים ברמת חשבון, מצולמים מתוך `~/.claude/skills`.",
        "נוצר על ידי `scripts/build-index.py`. אין לערוך ידנית.",
        "",
        "העמודה החשובה כאן היא התיאור. זה השדה היחיד שקובע אם סקיל נטען בכלל,",
        "וכשכולם זה לצד זה אפשר לראות אילו שניים מתחרים על אותה בקשה.",
        "",
        "| סקיל | קבצים | גודל SKILL.md | תיאור |",
        "| --- | --- | --- | --- |",
    ]
    for name, desc, n_files, size in rows:
        desc = desc.replace("|", "\\|")
        if len(desc) > MAX_DESC:
            desc = desc[:MAX_DESC].rstrip() + "…"
        lines.append(f"| `{name}` | {n_files} | {size:,} B | {desc} |")

    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index written: {len(rows)} skills")


if __name__ == "__main__":
    main()
