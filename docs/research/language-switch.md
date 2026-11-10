# Language switch (P9): measured effect on context size

- Date: 2026-11-10 · Claude Code 2.1.322 · before = tag `pre-p9` (`a26ca25`, Vietnamese AI-facing text) · after = the P9 tree (English AI-facing text).
- Tool: `scripts/measure-context.py` (stdlib; uses `tiktoken` when importable). Run here with `tiktoken` 0.x installed in a scratch virtualenv, not as a kit dependency.
- **Tokenizer caveat:** Claude's tokenizer is not public. The numbers below use two OpenAI BPE encodings as proxies: `o200k_base` (newer, multilingual-friendly) and `cl100k_base` (older). They bracket the likely effect but are not Claude's count. An attempt to read Claude's own counts from `claude -p` usage failed: `--bare` needs an API key, and without it the Claude Code system prompt (~58k tokens with plugins loaded) changes between calls by more than the groups being measured.

## Groups
- **always** — what every call carries: all 13 agent bodies, `skills/handbook` + `handbook/STD-short.md`, `skills/using-team`, `templates/project/claude/rules/*.tmpl` (20 files).
- **feature** — a typical feature run: always + the bodies of `analyze`, `plan`, `build`, `verify` (24 files).
- **repo** — every tracked text file (md, sh, py, json, yml, tmpl, txt), excluding eval run outputs.

## Before / after
| Group | Measure | pre-p9 | P9 | Δ |
|---|---|---|---|---|
| always | characters | 83,368 | 95,800 | +14.9% |
| always | words | 14,965 | 14,942 | −0.2% |
| always | tokens, o200k_base | 27,310 | 25,583 | **−6.3%** |
| always | tokens, cl100k_base | 35,584 | 25,722 | **−27.7%** |
| feature | characters | 117,366 | 135,996 | +15.9% |
| feature | words | 20,923 | 21,188 | +1.3% |
| feature | tokens, o200k_base | 38,268 | 36,203 | **−5.4%** |
| feature | tokens, cl100k_base | 49,799 | 36,352 | **−27.0%** |
| repo | characters | 1,072,250 | 1,278,221 | +19.2% |
| repo | words | 173,886 | 194,401 | +11.8% |
| repo | tokens, o200k_base | 340,041 | 369,489 | +8.7% |
| repo | tokens, cl100k_base | 403,352 | 390,855 | −3.1% |

## What this means — stated plainly
- **The saving is smaller than expected.** With the newer encoding the always-loaded context shrinks only 6%; with the older one 28%. Vietnamese with diacritics is not as expensive in modern multilingual tokenizers as it is in older ones.
- **Why so small:** the English bodies carry *more* content. The word-budget bands (always-loaded ≤ 400; other skills 1,200–2,500; agents 600–1,200) were set when Vietnamese was counted per syllable; a faithful English version is ~25–35% shorter in words, so the rewrite deepened steps, checkpoints and rationalization cells to stay in band (word counts almost unchanged, characters +15%). Holding the same word count in English means holding more information per file.
- **The repo grew** (+9% o200k): it now holds the Vietnamese artifact templates (`templates/artifacts/vi/`), `GUIDE-VI.md`, `scripts/vi-strings.json` and new tooling. None of that is loaded into an agent's context by default.
- Where the switch clearly helps: per-token cost on older tokenizers, consistency with Claude Code docs and the reference kits (all English), and no mixed-language prompts inside agents. Whether the always-loaded context costs fewer Claude tokens can only be settled with Claude's own counter (API `count_tokens` with an API key).

## Reproduce
```
python3 -m venv /tmp/tk && /tmp/tk/bin/pip install tiktoken
/tmp/tk/bin/python scripts/measure-context.py --ref pre-p9 [--encoding cl100k_base]
/tmp/tk/bin/python scripts/measure-context.py            [--encoding cl100k_base]
python3 scripts/measure-context.py   # without tiktoken: heuristic ceil(utf8_bytes/3.6), labelled "estimate"
```
