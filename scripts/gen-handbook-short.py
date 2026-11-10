#!/usr/bin/env python3
"""Generate handbook/STD-short.md from handbook/STD.md (standard library only).

The short version holds only: level 2 and 3 rules (code + rule sentence), the two checklists,
and the finding format. Output is deterministic. Usage:
  scripts/gen-handbook-short.py                 write handbook/STD-short.md
  scripts/gen-handbook-short.py --stdout        print to stdout (validate.sh compares it)
  scripts/gen-handbook-short.py --stats         print the rule count per area
Exit code 1 when STD.md is structurally invalid.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "handbook" / "STD.md"
DST = ROOT / "handbook" / "STD-short.md"
AREAS = ["STRUCT", "NAME", "STYLE", "DESIGN", "TEST", "ERR", "GIT", "CI", "DOC", "SEC", "DEP", "OPS"]
ENFORCERS = {"hook", "script", "CI", "reviewer", "qa", "text"}
MAX_LINES = 120
RULE_RE = re.compile(r"^\|\s*(STD-([A-Z]+)-(\d+))\s*\|(.+?)\|\s*([123])\s*\|(.+?)\|(.+?)\|\s*$")
HEADER = "<!-- GENERATED — do not edit; run scripts/gen-handbook-short.py -->"


def die(msg):
    print(f"handbook/STD.md: {msg}", file=sys.stderr)
    sys.exit(1)


def section(lines, title):
    """Return the lines between '## <title>' and the next '## ' heading."""
    try:
        start = lines.index(f"## {title}")
    except ValueError:
        die(f"missing section '## {title}'")
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out


def parse():
    lines = SRC.read_text(encoding="utf-8").split("\n")
    rules, seen = [], set()
    for line in lines:
        m = RULE_RE.match(line)
        if not m:
            continue
        code, area, num, text, level, enforcers, slot = m.groups()
        if area not in AREAS:
            die(f"{code}: unknown area")
        if code in seen:
            die(f"{code}: duplicate code")
        seen.add(code)
        bad = {e.strip() for e in enforcers.split(",")} - ENFORCERS
        if bad:
            die(f"{code}: unknown enforcer {sorted(bad)}")
        if not slot.strip():
            die(f"{code}: empty profile-slot column (use —)")
        rules.append((area, int(num), code, text.strip(), int(level)))
    for area in AREAS:
        nums = sorted(n for a, n, *_ in rules if a == area)
        if not nums:
            die(f"area {area} has no rules")
        if nums != list(range(1, len(nums) + 1)):
            die(f"area {area} numbering has gaps: {nums}")
    review = [l for l in section(lines, "Review checklist (10)") if re.match(r"^\d+\. ", l)]
    accept = [l for l in section(lines, "Acceptance checklist (6)") if re.match(r"^\d+\. ", l)]
    if len(review) != 10:
        die(f"Review checklist has {len(review)} items, expected 10")
    if len(accept) != 6:
        die(f"Acceptance checklist has {len(accept)} items, expected 6")
    for item in review + accept:
        for code in re.findall(r"STD-[A-Z]+-\d+", item):
            if code not in seen:
                die(f"checklist references unknown code {code}")
    finding = [l for l in section(lines, "Finding format") if l.strip()]
    rules.sort(key=lambda r: (AREAS.index(r[0]), r[1]))
    return rules, review, accept, finding


def render(rules, review, accept, finding):
    out = [HEADER, "# STD-short — short version of handbook/STD.md", ""]
    out.append("## Level 2–3 rules (level in parentheses)")
    for area, _, code, text, level in rules:
        if level >= 2:
            out.append(f"- {code} ({level}) {text}")
    out += ["", "## Review checklist (10)", *review, "", "## Acceptance checklist (6)", *accept,
            "", "## Finding format", *finding]
    return "\n".join(out) + "\n"


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    rules, review, accept, finding = parse()
    if "--stats" in argv:
        for area in AREAS:
            rs = [r for r in rules if r[0] == area]
            print(f"{area:7} {len(rs)} rules (L3={sum(r[4] == 3 for r in rs)}, "
                  f"L2={sum(r[4] == 2 for r in rs)}, L1={sum(r[4] == 1 for r in rs)})")
        print(f"TOTAL   {len(rules)} rules")
        return 0
    text = render(rules, review, accept, finding)
    n = text.count("\n")
    if n > MAX_LINES:
        die(f"short version would be {n} lines (max {MAX_LINES})")
    if "--stdout" in argv:
        sys.stdout.write(text)
    else:
        DST.write_text(text, encoding="utf-8")
        print(f"wrote {DST.relative_to(ROOT)} ({n} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
