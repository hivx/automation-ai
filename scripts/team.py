#!/usr/bin/env python3
"""team.py — trạng thái đội tính từ artifact (chỉ thư viện chuẩn). Không lưu con trỏ.

Lệnh con:
  status [<ID>] [--brief] [--waiting]   bảng giai đoạn từng feature + dòng "Chờ người"
  next <ID>                             lệnh skill kế tiếp
  metrics                               gộp docs/team/metrics/runs.jsonl theo agent/skill/cỡ
  scorecard                             ghi docs/team/metrics/scorecard.json
Cờ chung: --root DIR (mặc định $CLAUDE_PROJECT_DIR hoặc thư mục hiện tại), --json.

Giai đoạn (SPEC §4): intaken → specified → [researched] → [architected] → [designed] → planned
→ built → verified → released. Cổng bật mà chưa có `Approved-by:` (G5: `Approved-by-prod:`) chặn
MỌI giai đoạn sau, kể cả khi artifact sau đã có. Cỡ S không qua G1, G3 (ADJ-09);
playbook refactor và data-migration luôn bật G2b (ADJ-16).
"""
import json
import os
import re
import statistics
import sys

ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9-]+$")
APPROVED = re.compile(r"^\s*(?:[-*]\s*)?\**Approved-by\**\s*:\s*\**\s*(\S.*?\d{4}-\d{2}-\d{2}.*)$", re.M)
APPROVED_PROD = re.compile(r"^\s*(?:[-*]\s*)?\**Approved-by-prod\**\s*:\s*\**\s*(\S.*?\d{4}-\d{2}-\d{2}.*)$", re.M)
TASK = re.compile(r"^\s*-\s*\[( |x|X)\]\s*[*_`]*(T\d+)\b(.*)$", re.M)


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def kit_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def config(root):
    cfg = load_json(os.path.join(root, ".team", "config.json"), None)
    if cfg is None:
        cfg = load_json(os.path.join(kit_dir(), "templates", "project", "team", "config.json"), {})
    return cfg


def header(text, n=20):
    return "\n".join((text or "").split("\n")[:n])


def approved(text, prod=False):
    return bool((APPROVED_PROD if prod else APPROVED).search(header(text)))


def field(text, *names):
    for name in names:
        m = re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{name}\**\s*:\s*\**\s*([^\n]+)", text or "")
        if m:
            return m.group(1).strip().strip("*").strip()
    return ""


def title_of(fid, intake, spec):
    for text in (intake, spec):
        m = re.search(r"(?m)^#\s+(.+)$", text or "")
        if m:
            t = m.group(1).strip()
            t = re.sub(r"(?i)^(intake|spec|tiếp nhận)\s*[:\-—]?\s*", "", t)
            t = re.sub(rf"^{re.escape(fid)}\s*[—–:\-]?\s*", "", t).strip()
            if t and t != fid:
                return t
    req = field(intake, "Yêu cầu", "Request", "Yêu cầu gốc")
    return req.strip('"“”') or "—"


GATES = [("specified", "G1_spec", "spec.md"), ("architected", "G2_arch", "arch-impact.md"),
         ("designed", "G2b_design", "design.md"), ("planned", "G3_plan", "plan.md"),
         ("verified", "G4_uat", "acceptance.md")]


def feature_state(root, fid, cfg):
    d = os.path.join(root, "docs", "team", "features", fid)
    art = {n: read(os.path.join(d, n)) for n in ("intake.md", "spec.md", "research.md", "arch-impact.md",
                                                  "design.md", "plan.md", "tasks.md", "acceptance.md",
                                                  "asbuilt.md", "questions.md")}
    intake = art["intake.md"] or ""
    size_m = re.search(r"(?i)(?:cỡ|size)\**\s*:\**\s*\**\s*([SML])\b", intake)
    size = size_m.group(1).upper() if size_m else ""
    pb_m = re.search(r"(?i)playbook\**\s*:\**\s*\[?`?([a-z][a-z-]*)", intake)
    playbook = pb_m.group(1).lower() if pb_m else ""
    mode_m = re.search(r"(?i)(?:chế độ|mode)\**\s*:\**\s*\**\s*(ask|decide)\b", intake)
    mode = mode_m.group(1).lower() if mode_m else ""
    gates_cfg = dict(cfg.get("gates") or {})
    if playbook in ("refactor", "data-migration"):
        gates_cfg["G2b_design"] = True
    if size == "S":
        gates_cfg["G1_spec"] = False
        gates_cfg["G3_plan"] = False
        gates_cfg["G2b_design"] = gates_cfg.get("G2b_design", False) and playbook in ("refactor", "data-migration")

    tasks = TASK.findall(art["tasks.md"] or "")
    done = [t for t in tasks if t[0].lower() == "x"]
    blocked_task = next((t[1] for t in tasks if t[0] == " " and "BLOCKED" in t[2]), None)
    verdict_m = re.search(r"(?i)(?:verdict|phán quyết)\**\s*:\**\s*\**\s*(accepted|rework|design-defect)", art["acceptance.md"] or "")
    verdict = verdict_m.group(1).lower() if verdict_m else ""
    arch_ref = "architecture.md" in (intake + (art["spec.md"] or "") + (art["design.md"] or ""))
    cond = {
        "intaken": art["intake.md"] is not None,
        "specified": art["spec.md"] is not None and re.search(r"(?m)^##\s+Definition of Done", art["spec.md"]) is not None,
        "researched": art["research.md"] is not None,
        "architected": art["arch-impact.md"] is not None or (arch_ref and os.path.isfile(os.path.join(root, "docs", "team", "architecture.md"))),
        "designed": art["design.md"] is not None,
        "planned": art["plan.md"] is not None and art["tasks.md"] is not None,
        "built": bool(tasks) and len(done) == len(tasks),
        "verified": verdict == "accepted",
        "released": art["asbuilt.md"] is not None and re.search(r"(?m)^\s*(?:[-*]\s*)?\**Released\**\s*:\s*\S", art["asbuilt.md"]) is not None,
    }
    optional = {"researched", "architected", "designed"} | ({"planned"} if size == "S" else set())
    order = ["intaken", "specified", "researched", "architected", "designed", "planned", "built", "verified", "released"]
    gate_of = {s: (g, f) for s, g, f in GATES}
    stage, status, gate, wfile = "", "READY", "", ""
    for i, s in enumerate(order):
        if not cond[s]:
            if s in optional:
                continue
            break
        stage = s
        if s in gate_of:
            g, f = gate_of[s]
            if gates_cfg.get(g, False) and not approved(art[f]):
                status, gate, wfile = "WAITING_FOR_APPROVAL", g, f
                break
    later = []
    if status == "WAITING_FOR_APPROVAL":
        idx = order.index(stage)
        later = [s for s in order[idx + 1:] if cond[s]]
    if not stage:
        status = "EMPTY"
    elif status == "READY":
        if art["questions.md"] is not None and (art["spec.md"] is None or
                                                os.path.getmtime(os.path.join(d, "questions.md")) > os.path.getmtime(os.path.join(d, "spec.md"))):
            status = "WAITING_FOR_ANSWER"
            wfile = "questions.md"
        elif blocked_task:
            status, wfile = "BLOCKED", f"tasks.md ({blocked_task})"
        elif verdict == "rework":
            status, wfile = "REWORK", "acceptance.md"
        elif verdict == "design-defect":
            status, wfile = "DESIGN_DEFECT", "acceptance.md"
        elif stage == "released":
            status = "RELEASED"
    cur = load_json(os.path.join(root, ".team", "current.json"), {}) or {}
    st = dict(id=fid, title=title_of(fid, art["intake.md"], art["spec.md"]), playbook=playbook or "—",
              size=size or "—", mode=mode or "—", stage=stage or "—", status=status, gate=gate,
              waiting_file=f"docs/team/features/{fid}/{wfile}" if wfile else "",
              blocked_later=later, tasks_done=len(done), tasks_total=len(tasks),
              g5_approved=approved(art["asbuilt.md"], prod=True), has_asbuilt=art["asbuilt.md"] is not None,
              active=cur.get("feature") == fid,
              gates=[g for g in ("G1_spec", "G2_arch", "G2b_design", "G3_plan", "G4_uat", "G5_prod") if gates_cfg.get(g)])
    st["next"] = next_cmd(st, cond)
    return st


def next_cmd(st, cond):
    fid, s, pb, size = st["id"], st["stage"], st["playbook"], st["size"]
    if st["status"] == "WAITING_FOR_APPROVAL":
        return f"Duyệt {st['waiting_file']} ({st['gate']}): thêm `Approved-by: <tên> <YYYY-MM-DD>`, rồi /team:run {fid}"
    if st["status"] == "WAITING_FOR_ANSWER":
        return f"Trả lời {st['waiting_file']}, rồi /team:run {fid}"
    if st["status"] == "BLOCKED":
        return f"Gỡ chặn {st['waiting_file']}, rồi /team:build {fid}"
    if st["status"] == "REWORK":
        return f"/team:build {fid}"
    if st["status"] == "DESIGN_DEFECT":
        return f"/team:design {fid}"
    if s == "—":
        return f"/team:intake (chưa có intake.md cho {fid})"
    if s == "intaken":
        return {"bug-fix": f"/team:build {fid}", "hotfix": f"/team:build {fid}",
                "refactor": f"/team:design {fid} --short", "dependency-upgrade": f"/team:research {fid}",
                "integration": f"/team:research {fid}", "spike": f"/team:research {fid}",
                "ci-fix": "/team:ci fix", "change-request": f"/team:analyze {fid} --amend",
                "docs-only": f"team-leader giao writer (playbook docs-only), rồi /team:pr {fid}"}.get(pb, f"/team:analyze {fid}")
    if s == "specified":
        if not cond["researched"] and pb in ("integration", "dependency-upgrade", "new-project"):
            return f"/team:research {fid}"
        if size == "S" or pb in ("bug-fix", "hotfix"):
            return f"/team:build {fid}"
        if size == "L" and not cond["architected"]:
            return f"/team:architect {fid}"
        if pb == "client-docs":
            return f"team-leader giao writer (playbook client-docs), rồi /team:pr {fid}"
        return f"/team:design {fid}"
    if s == "researched":
        if pb == "spike":
            return "Xong spike: đọc research.md; đề xuất ADR nếu cần"
        if pb == "dependency-upgrade":
            return f"/team:plan {fid}"
        if size == "L" or pb in ("integration", "new-project"):
            return f"/team:architect {fid}"
        return f"/team:design {fid}"
    if s == "architected":
        return f"/team:design {fid}"
    if s == "designed":
        return f"/team:clean <kind> (playbook refactor)" if pb == "refactor" else f"/team:plan {fid}"
    if s == "planned":
        return f"/team:build {fid}"
    if s == "built":
        return f"/team:verify {fid}"
    if s == "verified":
        if not st["has_asbuilt"]:
            return f"/team:asbuilt {fid}"
        if not st["g5_approved"]:
            return f"/team:pr {fid}, rồi /team:release {fid} (staging); prod cần `Approved-by-prod:` trong asbuilt.md"
        return f"/team:release {fid} prod"
    if s == "released":
        return "Đã phát hành — không còn việc."
    return f"/team:run {fid}"


def features(root):
    base = os.path.join(root, "docs", "team", "features")
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)) and ID_RE.match(d))


def waiting_lines(st):
    if st["status"] == "WAITING_FOR_APPROVAL":
        extra = f" (artifact sau đã có nhưng bị chặn: {', '.join(st['blocked_later'])})" if st["blocked_later"] else ""
        return [f"Chờ người: duyệt {st['gate']} — {st['waiting_file']}{extra}"]
    if st["status"] in ("WAITING_FOR_ANSWER", "BLOCKED", "DESIGN_DEFECT", "REWORK"):
        return [f"Chờ người: {st['status']} — {st['waiting_file']}"]
    return []


def table(rows):
    head = ["ID", "Tiêu đề", "Playbook", "Cỡ", "Cổng áp dụng", "Giai đoạn", "Trạng thái", "Tiếp theo"]
    body = [[r["id"], r["title"][:40], r["playbook"], r["size"], ",".join(g.split("_")[0] for g in r["gates"]) or "—", r["stage"],
             r["status"] + (f" {r['gate']}" if r["gate"] else ""), r["next"]] for r in rows]
    widths = [max(len(str(x)) for x in col) for col in zip(head, *body)] if body else [len(h) for h in head]
    fmt = "  ".join("{:<%d}" % w for w in widths[:-1]) + "  {}"
    return "\n".join([fmt.format(*head), fmt.format(*["-" * w for w in widths])] + [fmt.format(*b) for b in body])


def runs(root):
    out = []
    path = os.path.join(root, "docs", "team", "metrics", "runs.jsonl")
    for line in (read(path) or "").split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def median(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return statistics.median(xs) if xs else None


REJECT = {"request-changes", "rework", "design-defect", "rejected", "DESIGN_CONFLICT", "BLOCKED"}


def aggregate(rs):
    groups = {}
    for r in rs:
        for kind in ("agent", "skill"):
            name = r.get(kind)
            if not name:
                continue
            key = (f"{kind}:{name}", r.get("size") or "?")
            groups.setdefault(key, []).append(r)
    out = []
    for (subject, size), items in sorted(groups.items()):
        out.append(dict(subject=subject, size=size, calls=len(items),
                        median_turns=median([i.get("turns") for i in items]),
                        median_duration_s=median([i.get("duration_s") for i in items]),
                        rework=sum(1 for i in items if (i.get("rework_round") or 0) > 0),
                        rejections=sum(1 for i in items if i.get("result") in REJECT),
                        std_violations=sum(int(i.get("std_violations") or 0) for i in items),
                        human_interventions=sum(int(i.get("human_interventions") or 0) for i in items)))
    return out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    sub, rest = argv[0], argv[1:]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    flags, pos, i = set(), [], 0
    while i < len(rest):
        if rest[i] == "--root" and i + 1 < len(rest):
            root, i = rest[i + 1], i + 2
            continue
        (flags.add if rest[i].startswith("--") else pos.append)(rest[i])
        i += 1
    root = os.path.abspath(root)
    as_json = "--json" in flags
    cfg = config(root)
    if sub in ("status", "next"):
        ids = pos or features(root)
        if sub == "next" and not pos:
            cur = load_json(os.path.join(root, ".team", "current.json"), {}) or {}
            ids = [cur["feature"]] if cur.get("feature") else []
        rows = [feature_state(root, f, cfg) for f in ids]
        if sub == "next":
            if not rows:
                print("/team:intake \"<yêu cầu>\"")
                return 0
            print(json.dumps({"id": rows[0]["id"], "next": rows[0]["next"]}, ensure_ascii=False) if as_json else rows[0]["next"])
            return 0
        if as_json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            return 0
        if "--waiting" in flags:
            for r in rows:
                for l in waiting_lines(r):
                    print(l)
            return 0
        if not rows:
            print("team: chưa có feature nào — bắt đầu bằng /team:intake \"<yêu cầu>\".")
            return 0
        if "--brief" in flags:
            for r in rows[:5]:
                print(f"team: {r['id']} · {r['stage']} · {r['status']}{(' ' + r['gate']) if r['gate'] else ''} · cổng áp dụng {','.join(g.split('_')[0] for g in r['gates']) or '—'} → {r['next']}")
            return 0
        print(table(rows))
        lines = [l for r in rows for l in waiting_lines(r)]
        if lines:
            print()
            print("\n".join(lines))
        return 0
    if sub in ("metrics", "scorecard"):
        agg = aggregate(runs(root))
        if sub == "scorecard":
            rs = runs(root)
            card = {"generated_from": max((r.get("ts", "") for r in rs), default=""), "rows": agg}
            path = os.path.join(root, "docs", "team", "metrics", "scorecard.json")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(card, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
            print(json.dumps(card, ensure_ascii=False, indent=2) if as_json else f"wrote {os.path.relpath(path, root)} ({len(agg)} rows)")
            return 0
        if as_json:
            print(json.dumps(agg, ensure_ascii=False, indent=2))
            return 0
        print("| Đối tượng | Cỡ | Lần gọi | Lượt (trung vị) | Thời gian s (trung vị) | Rework | Bị từ chối |")
        print("|---|---|---|---|---|---|---|")
        for a in agg:
            print(f"| {a['subject']} | {a['size']} | {a['calls']} | {a['median_turns']} | {a['median_duration_s']} | {a['rework']} | {a['rejections']} |")
        return 0
    print(f"team.py: unknown subcommand {sub}", file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
