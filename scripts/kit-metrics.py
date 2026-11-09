#!/usr/bin/env python3
"""kit-metrics.py — đo từng skill/agent so với chuẩn chất lượng (chỉ thư viện chuẩn).

Đọc chuẩn từ scripts/skill-budgets.txt, scripts/skill-sections.txt, scripts/agent-sections.txt.
Mỗi mục: số chữ thân, tiêu đề có/thiếu (đúng thứ tự), số dòng tự bào chữa, số dấu hiệu sai, số ô kiểm,
mô tả (độ dài, tiền tố), số file references/, lệnh stack ghi cứng, ngày đổi git cuối, score 0–100.
score = 100 − Σ trọng số × khoảng cách tới chuẩn (WEIGHTS; thiếu chữ nặng nhất).

Dùng: kit-metrics.py [--only <tên>] [--json] [--md]   (mặc định in Markdown)
      kit-metrics.py --check   thoát 1 nếu mục nào (ngoài scripts/quality-backlog.txt) chưa đạt chuẩn
"""
import json
import os
import re
import statistics
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS = {"words": 40, "sections": 30, "rows": 10, "bullets": 10, "checks": 10}
SKILL_PREFIX, SKILL_DESC_MAX = "Dùng khi", 500
AGENT_PREFIX, AGENT_DESC_MAX = "Giao khi", 300


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def load_budgets():
    classes, members = {}, {}
    for line in read(os.path.join(ROOT, "scripts", "skill-budgets.txt")).splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        classes[parts[0]] = (int(parts[1]), int(parts[2]))
        for m in parts[3:]:
            members[m] = parts[0]
    return classes, members


def parse_rule(line):
    parts = [p.strip() for p in line.split("|")]
    heading, req = parts[0], {}
    for p in parts[1:]:
        m = re.match(r"(rows|bullets|checks)>=(\d+)$", p)
        if m:
            req[m.group(1)] = int(m.group(2))
        elif p.startswith("contains="):
            req["contains"] = p.split("=", 1)[1]
    return heading, req


def load_sections():
    skills = {}
    for line in read(os.path.join(ROOT, "scripts", "skill-sections.txt")).splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cls, rest = line.split("|", 1)
        skills.setdefault(cls.strip(), []).append(parse_rule(rest))
    agents = [parse_rule(l) for l in read(os.path.join(ROOT, "scripts", "agent-sections.txt")).splitlines()
              if l.strip() and not l.startswith("# ")]
    return skills, agents


def split(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        fm = {}
        for l in lines[1:end]:
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", l)
            if m:
                v = m.group(2).strip()
                fm[m.group(1)] = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"" else v
        return fm, "\n".join(lines[end + 1:])
    return {}, text


def sections(body):
    out, cur = {}, None
    in_code = False
    for l in body.split("\n"):
        if l.startswith("```"):
            in_code = not in_code
        if not in_code and l.startswith("## "):
            cur = l.strip()
            out[cur] = []
            continue
        if cur:
            out[cur].append(l)
    return out


def count(lines, kind):
    if kind == "rows":
        rows = [l for l in lines if l.strip().startswith("|")]
        return max(0, len([r for r in rows if not re.match(r"^\|\s*:?-{2,}", r.strip())]) - 1)
    if kind == "checks":
        return sum(1 for l in lines if re.match(r"^\s*- \[[ xX]\]", l))
    return sum(1 for l in lines if re.match(r"^\s*- ", l))


def stack_terms():
    t = read(os.path.join(ROOT, "scripts", "validate.sh"))
    m = re.search(r'STACK_CMD_BLACKLIST="([^"]+)"', t)
    return [x for x in (m.group(1).split("|") if m else []) if x]


def last_change(path):
    try:
        return subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT,
                              capture_output=True, text=True, timeout=10).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def measure(kind, name, path, budgets, members, skill_rules, agent_rules, terms):
    fm, body = split(read(path))
    words = len(body.split())
    if kind == "agent":
        cls, rules, prefix, dmax = "agent", agent_rules, AGENT_PREFIX, AGENT_DESC_MAX
    else:
        cls = members.get(name, "full")
        rules, prefix, dmax = skill_rules.get(cls, []), SKILL_PREFIX, SKILL_DESC_MAX
    lo, hi = budgets[cls]
    secs = sections(body)
    want = [h for h, _ in rules]
    present = [h for h in want if h in secs]
    order_ok = [h for h in secs if h in want] == want
    missing = [h for h in want if h not in secs]
    counts, needs = {}, {}
    for h, req in rules:
        for k, n in req.items():
            if k == "contains":
                ok = h in secs and req["contains"] in "\n".join(secs[h])
                counts[f"{h} contains"] = ok
                needs[f"{h} contains"] = (ok, 1)
            else:
                got = count(secs.get(h, []), k)
                counts[k] = got
                needs[k] = (got, n)
    gap = {}
    gap["words"] = (lo - words) / lo if words < lo and lo else ((words - hi) / hi if words > hi else 0)
    gap["sections"] = (len(missing) + (0 if order_ok else 0.5)) / max(1, len(want))
    for k in ("rows", "bullets", "checks"):
        if k in needs:
            got, n = needs[k]
            gap[k] = max(0, (n - got) / n)
    contains_fail = [k for k, v in needs.items() if k.endswith("contains") and not v[0]]
    if contains_fail:
        gap["sections"] = min(1, gap["sections"] + 0.25 * len(contains_fail) / max(1, len(want)))
    wsum = sum(WEIGHTS[k] for k in gap)
    score = round(100 - sum(WEIGHTS[k] * min(1, v) for k, v in gap.items()) * 100 / wsum)
    desc = fm.get("description", "")
    pat = re.compile("|".join(r"(?<![\w-])" + re.escape(t.rstrip()) + (r"(?=\s)" if t.endswith(" ") else r"(?![\w-])") for t in terms)) if terms else None
    refs = os.path.join(os.path.dirname(path), "references") if kind == "skill" else None
    at_bar = (gap["words"] == 0 and not missing and order_ok and all(v == 0 for k, v in gap.items() if k != "sections")
              and not contains_fail and desc.startswith(prefix) and len(desc) <= dmax)
    return dict(kind=kind, name=name, cls=cls, words=words, budget=[lo, hi], sections_present=len(present),
                sections_required=len(want), missing=missing, order_ok=order_ok, counts=counts,
                contains_fail=contains_fail, desc_len=len(desc), desc_prefix_ok=desc.startswith(prefix),
                references=len([f for f in os.listdir(refs)]) if refs and os.path.isdir(refs) else 0,
                stack_hits=len(pat.findall(body)) if pat else 0, last_change=last_change(os.path.relpath(path, ROOT)),
                score=score, at_bar=at_bar)


def collect():
    budgets, members = load_budgets()
    skill_rules, agent_rules = load_sections()
    terms = stack_terms()
    items = []
    for d in sorted(os.listdir(os.path.join(ROOT, "skills"))):
        p = os.path.join(ROOT, "skills", d, "SKILL.md")
        if os.path.isfile(p):
            items.append(measure("skill", d, p, budgets, members, skill_rules, agent_rules, terms))
    for f in sorted(os.listdir(os.path.join(ROOT, "agents"))):
        if f.endswith(".md"):
            items.append(measure("agent", f[:-3], os.path.join(ROOT, "agents", f), budgets, members, skill_rules, agent_rules, terms))
    return items


def summary(items):
    out = {}
    for cat in ("always", "full", "agent"):
        xs = [i for i in items if i["cls"] == cat]
        if xs:
            out[cat] = dict(count=len(xs), median_words=statistics.median(i["words"] for i in xs),
                            at_bar_pct=round(100 * sum(i["at_bar"] for i in xs) / len(xs)),
                            median_score=statistics.median(i["score"] for i in xs))
    disc = [i for i in items if i["name"] in ("using-team", "analyze", "build", "verify", "commit", "pr", "takeover", "make-skill") and i["kind"] == "skill"]
    out["discipline"] = dict(count=len(disc), median_words=statistics.median(i["words"] for i in disc) if disc else 0)
    out["all"] = dict(count=len(items), at_bar_pct=round(100 * sum(i["at_bar"] for i in items) / len(items)))
    return out


def markdown(items, summ):
    lines = ["| Mục | Lớp | Chữ | Ngân sách | Tiêu đề | Tự bào chữa | Dấu hiệu sai | Kiểm chứng | Mô tả | refs | Score | Đạt |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i in sorted(items, key=lambda x: (x["score"], x["kind"], x["name"])):
        c = i["counts"]
        lines.append(f"| {i['kind']}:{i['name']} | {i['cls']} | {i['words']} | {i['budget'][0]}–{i['budget'][1]} | "
                     f"{i['sections_present']}/{i['sections_required']}{'' if i['order_ok'] else ' (thứ tự)'} | "
                     f"{c.get('rows', '—')} | {c.get('bullets', '—')} | {c.get('checks', '—')} | "
                     f"{i['desc_len']}{'' if i['desc_prefix_ok'] else ' (tiền tố!)'} | {i['references']} | {i['score']} | "
                     f"{'✓' if i['at_bar'] else '—'} |")
    lines += ["", "| Nhóm | Số mục | Trung vị chữ | % đạt chuẩn | Trung vị score |", "|---|---|---|---|---|"]
    for k in ("always", "full", "agent"):
        if k in summ:
            s = summ[k]
            lines.append(f"| {k} | {s['count']} | {s['median_words']} | {s['at_bar_pct']}% | {s['median_score']} |")
    lines.append(f"| discipline skills | {summ['discipline']['count']} | {summ['discipline']['median_words']} | — | — |")
    lines.append(f"| tất cả | {summ['all']['count']} | — | {summ['all']['at_bar_pct']}% | — |")
    return "\n".join(lines)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    items = collect()
    if "--only" in argv:
        names = argv[argv.index("--only") + 1].split(",")
        items = [i for i in items if i["name"] in names or f"{i['kind']}:{i['name']}" in names]
    if "--check" in argv:
        backlog_file = os.path.join(ROOT, "scripts", "quality-backlog.txt")
        backlog = set()
        if os.path.isfile(backlog_file):
            backlog = {l.strip() for l in read(backlog_file).splitlines() if l.strip() and not l.startswith("#")}
        bad = 0
        for i in items:
            key = f"{i['kind']}:{i['name']}"
            if i["at_bar"] and key in backlog:
                print(f"{key}: đã đạt chuẩn — xóa khỏi scripts/quality-backlog.txt")
                bad += 1
            elif not i["at_bar"] and key not in backlog:
                why = []
                if i["words"] < i["budget"][0] or i["words"] > i["budget"][1]:
                    why.append(f"{i['words']} chữ (cần {i['budget'][0]}–{i['budget'][1]})")
                if i["missing"]:
                    why.append("thiếu " + ", ".join(i["missing"]))
                if not i["order_ok"]:
                    why.append("sai thứ tự tiêu đề")
                for k, v in i["counts"].items():
                    if isinstance(v, int):
                        why.append(f"{k}={v}")
                why += [f"thiếu nội dung: {k}" for k in i["contains_fail"]]
                if not i["desc_prefix_ok"]:
                    why.append("mô tả sai tiền tố")
                print(f"{key}: chưa đạt chuẩn (score {i['score']}): {'; '.join(why)}")
                bad += 1
        return 1 if bad else 0
    summ = summary(items)
    if "--json" in argv:
        print(json.dumps({"items": items, "summary": summ}, ensure_ascii=False, indent=2))
    else:
        print(markdown(items, summ))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
