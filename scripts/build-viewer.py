#!/usr/bin/env python3
"""Builds viewer/index.html, a card grid over the snapshotted skills.

Reads skills/, computes the description-overlap signal, and writes a single
self-contained page with the data inlined. Regenerate after every snapshot:

    python3 scripts/build-viewer.py

Design follows the Flowly "Editorial Warmth" spec: cream paper rather than
white, Frank Ruhl Libre paired with Heebo and nothing else, forest-tinted
shadows, mustard as a rare accent.
"""

import html
import json
import pathlib
import re
from itertools import combinations

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
OUT = ROOT / "viewer" / "index.html"

# Terms that appear in nearly every description because the format invites
# them. Left in, they make every skill look like every other skill.
STOPWORDS = {
    # English scaffolding
    "the", "this", "that", "and", "for", "with", "when", "use", "user", "users",
    "not", "any", "from", "into", "your", "you", "are", "was", "has", "have",
    "can", "will", "should", "would", "using", "used", "uses", "asks", "ask",
    "want", "wants", "like", "such", "other", "than", "also", "only", "even",
    "instead", "trigger", "triggers", "skill", "skills", "these", "those",
    "them", "they", "its", "their", "about", "over", "more", "most", "some",
    "all", "one", "two", "new", "example", "examples", "including", "include",
    # Hebrew scaffolding
    "של", "את", "על", "לא", "או", "גם", "כמו", "כדי", "אבל", "זה", "זו",
    "יש", "אין", "כל", "כאשר", "אם", "רק", "עם", "אל", "לו", "לה", "הוא",
    "היא", "הם", "הן", "אני", "אתה", "אנחנו", "מה", "מי", "איך", "למה",
    "השתמש", "בסקיל", "סקיל", "הזה", "הזאת", "אותו", "אותה", "בכל", "פעם",
    "משתמש", "המשתמש", "צריך", "יכול", "כמה", "בין", "לפי", "תוך", "אחר",
    "אחרת", "במקום", "וגם", "שלו", "שלה", "שלי", "עבור", "בתוך",
}

TOKEN = re.compile(r"[A-Za-z֐-׿][A-Za-z֐-׿'-]{2,}")

# A term carried by more than this share of the corpus says nothing about which
# skill it belongs to, so it is dropped before similarity is measured.
UBIQUITY_CUTOFF = 0.45
# Jaccard over the surviving vocabulary. Tuned against this corpus: high enough
# that unrelated skills stay silent, low enough to surface genuine rivals.
OVERLAP_THRESHOLD = 0.075


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def field(fm: str, name: str) -> str:
    m = re.search(
        rf"^{name}:\s*(>-|\|)?\s*\n?((?:(?:  +.*|.*)\n?)*?)(?=^\w+:|\Z)", fm, re.M
    )
    return " ".join(m.group(2).split()) if m else ""


def terms(text: str) -> set:
    return {t.lower() for t in TOKEN.findall(text)} - STOPWORDS


def script_of(text: str) -> str:
    heb = len(re.findall(r"[֐-׿]", text))
    lat = len(re.findall(r"[A-Za-z]", text))
    if heb and lat:
        ratio = heb / (heb + lat)
        if 0.15 < ratio < 0.85:
            return "מעורב"
        return "עברית" if ratio >= 0.85 else "אנגלית"
    return "עברית" if heb else "אנגלית"


def collect() -> list:
    rows = []
    for d in sorted(SKILLS.iterdir()):
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        desc = field(fm, "description")
        rows.append(
            {
                "name": d.name,
                "title": field(fm, "name") or d.name,
                "desc": desc,
                "files": sum(1 for p in d.rglob("*") if p.is_file()),
                "bytes": skill_md.stat().st_size,
                "script": script_of(desc),
                "terms": terms(desc),
            }
        )
    return rows


def find_overlaps(rows: list) -> list:
    """Pairs of skills whose descriptions compete for the same requests.

    Only the distinctive vocabulary counts: a term that most descriptions carry
    is scaffolding, not a claim about what the skill is for.

    Lexical overlap alone would mislead, and this corpus shows exactly how.
    skill-forge, skill-creator and skills-il-skill-creator obviously compete,
    yet they score near zero against each other, because their descriptions
    were written to disambiguate and therefore deliberately avoid each other's
    words. So each pair also carries whether either description names the other
    skill. A pair that shares vocabulary and does NOT cross-reference is the
    one worth acting on; a pair that cross-references has already been handled.
    """
    n = len(rows)
    freq = {}
    for r in rows:
        for t in r["terms"]:
            freq[t] = freq.get(t, 0) + 1
    common = {t for t, c in freq.items() if c > n * UBIQUITY_CUTOFF}

    pairs = []
    for a, b in combinations(rows, 2):
        ta, tb = a["terms"] - common, b["terms"] - common
        if not ta or not tb:
            continue
        shared = ta & tb
        score = len(shared) / len(ta | tb)
        cross = b["name"] in a["desc"] or a["name"] in b["desc"]
        if score >= OVERLAP_THRESHOLD or cross:
            pairs.append(
                {
                    "a": a["name"],
                    "b": b["name"],
                    "score": round(score, 3),
                    "shared": sorted(shared, key=len, reverse=True)[:8],
                    "cross": cross,
                }
            )
    # Unhandled collisions first: those are the ones that need a decision.
    return sorted(pairs, key=lambda p: (p["cross"], -p["score"]))


def main() -> None:
    rows = collect()
    overlaps = find_overlaps(rows)
    # Only unhandled collisions earn a badge on the card. A cross-referenced
    # pair is documented, not a problem.
    unhandled = [p for p in overlaps if not p["cross"]]
    flagged = {p["a"] for p in unhandled} | {p["b"] for p in unhandled}

    for r in rows:
        r.pop("terms")
        r["flagged"] = r["name"] in flagged

    template = (pathlib.Path(__file__).parent / "viewer-template.html").read_text(
        encoding="utf-8"
    )
    page = template.replace(
        "/*__DATA__*/",
        "const SKILLS = %s;\nconst OVERLAPS = %s;"
        % (
            json.dumps(rows, ensure_ascii=False),
            json.dumps(overlaps, ensure_ascii=False),
        ),
    ).replace("__COUNT__", str(len(rows))).replace(
        "__OVERLAP_COUNT__", str(len(overlaps))
    )

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(
        f"viewer written: {len(rows)} skills, {len(overlaps)} pairs "
        f"({len(unhandled)} unhandled)"
    )
    for p in overlaps[:10]:
        mark = "   " if p["cross"] else " ! "
        print(f" {mark}{p['score']:.2f}  {p['a']} <-> {p['b']}  {' '.join(p['shared'][:4])}")


if __name__ == "__main__":
    main()
