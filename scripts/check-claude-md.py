#!/usr/bin/env python3
"""check-claude-md.py — machine checks for a project's CLAUDE.md (standard library only).

CLAUDE.md describes the PROJECT. The team keeps two blocks in it:
  <!-- project:start --> … <!-- project:end -->  what the system is, commands, layout, conventions, gotchas
                                                  (written by /team:onboard, kept current by /team:asbuilt)
  <!-- team:start --> … <!-- team:end -->        how to work with the team (rendered by /team:onboard)
Text outside both blocks belongs to the human; the team never edits it.

Checks (one line `CLAUDE.md: <problem>` each; exit 1 if any):
  1. each block appears exactly once, the project block before the team block;
  2. project block <= 150 lines, team block <= 25 lines, whole file <= 200 lines;
  3. no `{{` and no `<fill:` placeholder left in either block;
  4. every path quoted in backticks inside the project block exists (a stale path misleads every session).
     A token counts as a path when it ends in a known file extension, or has a `/` and its first segment exists
     (so `origin/main`, `cmd.test`, `frappe.get_doc` are not paths).
The last line is a summary: `check-claude-md: project <n>/150, team <n>/25, total <n>/200, <k> problems`.
Usage: scripts/check-claude-md.py [--root DIR] [--file PATH]
"""
import glob
import os
import re
import sys

BLOCKS = {"project": ("<!-- project:start -->", "<!-- project:end -->", 150),
          "team": ("<!-- team:start -->", "<!-- team:end -->", 25)}
MAX_TOTAL = 200
TOKEN = re.compile(r"`([A-Za-z0-9_.*/-]+)`")
EXT = re.compile(r"\.(?:md|py|pyi|js|jsx|ts|tsx|vue|json|jsonl|ya?ml|toml|ini|cfg|conf|env|sh|bash|txt|csv|sql|html?|css|scss|go|rs|java|kt|rb|php|cs|swift|c|h|cpp|hpp|xml|lock|tf|ipynb)$", re.I)


def block(text, start, end):
    """(count of start markers, count of end markers, body or None, index of start)."""
    ns, ne = text.count(start), text.count(end)
    if ns != 1 or ne != 1:
        return ns, ne, None, -1
    i, j = text.index(start), text.index(end)
    return ns, ne, (text[i + len(start):j] if j > i else None), i


def is_path(tok, root):
    if tok.startswith(("-", ".", "*")) and not tok.startswith((".team/", ".claude/", ".github/")):
        return False
    if "/" not in tok and not EXT.search(tok):
        return False
    if re.match(r"^[0-9.]+$", tok):
        return False  # version numbers
    first = tok.split("/", 1)[0]
    return bool(EXT.search(tok.rstrip("/"))) or os.path.exists(os.path.join(root, first))


def exists(tok, root):
    p = os.path.join(root, tok)
    return bool(glob.glob(p)) if any(c in tok for c in "*?[") else os.path.exists(p)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv and argv.index(k) + 1 < len(argv) else d
    root = os.path.abspath(opt("--root", os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()))
    path = opt("--file", os.path.join(root, "CLAUDE.md"))
    name = os.path.relpath(path, root)
    problems, sizes = [], {"project": 0, "team": 0}
    if not os.path.isfile(path):
        print(f"{name}: missing (run /team:onboard)")
        print("check-claude-md: project 0/150, team 0/25, total 0/200, 1 problems")
        return 1
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    pos = {}
    for key, (start, end, cap) in BLOCKS.items():
        ns, ne, body, at = block(text, start, end)
        if body is None:
            problems.append(f"{key} block: expected one {start} … {end} pair, found {ns} start / {ne} end")
            continue
        pos[key] = at
        sizes[key] = len(body.strip("\n").splitlines())
        if sizes[key] > cap:
            problems.append(f"{key} block: {sizes[key]} lines > {cap} (prune before adding)")
        for n, line in enumerate(body.splitlines(), 1):
            if "{{" in line or "<fill:" in line:
                problems.append(f"{key} block line {n}: placeholder left: {line.strip()[:80]}")
        if key == "project":
            for tok in sorted(set(TOKEN.findall(body))):
                if is_path(tok, root) and not exists(tok.rstrip("/"), root):
                    problems.append(f"project block: path `{tok}` does not exist (stale line)")
    if len(pos) == 2 and pos["project"] > pos["team"]:
        problems.append("the project block must come before the team block")
    total = len(text.splitlines())
    if total > MAX_TOTAL:
        problems.append(f"{total} lines > {MAX_TOTAL} in total (move detail into docs/ and link it)")
    for p in problems:
        print(f"{name}: {p}")
    print(f"check-claude-md: project {sizes['project']}/150, team {sizes['team']}/25, "
          f"total {total}/{MAX_TOTAL}, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
