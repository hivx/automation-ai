#!/usr/bin/env python3
"""Sinh bảng vai trong docs/02-team.md từ frontmatter của agents/*.md (chỉ stdlib).

Bảng nằm giữa <!-- team-table:start --> và <!-- team-table:end -->.
Dùng: scripts/gen-team-table.py           ghi đè bảng trong docs/02-team.md
      scripts/gen-team-table.py --check   mã thoát 1 nếu bảng lệch
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "02-team.md"
START, END = "<!-- team-table:start -->", "<!-- team-table:end -->"
ORDER = ["team-leader", "tech-lead", "coach", "analyst", "researcher", "architect", "designer",
         "dev", "reviewer", "qa", "writer", "maintainer", "devops"]


def frontmatter(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    end = lines.index("---", 1)
    data, key = {}, None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data[key] = [] if val == "" else val
        elif key and line.strip().startswith("- "):
            data[key].append(line.strip()[2:])
    return data


def render():
    files = {p.stem: p for p in (ROOT / "agents").glob("*.md")}
    names = [n for n in ORDER if n in files] + sorted(set(files) - set(ORDER))
    rows = ["| Vai | Giao khi | Tools | Model | Effort | maxTurns | Memory | Isolation | Skills nạp sẵn |",
            "|---|---|---|---|---|---|---|---|---|"]
    for n in names:
        fm = frontmatter(files[n])
        desc = fm.get("description", "").replace("|", "\\|")
        if desc.startswith("Giao khi "):
            desc = desc[len("Giao khi "):]
        skills = fm.get("skills", [])
        skills = ", ".join(skills) if isinstance(skills, list) else skills
        rows.append(f"| [{n}](../agents/{n}.md) | {desc} | {fm.get('tools', 'inherit')} | "
                    f"{fm.get('model', '—')} | {fm.get('effort', '—')} | {fm.get('maxTurns', '—')} | "
                    f"{fm.get('memory', '—')} | {fm.get('isolation', '—')} | {skills or '—'} |")
    return "\n".join(rows)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    text = DOC.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"{DOC.relative_to(ROOT)}: missing {START} / {END} markers", file=sys.stderr)
        return 1
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{START}\n{render()}\n{END}{tail}"
    if "--check" in argv:
        return 0 if new == text else 1
    DOC.write_text(new, encoding="utf-8")
    print(f"wrote table in {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
