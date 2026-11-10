#!/usr/bin/env python3
"""gen-vi-guide.py — regenerate the generated blocks of the owner's Vietnamese guide (stdlib only).

The guide file name is read from scripts/vi-guide.conf (GUIDE_FILE=..., default GUIDE-VI.md).
Blocks between `<!-- gen:<name> -->` and `<!-- /gen:<name> -->` are rebuilt from the repo:
  skills, agents, playbooks, gates, config, std, anchors, stats.
Everything outside the markers is hand-written and kept byte for byte.
Vietnamese one-liners come from scripts/vi-strings.json; a skill, agent, playbook, STD code or
config/profile key without a line there is an error.

Usage: gen-vi-guide.py            rewrite the guide in place
       gen-vi-guide.py --check    exit 1 if the guide is stale or vi-strings.json has gaps
                                  (the commit/date lines of gen:stats are ignored when comparing)
"""
import datetime
import glob
import json
import os
import re
import statistics
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKS = ["skills", "agents", "playbooks", "gates", "config", "std", "anchors", "stats"]
PLAYBOOKS = ["takeover", "new-project", "new-feature", "change-request", "bug-fix", "hotfix", "refactor",
             "dependency-upgrade", "data-migration", "integration", "ci-fix", "docs-only", "client-docs",
             "release", "spike", "retro"]
GATE_ARTIFACT = {"G0_takeover": "docs/team/ai-readiness.md", "G1_spec": "spec.md", "G2_arch": "arch-impact.md",
                 "G2b_design": "design.md", "G3_plan": "plan.md", "G4_uat": "acceptance.md", "G5_prod": "asbuilt.md"}



def rd(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as fh:
        return fh.read()


def guide_name():
    try:
        for line in rd("scripts", "vi-guide.conf").splitlines():
            if line.startswith("GUIDE_FILE="):
                return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return "GUIDE-VI.md"


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for l in m.group(1).split("\n"):
            mm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", l)
            if mm:
                v = mm.group(2).strip()
                fm[mm.group(1)] = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"" else v
    return fm, text[m.end():] if m else text


def section(body, title):
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def cell(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def strings():
    return json.loads(rd("scripts", "vi-strings.json"))


G = strings().get("guide", {})  # every Vietnamese label of the generated tables lives in vi-strings.json
VOLATILE = re.compile(r"^- (Commit|" + re.escape(G.get("stat_date_label", "date")) + r"): ")


def gaps(vs):
    miss = []
    skills = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")))
    agents = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT, "agents", "*.md")))
    std = re.findall(r"^\| (STD-[A-Z]+-\d+) \|", rd("handbook", "STD.md"), re.M)
    miss += [f"skills.{s}" for s in skills if not vs["skills"].get(s)]
    miss += [f"agents.{a}" for a in agents if not (vs["agents"].get(a) or {}).get("viec")]
    miss += [f"playbooks.{p}" for p in PLAYBOOKS if not (vs["playbooks"].get(p) or {}).get("khi")]
    miss += [f"std.{c}" for c in std if not vs["std"].get(c)]
    for kind, schema in (("config", "config.schema.json"), ("profile", "profile.schema.json")):
        for key, _, _ in schema_keys(schema):
            if not vs[kind].get(key):
                miss.append(f"{kind}.{key}")
    return miss


def schema_keys(name):
    d = json.loads(rd("templates", "schemas", name))
    out = []

    def walk(n, p=""):
        for k, v in (n.get("properties") or {}).items():
            t = v.get("type", "")
            t = "/".join(t) if isinstance(t, list) else t
            if "enum" in v:
                t += " (" + " | ".join(str(x) for x in v["enum"]) + ")"
            out.append((p + k, t, v.get("default", "")))
            if isinstance(v, dict):
                walk(v, p + k + ".")
    walk(d)
    return out


def gen_skills(vs):
    rows = [G["skills_head"], "|---|---|---|---|---|"]
    for p in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(p))
        fm, body = frontmatter(rd(p))
        who = G["who_human"] if fm.get("disable-model-invocation") == "true" else (
            G["who_claude"] if fm.get("user-invocable") == "false" else G["who_both"])
        agent = fm.get("agent", "")
        role = agent.split(":", 1)[1] if agent.startswith("team:") else G["main_session"]
        outs = re.sub(r"```.*?```", "", section(body, "Outputs"), flags=re.S)
        arts = []
        for a in re.findall(r"`([^`\n]+)`", outs):
            if ("/" in a or a.endswith((".md", ".json", ".jsonl"))) and a not in arts:
                arts.append(a)
        rows.append(f"| `/team:{name}` | {who} | {role} | {cell(', '.join(arts[:3])) or '—'} | {cell(vs['skills'].get(name, ''))} |")
    return rows


def gen_agents(vs):
    rows = [G["agents_head"], "|---|---|---|---|---|"]
    for p in sorted(glob.glob(os.path.join(ROOT, "agents", "*.md"))):
        name = os.path.basename(p)[:-3]
        fm, _ = frontmatter(rd(p))
        a = vs["agents"].get(name) or {}
        rows.append(f"| `{name}` | {cell(a.get('viec', ''))} | {cell(a.get('khong', ''))} | {fm.get('model', '')} / {fm.get('effort', '')} | {fm.get('maxTurns', '')} |")
    return rows


def gen_playbooks(vs):
    rows = [G["playbooks_head"], "|---|---|---|---|"]
    for n in PLAYBOOKS:
        try:
            text = rd("workflows", f"{n}.md")
        except OSError:
            text = ""
        gates = sorted(set(re.findall(r"\bG(?:0|1|2b|2|3|4|5)\b", section(text, "Gates"))),
                       key=lambda g: ["G0", "G1", "G2", "G2b", "G3", "G4", "G5"].index(g))
        p = vs["playbooks"].get(n) or {}
        rows.append(f"| `{n}` | {cell(p.get('khi', ''))} | {cell(p.get('chuoi', ''))} | {', '.join(gates) or '—'} |")
    return rows


def gen_gates(vs):
    cfg = json.loads(rd("templates", "project", "team", "config.json"))
    rows = [G["gates_head"], "|---|---|---|---|"]
    for g, on in cfg.get("gates", {}).items():
        art = GATE_ARTIFACT.get(g, "—")
        art = art if art.startswith("docs/") else f"docs/team/features/<ID>/{art}"
        how = G["gate_g5"] if g == "G5_prod" else G["gate_how"].format(code=g.split("_")[0])
        rows.append(f"| `{g}` | `{art}` | {how} | {G['on'] if on else G['off']} |")
    return rows


def gen_config(vs):
    rows = []
    for kind, schema, label in (("config", "config.schema.json", "`.team/config.json`"),
                                ("profile", "profile.schema.json", "`.team/profile.json`")):
        rows += [f"**{label}**", "", G["config_head"], "|---|---|---|---|"]
        for key, t, d in schema_keys(schema):
            dv = json.dumps(d, ensure_ascii=False) if d != "" else "—"
            rows.append(f"| `{key}` | {cell(t)} | {cell(dv)} | {cell(vs[kind].get(key, ''))} |")
        rows.append("")
    return rows[:-1]


def gen_std(vs):
    rows = [G["std_head"], "|---|---|---|"]
    for m in re.finditer(r"^\| (STD-[A-Z]+-\d+) \| .*? \| (\d) \|", rd("handbook", "STD.md"), re.M):
        rows.append(f"| `{m.group(1)}` | {m.group(2)} | {cell(vs['std'].get(m.group(1), ''))} |")
    rows += ["", G["std_note"]]
    return rows


def gen_anchors(vs):
    rows = [G["anchors_note"], ""]
    for line in rd("scripts", "anchors.txt").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        rows.append(f"- `{line.split(chr(9), 1)[0]}`")
    return rows


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def gen_stats(vs):
    km = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kit-metrics.py"), "--json"], cwd=ROOT,
                        capture_output=True, text=True).stdout
    items = json.loads(km)["items"] if km.strip().startswith("{") else []
    med = lambda c: statistics.median([i["words"] for i in items if i["cls"] == c]) if any(i["cls"] == c for i in items) else 0
    version = json.loads(rd(".claude-plugin", "plugin.json")).get("version", "?")
    n_scripts = len([f for f in os.listdir(os.path.join(ROOT, "scripts")) if f.endswith((".sh", ".py"))])
    return [G["stat_version"].format(version=version),
            G["stat_counts"].format(skills=len(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))),
                                    agents=len(glob.glob(os.path.join(ROOT, "agents", "*.md"))), playbooks=len(PLAYBOOKS),
                                    batch=len(glob.glob(os.path.join(ROOT, "workflows", "batch", "*.md"))), scripts=n_scripts),
            G["stat_words"].format(always=med("always"), full=med("full"), agent=med("agent")),
            G["stat_commit"].format(commit=git("rev-parse", "--short", "HEAD")),
            G["stat_date"].format(label=G["stat_date_label"], date=datetime.date.today().isoformat())]


def render(text, vs):
    for b in BLOCKS:
        start, end = f"<!-- gen:{b} -->", f"<!-- /gen:{b} -->"
        if start not in text or end not in text:
            raise SystemExit(f"gen-vi-guide: marker {start} / {end} missing in the guide")
        body = "\n".join(globals()[f"gen_{b}"](vs))
        text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: f"{start}\n{body}\n{end}", text, flags=re.S)
    return text


def main(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    vs = strings()
    path = os.path.join(ROOT, guide_name())
    old = open(path, encoding="utf-8").read()
    new = render(old, vs)
    missing = gaps(vs)
    if "--check" in argv:
        strip = lambda t: "\n".join(l for l in t.split("\n") if not VOLATILE.match(l))
        bad = 0
        if strip(new) != strip(old):
            print(f"gen-vi-guide: {guide_name()} is stale — run scripts/gen-vi-guide.py")
            bad = 1
        for m in missing:
            print(f"gen-vi-guide: scripts/vi-strings.json lacks a Vietnamese line for {m}")
            bad = 1
        return bad
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new)
    for m in missing:
        print(f"gen-vi-guide: scripts/vi-strings.json lacks a Vietnamese line for {m}", file=sys.stderr)
    print(f"gen-vi-guide: wrote {guide_name()}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
