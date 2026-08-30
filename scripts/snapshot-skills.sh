#!/usr/bin/env bash
# Snapshots account-level Claude skills into this repo.
#
# Skills configured on claude.ai are materialised into every Claude Code
# session's container at ~/.claude/skills. Inside a session they are ordinary
# files, so this script is a plain copy: no API, no app integration.
#
#   claude.ai  ->  (automatic, at session start)  ->  ~/.claude/skills
#              ->  (this script)                  ->  skills/  ->  git
#
# The reverse direction does not exist. Editing a skill here does not change
# what claude.ai serves; that still needs a manual upload in the account
# settings. Treat this repo as a mirror, not as the source of truth.
#
# Usage, from a Claude Code session with this repo cloned:
#   bash scripts/snapshot-skills.sh && git add -A && git commit && git push

set -euo pipefail

SRC="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/skills"

if [ ! -d "$SRC" ]; then
  echo "No skills directory at $SRC" >&2
  echo "Run this inside a Claude Code session, or set CLAUDE_SKILLS_DIR." >&2
  exit 1
fi

# Refuse to touch anything that is not this repo's skills/ directory. The swap
# below deletes a tree, and a wrong ROOT would delete the wrong one.
if [ ! -d "$ROOT/.git" ] || [ "$(basename "$DEST")" != "skills" ]; then
  echo "Refusing to run: $DEST is not this repo's skills directory." >&2
  exit 1
fi

# Mirror rather than merge, so a skill deleted on claude.ai disappears here too
# and the snapshot reflects the account as it actually is.
#
# The copy lands in a staging sibling first and only then replaces skills/, so
# a failure partway leaves the existing snapshot untouched. Deleting first and
# copying second would turn a full disk or an interrupted run into an empty
# skills/ that is easy to commit without noticing.
STAGE="$(mktemp -d "$ROOT/.skills-stage.XXXXXX")"
RETIRED=""
cleanup() {
  [ -n "$STAGE" ] && rm -rf "$STAGE"
  [ -n "$RETIRED" ] && rm -rf "$RETIRED"
  return 0
}
trap cleanup EXIT

# Keyed on where SKILL.md actually is, rather than copying $SRC wholesale.
#
# Claude materialises the account's skills under $SRC, but not at a fixed
# depth: they used to sit directly inside it, then most moved one level down
# into synced/ while a few stayed at the top, and now the synced/ ones sit
# another level down again inside a per-account bucket directory. A plain copy
# mirrors that nesting into skills/, where both builders look for SKILL.md
# exactly one level down — so they would see one skill instead of thirty-eight,
# and because this is a mirror rather than a merge, committing that would
# delete all the rest. It fails silently too: every command still exits 0.
#
# So the search is depth-agnostic rather than pinned to whatever the layout
# happens to be this month: any directory holding a SKILL.md is a skill, at
# whatever depth it turns up. Pinning it is what broke the last two times.
# Pruning at each match keeps a SKILL.md bundled inside a skill's own reference
# material from being mistaken for a skill in its own right.
#
# Flattening by basename keeps skills/ in the shape the rest of the repo
# expects, and leaves it working whichever depth the next layout change picks.
found=0
while IFS= read -r skill; do
  name="$(basename "$skill")"
  if [ -e "$STAGE/$name" ]; then
    echo "Two skills named $name under $SRC; refusing to pick one." >&2
    exit 1
  fi
  cp -r "$skill" "$STAGE/$name"
  found=$((found + 1))
done < <(find "$SRC" -mindepth 1 -type d -exec test -e '{}/SKILL.md' ';' -print -prune | sort)

if [ "$found" -eq 0 ]; then
  echo "No SKILL.md found anywhere under $SRC." >&2
  exit 1
fi

# Carried alongside the skills because the previous snapshot has one, and a
# mirror that drops a file it used to hold is not mirroring.
#
# Depth-agnostic for the same reason the skill search above is: the manifest
# travels with the skills, so every layout change moves it too, and a depth
# pinned here goes stale exactly when the one above does. Skill directories are
# pruned so a manifest.json bundled inside a skill is never mistaken for the
# account's own.
manifest="$(find "$SRC" \
  \( -type d -exec test -e '{}/SKILL.md' ';' -prune \) -o \
  \( -name manifest.json -print \) | sort | head -1)"
if [ -n "$manifest" ]; then
  cp "$manifest" "$STAGE/manifest.json"
elif [ -e "$DEST/manifest.json" ] && [ "${FORCE:-}" != "1" ]; then
  # Losing a file the snapshot already holds is the same class of failure as
  # the collapsing skill count below — the layout moved and the search missed
  # it — and it is quieter, so it gets the same refusal rather than a shrug.
  echo "Refusing: skills/manifest.json exists but no manifest.json was found under $SRC." >&2
  echo "Check the layout under $SRC, or re-run with FORCE=1 if that is real." >&2
  exit 1
fi

# A snapshot that collapses is the signature of the source layout moving
# again, not of thirty skills being deleted from the account on one afternoon.
# The whole point of the staging swap above is that a bad snapshot never lands,
# and "structurally bad" belongs in that category as much as "interrupted".
if [ -d "$DEST" ] && [ "${FORCE:-}" != "1" ]; then
  had=$(find "$DEST" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
  if [ "$had" -gt 0 ] && [ "$found" -lt $(( (had + 1) / 2 )) ]; then
    echo "Refusing: skills/ holds $had skills, this snapshot found only $found." >&2
    echo "Check the layout under $SRC, or re-run with FORCE=1 if that is real." >&2
    exit 1
  fi
fi

# Both moves are renames within the repo, so the window where skills/ does not
# exist is a single syscall wide rather than a whole copy long.
if [ -d "$DEST" ]; then
  RETIRED="$(mktemp -d "$ROOT/.skills-old.XXXXXX")"
  mv "$DEST" "$RETIRED/skills"
fi
mv "$STAGE" "$DEST"
STAGE=""  # consumed by the move; the trap must not delete the new snapshot

count=$(find "$DEST" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
files=$(find "$DEST" -type f | wc -l | tr -d ' ')
echo "Snapshotted $count skills, $files files."
