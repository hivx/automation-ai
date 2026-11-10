#!/usr/bin/env python3
"""check-lang.py — language-zone checks for the kit (stdlib only).

1. Anchors: no translated form of a machine-read anchor (scripts/anchors.txt) appears in any checked file.
2. Zones: Vietnamese prose (Vietnamese diacritics) appears only in the allowlist:
   the guide file named in scripts/vi-guide.conf, scripts/vi-strings.json, templates/artifacts/vi/**,
   docs/requirements/**, docs/acceptance/**, and CHANGELOG.md entries for versions up to 0.3.0.
Files checked: git-tracked and untracked-not-ignored text files, minus the owner's input files (automation-ai_*.md).
Usage: check-lang.py [--anchors-only | --zones-only] ; exit 0 when clean, 1 otherwise.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VI = re.compile("[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
                "ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]")
TEXT_EXT = (".md", ".sh", ".py", ".json", ".jsonl", ".yml", ".yaml", ".tmpl", ".txt", ".conf")
HISTORY = ("docs/requirements/", "docs/acceptance/")
OWNER_INPUT = re.compile(r"^automation-ai_.*\.md$")
SELF = ("scripts/check-lang.py", "scripts/anchors.txt")


def guide_file():
    try:
        for line in open(os.path.join(ROOT, "scripts", "vi-guide.conf"), encoding="utf-8"):
            if line.startswith("GUIDE_FILE="):
                return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return "GUIDE-VI.md"


def files():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()
    return [f for f in out if f.endswith(TEXT_EXT) and os.path.isfile(os.path.join(ROOT, f))
            and not OWNER_INPUT.match(f) and "/out/" not in f]


def anchors():
    pairs = []
    for line in open(os.path.join(ROOT, "scripts", "anchors.txt"), encoding="utf-8"):
        if line.startswith("#") or "\t" not in line:
            continue
        anchor, forms = line.rstrip("\n").split("\t", 1)
        pairs += [(anchor, f.strip()) for f in forms.split(" | ") if f.strip()]
    return pairs


def changelog_allowed_from(text):
    m = re.search(r"(?m)^## \[0\.3\.0\]", text)
    return text[:m.start()].count("\n") if m else None


def main(argv):
    do_anchors = "--zones-only" not in argv
    do_zones = "--anchors-only" not in argv
    guide = guide_file()
    allow = {guide, "scripts/vi-strings.json"}
    bad_anchor, bad_zone = [], []
    pairs = anchors()
    for f in files():
        text = open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read()
        lines = text.split("\n")
        hist = f.startswith(HISTORY)
        if do_anchors and not hist and f not in SELF:
            for n, line in enumerate(lines, 1):
                for anchor, form in pairs:
                    if form in line and not (f == "CHANGELOG.md" and changelog_allowed_from(text) is not None
                                             and n > changelog_allowed_from(text)):
                        bad_anchor.append(f"{f}:{n}: translated anchor '{form}' (use '{anchor}')")
        if do_zones and not hist and f not in allow and not f.startswith("templates/artifacts/vi/") and f not in SELF:
            start = changelog_allowed_from(text) if f == "CHANGELOG.md" else None
            for n, line in enumerate(lines, 1):
                if start is not None and n > start:
                    break
                if VI.search(line):
                    bad_zone.append(f"{f}:{n}: Vietnamese text outside the allowlist")
    for msg in bad_anchor:
        print("FAIL anchor:", msg)
    files_vi = sorted({m.split(":", 1)[0] for m in bad_zone})
    for f in files_vi:
        n = sum(1 for m in bad_zone if m.startswith(f + ":"))
        first = next(m for m in bad_zone if m.startswith(f + ":"))
        print(f"FAIL zone: {first} ({n} lines)")
    print(f"check-lang: {len(bad_anchor)} translated anchors, {len(bad_zone)} Vietnamese lines in {len(files_vi)} files outside the allowlist")
    return 1 if bad_anchor or bad_zone else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
