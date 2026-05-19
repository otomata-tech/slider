#!/usr/bin/env bash
# install.sh — Install slider in a cloistered (mission-scoped) environment.
#
# Creates two symlinks INSIDE the mission, without touching global ~/.claude
# or ~/.local. Run from anywhere; paths are resolved relative to this script.
#
# Skill : <mission>/.claude/skills/slide-craft  -> <repo>/demo
# CLI   : <repo>/demo/bin/slide-craft           -> <repo>/demo/scripts/slide-craft
#
# To make the CLI callable as `slide-craft` in your shell:
#     source <repo>/demo/activate.sh
# (adds <repo>/demo/bin/ to PATH for the current shell session).

set -e

# Resolve script directory (portable: works on Linux + macOS).
DEMO="$(python3 -c 'import os, sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$0")"
REPO="$(dirname "$DEMO")"
MISSION="$(dirname "$(dirname "$REPO")")"   # <mission>/code/<repo> → <mission>

SKILL_DIR="$MISSION/.claude/skills"
BIN_DIR="$DEMO/bin"

echo "Repo     : $REPO"
echo "Mission  : $MISSION"
echo

# 1. Skill — Claude Code detects it when running inside the mission
mkdir -p "$SKILL_DIR"
ln -sfn "$DEMO" "$SKILL_DIR/slide-craft"
echo "✓ Skill   : $SKILL_DIR/slide-craft -> $DEMO"

# 2. CLI bin (mission-scoped)
mkdir -p "$BIN_DIR"
ln -sfn "$DEMO/scripts/slide-craft" "$BIN_DIR/slide-craft"
echo "✓ CLI     : $BIN_DIR/slide-craft -> $DEMO/scripts/slide-craft"

echo
echo "Done. To use the CLI in your shell, run:"
echo "    source $DEMO/activate.sh"
echo
echo "To uninstall:"
echo "    $DEMO/uninstall.sh"
