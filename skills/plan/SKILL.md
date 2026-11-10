---
name: plan
description: Dùng khi feature đã có spec và design được duyệt và cần chia thành task 2–5 phút có touchpoints, hoặc khi change-request cần chèn task mới (--insert).
argument-hint: "<ID> [--insert]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git branch *)
---

# Lập kế hoạch → plan.md + tasks.md

## Tổng quan
Skill này chia feature thành task 2–5 phút, mỗi task có đường dẫn file cụ thể, file test, tiêu chí và phụ thuộc, để một dev chỉ nhìn một dòng task vẫn làm đúng mà không hỏi lại. Skill chạy trong ngữ cảnh `tech-lead` (fork). Kế hoạch là các QUYẾT ĐỊNH (file, chữ ký, tên test, thứ tự), không phải chương trình viết sẵn.

Kế hoạch tốt: mọi touchpoint trong `design.md` thuộc ít nhất một task; mọi tiêu chí trong `spec.md` có ít nhất một task phủ; không hai task song song chạm cùng file; cỡ L có walking skeleton làm task đầu.

`$ARGUMENTS`: mã `<ID>`; `--insert` khi change-request thêm task vào kế hoạch đang chạy. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Spec và (cỡ M/L) design đã duyệt theo cổng mà `team.py` báo áp dụng.
- Playbook dependency-upgrade sau research: mỗi thay đổi phá vỡ một task.
- Change-request đã có Amendment và arch-impact → `--insert`.

Không dùng khi:
- Cỡ S, bug-fix, hotfix: `/team:build` tự tạo `tasks.md` một task từ `spec.md`.
- Design còn thiếu touchpoints hay test plan → trả `DESIGN_CONFLICT`, không tự thiết kế.
- `tasks.md` đã có task chưa tick của việc KHÁC → dừng, leo thang (không ghi đè).

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `structure.src`, `structure.tests`, `naming.test_file`, `structure.allowed_new_file_roots`, `cmd.test_one`. Tên file test trong task theo `naming.test_file`; file mới chỉ trong allowed roots.
2. Read `.team/config.json`: `limits.max_parallel_dev`, `limits.max_rework`, `base_branch`.
3. Kiểm touchpoints "sửa" thật sự tồn tại (Glob); touchpoints "mới" nằm trong allowed roots. Lệch → `DESIGN_CONFLICT`.
4. Không chạy `cmd.*` nào; planning chỉ đọc và viết hai file.

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/spec.md` có `## Definition of Done`.
- `design.md` (cỡ M/L), `arch-impact.md` hoặc `docs/team/architecture.md` (cỡ L).
- `python3 "<kit>/scripts/team.py" status <ID>`: cổng trước đã qua (không `WAITING_FOR_APPROVAL`). Đang chờ cổng → trả lại, dừng.
- `--insert`: spec có `## Amendment <n>` mới nhất chưa được kế hoạch hóa.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature, stage: "plan", agent: "tech-lead", started_at}.
2. **Bản đồ file trước, task sau.** Liệt kê mỗi file sẽ tạo/sửa và trách nhiệm của nó (từ touchpoints của design). Task được suy ra từ bản đồ này, không ngược lại.
3. **Ràng buộc chung.** Mục `## Ràng buộc chung` trong `plan.md`: chép NGUYÊN giá trị từ spec/design (tên trường, định dạng, giới hạn, phiên bản). Mọi task thừa hưởng; dev không phải đoán.
4. **Đồ thị phụ thuộc.** Viết `depends:` theo luồng dữ liệu và hợp đồng (thứ gì phải có trước để test của task kia chạy), không theo cảm tính. Nền móng trước; phần rủi ro cao sớm để thất bại sớm.
5. **Cắt dọc.** Mỗi task (hoặc nhóm nhỏ) giao một hành vi kiểm được. Cấm chia ngang "toàn bộ DB rồi toàn bộ API" ở cỡ M/L.
6. **Walking skeleton (cỡ L).** T1 chạy đầu–cuối qua mọi tầng với phần lõi giả; bằng chứng là một test đầu–cuối chạy bằng `cmd.test_one`. Không task nào khác bắt đầu trước khi T1 được review approve.
7. **Viết tasks.md.** Write từ `<kit>/templates/artifacts/tasks.md`, mỗi task một dòng:
   `- [ ] T<N> — <tên> — files: <đường dẫn> — test: <file test> — depends: <T… hoặc —>`
   rồi các dòng con: tiêu chí (trích `AC-n`), giao diện (`Nhận:` / `Trả:` với tên và chữ ký chính xác), `Kỳ vọng:` đầu ra của `cmd.test_one`.
   Không dùng chữ in đậm quanh mã task (`team.py` đếm task theo `- [ ] T<N>`).
8. **Đúng cỡ task.** Tách khi reviewer có thể từ chối một phần và chấp nhận phần kia; gộp việc chuẩn bị/tài liệu vào task cần nó. Task > 5 file hoặc tên chứa "và" → xem lại. Mỗi task 2–5 phút.
9. **Song song.** Bảng "một file một chủ" trong `plan.md`. Hai task chung file → nối `depends:`. Migration và trạng thái dùng chung luôn tuần tự. Tối đa `limits.max_parallel_dev` task cùng lúc.
10. **Điểm kiểm.** Sau mỗi 2–3 task và ở cuối: `cmd.test` xanh trên `team/<ID>`, luồng chính chạy được — ghi trong `plan.md`.
11. **Trọng tâm review.** ≤ 5 đầu vào hoặc chế độ lỗi mà spec ngụ ý nhưng chưa task nào test; thêm test vào task chủ.
12. **`--insert`.** Thêm task mới sau task cuối đã tick; task bị Amendment ảnh hưởng ghi `[affected]` ở cuối dòng. Không đánh số lại task cũ.
13. **Nhánh.** `git branch --list team/<ID>`; chưa có → tạo từ `config.base_branch`.
14. **Tự kiểm 5 điểm trước khi trả** (chi tiết: `${CLAUDE_SKILL_DIR}/references/self-review.md`): phủ spec, không chữ mơ hồ ("TBD", "xử lý biên"), tên nhất quán giữa các task, trọng tâm review, tỉ lệ (kế hoạch không dài hơn code nó mô tả).
15. **Trả và dừng.** Tin trả ≤ 10 dòng; tech-lead KHÔNG bắt đầu build khi G3 áp dụng mà chưa duyệt.

## Đầu ra
- `docs/team/features/<ID>/plan.md` (mẫu `<kit>/templates/artifacts/plan.md`): thứ tự, ràng buộc chung, bảng một-file-một-chủ, điểm kiểm, rủi ro, trọng tâm review.
- `docs/team/features/<ID>/tasks.md` (mẫu `<kit>/templates/artifacts/tasks.md`).
- Nhánh `team/<ID>`; `.team/current.json` {stage: "plan"}.
- Tin trả mẫu:
  ```
  tech-lead -> team-leader | FEAT-012 | planned
  Task: 6 (T1 walking skeleton), 2 nhóm song song {T2,T3} {T5,T6}; không chung file
  Touchpoint → task: 9/9 đã phủ; AC → task: 4/4
  Rủi ro: T4 đụng migration, chạy tuần tự
  Cổng G3: áp dụng — chờ Approved-by trong plan.md
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Task hiển nhiên, cứ bắt đầu" | Viết tasks.md trước; phụ thuộc ẩn lộ ra khi liệt kê. |
| "Task: 'làm phần backend'" | Tách tới 2–5 phút với file và file test cụ thể. |
| "Hai task chung file nhưng nhanh" | Nối `depends:`; không song song. |
| "Cỡ L, walking skeleton tốn công" | Bắt buộc; nó chứng minh phần tích hợp rủi ro nhất trước. |
| "File test để dev tự chọn" | Ghi `test:` ngay bây giờ. |
| "Lên kế hoạch đường thuận, biên tính sau" | Trọng tâm review liệt kê biên kèm test. |
| "tasks.md cũ đã lỗi thời, ghi đè" | Task chưa tick có thể đang chạy; dừng, leo thang. |
| "Touchpoint đó nhỏ, bỏ qua" | Bảng touchpoint → task phải phủ đủ. |
| "Dán luôn code vào kế hoạch cho dev chép" | Kế hoạch là chữ ký và tên test, không phải chương trình. |
| "In đậm mã task cho dễ đọc" | `team.py` đọc `- [ ] T<N>`; giữ nguyên dạng. |

## Dấu hiệu sai
- Task không có `files:` hoặc `test:`; `depends:` thiếu.
- Touchpoint trong `design.md` không thuộc task nào.
- Task chạm > 5 file, hoặc chia ngang theo tầng ở cỡ M/L.
- Cỡ L không có walking skeleton; T1 không có test đầu–cuối.
- Hai task song song cùng chạm một file.
- Tên hàm/trường khác nhau giữa các task.
- Lệnh stack ghi cứng trong plan (phải là khe `cmd.*`).

## Kiểm chứng
- [ ] Dán bảng touchpoint → task, không dòng nào trống.
- [ ] Dán bảng AC → task, mọi tiêu chí có ít nhất một task.
- [ ] `grep -cE '^- \[ \] T[0-9]+' docs/team/features/<ID>/tasks.md` bằng số task trong tin trả.
- [ ] Mỗi dòng task có `files:`, `test:`, `depends:` (dán đầu ra kiểm `grep -L`/awk rỗng).
- [ ] `git branch --list team/<ID>` cho thấy nhánh.
- [ ] Dán đầu ra `team.py status <ID>` cho thấy `planned` (hoặc chờ G3).

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/self-review.md` — 5 điểm tự kiểm, mẫu khối giao diện.
- Agent `tech-lead`; `<kit>/templates/artifacts/plan.md`, `tasks.md`.
- `/team:design` (bước trước), `/team:build` (bước sau), `/team:analyze --amend` (khi kế hoạch lộ mâu thuẫn spec).
- `handbook/STD.md`: STD-DESIGN-1 (touchpoints), STD-GIT-1 (một task một PR/commit), STD-TEST-2.
