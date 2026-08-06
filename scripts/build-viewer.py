#!/usr/bin/env python3
"""Builds viewer/index.html, a card grid over the snapshotted skills.

Reads skills/, computes the description-overlap signal, and writes a single
self-contained page with the data inlined. Regenerate after every snapshot:

    python3 scripts/build-viewer.py

Design follows the Flowly "Editorial Warmth" spec: cream paper rather than
white, Frank Ruhl Libre paired with Heebo and nothing else, forest-tinted
shadows, mustard as a rare accent.
"""

import hashlib
import html
import json
import pathlib
import re
import sys
from itertools import combinations

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import markdown  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
OUT = ROOT / "viewer" / "index.html"
TRANSLATIONS = ROOT / "viewer" / "translations.json"
BODY_TRANSLATIONS = ROOT / "viewer" / "translations"

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
        rf"^{name}:\s*([>|][-+]?)?\s*\n?((?:(?:  +.*|.*)\n?)*?)(?=^\w+:|\Z)", fm, re.M
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


# A Latin token carrying a dot, slash or hyphen: ".docx", "Monday.com",
# "React/Next.js", "validate-skill.sh". Those inner characters are BiDi-neutral,
# so inside Hebrew flow they drift to the wrong end of the token and a file
# extension renders as "docx." A bare Latin word needs no help and is left
# alone.
TECHNICAL = re.compile(
    r"(?<![\w./-])(\.[A-Za-z][A-Za-z0-9]*|[A-Za-z][A-Za-z0-9]*(?:[._/-][A-Za-z0-9]+)+)"
)


def isolate(text: str) -> str:
    """Escapes for HTML, then wraps technical tokens in <bdi>."""
    return TECHNICAL.sub(r"<bdi>\1</bdi>", escape(text))


def escape(text: str) -> str:
    # Element content, never an attribute value, so quotes stay literal and the
    # in-page search still matches a description the way it is written.
    return html.escape(text, quote=False)


def load_translations() -> dict:
    if not TRANSLATIONS.is_file():
        return {}
    return json.loads(TRANSLATIONS.read_text(encoding="utf-8"))


def translation_for(name: str, entry, sha: str):
    """Returns (hebrew_text, is_stale) for one skill.

    translations.json is hand-maintained, so a malformed or half-written entry
    is a normal thing to hit. Warn and fall back to untranslated rather than
    crashing the build: a viewer missing one translation is far more useful
    than no viewer at all.
    """
    if entry is None:
        return "", False
    if not isinstance(entry, dict):
        print(f"  translation for {name} is {type(entry).__name__}, expected object")
        return "", False
    he = entry.get("he") or ""
    if not he:
        print(f"  translation for {name} has no 'he' text")
        return "", False
    return he, entry.get("src_sha") != sha


def load_body_translation(name: str, src: str):
    """Returns (rendered_html, is_stale) for a full-body Hebrew translation.

    These live in viewer/translations/<skill>.md rather than beside the source
    as SKILL_HE.md, because snapshot-skills.sh replaces skills/ wholesale from
    the account: anything added inside it disappears on the next refresh without
    a word. Outside the mirror they survive.

    Each file carries src_sha, a hash of the SKILL.md it was translated from, so
    an upstream edit marks the translation stale instead of leaving Hebrew that
    quietly no longer matches the English beside it.
    """
    path = BODY_TRANSLATIONS / f"{name}.md"
    if not path.is_file():
        return "", False
    text = path.read_text(encoding="utf-8", errors="replace")
    sha = hashlib.sha256(src.encode()).hexdigest()[:16]
    declared = field(frontmatter(text), "src_sha")
    if not declared:
        print(f"  body translation for {name} has no src_sha; treating as stale")
    body = markdown.body_of(text)
    if not body.strip():
        print(f"  body translation for {name} is empty, skipping")
        return "", False
    return markdown.render(body), declared != sha


def collect() -> list:
    """Reads every skill, attaching its Hebrew translation where one exists.

    Each translation stores a hash of the description it was made from, so a
    description edited upstream marks its translation stale instead of quietly
    showing text that no longer matches. The original is always what the viewer
    shows first: it is the artefact under inspection, and it is what actually
    decides whether the skill loads.
    """
    tr = load_translations()
    rows = []
    for d in sorted(SKILLS.iterdir()):
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        desc = field(fm, "description")
        sha = hashlib.sha256(desc.encode()).hexdigest()[:16]
        he_raw, stale = translation_for(d.name, tr.get(d.name), sha)
        body_he, body_he_stale = load_body_translation(d.name, text)
        rows.append(
            {
                "name": d.name,
                "title": field(fm, "name") or d.name,
                # Rendered as HTML by the viewer, so both are escaped here and
                # the Hebrew gets its technical tokens isolated.
                "desc": escape(desc),
                "he": isolate(he_raw) if he_raw else "",
                "stale": stale,
                # The whole file, rendered, so a card can open its source
                # instead of only advertising that it exists.
                "body": markdown.render(markdown.body_of(text)),
                # Inlined rather than fetched, so the page keeps its translations
                # when it is saved and opened offline.
                "body_he": body_he,
                "body_he_stale": body_he_stale,
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
    translated = sum(1 for r in rows if r["he"])
    stale = [r["name"] for r in rows if r["stale"]]
    untranslated = [r["name"] for r in rows if r["script"] == "אנגלית" and not r["he"]]
    print(
        f"viewer written: {len(rows)} skills, {len(overlaps)} pairs "
        f"({len(unhandled)} unhandled), {translated} translated"
    )
    if stale:
        print(f"  STALE translations (description changed): {', '.join(stale)}")
    if untranslated:
        print(f"  untranslated English: {', '.join(untranslated)}")
    for p in overlaps[:10]:
        mark = "   " if p["cross"] else " ! "
        print(f" {mark}{p['score']:.2f}  {p['a']} <-> {p['b']}  {' '.join(p['shared'][:4])}")


if __name__ == "__main__":
    main()
