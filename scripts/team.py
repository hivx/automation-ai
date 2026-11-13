#!/usr/bin/env python3
"""team.py — team state computed from the artifacts (standard library only). No stored pointer.

Subcommands:
  status [<ID>] [--brief] [--waiting]   stage table per feature + "Waiting on the human" lines
  next <ID>                             the next skill command
  wave                                  the features the team-leader can dispatch together now, one agent per
                                        feature, capped by limits.headcount[role] (max_parallel_dev for dev);
                                        builds whose tasks.md `files:` overlap go one at a time; each build
                                        gets its share of the team-wide dev and reviewer headcount
  metrics                               aggregate docs/team/metrics/runs.jsonl by agent/skill/size
  scorecard                             write docs/team/metrics/scorecard.json
Common flags: --root DIR (default $CLAUDE_PROJECT_DIR or the current directory), --json.

Stages (SPEC §4): intaken → specified → [researched] → [architected] → [designed] → planned
→ built → verified → released. An enabled gate without `Approved-by:` (G5: `Approved-by-prod:`) blocks
EVERY later stage, even when later artifacts already exist. Size S skips G1, G3 (ADJ-09);
the refactor and data-migration playbooks always enable G2b (ADJ-16).
Intake labels are read in English (`Size:`, `Mode:`, `Verdict:`) and, for older projects, in Vietnamese.
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
# Vietnamese labels of pre-English projects, still accepted when reading (escaped: scripts stay English).
LEGACY_INTAKE = "ti\u1ebfp nh\u1eadn"                            # title prefix "intake"
LEGACY_REQUEST = ("Y\u00eau c\u1ea7u", "Y\u00eau c\u1ea7u g\u1ed1c")      # "Request", "Original request"
LEGACY_SIZE, LEGACY_MODE = "c\u1ee1", "ch\u1ebf \u0111\u1ed9"          # "Size", "Mode"
LEGACY_VERDICT = "ph\u00e1n quy\u1ebft"                          # "Verdict"


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
            t = re.sub(rf"(?i)^(intake|spec|{LEGACY_INTAKE})\s*[:\-—]?\s*", "", t)
            t = re.sub(rf"^{re.escape(fid)}\s*[—–:\-]?\s*", "", t).strip()
            if t and t != fid:
                return t
    req = field(intake, LEGACY_REQUEST[0], "Request", LEGACY_REQUEST[1])
    return req.strip('"“”') or "—"


GATES = [("specified", "G1_spec", "spec.md"), ("architected", "G2_arch", "arch-impact.md"),
         ("designed", "G2b_design", "design.md"), ("planned", "G3_plan", "plan.md"),
         ("verified", "G4_uat", "acceptance.md")]


NO_SPEC_PLAYBOOKS = {"bug-fix", "hotfix", "refactor", "dependency-upgrade", "spike", "ci-fix", "docs-only", "quick"}
NO_PLAN_PLAYBOOKS = {"bug-fix", "hotfix", "refactor", "quick"}
# Right-sized chains (ADJ-36): quick = one dev, done when its task is ticked; size S = acceptance inside build, no As-Built.


def feature_state(root, fid, cfg):
    d = os.path.join(root, "docs", "team", "features", fid)
    art = {n: read(os.path.join(d, n)) for n in ("intake.md", "spec.md", "research.md", "arch-impact.md",
                                                  "design.md", "plan.md", "tasks.md", "acceptance.md",
                                                  "asbuilt.md", "questions.md")}
    intake = art["intake.md"] or ""
    size_m = re.search(rf"(?i)(?:{LEGACY_SIZE}|size)\**\s*:\**\s*\**\s*([SML])\b", intake)
    size = size_m.group(1).upper() if size_m else ""
    pb_m = re.search(r"(?i)playbook\**\s*:\**\s*\[?`?([a-z][a-z-]*)", intake)
    playbook = pb_m.group(1).lower() if pb_m else ""
    mode_m = re.search(rf"(?i)(?:{LEGACY_MODE}|mode)\**\s*:\**\s*\**\s*(ask|decide)\b", intake)
    mode = mode_m.group(1).lower() if mode_m else ""
    gates_cfg = dict(cfg.get("gates") or {})
    if playbook in ("refactor", "data-migration"):
        gates_cfg["G2b_design"] = True
    if playbook == "quick":
        size = "S"
    if size == "S":
        gates_cfg["G1_spec"] = False
        gates_cfg["G3_plan"] = False
        gates_cfg["G2b_design"] = gates_cfg.get("G2b_design", False) and playbook in ("refactor", "data-migration")

    tasks = TASK.findall(art["tasks.md"] or "")
    done = [t for t in tasks if t[0].lower() == "x"]
    blocked_task = next((t[1] for t in tasks if t[0] == " " and "BLOCKED" in t[2]), None)
    verdict_m = re.search(rf"(?i)(?:verdict|{LEGACY_VERDICT})\**\s*:\**\s*\**\s*(accepted|rework|design-defect)", art["acceptance.md"] or "")
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
    if playbook in NO_SPEC_PLAYBOOKS:  # the SPEC §5 chain has no analyze (K-47)
        optional.add("specified")
    if playbook in NO_PLAN_PLAYBOOKS:  # chain without plan: one-task build / clean writes tasks.md (K-47)
        optional.add("planned")
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
        return f"Approve {st['waiting_file']} ({st['gate']}): add `Approved-by: <name> <YYYY-MM-DD>`, then /team:run {fid}"
    if st["status"] == "WAITING_FOR_ANSWER":
        return f"Answer {st['waiting_file']}, then /team:run {fid}"
    if st["status"] == "BLOCKED":
        return f"Unblock {st['waiting_file']}, then /team:build {fid}"
    if st["status"] == "REWORK":
        return f"/team:build {fid}"
    if st["status"] == "DESIGN_DEFECT":
        return f"/team:design {fid}"
    if s == "—":
        return f"/team:intake (no intake.md yet for {fid})"
    if pb == "quick":
        if s == "built":
            return f"Done: branch team/{fid} is ready — merge it, or /team:pr {fid}"
        return f"team-leader calls one dev (playbook quick) for {fid}"
    if s == "intaken":
        return {"bug-fix": f"/team:build {fid}", "hotfix": f"/team:build {fid}",
                "refactor": f"/team:design {fid} --short", "dependency-upgrade": f"/team:research {fid}",
                "integration": f"/team:research {fid}", "spike": f"/team:research {fid}",
                "ci-fix": "/team:ci fix", "change-request": f"/team:analyze {fid} --amend",
                "docs-only": f"team-leader hands off to writer (playbook docs-only), then /team:pr {fid}"}.get(pb, f"/team:analyze {fid}")
    if s == "specified":
        if not cond["researched"] and pb in ("integration", "dependency-upgrade", "new-project"):
            return f"/team:research {fid}"
        if size == "S" or pb in ("bug-fix", "hotfix"):
            return f"/team:build {fid}"
        if size == "L" and not cond["architected"]:
            return f"/team:architect {fid}"
        if pb == "client-docs":
            return f"team-leader hands off to writer (playbook client-docs), then /team:pr {fid}"
        return f"/team:design {fid}"
    if s == "researched":
        if pb == "spike":
            return "Spike done: read research.md; propose an ADR if needed"
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
        if size == "S" and not st["has_asbuilt"]:  # size S: no As-Built; pr writes a short body itself
            return f"/team:pr {fid}, then /team:release {fid}"
        if not st["has_asbuilt"]:
            return f"/team:asbuilt {fid}"
        if not st["g5_approved"]:
            return f"/team:pr {fid}, then /team:release {fid} (staging); prod needs `Approved-by-prod:` in asbuilt.md"
        return f"/team:release {fid} prod"
    if s == "released":
        return "Released — nothing left to do."
    return f"/team:run {fid}"


HOLD = {"WAITING_FOR_APPROVAL", "WAITING_FOR_ANSWER", "BLOCKED", "DESIGN_DEFECT", "RELEASED"}
NEXT_CMD = re.compile(r"^/team:([a-z][a-z-]*)\s+(\S+)([^,]*)")
FILES = re.compile(r"files:\s*([^—\n]+)")


def headcount(cfg):
    """limits.headcount per role (default 1); dev falls back to limits.max_parallel_dev."""
    lim = cfg.get("limits") or {}
    hc = dict(lim.get("headcount") or {})
    hc.setdefault("dev", lim.get("max_parallel_dev", 1))
    hc.setdefault("reviewer", hc["dev"])
    return {k: v for k, v in hc.items() if isinstance(v, int) and v >= 1}


def skill_meta(name):
    """(role, human_only) of a kit skill, read from its frontmatter."""
    paths = [os.path.join(kit_dir(), "skills", name, "SKILL.md"),  # plugin
             os.path.join(os.path.dirname(kit_dir()), "skills", name, "SKILL.md")]  # local install: .claude/skills
    text = header(next((t for t in map(read, paths) if t), ""), 15)
    m = re.search(r"(?m)^agent:\s*(?:team:)?([a-z-]+)", text)
    return (m.group(1) if m else "team-leader"), bool(re.search(r"(?m)^disable-model-invocation:\s*true", text))


def task_files(root, fid):
    out = set()
    for m in FILES.finditer(read(os.path.join(root, "docs", "team", "features", fid, "tasks.md")) or ""):
        out |= {f.strip().strip("`") for f in m.group(1).split(",") if f.strip() and "<" not in f}
    return out


def wave(root, cfg, rows):
    """Pick what can run at the same time: per role up to headcount, builds with disjoint files."""
    hc, used, picked, held, busy = headcount(cfg), {}, [], [], set()
    for r in rows:
        m = NEXT_CMD.match(r["next"])
        if r["status"] in HOLD or not m or m.group(2) != r["id"] or "<" in r["next"]:
            reason = r["status"] if r["status"] in HOLD else ("team-leader step" if r["next"].startswith("team-leader")
                                                                else "done" if r["next"].startswith("Done") else "needs the human")
            held.append(dict(id=r["id"], reason=reason, next=r["next"]))
            continue
        skill = m.group(1)
        role, human_only = skill_meta(skill)
        if human_only:
            held.append(dict(id=r["id"], reason="human-only skill", next=r["next"]))
            continue
        if used.get(role, 0) >= hc.get(role, 1):
            held.append(dict(id=r["id"], reason=f"headcount {role}={hc.get(role, 1)} in use", next=r["next"]))
            continue
        files = task_files(root, r["id"]) if skill == "build" else set()
        if files & busy:
            held.append(dict(id=r["id"], reason="shares files with a build in this wave: " + ", ".join(sorted(files & busy)[:3]),
                             next=r["next"]))
            continue
        busy |= files
        used[role] = used.get(role, 0) + 1
        picked.append(dict(id=r["id"], skill=skill, role=role, args=(r["id"] + m.group(3)).strip(), command=m.group(0).strip()))
    builds = [d for d in picked if d["role"] == "tech-lead" and d["skill"] == "build"]
    for d in builds:  # dev and reviewer headcount is team-wide: split it between the builds of this wave
        d["devs"] = max(1, hc.get("dev", 1) // len(builds))
        d["reviewers"] = max(1, hc.get("reviewer", 1) // len(builds))
    return dict(dispatch=picked, held=held, headcount=hc)


def features(root):
    base = os.path.join(root, "docs", "team", "features")
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)) and ID_RE.match(d))


def waiting_lines(st):
    if st["status"] == "WAITING_FOR_APPROVAL":
        extra = f" (later artifacts exist but are blocked: {', '.join(st['blocked_later'])})" if st["blocked_later"] else ""
        return [f"Waiting on the human: approve {st['gate']} — {st['waiting_file']}{extra}"]
    if st["status"] in ("WAITING_FOR_ANSWER", "BLOCKED", "DESIGN_DEFECT", "REWORK"):
        return [f"Waiting on the human: {st['status']} — {st['waiting_file']}"]
    return []


def table(rows):
    head = ["ID", "Title", "Playbook", "Size", "Applicable gates", "Stage", "Tasks", "Status", "Next"]
    body = [[r["id"], r["title"][:40], r["playbook"], r["size"], ",".join(g.split("_")[0] for g in r["gates"]) or "—", r["stage"],
             f"{r.get('tasks_done', 0)}/{r['tasks_total']}" if r.get("tasks_total") else "—",
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
    return last_per_agent(out)


def last_per_agent(rows):
    """SubagentStop can fire many times for one agent (each time an agent it called stops); its rows repeat with a
    growing duration. Keep the last row per agent_id, in order; rows without agent_id are kept."""
    last = {r["agent_id"]: i for i, r in enumerate(rows) if isinstance(r, dict) and r.get("agent_id")}
    return [r for i, r in enumerate(rows) if not (isinstance(r, dict) and r.get("agent_id")) or last[r["agent_id"]] == i]


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
    if sub == "wave":
        w = wave(root, cfg, [feature_state(root, f, cfg) for f in (pos or features(root))])
        if as_json:
            print(json.dumps(w, ensure_ascii=False, indent=2))
            return 0
        for d in w["dispatch"]:
            share = f"  devs={d['devs']} reviewers={d['reviewers']}" if "devs" in d else ""
            print(f"dispatch  {d['id']}  {d['role']}  {d['command']}{share}")
        for h in w["held"]:
            print(f"hold      {h['id']}  {h['reason']}  ({h['next']})")
        if not w["dispatch"]:
            print("wave: nothing to dispatch")
        return 0
    if sub in ("status", "next"):
        ids = pos or features(root)
        if sub == "next" and not pos:
            cur = load_json(os.path.join(root, ".team", "current.json"), {}) or {}
            ids = [cur["feature"]] if cur.get("feature") else []
        rows = [feature_state(root, f, cfg) for f in ids]
        if sub == "next":
            if not rows:
                print("/team:intake \"<request>\"")
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
            print("team: no features yet — start with /team:intake \"<request>\".")
            return 0
        if "--brief" in flags:
            for r in rows[:5]:
                print(f"team: {r['id']} · {r['stage']} · {r['status']}{(' ' + r['gate']) if r['gate'] else ''} · applicable gates {','.join(g.split('_')[0] for g in r['gates']) or '—'} → {r['next']}")
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
        print("| Subject | Size | Calls | Turns (median) | Duration s (median) | Rework | Rejected |")
        print("|---|---|---|---|---|---|---|")
        for a in agg:
            print(f"| {a['subject']} | {a['size']} | {a['calls']} | {a['median_turns']} | {a['median_duration_s']} | {a['rework']} | {a['rejections']} |")
        return 0
    print(f"team.py: unknown subcommand {sub}", file=sys.stderr)
    return 64


class _LocalPrefix:
    """Local install (kit inside .claude/team-kit): commands are /team-<name> instead of /team:<name>."""
    def __init__(self, stream):
        self.stream = stream

    def write(self, s):
        return self.stream.write(s.replace("/team:", "/team-"))

    def flush(self):
        return self.stream.flush()


if __name__ == "__main__":
    if kit_dir().replace(os.sep, "/").endswith("/.claude/team-kit"):
        sys.stdout = _LocalPrefix(sys.stdout)
    sys.exit(main(sys.argv[1:]))
