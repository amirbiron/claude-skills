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

cp -r "$SRC/." "$STAGE/"

# Both moves are renames within the repo, so the window where skills/ does not
# exist is a single syscall wide rather than a whole copy long.
if [ -d "$DEST" ]; then
  RETIRED="$(mktemp -d "$ROOT/.skills-old.XXXXXX")"
  mv "$DEST" "$RETIRED/skills"
fi
mv "$STAGE" "$DEST"
STAGE=""  # consumed by the move; the trap must not delete the new snapshot

count=$(find "$DEST" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
files=$(find "$DEST" -type f | wc -l | tr -d ' ')
echo "Snapshotted $count skills, $files files."
