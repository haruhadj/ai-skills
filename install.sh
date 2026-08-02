#!/usr/bin/env bash
#
# Installs the clean-code skill for Claude Code and other Agent Skills-compatible tools.
#
#   curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash
#
# Options (environment variables):
#   SKILLS_DIR=path   install into a specific directory
#   SCOPE=project     install into ./.claude/skills instead of ~/.claude/skills
#   BRANCH=name       install from a branch other than main
#   REF=<git ref>     install from an exact ref or commit SHA (overrides BRANCH)
#
set -euo pipefail

REPO="haruhadj/ai-skills"
BRANCH="${BRANCH:-main}"
REF="${REF:-refs/heads/$BRANCH}"
SKILL_NAME="clean-code"

# --- work out where to install -------------------------------------------------
if [ -n "${SKILLS_DIR:-}" ]; then
  TARGET_ROOT="$SKILLS_DIR"
elif [ "${SCOPE:-user}" = "project" ]; then
  TARGET_ROOT=".claude/skills"
else
  TARGET_ROOT="$HOME/.claude/skills"
fi

TARGET="$TARGET_ROOT/$SKILL_NAME"

# --- fetch ---------------------------------------------------------------------
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading $SKILL_NAME from $REPO@$REF..."
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" \
  | tar -xz -C "$TMP" --strip-components=1

SRC="$TMP/plugins/$SKILL_NAME/skills/$SKILL_NAME"
if [ ! -f "$SRC/SKILL.md" ]; then
  echo "Error: SKILL.md not found in the downloaded archive." >&2
  exit 1
fi

# --- install -------------------------------------------------------------------
mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET"
cp -R "$SRC" "$TARGET"

echo "Installed to $TARGET"
echo
echo "Files:"
find "$TARGET" -type f | sed "s|^|  |"
echo
echo "Restart your agent (or run /reload-plugins in Claude Code) if it was already running."
