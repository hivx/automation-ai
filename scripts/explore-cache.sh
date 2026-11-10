#!/usr/bin/env bash
# explore-cache.sh — caches exploration results keyed by a directory hash.
# Hash = sha256 of the list (path + content sha256) of every file in `git ls-files <dir>`.
# Looks up docs/team/explore/<slug>.md (slug = dir, '/' → '-'): header line `hash: <h>` matches → HIT, differs/missing → MISS.
# Prints: `HIT <path>` | `MISS <path> <hash>`; --hash prints only the hash (for the header of a new cache file).
# Usage: explore-cache.sh [--root DIR] [--hash] <dir> ; explore-cache.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
only_hash=0; dir=""
while (( $# )); do case "$1" in --root) shift 2 ;; --hash) only_hash=1; shift ;; *) dir="$1"; shift ;; esac; done
[[ -n $dir ]] || { echo "explore-cache.sh: missing <dir>" >&2; exit 64; }
cd "$TEAM_ROOT" || exit 1
dir="${dir%/}"
h="$(git ls-files -z -- "$dir" | sort -z | xargs -0 -r sha256sum | sha256sum | cut -c1-16)"
(( only_hash )) && { echo "$h"; exit 0; }
slug="$(tr '/' '-' <<<"$dir")"; [[ $slug == . ]] && slug=root
cache="docs/team/explore/$slug.md"
if [[ -f $cache ]] && grep -qx "hash: $h" <(head -n 10 "$cache"); then echo "HIT $cache"; else echo "MISS $cache $h"; fi
