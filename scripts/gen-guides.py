#!/usr/bin/env python3
"""Sinh skills/README.md, docs/guides/want-x-type-y.md, docs/guides/decision-tree.md (chỉ stdlib).

Nguồn: frontmatter + mục '## Đầu ra' của skills/*/SKILL.md; bảng playbook trong workflows/README.md.
Dùng: scripts/gen-guides.py           ghi ba file
      scripts/gen-guides.py --check   mã thoát 1 nếu file nào lệch (in tên file lệch)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEN = "<!-- GENERATED — do not edit; run scripts/gen-guides.py -->"
# Vai chạy skill khi skill không fork sang một agent.
MAIN_ROLE = {"commit": "dev, maintainer", "handbook": "mọi vai (nạp sẵn)",
             "using-team": "team-leader, tech-lead (nạp sẵn)"}
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
            who = "người"
        elif fm.get("user-invocable") == "false":
            who = "Claude"
        else:
            who = "cả hai"
        agent = fm.get("agent", "")
        role = agent.split(":", 1)[1] if agent.startswith("team:") else MAIN_ROLE.get(name, "team-leader")
        outs = []
        for p in re.findall(r"`([^`]+)`", section(body, "Đầu ra")):
            if ("/" in p or p.endswith((".md", ".json", ".jsonl"))) and p not in outs:
                outs.append(p)
        desc = fm.get("description", "")
        when = desc[len("Dùng khi "):] if desc.startswith("Dùng khi ") else desc
        rows.append(dict(name=name, who=who, role=role, outs=outs[:3], when=when.rstrip("."),
                         hint=fm.get("argument-hint", "")))
    return rows


def render_skills_readme(rows):
    out = [GEN, "# Skills của plugin `team`", "",
           "Mỗi thư mục là một lệnh `/team:<tên>`. Cài cục bộ thì gõ `/<tên>`.", "",
           "| Skill | Ai gọi | Vai chạy | Artifact |", "|---|---|---|---|"]
    for r in rows:
        arts = ", ".join(f"`{cell(a)}`" for a in r["outs"]) or "—"
        out.append(f"| [`{r['name']}`]({r['name']}/SKILL.md) | {r['who']} | {r['role']} | {arts} |")
    return "\n".join(out) + "\n"


def render_want(rows):
    out = [GEN, "# Muốn X thì gõ Y", "",
           "Bảng sinh từ `skills/*/SKILL.md`. Cài cục bộ (không qua marketplace): bỏ tiền tố `team:`.", "",
           "| Khi | Gõ | Vai chạy | Để lại |", "|---|---|---|---|"]
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
    out = [GEN, "# Chọn playbook nào", "",
           "team-leader chọn ở `/team:intake`: xét từ trên xuống, dòng đầu tiên khớp thắng; rồi mới định cỡ.",
           "Nguồn: `workflows/README.md`. Chuỗi skill, cổng, điểm dừng của từng playbook nằm trong file playbook.", "",
           table, "",
           "Chạy không người trông: `workflows/batch/` (build-all-tasks, verify-all, weekly-retro, clean-sweep)."]
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
