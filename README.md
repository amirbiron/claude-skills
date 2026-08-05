# claude-skills

A mirror of my account-level Claude skills, so there is somewhere to read them,
diff them, and eventually manage them.

**Private on purpose.** Some of these skills are written about me personally:
`emotional-sharing` carries examples about medication and mood, `idea-storm`
names my projects and what went wrong with them. This repository should not
become public.

## What is here

| Path | What it holds |
| --- | --- |
| `skills/` | One directory per skill, copied verbatim from `~/.claude/skills` |
| `INDEX.md` | Generated table of every skill and its `description` |
| `scripts/snapshot-skills.sh` | Refreshes `skills/` from the current session |
| `scripts/build-index.py` | Regenerates `INDEX.md` |

## How the snapshot works

Skills configured on claude.ai are materialised into every Claude Code session's
container at `~/.claude/skills`. Inside a session they are ordinary files, so
capturing them needs no API and no app integration, just a copy.

```text
claude.ai  ->  (automatic, at session start)  ->  ~/.claude/skills
           ->  (scripts/snapshot-skills.sh)   ->  skills/  ->  git
```

To refresh, from a Claude Code session with this repo cloned:

```bash
bash scripts/snapshot-skills.sh
python3 scripts/build-index.py
git add -A && git commit -m "Refresh skills snapshot" && git push
```

The snapshot mirrors rather than merges, so a skill deleted on claude.ai
disappears here too and the repo reflects the account as it actually is.

## The direction that does not exist

There is no sync back. Editing a `SKILL.md` here changes nothing about what
Claude loads; that still requires uploading the skill in the claude.ai account
settings. This repository is a mirror, not a source of truth, and every workflow
built on it should assume that.

## Why the index matters

`description` is the only field that decides whether a skill loads at all. With
28 skills the descriptions start overlapping quietly, and two of them claiming
the same kind of request will compete with no visible symptom. `INDEX.md` puts
them side by side so the collisions are readable.
