#!/usr/bin/env bash
# explore-cache.sh — cache kết quả khám phá theo hash thư mục.
# Hash = sha256 của danh sách (đường dẫn + sha256 nội dung) mọi file `git ls-files <dir>`.
# Tra docs/team/explore/<slug>.md (slug = dir, '/' → '-'): dòng header `hash: <h>` khớp → HIT, khác/thiếu → MISS.
# In: `HIT <path>` | `MISS <path> <hash>`; --hash chỉ in hash (để ghi vào header cache mới).
# Dùng: explore-cache.sh [--root DIR] [--hash] <dir> ; explore-cache.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
only_hash=0; dir=""
while (( $# )); do case "$1" in --root) shift 2 ;; --hash) only_hash=1; shift ;; *) dir="$1"; shift ;; esac; done
[[ -n $dir ]] || { echo "explore-cache.sh: thiếu <dir>" >&2; exit 64; }
cd "$TEAM_ROOT" || exit 1
dir="${dir%/}"
h="$(git ls-files -z -- "$dir" | sort -z | xargs -0 -r sha256sum | sha256sum | cut -c1-16)"
(( only_hash )) && { echo "$h"; exit 0; }
slug="$(tr '/' '-' <<<"$dir")"; [[ $slug == . ]] && slug=root
cache="docs/team/explore/$slug.md"
if [[ -f $cache ]] && grep -qx "hash: $h" <(head -n 10 "$cache"); then echo "HIT $cache"; else echo "MISS $cache $h"; fi
