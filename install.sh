#!/usr/bin/env bash
#
# Installs skills from haruhadj/ai-skills for Claude Code and other
# Agent Skills-compatible tools. Installs every skill by default.
#
#   curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash
#
# Install only specific skills by passing them as arguments:
#
#   curl -fsSL .../install.sh | bash -s -- clean-code
#
# Options (environment variables):
#   SKILLS_DIR=path   install into a specific directory
#   SCOPE=project     install into ./.claude/skills instead of ~/.claude/skills
#   BRANCH=name       install from a branch other than main
#   REF=<git ref>     install from an exact ref or commit SHA (overrides BRANCH)
#   SKILLS="a b"      install only these skills (same as passing arguments)
#
set -euo pipefail

REPO="haruhadj/ai-skills"
BRANCH="${BRANCH:-main}"
REF="${REF:-refs/heads/$BRANCH}"

# Arguments win over $SKILLS; empty means "install everything".
if [ "$#" -gt 0 ]; then
  REQUESTED=("$@")
elif [ -n "${SKILLS:-}" ]; then
  read -r -a REQUESTED <<< "$SKILLS"
else
  REQUESTED=()
fi

# --- work out where to install -------------------------------------------------
if [ -n "${SKILLS_DIR:-}" ]; then
  TARGET_ROOT="$SKILLS_DIR"
elif [ "${SCOPE:-user}" = "project" ]; then
  TARGET_ROOT=".claude/skills"
else
  TARGET_ROOT="$HOME/.claude/skills"
fi

# --- fetch ---------------------------------------------------------------------
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading from $REPO@$REF..."
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" \
  | tar -xz -C "$TMP" --strip-components=1

# --- discover skills -----------------------------------------------------------
AVAILABLE=()
for skill_md in "$TMP"/plugins/*/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  skill_dir="$(dirname "$skill_md")"
  AVAILABLE+=("$(basename "$skill_dir")")
done

if [ "${#AVAILABLE[@]}" -eq 0 ]; then
  echo "Error: no skills found in the downloaded archive." >&2
  exit 1
fi

if [ "${#REQUESTED[@]}" -eq 0 ]; then
  SELECTED=("${AVAILABLE[@]}")
else
  SELECTED=()
  for want in "${REQUESTED[@]}"; do
    found=""
    for have in "${AVAILABLE[@]}"; do
      if [ "$want" = "$have" ]; then
        found="yes"
        break
      fi
    done
    if [ -z "$found" ]; then
      echo "Error: unknown skill '$want'. Available: ${AVAILABLE[*]}" >&2
      exit 1
    fi
    SELECTED+=("$want")
  done
fi

# --- install -------------------------------------------------------------------
mkdir -p "$TARGET_ROOT"

for skill in "${SELECTED[@]}"; do
  src=""
  for candidate in "$TMP"/plugins/*/skills/"$skill"; do
    if [ -f "$candidate/SKILL.md" ]; then
      src="$candidate"
      break
    fi
  done

  if [ -z "$src" ]; then
    echo "Error: SKILL.md not found for '$skill'." >&2
    exit 1
  fi

  target="$TARGET_ROOT/$skill"
  rm -rf "$target"
  cp -R "$src" "$target"
  echo "Installed $skill -> $target"
done

echo
echo "Files:"
for skill in "${SELECTED[@]}"; do
  find "$TARGET_ROOT/$skill" -type f | sed "s|^|  |"
done
echo
echo "Restart your agent (or run /reload-plugins in Claude Code) if it was already running."
