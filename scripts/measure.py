#!/usr/bin/env python3
"""measure.py — measures agent/skill effectiveness without an LLM (standard library only). Deterministic output.

Inputs: docs/team/metrics/runs.jsonl, feedback.jsonl, scorecard.json (fallback when runs are missing).
Per (subject, size): median duration, median turns, rework rate, rejection rate, STD violations,
human interventions, tokens (with --logs). Effectiveness score = weighted z-score against the median of
the same size (MAD); higher = better. Trend = sign of the duration slope over the last N runs. Anomaly =
more than 2 MAD from the same-size median. "Attention" ranking: anomalies first, then low score, then low feedback.

Usage: measure.py [--root DIR] [--runs F] [--feedback F] [--scorecard F] [--since YYYY-MM-DD]
                  [--last N] [--logs DIR] [--json]
"""
import json
import os
import statistics
import sys

# Weights: for every metric, LOWER is better.
WEIGHTS = {"duration_s": 1.0, "turns": 1.0, "rework_rate": 2.0, "rejection_rate": 2.0,
           "std_violations": 1.5, "human_interventions": 1.5, "tokens": 0.5}
REJECT = {"request-changes", "rework", "design-defect", "rejected", "DESIGN_CONFLICT", "BLOCKED"}
MAD_K = 2.0


def read_jsonl(path):
    out = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        continue
    except OSError:
        pass
    return out


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def median(xs):
    xs = [x for x in xs if num(x) is not None]
    return statistics.median(xs) if xs else None


def mad(xs, med=None):
    xs = [x for x in xs if num(x) is not None]
    if not xs:
        return None
    med = statistics.median(xs) if med is None else med
    return statistics.median([abs(x - med) for x in xs])


def slope_sign(ys):
    """Sign of the least-squares slope of ys in order: 1, -1 or 0."""
    ys = [y for y in ys if num(y) is not None]
    n = len(ys)
    if n < 2:
        return 0
    mx = (n - 1) / 2
    my = sum(ys) / n
    s = sum((i - mx) * (y - my) for i, y in enumerate(ys))
    return 0 if abs(s) < 1e-9 else (1 if s > 0 else -1)


def tokens_for(run, logs):
    if not logs or not run.get("agent_id"):
        return None
    target = f"agent-{run['agent_id']}.jsonl"
    for d, _, names in os.walk(logs):
        if target in names:
            total = 0
            for rec in read_jsonl(os.path.join(d, target)):
                usage = (rec.get("message") or {}).get("usage") or {}
                for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
                    total += usage.get(k) or 0
            return total or None
    return None


def subjects(run):
    out = []
    if run.get("agent"):
        out.append(f"agent:{run['agent']}")
    if run.get("skill"):
        out.append(f"skill:{run['skill']}")
    return out


def group_runs(runs, logs=None):
    groups = {}
    for r in runs:
        for s in subjects(r):
            groups.setdefault((s, r.get("size") or "?"), []).append(r)
    rows = {}
    for key, items in groups.items():
        n = len(items)
        rows[key] = {
            "runs": n,
            "duration_s": median([i.get("duration_s") for i in items]),
            "turns": median([i.get("turns") for i in items]),
            "rework_rate": sum(1 for i in items if (num(i.get("rework_round")) or 0) > 0) / n,
            "rejection_rate": sum(1 for i in items if i.get("result") in REJECT) / n,
            "std_violations": sum(num(i.get("std_violations")) or 0 for i in items) / n,
            "human_interventions": sum(num(i.get("human_interventions")) or 0 for i in items) / n,
            "tokens": median([tokens_for(i, logs) for i in items]) if logs else None,
        }
    return rows, groups


def from_scorecard(card):
    rows = {}
    for r in (card or {}).get("rows", []):
        n = r.get("calls") or 0
        if not n:
            continue
        rows[(r["subject"], r.get("size") or "?")] = {
            "runs": n, "duration_s": r.get("median_duration_s"), "turns": r.get("median_turns"),
            "rework_rate": (r.get("rework") or 0) / n, "rejection_rate": (r.get("rejections") or 0) / n,
            "std_violations": (r.get("std_violations") or 0) / n,
            "human_interventions": (r.get("human_interventions") or 0) / n, "tokens": None}
    return rows


def score(rows):
    """Add score and anomalies to each row, against the median of the same size."""
    by_size = {}
    for (s, size), row in rows.items():
        by_size.setdefault(size, []).append(row)
    for (s, size), row in rows.items():
        peers = by_size[size]
        total, wsum, anomalies = 0.0, 0.0, []
        for m, w in WEIGHTS.items():
            v = num(row.get(m))
            vals = [num(p.get(m)) for p in peers if num(p.get(m)) is not None]
            if v is None or len(vals) < 2:
                continue
            med = statistics.median(vals)
            d = mad(vals, med)
            scale = 1.4826 * d if d else (statistics.pstdev(vals) or 1.0)
            total += w * (v - med) / scale
            wsum += w
            if d and abs(v - med) > MAD_K * d and v > med:
                anomalies.append(m)
        row["score"] = round(-total / wsum, 3) if wsum else 0.0
        row["anomalies"] = sorted(anomalies)
    return rows


def main(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    opts = {"--root": os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd(), "--last": "5"}
    flags, i = set(), 0
    while i < len(argv):
        if argv[i] in ("--root", "--runs", "--feedback", "--scorecard", "--since", "--last", "--logs") and i + 1 < len(argv):
            opts[argv[i]] = argv[i + 1]
            i += 2
        else:
            flags.add(argv[i])
            i += 1
    mdir = os.path.join(opts["--root"], "docs", "team", "metrics")
    runs = read_jsonl(opts.get("--runs") or os.path.join(mdir, "runs.jsonl"))
    feedback = read_jsonl(opts.get("--feedback") or os.path.join(mdir, "feedback.jsonl"))
    if opts.get("--since"):
        runs = [r for r in runs if str(r.get("ts", "")) >= opts["--since"]]
        feedback = [f for f in feedback if str(f.get("ts", "")) >= opts["--since"]]
    logs = os.path.expanduser(opts["--logs"]) if opts.get("--logs") else None
    rows, groups = group_runs(runs, logs)
    if not rows:
        try:
            with open(opts.get("--scorecard") or os.path.join(mdir, "scorecard.json"), encoding="utf-8") as fh:
                rows = from_scorecard(json.load(fh))
        except (OSError, ValueError):
            rows = {}
    score(rows)
    last = int(opts["--last"])
    fb = {}
    for f in feedback:
        about = f.get("about") or ""
        if num(f.get("score")) is not None:
            key = about if about.startswith(("agent:", "skill:")) else f"agent:{about}"
            fb.setdefault(key, []).append(f["score"])
    result = []
    for (s, size), row in sorted(rows.items()):
        ordered = sorted((r for r in runs if s in subjects(r) and (r.get("size") or "?") == size), key=lambda r: str(r.get("ts", "")))
        trend = slope_sign([r.get("duration_s") for r in ordered[-last:]])
        fscore = round(statistics.mean(fb[s]), 2) if s in fb else None
        notes = []
        if row["anomalies"]:
            notes.append("anomaly: " + ", ".join(row["anomalies"]))
        if trend > 0:
            notes.append("slowing down")
        if fscore is not None and fscore < 3:
            notes.append("low feedback")
        result.append(dict(subject=s, size=size, runs=row["runs"], score=row["score"], trend=trend,
                           anomalies=row["anomalies"], feedback=fscore,
                           metrics={k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()
                                    if k in WEIGHTS}, notes=notes))
    result.sort(key=lambda r: (-len(r["anomalies"]), r["score"], r["feedback"] if r["feedback"] is not None else 5, r["subject"], r["size"]))
    for n, r in enumerate(result, 1):
        r["rank"] = n
    if "--json" in flags:
        print(json.dumps({"weights": WEIGHTS, "ranking": result}, ensure_ascii=False, indent=2))
        return 0
    print("# Attention ranking\n")
    print("| # | Subject | Size | Runs | Score | Trend | Feedback | Notes |")
    print("|---|---|---|---|---|---|---|---|")
    arrow = {1: "↑ slower", -1: "↓ faster", 0: "→"}
    for r in result:
        print(f"| {r['rank']} | {r['subject']} | {r['size']} | {r['runs']} | {r['score']} | {arrow[r['trend']]} | "
              f"{r['feedback'] if r['feedback'] is not None else '—'} | {'; '.join(r['notes']) or '—'} |")
    if not result:
        print("| — | (no data yet) | | | | | | |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
