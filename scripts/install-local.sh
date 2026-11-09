#!/usr/bin/env bash
# install-local.sh — chép bộ kit `team` vào .claude/ của một dự án (không qua marketplace).
# Dùng: scripts/install-local.sh [--force] [--dry-run] <project-dir>
#   agents/  -> <project>/.claude/agents/
#   skills/  -> <project>/.claude/skills/
#   hooks/ scripts/ handbook/ profiles/ templates/ -> <project>/.claude/team-kit/
#   ghi <project>/.team/plugin_root = đường dẫn tuyệt đối tới .claude/team-kit
#   nối hooks/hooks.json vào <project>/.claude/settings.json (${CLAUDE_PROJECT_DIR}/.claude/team-kit/scripts/...)
#   bỏ tiền tố `team:` trong `agent:` của skill (không có namespace plugin khi cài cục bộ)
# Chạy lại an toàn: file giống hệt thì bỏ qua; file khác thì KHÔNG ghi đè nếu thiếu --force.
# Mã thoát: 0 = xong; 1 = có file bị bỏ qua vì khác bản đích; 64 = sai tham số.

set -euo pipefail

FORCE=0
DRY=0
TARGET=""
usage() { sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; }
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --dry-run) DRY=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "install-local.sh: unknown option: $arg" >&2; usage >&2; exit 64 ;;
    *) [[ -z $TARGET ]] || { echo "install-local.sh: only one project dir" >&2; exit 64; }; TARGET="$arg" ;;
  esac
done
[[ -n $TARGET ]] || { usage >&2; exit 64; }
[[ -d $TARGET ]] || { echo "install-local.sh: not a directory: $TARGET" >&2; exit 64; }

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="$(cd "$TARGET" && pwd)"
[[ $PROJECT != "$KIT" ]] || { echo "install-local.sh: target is the kit repo itself" >&2; exit 64; }

copied=0; same=0; skipped=0; overwritten=0

act() { # act <verb> <message>
  if (( DRY )); then echo "[dry-run] $1 $2"; else echo "$1 $2"; fi
}

copy_tree() { # copy_tree <src-dir-in-kit | /abs/dir> <dest-dir-in-project>
  local src dest="$PROJECT/$2" rel s d
  if [[ $1 == /* ]]; then src="$1"; else src="$KIT/$1"; fi
  [[ -d $src ]] || return 0
  while IFS= read -r -d '' s; do
    rel="${s#"$src"/}"
    d="$dest/$rel"
    if [[ ! -e $d ]]; then
      act "copy     " "${2}/${rel}"
      (( DRY )) || { mkdir -p "$(dirname "$d")"; cp -p "$s" "$d"; }
      copied=$((copied + 1))
    elif cmp -s "$s" "$d"; then
      same=$((same + 1))
    elif (( FORCE )); then
      act "overwrite" "${2}/${rel}"
      (( DRY )) || cp -p "$s" "$d"
      overwritten=$((overwritten + 1))
    else
      act "skip     " "${2}/${rel} (differs; rerun with --force to overwrite)"
      skipped=$((skipped + 1))
    fi
  done < <(find "$src" -type f ! -name '.gitkeep' ! -path '*/__pycache__/*' -print0 | sort -z)
}

STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
cp -R "$KIT/agents" "$KIT/skills" "$STAGE/"
find "$STAGE/skills" -name SKILL.md -exec sed -i 's/^agent: team:/agent: /' {} +
ROLES="team-leader|tech-lead|coach|analyst|researcher|architect|designer|dev|reviewer|qa|writer|maintainer|devops"
find "$STAGE/skills" "$STAGE/agents" -name '*.md' -exec sed -i -E "s#/team:([a-z-]+)#/\\1#g; s#\\bteam:($ROLES)\\b#\\1#g" {} +
copy_tree "$STAGE/agents" .claude/agents
copy_tree "$STAGE/skills" .claude/skills
for d in hooks scripts handbook profiles templates; do
  copy_tree "$d" ".claude/team-kit/$d"
done

ROOT_FILE="$PROJECT/.team/plugin_root"
ROOT_VALUE="$PROJECT/.claude/team-kit"
if [[ -f $ROOT_FILE && "$(cat "$ROOT_FILE")" == "$ROOT_VALUE" ]]; then
  same=$((same + 1))
else
  act "write    " ".team/plugin_root -> $ROOT_VALUE"
  (( DRY )) || { mkdir -p "$PROJECT/.team"; printf '%s\n' "$ROOT_VALUE" >"$ROOT_FILE"; }
fi

SETTINGS="$PROJECT/.claude/settings.json"
sed 's#${CLAUDE_PLUGIN_ROOT}#${CLAUDE_PROJECT_DIR}/.claude/team-kit#g' "$KIT/hooks/hooks.json" >"$STAGE/hooks.json"
if [[ -f $SETTINGS ]]; then cp "$SETTINGS" "$STAGE/settings.json"; else echo '{}' >"$STAGE/settings.json"; fi
python3 -I "$KIT/scripts/render.py" --json --template "$STAGE/hooks.json" --merge-into "$STAGE/settings.json" --root "$PROJECT" >/dev/null
if [[ -f $SETTINGS ]] && cmp -s "$STAGE/settings.json" "$SETTINGS"; then
  same=$((same + 1))
else
  act "merge    " ".claude/settings.json (hooks)"
  (( DRY )) || { mkdir -p "$PROJECT/.claude"; cp "$STAGE/settings.json" "$SETTINGS"; }
fi

echo "install-local: ${copied} copied, ${overwritten} overwritten, ${same} unchanged, ${skipped} skipped -> $PROJECT"
cat <<'NOTE'
Lưu ý: cài cục bộ không có namespace plugin (gõ /<tên>, không phải /team:<tên>; agent là <vai>).
       Hook đã nối vào .claude/settings.json; đặt "agent": "team-leader" khi onboard.
       Bước tiếp: mở Claude Code trong dự án và chạy skill takeover.
NOTE
(( skipped == 0 ))
