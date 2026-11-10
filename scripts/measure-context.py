#!/usr/bin/env python3
"""measure-context.py — size of the text the kit puts into Claude's context (stdlib; tiktoken optional).

Reports characters, words and tokens for three groups:
  always    every agent body (frontmatter stripped) + skills/handbook + handbook/STD-short.md
            + skills/using-team + templates/project/claude/rules/*.tmpl
  feature   always + 4 discipline skills (analyze, plan, build, verify — SKILL.md bodies)
  repo      every tracked text file (md, sh, py, json, yml, tmpl, txt), excluding eval run outputs
Tokens: if `tiktoken` is importable, a real BPE count with the named encoding (default o200k_base) —
a PROXY for Claude's tokenizer, which is not public. Otherwise an estimate: ceil(utf8_bytes / 3.6),
labelled "estimate". Both are printed when tiktoken is available.

Usage: measure-context.py [--root DIR] [--ref GITREF] [--encoding NAME] [--json]
  --ref reads files from a git ref (e.g. pre-p9) instead of the working tree.
"""
import glob
import json
import math
import os
import re
import subprocess
import sys

DISCIPLINE = ["analyze", "plan", "build", "verify"]
TEXT_EXT = (".md", ".sh", ".py", ".json", ".yml", ".yaml", ".tmpl", ".txt")


def body(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:]
    return text


class Source:
    def __init__(self, root, ref=None):
        self.root, self.ref = root, ref

    def ls(self):
        cmd = ["git", "ls-tree", "-r", "--name-only", self.ref] if self.ref else ["git", "ls-files"]
        return subprocess.run(cmd, cwd=self.root, capture_output=True, text=True).stdout.splitlines()

    def read(self, path):
        if self.ref:
            r = subprocess.run(["git", "show", f"{self.ref}:{path}"], cwd=self.root, capture_output=True, text=True)
            return r.stdout if r.returncode == 0 else None
        try:
            with open(os.path.join(self.root, path), encoding="utf-8") as fh:
                return fh.read()
        except OSError:
            return None


def groups(src):
    files = src.ls()
    pick = lambda pat: sorted(f for f in files if re.fullmatch(pat, f))
    always = (pick(r"agents/[^/]+\.md") + ["skills/handbook/SKILL.md", "handbook/STD-short.md", "skills/using-team/SKILL.md"]
              + pick(r"templates/project/claude/rules/[^/]+\.tmpl"))
    feature = always + [f"skills/{n}/SKILL.md" for n in DISCIPLINE]
    repo = [f for f in files if f.endswith(TEXT_EXT) and "/out/" not in f]
    return {"always": always, "feature": feature, "repo": repo}


def counter(encoding):
    try:
        import tiktoken  # optional, not a kit dependency
        enc = tiktoken.get_encoding(encoding)
        return lambda t: len(enc.encode(t, disallowed_special=())), f"tiktoken {encoding} (proxy for Claude)"
    except Exception:
        return None, None


def measure(src, encoding):
    real, label = counter(encoding)
    out = {}
    for g, paths in groups(src).items():
        chars = words = byts = tokens = 0
        n = 0
        for p in paths:
            t = src.read(p)
            if t is None:
                continue
            if g != "repo" and (p.startswith("agents/") or p.startswith("skills/")):
                t = body(t)
            n += 1
            chars += len(t)
            words += len(t.split())
            byts += len(t.encode("utf-8"))
            if real:
                tokens += real(t)
        row = {"files": n, "chars": chars, "words": words, "estimate_tokens": math.ceil(byts / 3.6)}
        if real:
            row["tokens"] = tokens
        out[g] = row
    return out, label or "estimate: ceil(utf8_bytes / 3.6)"


def main(argv):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ref, encoding, as_json = None, "o200k_base", "--json" in argv
    for i, a in enumerate(argv):
        if a == "--root":
            root = argv[i + 1]
        if a == "--ref":
            ref = argv[i + 1]
        if a == "--encoding":
            encoding = argv[i + 1]
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    data, label = measure(Source(root, ref), encoding)
    if as_json:
        print(json.dumps({"ref": ref or "WORKTREE", "tokenizer": label, "groups": data}, indent=1))
        return 0
    print(f"measure-context ({ref or 'working tree'}) — tokenizer: {label}")
    print("| group | files | chars | words | tokens | estimate |")
    print("|---|---|---|---|---|---|")
    for g, r in data.items():
        print(f"| {g} | {r['files']} | {r['chars']} | {r['words']} | {r.get('tokens', '—')} | {r['estimate_tokens']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
