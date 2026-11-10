#!/usr/bin/env python3
"""diff-structure.py — prove that a rewrite kept the structure of the kit (stdlib only).

Compares two git refs (or a ref and the working tree) file by file and reports, per file,
any difference in: frontmatter keys/values (description and argument-hint are reported as
"intended: language"), heading list (mapped through scripts/heading-map.txt), number of
process steps, rationalization rows, red flags, verification items, and STD codes cited.

Usage: diff-structure.py <old-ref> [<new-ref>|WORKTREE] [--paths <glob>...] [--json]
       diff-structure.py pre-p9 HEAD
Exit 0 when there is no unintended difference, 1 otherwise.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATHS = ["agents/*.md", "skills/*/SKILL.md", "skills/*/references/*.md", "workflows/*.md",
                 "workflows/batch/*.md", "handbook/*.md", "templates/artifacts/*.md",
                 "templates/project/CLAUDE.md.tmpl", "templates/project/claude/rules/*.tmpl"]
LANG_KEYS = {"description", "argument-hint"}  # prose values: change of language is intended


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def files_at(ref):
    if ref == "WORKTREE":
        out = git("ls-files", "--cached", "--others", "--exclude-standard")
    else:
        out = git("ls-tree", "-r", "--name-only", ref)
    return [l for l in out.splitlines() if l]


def read_at(ref, path):
    if ref == "WORKTREE":
        try:
            with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
                return fh.read()
        except OSError:
            return None
    r = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def load_map():
    m = {}
    with open(os.path.join(ROOT, "scripts", "heading-map.txt"), encoding="utf-8") as fh:
        for line in fh:
            if " = " in line and not line.startswith("# "):
                a, b = line.rstrip("\n").split(" = ", 1)
                m[a.strip().encode("ascii").decode("unicode_escape")] = b.strip()
    return m


HMAP = load_map()
SECTION_ROLE = {  # English heading -> role of the section for counting
    "## Process": "steps", "## 4. Procedure": "steps", "## Chain": "steps",
    "## Common rationalizations": "rows", "## 8. Common rationalizations": "rows",
    "## Red flags": "bullets", "## 9. Red flags": "bullets",
    "## Verification": "checks", "## 7. Never": "never",
}


def split_fm(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            return {}, text
        fm, key = {}, None
        for l in lines[1:end]:
            mm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", l)
            if mm:
                key = mm.group(1)
                fm[key] = mm.group(2).strip()
            elif key:
                fm[key] += "\n" + l.rstrip()
        return fm, "\n".join(lines[end + 1:])
    return {}, text


def facts(text):
    fm, body = split_fm(text)
    heads, cur, sec = [], None, {}
    in_code = False
    for l in body.split("\n"):
        if l.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{1,6} ", l):
            h = l.strip()
            if h.startswith("## "):
                h = HMAP.get(h, h)
            heads.append(h)
            cur = h
            sec[cur] = []
            continue
        if cur is not None:
            sec[cur].append(l)
    counts = {}
    for h, lines in sec.items():
        role = SECTION_ROLE.get(h)
        if not role:
            continue
        if role == "steps":
            n = sum(1 for l in lines if re.match(r"^\d+[a-z]?\. ", l))
        elif role == "rows":
            rows = [l for l in lines if l.strip().startswith("|")]
            n = max(0, len([r for r in rows if not re.match(r"^\|\s*:?-{2,}", r.strip())]) - 1)
        elif role == "checks":
            n = sum(1 for l in lines if re.match(r"^\s*- ", l))
        else:
            n = sum(1 for l in lines if re.match(r"^\s*- ", l))
        counts[role] = counts.get(role, 0) + n
    levels = [len(h.split(" ", 1)[0]) for h in heads]
    std = sorted(set(re.findall(r"STD-[A-Z]+-\d+", text)))
    return {"fm": fm, "heads": heads, "levels": levels, "counts": counts, "std": std}


def compare(path, a, b):
    out = []
    fa, fb = facts(a), facts(b)
    for k in sorted(set(fa["fm"]) | set(fb["fm"])):
        va, vb = fa["fm"].get(k), fb["fm"].get(k)
        if va != vb:
            kind = "intended: language" if k in LANG_KEYS and va is not None and vb is not None else "UNINTENDED"
            out.append((kind, f"frontmatter {k}"))
    mapped_a = [HMAP.get(h, h) for h in fa["heads"]]
    if fa["levels"] != fb["levels"]:
        out.append(("UNINTENDED", f"heading levels {len(fa['levels'])} -> {len(fb['levels'])}"))
    else:
        checked = [h for h in mapped_a if h in HMAP.values()]
        checked_b = [h for h in fb["heads"] if h in HMAP.values()]
        if checked != checked_b:
            out.append(("UNINTENDED", f"mapped headings differ: {checked} -> {checked_b}"))
    for k in sorted(set(fa["counts"]) | set(fb["counts"])):
        if fa["counts"].get(k) != fb["counts"].get(k):
            out.append(("UNINTENDED", f"{k} {fa['counts'].get(k)} -> {fb['counts'].get(k)}"))
    if fa["std"] != fb["std"]:
        lost, new = sorted(set(fa["std"]) - set(fb["std"])), sorted(set(fb["std"]) - set(fa["std"]))
        out.append(("UNINTENDED", f"STD codes lost {lost} added {new}"))
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    paths = DEFAULT_PATHS
    if "--paths" in argv:
        paths = argv[argv.index("--paths") + 1:]
        args = args[:2]
    if not args:
        print(__doc__.strip())
        return 0
    old, new = args[0], (args[1] if len(args) > 1 else "WORKTREE")
    fa, fb = set(files_at(old)), set(files_at(new))
    sel = lambda fs: sorted(f for f in fs if any(fnmatch.fnmatch(f, p) for p in paths))
    report, unintended, intended = {}, 0, 0
    for f in sel(fa | fb):
        a, b = read_at(old, f), read_at(new, f)
        if a is None or b is None:
            report[f] = [("UNINTENDED" if a is not None else "added", "file removed" if a is not None else "file added")]
        else:
            report[f] = compare(f, a, b)
        unintended += sum(1 for k, _ in report[f] if k == "UNINTENDED")
        intended += sum(1 for k, _ in report[f] if k != "UNINTENDED")
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for f, items in report.items():
            for k, msg in items:
                if k != "intended: language":
                    print(f"{k:12} {f}: {msg}")
        print(f"diff-structure {old} -> {new}: {len(report)} files, {unintended} unintended, {intended} intended (language/added)")
    return 1 if unintended else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
