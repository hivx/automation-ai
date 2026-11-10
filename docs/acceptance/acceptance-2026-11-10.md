# Biên bản nghiệm thu `automation-ai` (plugin `team`) — 2026-11-10

- Đối tượng: commit `e24f0edf086ebcb260c373412452f412b917d0cf` (tag `v0.3.0`), Claude Code 2.1.322.
- Nguồn sự thật: `docs/requirements/ban-hieu-yeu-cau.md`, sha256 `2b781a21…911523f`, giống từng byte với bản người đưa.
- Cách làm:
  - Sổ yêu cầu 379 dòng (`requirements-register.md`).
  - Kiểm tĩnh do bốn người kiểm độc lập, mỗi người một nhóm phần: A/G/H/I/J, B/D, C, E/F. Mọi file agent và mọi SKILL.md đều được mở.
  - Tự chạy lại các công cụ của kit.
  - Kiểm sống B1–B12 trên `/tmp/acceptance-sample`: Python, 3 module, 23 commit, CLAUDE.md cũ 130 dòng, 1 test skip, 1 TODO, README hứa một hàm chưa có.
  - Chi phí kiểm sống khoảng $9,4.
- Kết quả đầy đủ: `traceability-2026-11-10.md`. Đo chất lượng: `measured-quality.md`. So SPEC: `spec-vs-requirements.md`.

## 1. Phán quyết: **TỪ CHỐI (REJECT)**
Luật áp dụng: TỪ CHỐI nếu có yêu cầu `must` bị FAIL ở Phần A–C hoặc E–F. Có 11 `must` FAIL:
- Phần B: 1 (REQ-B3-5).
- Phần C: 2 (REQ-C5-10, REQ-C7-13).
- Phần E: 3 (REQ-E1-9, REQ-E2-3, REQ-E2-6).
- Phần F: 3 (REQ-F1-33, REQ-F1-35, REQ-F2-5).
- Ngoài ra Phần H và I mỗi phần 1 (REQ-H3-8, REQ-I-5).

Nhận định chung: phần lớn đã có và đúng (71,5% PASS). Kit dựng được, hook chặn đúng, trạng thái tính từ đĩa, takeover và onboard chạy sạch, nghiệm thu bằng lệnh thật. Nhưng một dự án mới chưa đi trọn feature cỡ S nếu người không sửa tay. Một playbook bị kẹt. Skill tạm không tự kích hoạt. Ngân sách chữ trái câu chữ tài liệu. Vài giá trị mặc định lệch.

## 2. Số đếm
| Phần | PASS | PARTIAL | FAIL | UNVERIFIED | Tổng |
|---|---|---|---|---|---|
| A | 28 | 4 | 0 | 3 | 35 |
| B | 33 | 19 | 1 | 0 | 53 |
| C | 87 | 16 | 2 | 1 | 106 |
| D | 14 | 14 | 0 | 0 | 28 |
| E | 18 | 11 | 4 | 0 | 33 |
| F | 54 | 17 | 3 | 0 | 74 |
| G | 17 | 2 | 0 | 0 | 19 |
| H | 6 | 6 | 1 | 0 | 13 |
| I | 7 | 1 | 1 | 0 | 9 |
| J | 7 | 2 | 0 | 0 | 9 |
| **Tổng** | **271** | **92** | **12** | **4** | **379** |

| Mức | PASS | PARTIAL | FAIL | UNVERIFIED |
|---|---|---|---|---|
| must | 253 | 85 | 11 | 3 |
| should | 18 | 7 | 1 | 1 |

Số trên bằng số trong `traceability-2026-11-10.md` (379 dòng). Tỉ lệ PASS là 71,5%. Ngưỡng CHẤP NHẬN là 95%, và còn 85 `must` PARTIAL.

## 3. Ma trận truy vết
Toàn bộ nằm ở `docs/acceptance/traceability-2026-11-10.md`, gồm REQ-ID, yêu cầu, cách kiểm, mức, kết quả, bằng chứng, ghi chú. Sổ không có kết quả nằm ở `requirements-register.md`. Các dòng "Hành vi: …" là kết quả kiểm sống.

## 4. Mười khoảng trống quan trọng nhất
| # | REQ-ID | Tài liệu đòi | Đang có | Bằng chứng | Đề xuất sửa | Prompt |
|---|---|---|---|---|---|---|
| 1 | REQ-E1-9, REQ-C5-10 | Profile chỉ có khe kit dùng được; feature cỡ S đi từ analyze tới verify | takeover đề xuất `naming.test_file: "tests/test_<module>.py"`, onboard ghi nguyên. `check-structure.sh:37` so basename với mẫu `{name}`, nên mọi test mới bị báo STD-NAME-3 và build BLOCKED | B6 "DỪNG: tech-lead báo BLOCKED ở T1…"; sau khi người sửa profile, B6c accepted 5/5 | Schema bắt `naming.test_file` có `{name}` và không có `/`; mẫu profile-proposal nêu luật; check-structure chấp nhận mẫu có thư mục; ca thử; chạy lại B6 | P9 (sửa lỗi) |
| 2 | REQ-C7-13 | Playbook integration: research → architect → design → … | `team.py:89` không có `integration` trong `NO_SPEC_PLAYBOOKS`, nên feature kẹt ở `intaken` và `/team:run` lặp research | fixture INT-010 của người kiểm C | Thêm `integration` (và kiểm lại `new-project`, `client-docs`); ca thử cho từng playbook | P9 |
| 3 | REQ-F2-5 | team-leader thấy chuyên môn lặp thì điều phối `make-skill` | Yêu cầu "6 màn hình CRUD giống hệt nhau" ra intake "Skill tạm: không cần" | B9; `FEAT-003/intake.md:17` | Bước kiểm cụ thể ở intake/plan: ≥ 3 đơn vị cùng khuôn hoặc chuỗi bước lặp thì đề xuất make-skill (headless: in nội dung, K-72). Kèm eval cho tình huống này | P7 vòng 3 (độ sâu hành vi) |
| 4 | REQ-F1-33, REQ-I-5 | Skill hay nạp < 200 từ, khác < 500 | ≤ 400 / 1.200–2.500 / agent 600–1.200 theo P7 | `scripts/skill-budgets.txt`; `measured-quality.md` | Người quyết: sửa F1 và I trong tài liệu theo chuẩn P7, hoặc đặt lại trần cũ | người quyết |
| 5 | REQ-F1-35 | Mỗi skill có eval baseline → with-skill trước khi phát hành | 9/26 skill có kịch bản; baseline thật chỉ có ở verify, using-team | `ls evals/` | Kịch bản cho 17 skill còn lại (ưu tiên skill kỷ luật); chạy baseline và with-skill | P7 vòng 3 |
| 6 | REQ-B3-5 | Ghi đè `models` trong config có hiệu lực | Không script hay skill nào đọc `models`; designer cỡ S/M không chuyển sang sonnet (ADJ-10) | grep `models` chỉ thấy ở `audit-xref.py` | team-leader truyền `model` từ config khi gọi Agent, có ca thử; hoặc bỏ khóa và sửa tài liệu | P9 |
| 7 | REQ-E2-3, REQ-E2-6 | `protected_branches` = main, master, develop, release; `approvers` = `["@owner"]` | `["main","master","release/*"]`; mọi cổng `[]` | `templates/project/team/config.json` | Sửa mẫu theo tài liệu; release kiểm tên người duyệt khi danh sách có `@owner` | P9 |
| 8 | REQ-A3-9 (PARTIAL) | Không lách cổng đang bật (điều không được sai phải là máy) | analyst hay team-leader ghi được `Approved-by:` vào artifact (hook cho qua) | người kiểm A: Write mô phỏng exit 0 | Hook chặn vai agent thêm hay sửa dòng `Approved-by*:`; chỉ người hay workflow comment `@claude approve` được ghi | P9 |
| 9 | REQ-H3-8 | validate kiểm định danh tiếng Anh | validate không bắt tên file non-ASCII | người kiểm A: thêm `workflows/batch/dọn-dẹp.md`, validate vẫn 0 fail | validate.sh kiểm tên file và key JSON là ASCII trong kit, profile, template | P9 |
| 10 | REQ-D1-*, REQ-B1 devops (PARTIAL) | Mức 3 = máy chặn; devops không tự deploy prod | STD-TEST-4, STD-NAME-5, STD-CI-6, STD-OPS-7 ghi mức 3 nhưng không hook nào chặn; role-policy cho devops `write *`, `bash any` | người kiểm B/D: `kubectl apply -f prod.yaml` exit 0 | Hoặc thêm hook (skip marker trong diff ở stop-check, commit message sai → chặn), hoặc hạ mức về 2; thu hẹp role-policy devops | P9 |

Khoảng trống đáng kể khác (PARTIAL), chi tiết trong ma trận:
- **Retro:** không ra đề xuất trên dữ liệu ít (REQ-F6-9), nên định dạng diff/eval/canary chưa kiểm được trên thực tế.
- **Bàn giao phiên:** quá mỏng, có lần đề xuất sai việc tiếp (REQ-F5-6).
- **`scorecard.json`:** lần chạy không tự ghi (REQ-F6-10).
- **Cổng G5 và G0:** không nằm trong `team.py` (REQ-C1-10, C1-1).
- **Cỡ L:** kiến trúc không bắt buộc (REQ-C3-3).
- **change-request:** `team.py` không đi tới architect impact (REQ-C7-7).
- **`tools`:** 13/13 vai khác bảng B1, đều có ADJ trừ devops.
- **Handbook D2:** thiếu khoảng 11 bất biến, ví dụ hàm ≤ 50 dòng và ≤ 4 tham số, TODO có ID, squash merge.
- **Schema profile:** nhận `test_one` rỗng và nhận placeholder lạ (REQ-E1-2, E1-3).
- **`.github/`:** không thuộc `allowed_new_file_roots` của profile mẫu (REQ-E1-5).

## 5. SPEC so với tài liệu yêu cầu
Chi tiết ở `docs/acceptance/spec-vs-requirements.md`, gồm 13 khác biệt của SPEC (S1–S13) và 13 chỗ repo đi khác qua ADJ hay prompt sau (R1–R13). Khuyến nghị:
- **Sửa tài liệu yêu cầu:**
  - Tên file `docs/` và thư mục `lot/`, tiêu đề `## Giả định tự quyết` / `## Nguồn`, dòng overlay (S1–S5). Tài liệu tự mâu thuẫn với luật A5, định danh tiếng Anh.
  - Giới hạn của Claude Code: `--bare` tắt hook (R2), subagent không có `AskUserQuestion` (R5), TaskCreate (R3).
- **Người quyết:**
  - Ngân sách chữ (R1, tức khoảng trống #4).
  - Thêm Bash/Write cho analyst, architect, designer, writer, qa (R4).
  - Cỡ S có qa nghiệm thu (R6).
- **Sửa repo hoặc sửa tài liệu:** nhánh `team/<ID>` khác `team/<ID>-<slug>` của STD-NAME (R10).
- **Chấp nhận:** các bổ sung S6–S13, R7–R9, R11–R13.

## 6. Vượt phạm vi
- Khung GitLab CI `templates/project/gitlab/.gitlab-ci.yml` (đánh dấu "TODO(v2)") được onboard chép khi `ci.provider = gitlab`. Tài liệu J đưa GitLab CI vào bản 2. Khuyến nghị: giữ, vì chỉ là khung đánh dấu v2, nhưng ghi rõ trong README; hoặc gỡ.
- Không viết MCP server hay plugin mới. Không có cấu hình MCP mẫu, scorecard nâng cao, canary tự động, thăng cấp skill lên kit hay workflow lô mở rộng (vẫn 4). Đúng J.

## 7. Chưa kiểm được và cách người kiểm
| REQ-ID | Vì sao | Người làm |
|---|---|---|
| REQ-A4-2 | Cần CLI `npx skills` và repo trên GitHub | Đẩy repo lên GitHub. Ở một dự án trống chạy `npx skills add <owner>/automation-ai`. Kiểm `ls .claude/skills \| wc -l` = 26; mở Claude Code, gõ `/team-status`. |
| REQ-C1-13 | Cần GitHub Actions thật | Onboard một repo thử có `ci.provider: github`, thêm secret `ANTHROPIC_API_KEY`. Tạo issue nhãn `team:intake`, đợi tới G1, bình luận `@claude approve G1`. Kiểm `spec.md` có `Approved-by: <bạn> <ngày>`. |
| REQ-A1-6, REQ-A4-4 | Lịch sử quy trình (ai viết repo, có duyệt từng bước, có tra docs không) | Người xác nhận theo trí nhớ và lịch sử phiên; không kiểm được từ file. |

## 8. Nhật ký kiểm sống B1–B12
| # | Lệnh | Trích đầu ra / bằng chứng | Kết quả |
|---|---|---|---|
| B1 | `/team:takeover` | "T0: 5 lệnh / T1: 3 tài liệu / T2: đọc trực tiếp (12 file) / T3 không chạy". Thấy README hứa `overdue_report` mà code thiếu, TODO ở loans.py:26, 1 skip. Có 5 báo cáo. `git status`: chỉ `?? .team/ ?? docs/`. ai-readiness `clean-first` (CLAUDE.md 130 dòng, mô tả Flask/Redis). | PASS |
| B2 | `/team:onboard --yes` trước khi duyệt | "Onboard dừng ở điều kiện trước, chưa ghi file nào… Chưa duyệt G0"; git status không đổi | PASS |
| B3 | Thêm `Approved-by:`; `/team:onboard --yes` → dừng ở `clean-first` (K-09); `--yes --accept-clean-first` | check-profile OK cho profile và config. Khối CLAUDE.md 16 dòng, 0 dòng cũ bị xóa. settings: agent `team:team-leader`, 15 allow, 6 deny. 4 rule. Có khung `docs/team/`. gitignore có `.team/current.json`, `plugin_root`, `session/`, `settings.local.json`, `worktrees/`. "Plugin chưa cài: không có". Không sinh `.github/` vì `ci.provider: none`. Profile ghi `naming.test_file` sai mẫu và `protected_paths` chỉ `.env`. | PASS, kèm lỗi nội dung profile (REQ-E1-9 FAIL, REQ-E1-10 PARTIAL) |
| B4 | Phiên haiku thử 4 việc, cộng hook chạy trực tiếp | "BLOCKED (STD-STRUCT-1): file mới 'random/new.py'…"; "BLOCKED (STD-GIT-3): push vào nhánh bảo vệ `main`". `.env`: phiên sống bị deny của Claude Code; `protect.sh` trực tiếp ra "BLOCKED (STD-SEC-1)…", exit 2. Push `team/FEAT-001`: check-git exit 0. Stop với test đỏ: `test_hooks.sh` "stop: build có lint đỏ bị chặn" và "stop_hook_active cho dừng" (124/124). | PASS |
| B5 | `/team:intake "Implement the overdue report the README promises" --size S --decide` | FEAT-001 new-feature S decide; có quyết định và điểm còn mở; journal 1 dòng đúng mẫu; "Ngân sách vai: tối đa 3, đã dùng 0" | PASS |
| B6 | `/team:run FEAT-001 --until-blocked` | analyst: spec 5 AC. dev commit `2d15a85`. Rồi "DỪNG: tech-lead báo BLOCKED ở T1. check-structure.sh không khớp naming.test_file". Người sửa profile (commit `d7cdc50`); B6c "Chạy /team:build FEAT-001 --task T1, rồi tiếp /team:run…": dev trong worktree, đỏ rồi xanh; reviewer vòng 1 request-changes (major STD-TEST-2), vòng 2 approve; commit `feat(report): add overdue_report (FEAT-001)`, `test(report): … (FEAT-001)`; diff chỉ `library/report.py`, `tests/test_report.py`; nhánh `team/FEAT-001`; qa trên worktree tách rời: "Ran 9 tests OK (skipped=1)", `Verdict: accepted`, dừng `WAITING_FOR_APPROVAL G4_uat`; 3/3 vai (analyst, tech-lead, qa); `runs.jsonl` 17 dòng; `scorecard.json` chỉ có sau khi chạy tay `team.py scorecard` | FAIL (không qua được nếu người không sửa); chuỗi sau sửa PASS |
| B7 | Xóa `.team/current.json`; phiên mới `/team:status`; viết tay `design.md` cho FEAT-002 (spec chưa duyệt, cỡ M) | `team.py status` trước và sau giống hệt. Phiên mới in cùng bảng. FEAT-002 "WAITING_FOR_APPROVAL G1_spec … (artifact sau đã có nhưng bị chặn: designed)" | PASS |
| B8 | Yêu cầu mơ hồ "Cho phép thành viên gia hạn sách đang mượn": intake + analyze (ask); rồi `--decide` | ask: `questions.md` 3 câu, mỗi câu a/b/c + "Khuyến nghị" + "hậu quả", "vòng 1/2", 8 giả định nhỏ. decide: team-leader dùng lại FEAT-002 (yêu cầu trùng); analyst `--decide` → SPECIFIED, A9–A14, không câu hỏi mới | PASS |
| B9 | "Tạo 6 màn hình CRUD giống hệt nhau … Chế độ decide." | FEAT-003 new-feature M, spec 11 AC, dừng G1; intake "Skill tạm: không cần"; không có `.claude/skills/`; registry rỗng. Còn B5 (S thường) không tạo skill tạm: đúng | FAIL (REQ-F2-5) |
| B10 | `/team:retro --decide` | `retro/2026-11-10.md`: "0 đề xuất, 5 theo dõi" (luật mẫu tối thiểu); dẫn measure.py; chẩn đoán đúng lỗi `naming.test_file` (lỗi kit, không phải prompt); không file agent hay skill nào đổi; memory coach có ngày | PARTIAL (không có đề xuất để kiểm định dạng) |
| B11 | Xem `.team/session/`; `session-start.sh` với source=compact; `handoff.sh` PreCompact | Bàn giao SessionEnd/PreCompact 2–3 dòng (≤ 40) nhưng chỉ feature/stage/việc tiếp. Có lần ghi "Việc đầu tiên phiên sau: /team:intake (chưa có intake.md cho retro)". Sau compact in "Sáu luật cốt lõi: (1)…(6)" | PARTIAL |
| B12 | `claude plugin marketplace add <kit>` + `claude plugin install team@automation-ai --scope project`; `scripts/install-local.sh` | marketplace: 13 agent `team:`, 18 skill model thấy được, 8 skill chỉ người gọi; gỡ lại sau khi thử. install-local: 26 thư mục `team-*`, 13 agent, hook 8 sự kiện | PASS |

## Sửa trong lúc nghiệm thu
Không có. Không gặp lỗi máy móc nào chặn việc kiểm: thiếu bit thực thi, link hỏng, file sinh cũ.

Ghi chú: `scripts/validate.sh --strict` hiện báo FAIL vì ba file mới của bước này (`docs/requirements/ban-hieu-yeu-cau.md`, `docs/acceptance/*.md`) chưa được liên kết từ `docs/00-overview.md` hay README. Thêm liên kết là sửa tài liệu ngoài phạm vi được phép, nên để người làm: một dòng trong bảng tài liệu của `docs/00-overview.md`. Trước bước này, `--strict` cho 0 fail (người kiểm A chạy trên bản sao không có các file đó).
