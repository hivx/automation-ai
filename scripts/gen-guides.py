#!/usr/bin/env python3
"""Generates skills/README.md, docs/guides/want-x-type-y.md, docs/guides/decision-tree.md (stdlib only).

Sources: frontmatter + the '## Outputs' section of skills/*/SKILL.md; the playbook table in workflows/README.md.
Usage: scripts/gen-guides.py           write the three files
       scripts/gen-guides.py --check   exit code 1 if any file is stale (prints the stale file names)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEN = "<!-- GENERATED — do not edit; run scripts/gen-guides.py -->"
# Role that runs a skill when the skill does not fork to an agent.
MAIN_ROLE = {"commit": "dev, maintainer", "handbook": "every role (preloaded)",
             "using-team": "team-leader, tech-lead (preloaded)"}
# Vietnamese forms of skills not yet converted (P9 transition), escaped so this file stays English.
LEGACY_OUTPUTS, LEGACY_PREFIX = "\u0110\u1ea7u ra", "D\u00f9ng khi "  # "Outputs", "Use when "
PB_START, PB_END = "<!-- playbook-table:start -->", "<!-- playbook-table:end -->"


def frontmatter(text):
    lines = text.split("\n")
    end = lines.index("---", 1)
    data = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1].replace('\\"', '"')
            data[m.group(1)] = v
    return data, "\n".join(lines[end + 1:])


def section(body, title):
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def cell(s):
    return s.replace("|", "\\|").strip()


def skills():
    rows = []
    for d in sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()):
        fm, body = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
        name = fm.get("name", d.name)
        if fm.get("disable-model-invocation") == "true":
            who = "human"
        elif fm.get("user-invocable") == "false":
            who = "Claude"
        else:
            who = "both"
        agent = fm.get("agent", "")
        role = agent.split(":", 1)[1] if agent.startswith("team:") else MAIN_ROLE.get(name, "team-leader")
        outs = []
        outsec = re.sub(r"```.*?```", "", section(body, "Outputs") or section(body, LEGACY_OUTPUTS), flags=re.S)  # drop example return-message blocks
        for p in re.findall(r"`([^`\n]+)`", outsec):
            if ("/" in p or p.endswith((".md", ".json", ".jsonl"))) and p not in outs:
                outs.append(p)
        desc = fm.get("description", "")
        when = next((desc[len(p):] for p in ("Use when ", LEGACY_PREFIX) if desc.startswith(p)), desc)
        rows.append(dict(name=name, who=who, role=role, outs=outs[:3], when=when.rstrip("."),
                         hint=fm.get("argument-hint", "")))
    return rows


def render_skills_readme(rows):
    out = [GEN, "# Skills of the `team` plugin", "",
           "Each folder is a `/team:<name>` command. With a local install, type `/team-<name>`.", "",
           "| Skill | Invoked by | Runs as role | Artifacts |", "|---|---|---|---|"]
    for r in rows:
        arts = ", ".join(f"`{cell(a)}`" for a in r["outs"]) or "—"
        out.append(f"| [`{r['name']}`]({r['name']}/SKILL.md) | {r['who']} | {r['role']} | {arts} |")
    return "\n".join(out) + "\n"


def render_want(rows):
    out = [GEN, "# Want X, type Y", "",
           "Table generated from `skills/*/SKILL.md`. Local install (without the marketplace): type `/team-<name>` instead of `/team:<name>`.", "",
           "| When | Type | Runs as role | Leaves behind |", "|---|---|---|---|"]
    for r in rows:
        if r["who"] == "Claude":
            continue
        cmd = f"/team:{r['name']} {r['hint']}".strip()
        arts = ", ".join(f"`{cell(a)}`" for a in r["outs"]) or "—"
        out.append(f"| {cell(r['when'])} | `{cell(cmd)}` | {r['role']} | {arts} |")
    return "\n".join(out) + "\n"


def render_tree():
    text = (ROOT / "workflows" / "README.md").read_text(encoding="utf-8")
    if PB_START not in text or PB_END not in text:
        raise SystemExit("workflows/README.md: missing playbook-table markers")
    table = text.split(PB_START, 1)[1].split(PB_END, 1)[0].strip("\n")
    table = re.sub(r"\]\((?!http)([^)]+)\)", r"](../../workflows/\1)", table)
    out = [GEN, "# Which playbook", "",
           "team-leader chooses at `/team:intake`: read from the top, the first matching row wins; size comes after.",
           "Source: `workflows/README.md`. Each playbook's skill chain, gates and stop points live in the playbook file.", "",
           table, "",
           "Unattended runs: `workflows/batch/` (build-all-tasks, verify-all, weekly-retro, clean-sweep)."]
    return "\n".join(out) + "\n"


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    rows = skills()
    targets = {
        ROOT / "skills" / "README.md": render_skills_readme(rows),
        ROOT / "docs" / "guides" / "want-x-type-y.md": render_want(rows),
        ROOT / "docs" / "guides" / "decision-tree.md": render_tree(),
    }
    stale = [p for p, t in targets.items() if not p.is_file() or p.read_text(encoding="utf-8") != t]
    if "--check" in argv:
        for p in stale:
            print(f"{p.relative_to(ROOT)}: stale; run scripts/gen-guides.py")
        return 1 if stale else 0
    for p, t in targets.items():
        p.write_text(t, encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
