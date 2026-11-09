# 05 — Token và memory

Nguồn chuẩn: `SPEC.md` §9 (Memory). Trang này giải thích lý do.

## Năm tầng
| Tầng | Là gì | Nằm ở đâu | Ai ghi |
|---|---|---|---|
| 0 Ngân sách ngữ cảnh | Nạp lười: rule theo đường dẫn, skill khi cần, handbook nạp sẵn; khám phá bằng `Explore`; một feature mỗi phiên; cảnh báo khi vượt `context_warn_pct` | — | hook SessionStart |
| 1 Trạng thái phiên | Bàn giao ≤ 40 dòng, chỉ phần khác so với artifact | `.team/session/<id>.md` (gitignore) | hook PreCompact, SessionEnd; nạp ở SessionStart |
| 2 Artifact feature | spec, design, plan, review, acceptance... | `docs/team/features/<ID>/` | các vai |
| 3 Kiến thức dự án | Chia hai: auto memory của Claude Code (máy cục bộ: thói quen, đặc điểm máy) và `docs/team/` (dùng chung, CI đọc được: ADR, cache research theo phiên bản, As-Built, glossary, cache explore có hash) | `~/.claude/projects/...` và `docs/team/` | các vai, theo rule |
| 4 Memory của agent | `memory: project` cho reviewer, qa, coach; nhỏ, có ngày | thư mục memory của agent | chính agent đó |

## Phép thử "có đáng lưu không"
Lưu khi: dùng lại ≥ 2 lần HOẶC tạo lại tốn kém. Khi lưu:
- Lưu kết luận, không lưu quá trình.
- Ghi ngày hoặc phiên bản để biết lúc hết hạn.
- Có trần kích thước và số file.
- coach dọn định kỳ.

## Giữ cache prompt
- Phần đầu prompt ổn định; không chèn dữ liệu thay đổi vào đầu.
- Không đổi model giữa phiên.
- Khi chia việc song song: cùng model, cùng bộ tool.
- Nén chủ động ở ranh giới giai đoạn, không đợi đầy.

## Mẹo cho người dùng
- Một feature mỗi phiên. Xong giai đoạn thì `/team:session` rồi mở phiên mới cũng được: trạng thái nằm trên đĩa.
- Ngữ cảnh đầy: xem `docs/guides/incidents.md`.

## Script và hook làm việc này
| Việc | Ở đâu |
|---|---|
| Ghi bàn giao ≤ `memory.handoff_max_lines` dòng trước khi nén và khi kết thúc phiên | `scripts/handoff.sh` (hook PreCompact, SessionEnd) → `.team/session/<session_id>.md` |
| Nạp lại: tóm tắt trạng thái, bàn giao mới nhất, nhắc 6 luật sau khi nén | `scripts/session-start.sh` (hook SessionStart, `additionalContext`) |
| Đếm số lần nén theo phiên/feature | `scripts/log-session.sh` (hook PostCompact, SessionEnd) → `docs/team/metrics/sessions.jsonl` |
| Cache khám phá theo hash thư mục | `scripts/explore-cache.sh <dir>` → `HIT`/`MISS` với `docs/team/explore/<slug>.md` (dòng `hash:`) |
| Trạng thái tính từ artifact (không con trỏ) | `scripts/team.py status` |
