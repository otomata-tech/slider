#!/usr/bin/env bash
# uninstall.sh — Remove the cloistered install.
set -e

DEMO="$(python3 -c 'import os, sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$0")"
REPO="$(dirname "$DEMO")"
MISSION="$(dirname "$(dirname "$REPO")")"

rm -f "$MISSION/.claude/skills/slide-craft"
echo "✓ removed $MISSION/.claude/skills/slide-craft"

rm -f "$DEMO/bin/slide-craft"
rmdir "$DEMO/bin" 2>/dev/null || true
echo "✓ removed $DEMO/bin/slide-craft"

echo
echo "Note: deactivate the shell PATH manually if you sourced activate.sh:"
echo "    deactivate-slide-craft"
