#!/usr/bin/env python3
"""teamlib.py — logic dùng chung cho hook của kit `team` (chỉ thư viện chuẩn).

Lệnh con:
  relpath --root R <path>              in đường dẫn tương đối (rỗng nếu ngoài R)
  is-protected --root R <rel>          thoát 0 nếu khớp protected_paths/.git/**; in mẫu khớp
  allowed-root --root R <rel>          thoát 0 nếu nằm dưới structure.allowed_new_file_roots
  test-glob <naming.test_file>         đổi mẫu tên test ({name}) thành glob
  check-git --root R                   đọc JSON hook (stdin), kiểm lệnh git trong tool_input.command
  role-policy --root R --policy F      đọc JSON hook (stdin), kiểm giới hạn theo vai (agent_type)
  protect-bash --root R                đọc JSON hook (stdin), chặn lệnh Bash ghi/xóa vùng cấm (K-24)
Mã thoát của check-git/role-policy/protect-bash: 0 cho qua, 2 chặn (lý do ở stderr).
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


def in_worktree(root, path):
    """Đường dẫn nằm trong một worktree của subagent (.claude/worktrees/<n>/...)."""
    path = path.replace("\\", "/")
    full = os.path.normpath(path if os.path.isabs(path) else os.path.join(root, path))
    wt = os.path.join(os.path.normpath(root), ".claude", "worktrees") + os.sep
    return full.startswith(wt) and len(full[len(wt):].split(os.sep)) >= 2


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
        bad_c = [seg[i + 1] for i, t in enumerate(seg[:-1]) if t == "-c" and re.match(r"^(alias\.|core\.hooksPath|core\.sshCommand|core\.pager|core\.editor|core\.fsmonitor|diff\.external|credential\.helper)", seg[i + 1], re.I)]
        if bad_c or "--exec-path" in " ".join(seg):
            return 2, f"BLOCKED (STD-GIT-2): `git -c {bad_c[0] if bad_c else '--exec-path'}` có thể bỏ qua hook hoặc chạy lệnh tùy ý.", warnings
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
    """Tách chuyển hướng: trả (token còn lại, đích ghi). `N>&M` (nhân bản fd) không phải đích ghi."""
    targets, clean, i = [], [], 0
    while i < len(seg):
        t = seg[i]
        nxt = seg[i + 1] if i + 1 < len(seg) else ""
        if t in (">", ">>", ">|", "&>", "&>>", "<>") or re.match(r"^\d?>>?$", t):
            if nxt:
                targets.append(nxt)
            if clean and re.match(r"^\d$", clean[-1]):
                clean.pop()  # "2 >" do shlex tách "2>"
            i += 2
            continue
        if t in (">&", "<&"):
            if nxt and not re.match(r"^(\d+|-)$", nxt) and t == ">&":
                targets.append(nxt)  # `>&file` = ghi file
            if clean and re.match(r"^\d$", clean[-1]):
                clean.pop()
            i += 2
            continue
        if t == "<":
            i += 2
            continue
        clean.append(t)
        i += 1
    return clean, targets


def sed_scripts(args):
    """Trả (danh sách script sed, có -f/--file không)."""
    scripts, has_file, explicit, i = [], False, False, 0
    positional = []
    while i < len(args):
        a = args[i]
        if a in ("-e", "--expression") and i + 1 < len(args):
            scripts.append(args[i + 1]); explicit = True; i += 2; continue
        if a.startswith("--expression="):
            scripts.append(a.split("=", 1)[1]); explicit = True; i += 1; continue
        if a.startswith("-e") and len(a) > 2 and not a.startswith("--"):
            scripts.append(a[2:]); explicit = True; i += 1; continue
        if a in ("-f", "--file") or a.startswith("--file=") or (a.startswith("-f") and not a.startswith("--")):
            has_file = True; i += 1; continue
        if not a.startswith("-"):
            positional.append(a)
        i += 1
    if not explicit and positional:
        scripts.append(positional[0])
    return scripts, has_file


SED_S_RE = re.compile(r"s(.)(?:\\.|(?!\1).)*\1(?:\\.|(?!\1).)*\1([A-Za-z0-9]*)")


def sed_writes_or_runs(script):
    """Script sed có lệnh e/w/W hoặc cờ s///e, s///w không (chạy lệnh, ghi file)."""
    for m in SED_S_RE.finditer(script):
        if set(m.group(2)) & {"e", "w"}:
            return True
    rest = SED_S_RE.sub(";", script)
    rest = re.sub(r"\\?/(?:\\.|[^/])*/", " ", rest)  # bỏ địa chỉ /regex/
    return bool(re.search(r"[ewW]", rest))


def kit_script(script, kits):
    """Tên script nếu `script` nằm đúng trong <kit>/scripts/ của một kit đã biết, ngược lại ''."""
    if not script:
        return ""
    full = os.path.realpath(script)
    for k in kits:
        if k and os.path.dirname(full) == os.path.realpath(os.path.join(k, "scripts")):
            return os.path.basename(full)
    return ""


def readonly_script_map(policy):
    """readonly_scripts: {tên: glob đích ghi | '' | {"write": glob, "when": [lệnh con]}}; chấp nhận dạng danh sách cũ."""
    rs = policy.get("readonly_scripts", {})
    return {n: "" for n in rs} if isinstance(rs, list) else dict(rs)


SAFE_ENV = {"LC_ALL", "LANG", "LANGUAGE", "TZ", "NO_COLOR", "TERM", "COLUMNS", "PYTHONIOENCODING", "PYTHONDONTWRITEBYTECODE"}


def unsafe_prefix(tokens):
    """Tiền tố có thể chạy lệnh: biến môi trường ngoài SAFE_ENV (GIT_EXTERNAL_DIFF, GIT_CONFIG_*, BASH_ENV, PAGER…), sudo."""
    for t in tokens:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=", t)
        if m:
            if m.group(1) not in SAFE_ENV:
                return True
            continue
        if t == "sudo":
            return True
        if t in ("env", "command", "exec", "time", "nohup"):
            continue
        return False
    return False


def is_readonly(seg, policy, kit, kits=None, writable=None):
    if unsafe_prefix(seg):
        return False
    seg = strip_prefix(seg)
    if not seg:
        return True
    if any(("$(" in t or "`" in t or "<(" in t or ">(" in t) for t in seg):
        return False  # thay thế lệnh có thể chạy bất cứ gì
    head = os.path.basename(seg[0])
    args = seg[1:]
    if head == "git":
        if any(t == "-c" or t.startswith(("--output", "--ext-diff", "-O", "--open-files-in-pager", "--textconv")) for t in args):
            return False
        parts = git_parts(seg)
        return bool(parts) and parts[1] in READONLY_GIT and git_listing_only(parts[1], parts[2])
    if head == "gh":
        return len(seg) >= 3 and (seg[1], seg[2]) in READONLY_GH
    if head in ("python3", "python", "bash", "sh"):
        if any(a in ("-c", "-m") for a in args):
            return False
        script = next((a for a in args if not a.startswith("-")), "")
        name = kit_script(script, kits or [kit])  # K-40: đúng đường dẫn <kit>/scripts/, không theo tên
        scripts = readonly_script_map(policy)
        if not name or name not in scripts:
            return False
        dest = scripts[name]
        if isinstance(dest, dict):  # chỉ ghi với vài lệnh con, ví dụ team.py scorecard
            dest = dest.get("write", "") if any(a in dest.get("when", []) for a in args) else ""
        if dest:  # script có ghi: vai phải được ghi đích của nó; không cho đổi gốc
            if "--root" in args:
                return False
            return bool(writable and writable(dest.replace("**", "x")))
        return True
    if head == "find":
        return not any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprint0", "-fprintf", "-fls") for a in seg)
    if head == "sed":
        if any(a.startswith(("-i", "--i")) or (a.startswith("-") and not a.startswith("--") and "i" in a[1:]) for a in args):
            return False
        scripts, has_file = sed_scripts(args)
        return not has_file and not any(sed_writes_or_runs(s) for s in scripts)
    if head == "sort":  # -o ghi file; --compress-program chạy lệnh; GNU nhận tên dài viết tắt
        return not any(a.startswith(("--o", "--com")) or (a.startswith("-") and not a.startswith("--") and "o" in a[1:])
                       for a in args)
    if head == "uniq":
        return len([a for a in args if not a.startswith("-")]) <= 1  # uniq IN OUT ghi OUT
    if head == "tree":
        return not any(a == "-o" or a.startswith("-o") for a in args)
    if head == "rg":
        return not any(a in ("--pre", "--pre-glob") or a.startswith(("--pre=", "--pre-glob=")) for a in args)
    if head == "date":
        return not any(a.startswith(("-s", "--s")) for a in args)
    if head == "file":
        return not any(a == "-C" or a.startswith("--c") for a in args)
    return head in set(policy.get("readonly_commands", []))


WRITE_ALL_ARGS = {"rm", "unlink", "shred", "truncate", "touch", "mkdir", "rmdir"}
WRITE_DEST = {"cp", "install", "ln"}


def bash_write_targets(command):
    """Đích ghi nhận ra được trong lệnh Bash (K-24, nỗ lực tốt nhất): trả [(thư mục cd, đích)].
    Nhận: chuyển hướng, tee, rm/touch/truncate/..., mv (cả nguồn), cp/install/ln (đích, -t),
    sed -i, chmod/chown, dd of=. Không nhận được: ghi bên trong script/chương trình khác."""
    out, cwd = [], ""
    for seg in segments(command):
        clean, targets = redirect_targets(seg)
        out += [(cwd, t) for t in targets]
        toks = strip_prefix(clean)
        if not toks:
            continue
        head, args = os.path.basename(toks[0]), toks[1:]
        pos = [a for a in args if not a.startswith("-")]
        if head == "cd":
            cwd = os.path.join(cwd, pos[0]) if pos else ""
            continue
        if head in WRITE_ALL_ARGS or head == "tee":
            out += [(cwd, a) for a in pos]
        elif head == "mv":
            out += [(cwd, a) for a in pos]
        elif head in WRITE_DEST:
            if "-t" in args and args.index("-t") + 1 < len(args):
                out.append((cwd, args[args.index("-t") + 1]))
            elif pos:
                out.append((cwd, pos[-1]))
        elif head in ("chmod", "chown", "chgrp"):
            out += [(cwd, a) for a in pos[1:]]
        elif head == "sort":
            for j, a in enumerate(args):
                if a.startswith("--o") and "=" in a:
                    out.append((cwd, a.split("=", 1)[1]))
                elif a.startswith("-") and not a.startswith("--") and "o" in a[1:]:
                    rest = a[a.index("o", 1) + 1:]
                    if rest:
                        out.append((cwd, rest))
                    elif j + 1 < len(args):
                        out.append((cwd, args[j + 1]))
                elif a.startswith("--o") and j + 1 < len(args):
                    out.append((cwd, args[j + 1]))
        elif head == "sed" and any(a.startswith(("-i", "--i")) or (a.startswith("-") and not a.startswith("--") and "i" in a[1:]) for a in args):
            scripts, _ = sed_scripts(args)
            files = [a for a in pos if a not in scripts]
            out += [(cwd, a) for a in files]
        elif head == "dd":
            out += [(cwd, a[3:]) for a in args if a.startswith("of=")]
    return out


def protect_bash(root, data):
    """Áp luật protect.sh cho đích ghi của lệnh Bash: .git/, settings, profile/config, protected_paths."""
    command = (data.get("tool_input") or {}).get("command", "")
    base = data.get("cwd") or root
    stage = (load_json(os.path.join(root, ".team", "current.json"), {}) or {}).get("stage", "")
    for cwd, t in bash_write_targets(command):
        if t in ("/dev/null", "/dev/stdout", "/dev/stderr", "-") or "$" in t:
            continue  # biến shell không giải được: ngoài phạm vi kiểm (ghi rõ trong docs)
        full = t if os.path.isabs(t) else os.path.join(base, cwd, t)
        rel = relpath(root, full)
        if not rel or rel == ".":
            continue
        if rel == ".git" or rel.startswith(".git/"):
            return 2, "BLOCKED (STD-SEC-1): không ghi vào .git/ bằng shell."
        if rel in (".claude/settings.json", ".claude/settings.local.json"):
            return 2, f"BLOCKED (STD-SEC-1): {rel} chỉ đổi qua /team:onboard hoặc do người sửa."
        if rel in (".team/profile.json", ".team/config.json") and stage != "onboard":
            return 2, f"BLOCKED (STD-SEC-1): {rel} chỉ đổi qua /team:onboard hoặc do người sửa."
        if rel.startswith("docs/team/") or rel == "CHANGELOG.md":
            continue
        pat = protected_match(root, rel)
        if pat:
            return 2, (f"BLOCKED (STD-SEC-1): lệnh shell ghi/xóa '{rel}' khớp protected_paths ('{pat}'). "
                       "Người sửa tay, hoặc sửa protected_paths trong .team/profile.json nếu khai nhầm.")
    return 0, ""


def cp_from_templates(seg, kits):
    """`cp` mà mọi nguồn nằm dưới <kit>/templates/ (đích là đối số cuối)."""
    toks = strip_prefix(seg)
    if not toks or os.path.basename(toks[0]) != "cp":
        return False
    pos = [a for a in toks[1:] if not a.startswith("-")]
    if len(pos) < 2 or any(a in ("-t", "--target-directory") for a in toks):
        return False
    roots = [os.path.realpath(os.path.join(k, "templates")) + os.sep for k in kits if k]
    return all(any(os.path.realpath(src).startswith(r) for r in roots) for src in pos[:-1])


def is_temp_agent(root, agent):
    """Agent dự án do /team:make-agent tạo: .claude/agents/<tên>.md có dấu `team: temp`."""
    name = agent.split(":", 1)[-1]
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        return False
    try:
        with open(os.path.join(root, ".claude", "agents", name + ".md"), encoding="utf-8") as fh:
            return "team: temp" in fh.read(4000)
    except OSError:
        return False


def cmd_prefixes(root):
    prof = profile(root) or {}
    out = []
    for v in (prof.get("cmd") or {}).values():
        if isinstance(v, str) and v.strip():
            out.append(v.split("{file}")[0].strip())
    return out


def role_policy(root, data, policy_path):
    agent = data.get("agent_type") or ""
    if agent and policy_path and not os.path.isfile(policy_path):
        return 2, f"BLOCKED (role-policy): không đọc được {policy_path} — hook an toàn không cho qua khi thiếu luật."
    policy = load_json(policy_path, {})
    roles = policy.get("roles") or {}
    role = roles.get(agent) or roles.get(f"team:{agent}")  # cài cục bộ: agent không có tiền tố plugin
    if not role and agent and is_temp_agent(root, agent):
        role = roles.get("_temp")  # agent tạm của make-agent: giới hạn mặc định, không phải tự do
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
        if rel != "" and role.get("worktree_write") and in_worktree(root, path):
            return True  # POC của researcher: chỉ trong worktree riêng (.claude/worktrees/<n>/), protect.sh vẫn áp
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
        base, cwd = data.get("cwd") or root, ""
        for seg in segments(command):
            clean, targets = redirect_targets(seg)
            for t in targets:
                full = t if os.path.isabs(t) else os.path.join(base, cwd, t)  # tính cả `cd` trước đó
                if t not in ("/dev/null",) and not writable(full):
                    return 2, f"BLOCKED (role-policy): {agent} không được ghi `{t}` bằng chuyển hướng."
            ct = strip_prefix(clean)
            if ct and ct[0] == "cd":
                dest = next((a for a in ct[1:] if not a.startswith("-")), "")
                cwd = os.path.join(cwd, dest) if dest and not os.path.isabs(dest) else (dest or "")
            text = " ".join(strip_prefix(clean))
            if is_readonly(clean, policy, kit, [kit, kit_path], writable):
                continue
            if "cp-from-kit-templates" in extra and cp_from_templates(clean, [kit, kit_path]):
                continue  # onboard: chỉ chép từ <kit>/templates/ (K-26)
            if any(p not in ("cmd.*", "cp-from-kit-templates") and fnmatch.fnmatchcase(text, p) for p in extra):
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
    if sub in ("check-git", "role-policy", "protect-bash"):
        try:
            data = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            if sub == "check-git":
                return 0
            print(f"BLOCKED ({sub}): JSON hook hỏng — hook an toàn không cho qua khi không đọc được đầu vào.", file=sys.stderr)
            return 2
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
        if sub == "protect-bash":
            code, msg = protect_bash(root, data)
            if code:
                print(msg, file=sys.stderr)
            return code
        code, msg = role_policy(root, data, policy)
        if code:
            print(msg, file=sys.stderr)
        return code
    print(f"teamlib.py: unknown subcommand {sub}", file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
