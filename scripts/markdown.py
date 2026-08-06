"""A small Markdown to HTML renderer for the skills viewer.

Deliberately not a full implementation. It covers what the SKILL.md corpus
actually uses, measured rather than guessed: headings, fenced code, tables,
ordered and unordered lists, blockquotes, rules, and inline emphasis, code and
links. Anything else falls through as a paragraph, which is the honest failure
mode for a source viewer.

Every block carries dir="auto" so Hebrew and English sections each read the
right way inside the same document. Code blocks are pinned LTR regardless.

Input is escaped before any markup is produced, so a SKILL.md cannot inject
HTML into the page.
"""

import html
import re

FENCE = re.compile(r"^```([\w-]*)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
RULE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
ULI = re.compile(r"^\s*[-*+]\s+(.*)$")
OLI = re.compile(r"^\s*(\d+)\.\s+(.*)$")
QUOTE = re.compile(r"^>\s?(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")

# Inline, applied to already-escaped text. Order matters: code first, so that
# emphasis markers inside a code span are left alone.
INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

# Only schemes that cannot execute. skills/ mirrors whatever is installed from
# a marketplace, so the markdown here is third-party text even though it sits in
# a private repo.
SAFE_SCHEME = re.compile(r"(?:https?:|mailto:)", re.I)


def href(target: str) -> str:
    """A link target safe to place inside a double-quoted attribute.

    Two separate holes. The scheme: `javascript:` renders as a live link that
    runs on click. And the quoting: the surrounding escape runs with
    quote=False, so a `"` in the target closes the attribute early and anything
    after it becomes markup — and since the LINK pattern only forbids spaces and
    `)`, an injected attribute can be separated with `/` instead of a space.

    Relative paths and fragments stay as they are; they cannot execute. Anything
    with a scheme must be http, https or mailto to survive.

    Only the quote is escaped here. The caller already ran the whole line through
    html.escape with quote=False, so `&`, `<` and `>` are encoded — escaping them
    a second time turns a query string's `&` into `&amp;amp;` and breaks the URL.
    """
    if ":" in target.split("/")[0] and not SAFE_SCHEME.match(target):
        return ""
    return target.replace('"', "&quot;")


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    holds = []

    def hold(m):
        holds.append(f"<code>{m.group(1)}</code>")
        return f"\x00{len(holds) - 1}\x00"

    out = INLINE_CODE.sub(hold, out)
    out = LINK.sub(
        lambda m: f'<a href="{href(m.group(2))}" rel="noopener noreferrer">{m.group(1)}</a>',
        out,
    )
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)
    return re.sub(r"\x00(\d+)\x00", lambda m: holds[int(m.group(1))], out)


def split_row(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out, i = [], 0

    while i < len(lines):
        line = lines[i]

        fence = FENCE.match(line)
        if fence:
            i += 1
            body = []
            while i < len(lines) and not FENCE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(body), quote=False)
            out.append(f'<pre dir="ltr"><code>{code}</code></pre>')
            continue

        if not line.strip():
            i += 1
            continue

        if RULE.match(line):
            out.append("<hr>")
            i += 1
            continue

        h = HEADING.match(line)
        if h:
            lvl = min(len(h.group(1)) + 1, 6)  # the card already supplies an h3
            out.append(f'<h{lvl} dir="auto">{inline(h.group(2))}</h{lvl}>')
            i += 1
            continue

        # Table: a header row followed by a separator row.
        if "|" in line and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            head = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            th = "".join(f'<th dir="auto">{inline(c)}</th>' for c in head)
            body = "".join(
                "<tr>" + "".join(f'<td dir="auto">{inline(c)}</td>' for c in r) + "</tr>"
                for r in rows
            )
            out.append(
                f'<div class="tbl"><table><thead><tr>{th}</tr></thead>'
                f"<tbody>{body}</tbody></table></div>"
            )
            continue

        if QUOTE.match(line):
            body = []
            while i < len(lines) and QUOTE.match(lines[i]):
                body.append(QUOTE.match(lines[i]).group(1))
                i += 1
            out.append(f'<blockquote dir="auto">{inline(" ".join(body))}</blockquote>')
            continue

        if ULI.match(line) or OLI.match(line):
            ordered = bool(OLI.match(line))
            pat = OLI if ordered else ULI
            items = []
            while i < len(lines) and pat.match(lines[i]):
                m = pat.match(lines[i])
                items.append(m.group(2) if ordered else m.group(1))
                i += 1
            tag = "ol" if ordered else "ul"
            li = "".join(f'<li dir="auto">{inline(t)}</li>' for t in items)
            out.append(f"<{tag}>{li}</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not (
            FENCE.match(lines[i])
            or HEADING.match(lines[i])
            or RULE.match(lines[i])
            or ULI.match(lines[i])
            or OLI.match(lines[i])
            or QUOTE.match(lines[i])
        ):
            para.append(lines[i])
            i += 1
        if para:
            out.append(f'<p dir="auto">{inline(" ".join(para))}</p>')

    return "".join(out)


def body_of(text: str) -> str:
    """Strips YAML frontmatter, leaving the prose the viewer should render."""
    m = re.match(r"^---\n.*?\n---\n(.*)$", text, re.S)
    return m.group(1) if m else text
