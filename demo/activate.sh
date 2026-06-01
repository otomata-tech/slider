# activate.sh — Confort HUMAIN : ajoute le CLI slide-craft au PATH du shell.
#
# Usage:
#     source <slider>/demo/activate.sh
#
# Removes via:
#     deactivate-slide-craft
#
# Session-scoped: only affects the current shell.
#
# NOTE : ne PAS s'appuyer là-dessus quand Claude pilote le skill — chaque appel
# de l'outil Bash est un shell neuf, donc le PATH posé ici n'y survit pas. Côté
# skill, le CLI est appelé par chemin absolu : "$CLAUDE_PLUGIN_ROOT/demo/bin/slide-craft"
# (le binaire s'auto-localise via realpath, aucune var d'env requise).

_SLIDER_DEMO="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
_SLIDER_ROOT="$(dirname "$_SLIDER_DEMO")"
_SLIDER_BIN="$_SLIDER_DEMO/bin"

if [ ! -x "$_SLIDER_BIN/slide-craft" ]; then
    echo "slide-craft: bin/slide-craft missing at $_SLIDER_BIN. Repo broken?" >&2
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
