#!/usr/bin/env python3
"""audit-xref.py — kiểm chéo tên và tham chiếu trong toàn bộ kit (chỉ thư viện chuẩn).

Báo (mỗi dòng `<file>: <vấn đề>`, thoát 1 nếu có):
  1. tên skill / agent / playbook / template / script được nhắc trong .md mà không tồn tại;
  2. artifact skill ghi ra mà không có template (trừ danh sách NO_TEMPLATE);
  3. template trong templates/artifacts/ mà không skill/agent nào ghi;
  4. mã STD trích trong agents/skills/workflows/templates/hooks không có trong handbook/STD.md;
  5. khóa config/profile nhắc trong scripts/skills/agents/workflows/templates không có trong schema;
  6. hook trỏ tới script không có;
  7. trang docs/ không được liên kết từ docs/00-overview.md hoặc README.md.
Dùng: scripts/audit-xref.py [--root DIR]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Artifact → template (tên file trong templates/artifacts/); None = cố ý không có template.
ARTIFACT_TEMPLATE = {
    "intake.md": "intake", "spec.md": "spec", "research.md": "research", "architecture.md": "architecture",
    "arch-impact.md": "arch-impact", "design.md": "design", "plan.md": "plan", "tasks.md": "tasks",
    "review-NN.md": "review", "acceptance.md": "acceptance", "asbuilt.md": "asbuilt", "ADR-NNN.md": "adr",
    "<date>.md": "retro", "questions.md": "question-comment", "assessment.md": "assessment",
    "ai-readiness.md": "ai-readiness", "profile-proposal.md": "profile-proposal", "debt.md": "debt",
    "open-questions.md": "open-questions", "<ID>.md": "journal-entry", "skills-registry.md": "skills-registry",
    "kit-issues.md": "kit-issues", "onboarding.md": "onboarding", "defects.md": "defects", "ci.md": "ci",
    "<agent-or-skill>.md": "proposal", "*.md": "proposal", "takeover.md": "journal-entry",
}
NO_TEMPLATE = {"diff.patch", "pr-body.md", "feedback.jsonl", "runs.jsonl", "sessions.jsonl", "scorecard.json",
               "CHANGELOG.md", "README.md", "CLAUDE.md", "plan.md@session", "<id>.md", "<topic>@<version>.md",
               "profile.json", "config.json", "current.json", "settings.json", "SKILL.md", "tests.md",
               "<name>.md", "<name>.tests.md", "explore", "<slug>.md"}
TEXT_DIRS = ["agents", "skills", "workflows", "handbook", "docs", "templates", "evals"]
TOP_FILES = ["README.md", "CLAUDE.md"]
EXTS = (".md", ".json", ".yml", ".tmpl", ".sh", ".py")


def walk(root, dirs, exts=(".md",)):
    for d in dirs:
        base = os.path.join(root, d)
        for dp, _, names in os.walk(base):
            if "/out" in dp.replace(os.sep, "/"):
                continue
            for n in sorted(names):
                if n.endswith(exts):
                    yield os.path.join(dp, n)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def rel(root, p):
    return os.path.relpath(p, root)


def schema_paths(schema, prefix=""):
    out = set()
    for k, v in (schema.get("properties") or {}).items():
        path = f"{prefix}{k}"
        out.add(path)
        if isinstance(v, dict):
            out |= schema_paths(v, path + ".")
    return out


def section(text, title):
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    root = os.path.abspath(argv[argv.index("--root") + 1]) if "--root" in argv else ROOT
    problems = []
    say = lambda f, msg: problems.append(f"{rel(root, f) if os.path.isabs(f) else f}: {msg}")

    skills = {d for d in os.listdir(os.path.join(root, "skills")) if os.path.isdir(os.path.join(root, "skills", d))}
    agents = {f[:-3] for f in os.listdir(os.path.join(root, "agents")) if f.endswith(".md")}
    playbooks = {f[:-3] for f in os.listdir(os.path.join(root, "workflows")) if f.endswith(".md") and f != "README.md"}
    templates = {f[:-3] for f in os.listdir(os.path.join(root, "templates", "artifacts")) if f.endswith(".md")}
    std_text = read(os.path.join(root, "handbook", "STD.md"))
    std_codes = set(re.findall(r"^\|\s*(STD-[A-Z]+-\d+)\s*\|", std_text, re.M))

    files = list(walk(root, TEXT_DIRS, EXTS)) + [os.path.join(root, f) for f in TOP_FILES]
    md_files = [f for f in files if f.endswith((".md", ".tmpl"))]

    # 1. tên không tồn tại
    for f in md_files:
        t = read(f)
        for m in re.finditer(r"(?<![\w/-])team:([a-z][a-z-]*)\b", t):
            name = m.group(1)
            if name in ("intake", "run", "ask", "decide", "needs-answer", "size", "start", "end") or name.startswith("size"):
                continue  # nhãn GitHub
            if name not in agents and name not in skills:
                say(f, f"`team:{name}` không phải agent hay skill")
        for m in re.finditer(r"[Pp]laybook\s+`([a-z][a-z-]*)`", t):
            if m.group(1) not in playbooks:
                say(f, f"playbook `{m.group(1)}` không có trong workflows/")
        for m in re.finditer(r"templates/artifacts/([a-z][a-z-]*)\.md", t):
            if m.group(1) not in templates:
                say(f, f"template {m.group(1)}.md không tồn tại")
        for m in re.finditer(r"(?<![\w.-])scripts/([a-z][a-z0-9-]*\.(?:sh|py))", t):
            if not os.path.isfile(os.path.join(root, "scripts", m.group(1))):
                say(f, f"script scripts/{m.group(1)} không tồn tại")

    # 2–3. artifact ↔ template
    written = set()
    for sk in sorted(skills):
        p = os.path.join(root, "skills", sk, "SKILL.md")
        if not os.path.isfile(p):
            continue
        t = read(p)
        written |= set(re.findall(r"templates/artifacts/([a-z][a-z-]*)\.md", t))
        for path in re.findall(r"`([^`\s]+)`", section(t, "Đầu ra")):
            base = path.rstrip("/").split("/")[-1]
            if not re.search(r"\.(md|json|jsonl|patch)$", base):
                continue
            if base in NO_TEMPLATE or path.startswith((".claude/", ".team/")) or base.startswith("team/"):
                continue
            tmpl = ARTIFACT_TEMPLATE.get(base)
            if tmpl is None:
                say(p, f"artifact `{path}` không có template (thêm template hoặc vào NO_TEMPLATE)")
            elif tmpl not in templates:
                say(p, f"artifact `{path}` cần templates/artifacts/{tmpl}.md")
            else:
                written.add(tmpl)
    for f in walk(root, ["agents"]):
        written |= set(re.findall(r"templates/artifacts/([a-z][a-z-]*)\.md", read(f)))
    for t in sorted(templates - written):
        say(f"templates/artifacts/{t}.md", "không skill hay agent nào ghi template này")

    # 4. mã STD
    for f in walk(root, ["agents", "skills", "workflows", "templates", "hooks"], EXTS):
        for code in set(re.findall(r"STD-[A-Z]+-\d+", read(f))):
            if code not in std_codes:
                say(f, f"{code} không có trong handbook/STD.md")

    # 5. khóa config/profile
    prof = schema_paths(json.load(open(os.path.join(root, "templates", "schemas", "profile.schema.json"))))
    conf = schema_paths(json.load(open(os.path.join(root, "templates", "schemas", "config.schema.json"))))
    valid = prof | conf
    ns = r"(?:cmd|structure|naming|test|ci|deploy|plugins|limits|gates|models|approvers|journal|memory|channels)"
    key_re = re.compile(rf"(?<![\w/.-])\.?({ns}\.[A-Za-z_][A-Za-z0-9_]*)(?![\w-]*\.(?:md|yml|yaml|json|sh|py|txt)\b)")
    cfg_re = re.compile(r"(?<![\w-])config\.([a-z_][a-z0-9_]*)\b(?![\w-]*\.(?:md|yml|yaml|json|sh|py|txt)\b)(?!\.ya?ml)")
    for f in list(walk(root, ["scripts", "skills", "agents", "workflows", "templates", "hooks"], EXTS)):
        if f.endswith("audit-xref.py") or "/tests/" in f:
            continue
        t = read(f)
        for m in key_re.finditer(t):
            key = m.group(1)
            if key.endswith("_") or key not in valid and not any(v.startswith(key + ".") for v in valid):
                if key not in valid:
                    say(f, f"khóa `{key}` không có trong schema profile/config")
        for m in cfg_re.finditer(t):
            if m.group(1) not in conf and m.group(1) not in ("json", "schema", "yml", "yaml", "md", "toml"):
                say(f, f"khóa `config.{m.group(1)}` không có trong config.schema.json")

    # 6. hook → script
    hooks = json.load(open(os.path.join(root, "hooks", "hooks.json")))
    for grp in hooks.get("hooks", {}).values():
        for g in grp:
            for h in g.get("hooks", []):
                for s in re.findall(r"scripts/([A-Za-z0-9_.-]+)", h.get("command", "")):
                    if not os.path.isfile(os.path.join(root, "scripts", s)):
                        say("hooks/hooks.json", f"script scripts/{s} không tồn tại")

    # 7. docs được liên kết
    index = read(os.path.join(root, "docs", "00-overview.md")) + read(os.path.join(root, "README.md"))
    for f in walk(root, ["docs"]):
        r = rel(root, f)
        if r == "docs/00-overview.md":
            continue
        name = os.path.basename(f)
        if name not in index and r not in index:
            say(f, "không được liên kết từ docs/00-overview.md hoặc README.md")

    for p in sorted(set(problems)):
        print(p)
    print(f"audit-xref: {len(set(problems))} vấn đề")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
