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
DEST="$(cd "$(dirname "$0")/.." && pwd)/skills"

if [ ! -d "$SRC" ]; then
  echo "No skills directory at $SRC" >&2
  echo "Run this inside a Claude Code session, or set CLAUDE_SKILLS_DIR." >&2
  exit 1
fi

# Mirror rather than merge, so a skill deleted on claude.ai disappears here too
# and the snapshot reflects the account as it actually is.
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"

count=$(find "$DEST" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
files=$(find "$DEST" -type f | wc -l | tr -d ' ')
echo "Snapshotted $count skills, $files files."
