#!/usr/bin/env python3
"""teamlib.py — logic dùng chung cho hook của kit `team` (chỉ thư viện chuẩn).

Lệnh con:
  relpath --root R <path>              in đường dẫn tương đối (rỗng nếu ngoài R)
  is-protected --root R <rel>          thoát 0 nếu khớp protected_paths/.git/**; in mẫu khớp
  allowed-root --root R <rel>          thoát 0 nếu nằm dưới structure.allowed_new_file_roots
  test-glob <naming.test_file>         đổi mẫu tên test ({name}) thành glob
  check-git --root R                   đọc JSON hook (stdin), kiểm lệnh git trong tool_input.command
  role-policy --root R --policy F      đọc JSON hook (stdin), kiểm giới hạn theo vai (agent_type)
Mã thoát của check-git/role-policy: 0 cho qua, 2 chặn (lý do ở stderr).
"""
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys

DEFAULT_PROTECTED = [".env", ".env.*"]
ALWAYS_WRITABLE = ["docs/team/**", ".team/**", ".claude/**"]
NEVER_WRITABLE = [".git/**", ".claude/settings.json", ".claude/settings.local.json"]
COMMIT_RE = re.compile(r"^(feat|fix|refactor|docs|test|chore|ci|build|perf)(\(.+\))?: .+ \((FEAT|BUG|CHG)-\d+\)$")


# ---------- đọc cấu hình ----------
def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def profile(root):
    return load_json(os.path.join(root, ".team", "profile.json"))


def config(root):
    cfg = load_json(os.path.join(root, ".team", "config.json"))
    if cfg is None:
        kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cfg = load_json(os.path.join(kit, "templates", "project", "team", "config.json"), {})
    return cfg


def get(d, dotted, default=None):
    for part in dotted.split("."):
        if not isinstance(d, dict) or part not in d:
            return default
        d = d[part]
    return d


# ---------- đường dẫn và glob ----------
def relpath(root, path):
    path = path.replace("\\", "/")
    full = os.path.normpath(path if os.path.isabs(path) else os.path.join(root, path))
    root = os.path.normpath(root)
    if full == root:
        return "."
    if not full.startswith(root + os.sep):
        return ""
    rel = os.path.relpath(full, root).replace(os.sep, "/")
    parts = rel.split("/")
    if len(parts) > 3 and parts[0] == ".claude" and parts[1] == "worktrees":
        rel = "/".join(parts[3:])  # worktree của subagent: luật áp như ở gốc repo
    return rel


def glob_re(pat):
    if pat.endswith("/"):
        pat += "**"
    out, i = "", 0
    while i < len(pat):
        if pat.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pat.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pat[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pat[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pat[i]), i + 1
    return re.compile("^" + out + "$")


def glob_match(rel, pat):
    """Gần với gitignore: mẫu không có '/' khớp bất kỳ thành phần nào của đường dẫn."""
    pat = pat.strip()
    if not pat:
        return False
    if pat.startswith("./"):
        pat = pat[2:]
    rx = glob_re(pat)
    if "/" in pat.rstrip("/"):
        return bool(rx.match(rel))
    parts = rel.split("/")
    return any(rx.match(p) for p in parts) or bool(rx.match(rel))


def protected_match(root, rel):
    prof = profile(root)
    pats = list(get(prof, "protected_paths", []) or []) if prof else list(DEFAULT_PROTECTED)
    pats.append(".git/**")
    for p in pats:
        if glob_match(rel, p):
            return p
    return None


def allowed_root(root, rel):
    prof = profile(root)
    roots = get(prof, "structure.allowed_new_file_roots", None) if prof else None
    if roots is None:
        return True  # chưa onboard: không giới hạn
    for r in roots:
        r = r.strip().rstrip("/")
        if r in ("", "."):
            return True
        if rel == r or rel.startswith(r + "/"):
            return True
    return False


def test_glob(pattern):
    return re.sub(r"\{[A-Za-z_]+\}", "*", pattern or "")


# ---------- phân tích lệnh shell ----------
SEPARATORS = {"&&", "||", ";", "|", "&", "\n", ";;", "|&"}


def segments(command):
    """Tách lệnh thành các đoạn (danh sách token) theo toán tử điều khiển."""
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=";&|<>")
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:
        return [command.split()]
    segs, cur = [], []
    for t in tokens:
        if t in SEPARATORS:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


def strip_prefix(tokens):
    """Bỏ gán biến môi trường và các tiền tố như env, command, time, sudo."""
    i = 0
    while i < len(tokens) and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[i])
                               or tokens[i] in ("env", "command", "exec", "time", "nohup", "sudo")):
        i += 1
    return tokens[i:]


def git_parts(tokens):
    """Trả (thư mục -C, subcommand, args) nếu đoạn là lệnh git, ngược lại None."""
    tokens = strip_prefix(tokens)
    if not tokens or os.path.basename(tokens[0]) != "git":
        return None
    i, cdir = 1, None
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") and i + 1 < len(tokens):
            if tokens[i] == "-C":
                cdir = tokens[i + 1]
            i += 2
        else:
            i += 1
    if i >= len(tokens):
        return None
    return cdir, tokens[i], tokens[i + 1:]


def git_out(cwd, *args):
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def branch_matches(name, patterns):
    return any(fnmatch.fnmatchcase(name, p) for p in patterns)


def check_git(root, data):
    """Trả (mã thoát, thông điệp, cảnh báo)."""
    cmd = get(data, "tool_input.command", "") or ""
    cwd = data.get("cwd") or root
    cfg = config(root)
    protected = list(get(cfg, "protected_branches", []) or []) + [get(cfg, "base_branch", "main") or "main"]
    warnings = []
    for seg in segments(cmd):
        parts = git_parts(seg)
        if not parts:
            continue
        cdir, sub, args = parts
        wd = os.path.join(cwd, cdir) if cdir else cwd
        current = git_out(wd, "rev-parse", "--abbrev-ref", "HEAD")
        if sub in ("filter-branch", "filter-repo"):
            return 2, f"BLOCKED (STD-GIT-4): `git {sub}` viết lại lịch sử — không bao giờ.", warnings
        if sub == "push":
            code, msg = check_push(args, wd, current, protected)
            if code:
                return code, msg, warnings
        elif sub == "commit":
            values = {"-m", "--message", "-F", "--file", "-C", "-c", "--author", "--date", "--fixup", "--squash"}
            msgs, skip = [], False
            for j, a in enumerate(args):
                if skip:
                    skip = False
                    continue
                if a in values:
                    if a in ("-m", "--message") and j + 1 < len(args):
                        msgs.append(args[j + 1])
                    skip = True
                    continue
                if a.startswith("--message="):
                    msgs.append(a.split("=", 1)[1])
                elif a == "--no-verify" or (re.match(r"^-[A-Za-z]+$", a) and "n" in a[1:]):
                    return 2, "BLOCKED (STD-GIT-2): `git commit --no-verify` bị cấm; sửa lỗi mà hook commit báo.", warnings
            if msgs:
                subject = msgs[0].split("\n", 1)[0].strip()
                if not COMMIT_RE.match(subject):
                    warnings.append(f"WARN (STD-NAME-5): message '{subject}' không đúng dạng "
                                    "`type(scope): description (<ID>)`, ví dụ `feat(text): add reverse (FEAT-001)`.")
        elif sub == "rebase" and any(a in ("-i", "--interactive") for a in args):
            if branch_matches(current, protected):
                return 2, f"BLOCKED (STD-GIT-4): `git rebase -i` trên nhánh bảo vệ `{current}`.", warnings
        elif sub == "reset" and "--hard" in args:
            if branch_matches(current, protected):
                return 2, f"BLOCKED (STD-GIT-4): `git reset --hard` trên nhánh bảo vệ `{current}`.", warnings
    return 0, "", warnings


def check_push(args, wd, current, protected):
    positional, tags_only = [], False
    for a in args:
        if a in ("--force", "--force-if-includes", "--mirror", "--all", "--prune") or a.startswith("--force-with-lease"):
            return 2, f"BLOCKED (STD-GIT-4): `git push {a}` bị cấm (không force-push, không đẩy hàng loạt)."
        if a in ("--delete", "-d"):
            return 2, "BLOCKED (STD-GIT-3): `git push --delete` bị cấm; người xóa nhánh trên remote."
        if a == "--tags":
            tags_only = True
            continue
        if re.match(r"^-[A-Za-z]+$", a):
            if "f" in a[1:]:
                return 2, "BLOCKED (STD-GIT-4): `git push -f` bị cấm."
            if "d" in a[1:]:
                return 2, "BLOCKED (STD-GIT-3): `git push -d` bị cấm."
            continue
        if a.startswith("-"):
            continue
        positional.append(a)
    refspecs = positional[1:]
    if not refspecs:
        if tags_only:
            return 0, ""
        refspecs = [current or "HEAD"]
    for spec in refspecs:
        if spec.startswith("+"):
            return 2, f"BLOCKED (STD-GIT-4): refspec `{spec}` là force-push."
        src, _, dst = spec.partition(":")
        if spec.startswith(":"):
            return 2, f"BLOCKED (STD-GIT-3): `{spec}` xóa nhánh trên remote."
        dst = dst or src
        if dst in ("HEAD", "@"):
            dst = current
        dst = dst.replace("refs/heads/", "", 1)
        if dst.startswith("refs/tags/") or git_out(wd, "show-ref", "--verify", f"refs/tags/{dst}"):
            continue
        if fnmatch.fnmatchcase(dst, "team/*"):
            continue
        if branch_matches(dst, protected):
            return 2, f"BLOCKED (STD-GIT-3): push vào nhánh bảo vệ `{dst}`. Chỉ push `team/*`, rồi mở PR (`/team:pr`)."
        return 2, f"BLOCKED (STD-GIT-3): chỉ push nhánh `team/*` (nhận `{dst}`)."
    return 0, ""


# ---------- giới hạn theo vai ----------
READONLY_GIT = {"status", "log", "diff", "show", "branch", "rev-parse", "ls-files", "blame", "grep",
                "shortlog", "rev-list", "tag", "describe", "merge-base", "remote", "symbolic-ref", "cat-file",
                "ls-tree", "for-each-ref", "show-ref", "worktree", "name-rev", "count-objects"}
READONLY_GH = {("issue", "view"), ("issue", "list"), ("pr", "view"), ("pr", "list"), ("pr", "checks"),
               ("pr", "diff"), ("run", "view"), ("run", "list"), ("auth", "status"), ("repo", "view")}


def git_listing_only(sub, args):
    """branch/tag/remote chỉ-đọc khi chỉ liệt kê; các subcommand khác trong READONLY_GIT luôn chỉ-đọc."""
    if sub == "worktree":
        return bool(args) and args[0] == "list"
    if sub not in ("branch", "tag", "remote"):
        return True
    writes = {"-d", "-D", "-m", "-M", "-c", "-C", "-f", "--delete", "--move", "--copy", "--force",
              "-u", "--set-upstream-to", "--unset-upstream", "-a" if sub == "tag" else "--edit-description",
              "-s", "add", "remove", "rm", "rename", "set-url", "prune"}
    if any(a in writes for a in args):
        return False
    listing = {"--list", "-l", "--merged", "--no-merged", "--contains", "-a", "-r", "-v", "-vv",
               "--sort", "show", "get-url", "--show-current"}
    positional = [a for a in args if not a.startswith("-")]
    return not positional or any(a in listing or a.startswith("--sort=") or a.startswith("--format=") for a in args)


def redirect_targets(seg):
    targets, clean, i = [], [], 0
    while i < len(seg):
        t = seg[i]
        if t in (">", ">>", ">|", "&>", "&>>") or re.match(r"^\d?>>?$", t):
            if i + 1 < len(seg):
                targets.append(seg[i + 1])
            i += 2
            continue
        if t == "<":
            i += 2
            continue
        clean.append(t)
        i += 1
    return clean, targets


def is_readonly(seg, policy, kit):
    seg = strip_prefix(seg)
    if not seg:
        return True
    if any(("$(" in t or "`" in t or "<(" in t or ">(" in t) for t in seg):
        return False  # thay thế lệnh có thể chạy bất cứ gì
    head = os.path.basename(seg[0])
    if head == "git":
        if any(t == "-c" or t.startswith(("--output", "--ext-diff", "-O")) for t in seg[1:]):
            return False
        parts = git_parts(seg)
        return bool(parts) and parts[1] in READONLY_GIT and git_listing_only(parts[1], parts[2])
    if head == "gh":
        return len(seg) >= 3 and (seg[1], seg[2]) in READONLY_GH
    if head in ("python3", "python", "bash", "sh"):
        if any(a in ("-c", "-m") for a in seg[1:]):
            return False
        script = next((a for a in seg[1:] if not a.startswith("-")), "")
        return os.path.basename(script) in set(policy.get("readonly_scripts", []))
    if head in ("find",):
        return not any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprint0", "-fprintf", "-fls") for a in seg)
    if head == "sed":
        return not any(a.startswith(("-i", "--in-place")) or (a.startswith("-") and not a.startswith("--") and "i" in a[1:]) for a in seg)
    return head in set(policy.get("readonly_commands", []))


def cmd_prefixes(root):
    prof = profile(root) or {}
    out = []
    for v in (prof.get("cmd") or {}).values():
        if isinstance(v, str) and v.strip():
            out.append(v.split("{file}")[0].strip())
    return out


def role_policy(root, data, policy_path):
    agent = data.get("agent_type") or ""
    policy = load_json(policy_path, {})
    roles = policy.get("roles") or {}
    role = roles.get(agent) or roles.get(f"team:{agent}")  # cài cục bộ: agent không có tiền tố plugin
    if not role:
        return 0, ""
    stage = (load_json(os.path.join(root, ".team", "current.json"), {}) or {}).get("stage", "")
    exc = (role.get("stage_exceptions") or {}).get(stage, {})
    writes = list(role.get("write", [])) + list(exc.get("write", []))
    bash = exc.get("bash", role.get("bash", "read-only"))
    tool = data.get("tool_name", "")
    kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tin = data.get("tool_input") or {}

    def writable(path):
        rel = relpath(root, path)
        return rel != "" and any(glob_match(rel, p) for p in writes)

    if tool in ("Edit", "Write", "NotebookEdit"):
        path = tin.get("file_path") or tin.get("notebook_path") or ""
        if "*" in writes or writable(path):
            return 0, ""
        return 2, (f"BLOCKED (role-policy): {agent} chỉ được ghi {', '.join(writes) or '(không gì)'}; "
                   f"nhận `{relpath(root, path) or path}`. Giao cho vai đúng.")
    if tool == "Agent":
        target = tin.get("subagent_type") or "general-purpose"
        allowed = role.get("agents", [])
        names = {target, target if target.startswith("team:") or target in ("Explore", "Plan", "general-purpose") else f"team:{target}"}
        if any(fnmatch.fnmatchcase(n, p) for n in names for p in allowed):
            return 0, ""
        return 2, f"BLOCKED (role-policy): {agent} không được gọi `{target}` (cho phép: {', '.join(allowed) or 'không ai'})."
    if tool == "Bash":
        if bash == "any":
            return 0, ""
        extra = bash.get("allow", []) if isinstance(bash, dict) else []
        prefixes = cmd_prefixes(root) if "cmd.*" in extra else []
        command = tin.get("command", "")
        try:
            with open(os.path.join(root, ".team", "plugin_root"), encoding="utf-8") as fh:
                kit_path = fh.read().strip() or kit
        except OSError:
            kit_path = kit
        for form in ('"$(cat .team/plugin_root)"', "$(cat .team/plugin_root)"):
            command = command.replace(form, kit_path)  # cách skill gọi script của kit; thay thế khác vẫn bị chặn
        for seg in segments(command):
            clean, targets = redirect_targets(seg)
            for t in targets:
                if t not in ("/dev/null",) and not writable(t):
                    return 2, f"BLOCKED (role-policy): {agent} không được ghi `{t}` bằng chuyển hướng."
            text = " ".join(strip_prefix(clean))
            if is_readonly(clean, policy, kit):
                continue
            if any(p != "cmd.*" and fnmatch.fnmatchcase(text, p) for p in extra):
                continue
            if any(text == p or text.startswith(p + " ") for p in prefixes if p):
                continue
            return 2, (f"BLOCKED (role-policy): {agent} chỉ chạy lệnh chỉ-đọc"
                       f"{' hoặc ' + ', '.join(extra) if extra else ''}; nhận `{text[:120]}`.")
    return 0, ""


# ---------- CLI ----------
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    sub, rest = argv[0], argv[1:]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    policy = None
    pos = []
    i = 0
    while i < len(rest):
        if rest[i] == "--root" and i + 1 < len(rest):
            root, i = rest[i + 1], i + 2
        elif rest[i] == "--policy" and i + 1 < len(rest):
            policy, i = rest[i + 1], i + 2
        else:
            pos.append(rest[i])
            i += 1
    root = os.path.abspath(root)
    if sub == "relpath":
        print(relpath(root, pos[0]) if pos else "")
        return 0
    if sub == "is-protected":
        m = protected_match(root, pos[0])
        if m:
            print(m)
        return 0 if m else 1
    if sub == "allowed-root":
        return 0 if allowed_root(root, pos[0]) else 1
    if sub == "test-glob":
        print(test_glob(pos[0] if pos else ""))
        return 0
    if sub in ("check-git", "role-policy"):
        try:
            data = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            return 0
        if sub == "check-git":
            code, msg, warns = check_git(root, data)
            for w in warns:
                print(w, file=sys.stderr)
            if code:
                print(msg, file=sys.stderr)
                return code
            if warns:
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                         "additionalContext": " ".join(warns)}}, ensure_ascii=False))
            return 0
        code, msg = role_policy(root, data, policy)
        if code:
            print(msg, file=sys.stderr)
        return code
    print(f"teamlib.py: unknown subcommand {sub}", file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
