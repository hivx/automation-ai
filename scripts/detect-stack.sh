#!/usr/bin/env bash
# detect-stack.sh — takeover tier T0: repository metadata as JSON, without reading file contents, without an LLM.
# Default: manifests, languages by file count, linter/formatter config files, CI files, root directories,
#   default branch, line counts of CLAUDE.md/AGENTS.md (ai_files). --deep adds: 90-day commits, 10 hot paths, author count, TODO/FIXME count,
#   test skip-marker counts (from the profile's test.skip_markers; without a profile, merged from the kit's profiles/),
#   unmerged branches, latest tags.
# Usage: detect-stack.sh [--root DIR] [--deep] ; detect-stack.sh --help
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
[[ ${1:-} == --help || ${1:-} == -h ]] && { show_help "$0"; exit 0; }
team_init "$@"
deep=0; for a in "$@"; do [[ $a == --deep ]] && deep=1; done
cd "$TEAM_ROOT" || exit 1
DEEP=$deep KIT_DIR="$KIT_DIR" python3 -I - <<'PY'
import collections, glob, json, os, re, subprocess

def git(*a):
    try:
        r = subprocess.run(["git", *a], capture_output=True, text=True, timeout=60)
        return r.stdout if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""

files = [f for f in git("ls-files").split("\n") if f]
if not files:
    files = [os.path.relpath(os.path.join(d, n)) for d, _, ns in os.walk(".") if "/.git" not in d for n in ns]
MANIFESTS = ["package.json", "pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "Pipfile",
             "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "pubspec.yaml", "Cargo.toml",
             "composer.json", "Gemfile", "mix.exs", "CMakeLists.txt", "Makefile", "deno.json", "*.csproj", "*.sln"]
LOCKS = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "uv.lock", "Pipfile.lock",
         "go.sum", "pubspec.lock", "Cargo.lock", "composer.lock", "Gemfile.lock"]
TOOLING = [".eslintrc*", "eslint.config.*", ".prettierrc*", "prettier.config.*", "ruff.toml", ".ruff.toml",
           ".flake8", "mypy.ini", ".pylintrc", "tox.ini", ".golangci.y*ml", "checkstyle*.xml",
           "analysis_options.yaml", ".editorconfig", "tsconfig.json", ".pre-commit-config.yaml", "biome.json"]
CI = [".github/workflows/*", ".gitlab-ci.yml", "Jenkinsfile", ".circleci/config.yml", "azure-pipelines.yml",
      "bitbucket-pipelines.yml", ".travis.yml"]
EXT_LANG = {".py": "python", ".ts": "typescript", ".tsx": "typescript", ".js": "javascript", ".jsx": "javascript",
            ".mjs": "javascript", ".go": "go", ".java": "java", ".kt": "kotlin", ".dart": "dart", ".rs": "rust",
            ".rb": "ruby", ".php": "php", ".cs": "csharp", ".swift": "swift", ".c": "c", ".h": "c", ".cpp": "cpp",
            ".scala": "scala", ".ex": "elixir", ".sql": "sql", ".sh": "shell", ".vue": "vue", ".svelte": "svelte"}

def match(patterns):
    out = []
    for f in files:
        base = os.path.basename(f)
        for p in patterns:
            if ("/" in p and glob.fnmatch.fnmatch(f, p)) or glob.fnmatch.fnmatch(base, p):
                out.append(f)
                break
    return sorted(out)

langs = collections.Counter(EXT_LANG[os.path.splitext(f)[1]] for f in files if os.path.splitext(f)[1] in EXT_LANG)
head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD").strip().replace("origin/", "")
current = git("rev-parse", "--abbrev-ref", "HEAD").strip()
result = {
    "root": os.getcwd(),
    "files_tracked": len(files),
    "manifests": [f for f in match(MANIFESTS) if f.count("/") <= 2],
    "lockfiles": match(LOCKS),
    "languages": dict(langs.most_common(10)),
    "tooling_configs": match(TOOLING),
    "ci_files": match(CI),
    "root_dirs": sorted({f.split("/", 1)[0] for f in files if "/" in f}),
    "default_branch": head or current or None,
    "current_branch": current or None,
    # K-08: the machine counts lines of AI instruction files (LLMs often miscount)
    "ai_files": {f: sum(1 for _ in open(f, encoding="utf-8", errors="replace"))
                 for f in ("CLAUDE.md", "AGENTS.md", ".claude/CLAUDE.md", "CLAUDE.local.md") if os.path.isfile(f)},
}
if os.environ.get("DEEP") == "1":
    since = "--since=90.days"
    hot = collections.Counter(p for p in git("log", since, "--name-only", "--format=").split("\n") if p)
    authors = {l.strip() for l in git("log", since, "--format=%ae").split("\n") if l.strip()}
    todo = sum(int(l.rsplit(":", 1)[1]) for l in git("grep", "-I", "-c", "-E", r"\b(TODO|FIXME)\b").split("\n")
               if ":" in l and l.rsplit(":", 1)[1].isdigit())
    markers = set()
    prof = os.path.join(".team", "profile.json")
    sources = [prof] if os.path.isfile(prof) else glob.glob(os.path.join(os.environ["KIT_DIR"], "profiles", "*.json"))
    for s in sources:
        try:
            markers.update(json.load(open(s, encoding="utf-8")).get("test", {}).get("skip_markers", []) or [])
        except (OSError, ValueError):
            pass
    skip_counts = {}
    for m in sorted(markers):
        out = git("grep", "-I", "-c", "-F", m)
        n = sum(int(l.rsplit(":", 1)[1]) for l in out.split("\n") if ":" in l and l.rsplit(":", 1)[1].isdigit())
        if n:
            skip_counts[m] = n
    base = result["default_branch"] or "HEAD"
    unmerged = [b.strip().lstrip("* ").strip() for b in git("branch", "-a", "--no-merged", base).split("\n") if b.strip()]
    result["deep"] = {
        "commits_90d": int(git("rev-list", "--count", since, "HEAD").strip() or 0),
        "hot_paths": [{"path": p, "changes": n} for p, n in hot.most_common(10)],
        "authors_90d": len(authors),
        "todo_fixme": todo,
        "skip_markers": skip_counts,
        "unmerged_branches": unmerged[:30],
        "tags": [t for t in git("tag", "--sort=-creatordate").split("\n") if t][:10],
        "last_commit": git("log", "-1", "--format=%cI").strip() or None,
    }
print(json.dumps(result, ensure_ascii=False, indent=2))
PY
