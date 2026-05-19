# activate.sh — Source this to add slide-craft CLI to your shell PATH.
#
# Usage:
#     source <repo>/demo/activate.sh
#
# Removes via:
#     deactivate-slide-craft
#
# Cloistered: only affects the current shell session, no global change.

_SLIDER_DEMO="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
_SLIDER_ROOT="$(dirname "$_SLIDER_DEMO")"
_SLIDER_BIN="$_SLIDER_DEMO/bin"

if [ ! -d "$_SLIDER_BIN" ]; then
    echo "slide-craft: not installed. Run: $_SLIDER_DEMO/install.sh" >&2
    return 1 2>/dev/null || exit 1
fi

# Prepend bin to PATH (idempotent)
case ":$PATH:" in
    *":$_SLIDER_BIN:"*) ;;
    *) export PATH="$_SLIDER_BIN:$PATH" ;;
esac

# Expose engine root so generated deck build.py can locate slider via env
export SLIDER_ROOT="$_SLIDER_ROOT"

deactivate-slide-craft() {
    PATH="${PATH//$_SLIDER_BIN:/}"
    PATH="${PATH//:$_SLIDER_BIN/}"
    PATH="${PATH//$_SLIDER_BIN/}"
    export PATH
    unset SLIDER_ROOT
    unset _SLIDER_DEMO _SLIDER_ROOT _SLIDER_BIN
    unset -f deactivate-slide-craft
    echo "slide-craft: deactivated"
}

echo "slide-craft: activated (CLI available as 'slide-craft' in this shell)"
echo "             SLIDER_ROOT=$_SLIDER_ROOT"
echo "             use 'deactivate-slide-craft' to remove from PATH"
