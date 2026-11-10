# SPEC.md so với tài liệu yêu cầu

- Tài liệu yêu cầu: `docs/requirements/ban-hieu-yeu-cau.md` (sha256 `2b781a2147d6180d04932acfdaa5643a9b4d370779bac7adb345f1e29911523f`, bản chốt 2026-11-09). Đây là nguồn sự thật duy nhất cho nghiệm thu.
- `SPEC.md`: bối cảnh chung (P0) bằng tiếng Anh, viết từ tài liệu yêu cầu. Kit được dựng theo SPEC.md cộng các điều chỉnh ADJ-01..ADJ-29 (`docs/00-overview.md`).
- Ngày so: 2026-11-10 · commit `e24f0ed` (tag `v0.3.0`) · Claude Code 2.1.322.

Nơi khác biệt được chia làm hai loại. (1) SPEC.md khác tài liệu. (2) SPEC.md khớp tài liệu, nhưng repo đã đi khác qua một ADJ hay một prompt sau. Cả hai loại đều là phát hiện. Người quyết sửa SPEC, sửa repo, hay chấp nhận lệch.

## 1. SPEC.md khác tài liệu yêu cầu
| # | Mục tài liệu | Tài liệu nói | SPEC.md nói | Loại khác |
|---|---|---|---|---|
| S1 | A5, G1 | Tên file tài liệu bằng tiếng Việt: `docs/00-tong-quan.md … 08-kenh-kich-hoat.md`, `docs/huong-dan/` (bat-dau-5-phut, muon-gi-go-gi, cay-quyet-dinh, phien-mau, ai-dang-cho-gi, su-co, ngay-dau-tren-du-an-cu) | `docs/00-overview … 08-channels + guides/` (5-minute start, "want X → type Y", …) | đổi tên. Bản thân tài liệu tự mâu thuẫn với A5, vốn đòi tên file bằng tiếng Anh. SPEC chọn A5. |
| S2 | G1 | `workflows/` có `lot/` (3–4 workflow kịch bản hoá) | `workflows/batch/` (4) | đổi tên (định danh tiếng Anh) |
| S3 | C4 | Mục giả định: `## Giả định tự quyết` | `## Assumptions decided by the team` | đổi tên tiêu đề |
| S4 | F3 | Stop khi research: phải có `## Nguồn` có URL | `## Sources` with URLs | đổi tên tiêu đề |
| S5 | F6 | Dòng đầu overlay: `# Overlay từ retro <date>: <lý do>` | `# Overlay from retro <date>: <reason>` | đổi chuỗi |
| S6 | A4.1 | Hỗ trợ `npx skills add` (không điều kiện) | "if that CLI exists at build time" | thêm điều kiện |
| S7 | A2 | "Không tự deploy production **khi cổng bật**" | "not something that deploys to production on its own" (tuyệt đối) | chặt hơn |
| S8 | E4 | Local scope: "ghi đè cá nhân, model riêng, MCP cá nhân"; User scope: `autoMemoryEnabled`, plugin cá nhân | Chỉ nêu tên file của local/user scope | bỏ nội dung |
| S9 | G1 | `templates/artifacts/`: 18 mẫu; `templates/schemas/`: `stage-result.json`, `profile.schema.json` | thêm `profile-proposal`, `debt`, `open-questions`, `kit-issues`; schema thêm `config.schema.json` | thêm |
| S10 | G1 | `scripts/` liệt kê 17 file | thêm `render.py` (ADJ-18), `teamlib.py`, `scorecard.sh`, `role-policy.sh`, `gen-*.py`… | thêm |
| S11 | F4 | `validate.sh`: frontmatter, tên, tham chiếu chéo, ngân sách chữ | thêm "JSON, bash -n, py_compile" | thêm |
| S12 | 0. PARAMETERS | Ngôn ngữ cố định tiếng Việt (A5) | `REPO_LANGUAGE` có thể đổi sang English | thêm tham số |
| S13 | H2 | Chuỗi P0–P6 | SPEC giữ P0–P6; thực tế thêm P7 (vòng nâng chất lượng) | thêm bước (không phải yêu cầu của repo) |

Các mục còn lại của SPEC.md (13 vai, bảng công cụ, 9 giai đoạn, cổng, cỡ, ask/decide, vòng build, 16 playbook, takeover 4 tầng, handbook 12 mảng, profile/config, 26 skill, hook, script, memory, journal, cấu trúc repo, kênh) khớp nội dung tài liệu, chỉ khác là bằng tiếng Anh.

## 2. Repo đi khác cả tài liệu (qua ADJ hoặc prompt sau)
| # | Mục tài liệu | Tài liệu nói | Repo làm | Nguồn quyết định |
|---|---|---|---|---|
| R1 | F1, I | Ngân sách chữ: skill hay nạp < 200 từ, skill khác < 500 | Skill hay nạp ≤ 400 chữ, skill khác 1.200–2.500, agent 600–1.200 (`scripts/skill-budgets.txt`) | Prompt P7 của người (thay ngân sách cũ) |
| R2 | H1 | Headless: `--bare --max-turns --max-budget-usd --output-format json` | Không `--bare` khi sửa file (`--bare` tắt mọi hook) | ADJ-03; người trả lời ở P0 (C3) |
| R3 | B1 | team-leader tool: `TaskCreate/Update`, `AskUserQuestion` | Bỏ `TaskCreate/TaskUpdate` (ADJ-07); `AskUserQuestion` chỉ ở phiên chính | ADJ-07, ADJ-01, ADJ-11 |
| R4 | B1 | analyst, architect, designer, writer không có Bash; tech-lead chỉ Edit; qa không Write | Thêm `Bash` (chỉ-đọc), `Write`, `Skill` | ADJ-11, ADJ-27 |
| R5 | B1 | analyst có `AskUserQuestion` | Subagent không có `AskUserQuestion`; analyst trả `NEEDS_ANSWER` + `questions.md` | ADJ-01 (giới hạn của Claude Code) |
| R6 | C3, F1 | Cỡ S: "verify (tự động, không qa riêng)"; skill `verify` "cỡ S chạy tự động" | Cỡ S vẫn fork sang qa (bước kiểm thu gọn) | ADJ-29, K-15 |
| R7 | C1, C3 | Cổng mặc định G1 bật | Cỡ S bỏ G1 và G3 (tài liệu C3 có "bỏ G1" cho S; G3 không có plan với S) | ADJ-09 (khớp C3) |
| R8 | C7 | `refactor`: cổng G2b bật; `data-migration`: G1, G3, G4 | Refactor và data-migration đều bật G2b | ADJ-16 (thêm cho data-migration) |
| R9 | C2 | Mọi giai đoạn tính theo một chuỗi | Playbook không có analyze/plan bỏ qua `specified`/`planned` | ADJ-26 (bug của chuỗi gốc) |
| R10 | D2 STD-NAME | Nhánh `team/<ID>-<slug>` | Nhánh feature là `team/<ID>`, task `team/<ID>-task-N` | quyết định khi dựng (build, verify, pr) |
| R11 | E1 | Không có khe cho deploy prod/rollback | Lệnh prod và rollback nằm ở `docs/team/ci.md` | ADJ-24 (khớp tài liệu, ghi rõ khoảng trống) |
| R12 | F2 | Skill tạm: 8 nội dung | Skill tạm 8 nội dung, 300–1.000 chữ | Vòng 2 P7 |
| R13 | C1 | `/team:intake` do team-leader chạy | Ban đầu chỉ người gọi được, đã sửa | ADJ-28 |

## Khuyến nghị (người quyết)
- S1, S2, S3, S4, S5: tài liệu tự mâu thuẫn với luật A5 (định danh tiếng Anh). Khuyến nghị: **sửa tài liệu yêu cầu** cho khớp A5, giữ repo.
- R1: lệnh P7 của người mâu thuẫn trực tiếp với F1 và I của tài liệu. Khuyến nghị: **người cập nhật tài liệu** (F1, I) theo chuẩn P7, hoặc đặt lại ngân sách cũ. Đây là FAIL theo tài liệu cho tới khi người quyết.
- R2, R3, R5: giới hạn của Claude Code hiện hành. Khuyến nghị: **chấp nhận lệch**, sửa tài liệu.
- R4, R6: quyết định thiết kế để kiểm được trạng thái và giữ người nghiệm thu độc lập. Khuyến nghị: người chọn. Hoặc chấp nhận và sửa tài liệu, hoặc yêu cầu repo quay lại đúng tài liệu.
- R10: lệch thật so với STD-NAME của tài liệu. Khuyến nghị: **sửa repo** (đổi nhánh feature thành `team/<ID>-<slug>`) hoặc sửa tài liệu.
- S6–S13, R7–R9, R11–R13: bổ sung hay làm rõ. Khuyến nghị: chấp nhận, ghi vào tài liệu.
