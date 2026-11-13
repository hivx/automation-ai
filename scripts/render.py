#!/usr/bin/env python3
"""render.py — builds project files from the kit's templates/project/ (standard library only). Called by onboard.

Placeholders: {{a.b}} comes from .team/profile.json (then .team/config.json); {{kit}} = the kit directory
(as //absolute/path inside permission rules). Lists are joined with ", ". A missing value → empty string.
JSON templates (--json): an array element "{{cmd.*}}" expands to Bash(<command> *) for every non-empty cmd.* slot
  (plus one entry per subcommand of a `a && b` value, `cd` left out);
an element containing "{{protected_paths}}" expands to one element per protected path.

Usage:
  render.py --template T [--root R] [--kit K] [--out O]            text
  render.py --template T --json [--merge-into F]                     JSON; merged into F (existing values win,
                                                                     arrays are unioned without duplicates)
  render.py --template T --insert-block F                           insert/replace the <!-- team:start -->…<!-- team:end -->
                                                                     block in F, leaving the rest untouched
"""
import json
import os
import re
import sys

START, END = "<!-- team:start -->", "<!-- team:end -->"


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def lookup(ctx, dotted):
    for src in ctx:
        cur, ok = src, True
        for part in dotted.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            return ", ".join(map(str, cur)) if isinstance(cur, list) else ("" if cur is None else str(cur))
    return ""


def subst(text, ctx):
    """{{a.b}}, {{a.b|or:x}} (empty → x), {{a.b|lines:N}} (array → one element per line, indented N).
    Leaves GitHub Actions ${{ ... }} alone."""
    def rep(m):
        key, filt = m.group(1), (m.group(2) or "")
        if filt.startswith("lines:"):
            raw = None
            for src in ctx:
                cur = src
                for part in key.split("."):
                    cur = cur.get(part) if isinstance(cur, dict) else None
                if cur is not None:
                    raw = cur
                    break
            items = raw if isinstance(raw, list) else ([raw] if raw else [])
            pad = " " * int(filt.split(":", 1)[1] or 0)
            return ("\n" + pad).join(str(x) for x in items) if items else "true"
        val = lookup(ctx, key)
        if not val and filt.startswith("or:"):
            return filt.split(":", 1)[1]
        return val
    return re.sub(r"(?<!\$)\{\{\s*([A-Za-z0-9_.]+)\s*(?:\|\s*([a-z]+:[^}]*?))?\s*\}\}", rep, text)


def perm_path(p):
    p = p.strip()
    return p if p.startswith(("**", "/", "~", "./")) else "./" + p


def expand_json(node, ctx, profile):
    if isinstance(node, dict):
        return {k: expand_json(v, ctx, profile) for k, v in node.items()}
    if isinstance(node, list):
        out = []
        for item in node:
            if item == "{{cmd.*}}":
                for v in (profile.get("cmd") or {}).values():
                    if isinstance(v, str) and v.strip():
                        head = v.split('{file}')[0].strip()
                        out.append(f"Bash({head} *)")
                        parts = [s for s in re.split(r"\s*(?:&&|\|\||;)\s*", head) if s]
                        if len(parts) > 1:  # `cd <dir> && <tool> …`: permissions are checked per subcommand
                            out += [f"Bash({s} *)" for s in parts if not re.match(r"^cd(\s|$)", s)]
            elif isinstance(item, str) and "{{protected_paths}}" in item:
                for p in profile.get("protected_paths") or []:
                    out.append(item.replace("{{protected_paths}}", perm_path(p)))
            else:
                out.append(expand_json(item, ctx, profile))
        seen, uniq = set(), []
        for x in out:
            key = json.dumps(x, sort_keys=True)
            if key not in seen:
                seen.add(key)
                uniq.append(x)
        return uniq
    if isinstance(node, str):
        return subst(node, ctx)
    return node


def merge(old, new):
    """Merge new into old: values already in old win; dicts recurse; arrays are unioned without duplicates."""
    if isinstance(old, dict) and isinstance(new, dict):
        out = dict(old)
        for k, v in new.items():
            out[k] = merge(old[k], v) if k in old else v
        return out
    if isinstance(old, list) and isinstance(new, list):
        out = list(old)
        for x in new:
            if x not in out:
                out.append(x)
        return out
    return old


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    opts, flags, i = {}, set(), 0
    while i < len(argv):
        if argv[i] in ("--template", "--root", "--kit", "--out", "--merge-into", "--insert-block") and i + 1 < len(argv):
            opts[argv[i]] = argv[i + 1]
            i += 2
        else:
            flags.add(argv[i])
            i += 1
    root = os.path.abspath(opts.get("--root", os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()))
    kit = opts.get("--kit") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profile = load(os.path.join(root, ".team", "profile.json"))
    config = load(os.path.join(root, ".team", "config.json"))
    with open(opts["--template"], encoding="utf-8") as fh:
        tmpl = fh.read()
    if "--json" in flags:
        ctx = [{"kit": "/" + os.path.abspath(kit), "kit_dir": os.path.abspath(kit)}, profile, config]
        data = expand_json(json.loads(tmpl), ctx, profile)
        target = opts.get("--merge-into") or opts.get("--out")
        if opts.get("--merge-into") and os.path.isfile(opts["--merge-into"]):
            data = merge(load(opts["--merge-into"]), data)
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    else:
        text = subst(tmpl, [{"kit": os.path.abspath(kit)}, profile, config])
        target = opts.get("--out")
        if opts.get("--insert-block"):
            target = opts["--insert-block"]
            block = text.strip("\n")
            if START not in block:
                block = f"{START}\n{block}\n{END}"
            old = open(target, encoding="utf-8").read() if os.path.isfile(target) else ""
            if START in old and END in old:
                head, rest = old.split(START, 1)
                text = head + block + rest.split(END, 1)[1]
            else:
                text = (old.rstrip("\n") + "\n\n" if old.strip() else "") + block + "\n"
    if target:
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"render: wrote {os.path.relpath(target, root)}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
