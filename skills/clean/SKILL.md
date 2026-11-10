---
name: clean
description: Dùng khi cần dọn dẹp không đổi hành vi đúng một loại nợ: code chết, đặt tên, cấu trúc, phụ thuộc thừa, test mồ côi, đơn giản hóa, ngừng dùng API cũ, hoặc bổ sung log/metric.
argument-hint: "<dead-code|naming|structure|deps|tests|simplify|deprecate|observe> [<đường dẫn>] [--decide]"
context: fork
agent: team:maintainer
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

# Dọn dẹp không đổi hành vi

## Tổng quan
Skill này làm đúng MỘT loại dọn dẹp và chứng minh hành vi không đổi bằng hai lần chạy `cmd.test` — trước và sau — cùng số test, cùng tên test, cùng kết quả. Skill chạy trong ngữ cảnh `maintainer` (fork). Bằng chứng "không đổi" chỉ có giá trị ở chỗ có test phủ: vùng không test nào chạm thì không chứng minh được gì, nên dừng hoặc viết test đặc tả (characterization) trước, trong commit riêng.

Trước khi xóa hay viết lại một đoạn, phải nói được vì sao nó tồn tại (`git log -L`, `git blame`). Không giải thích được → không đụng; ghi `debt.md` (hàng rào Chesterton). Đổi assertion để test xanh nghĩa là đã đổi hành vi — hoàn tác và leo thang.

`$ARGUMENTS`: loại, phạm vi đường dẫn, `--decide` (maintainer không bao giờ hỏi người; điểm chưa rõ → `NEEDS_ANSWER` về team-leader). `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Playbook `refactor` sau `/team:design --short` (G2b đã duyệt), hoặc batch `clean-sweep`.
- Mục nợ trong `docs/team/debt.md` đến lượt: code chết, tên lệch `naming.*`, file sai chỗ theo `structure.*`, phụ thuộc thừa, test mồ côi.
- Cần ngừng dùng một API nội bộ (đã có cái thay thế) hay thêm log/metric cho đường đang chạy.

Không dùng khi:
- Có bug cần sửa → `bug-fix`; trộn vào sẽ phá bằng chứng trước == sau.
- Đổi schema dữ liệu → playbook `data-migration` (mở rộng → chuyển → thu hẹp).
- Thay framework, tách module lớn → `change-request`/`new-feature` có design đầy đủ.
- Hai loại một lần → hai lần chạy, hai PR.

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `cmd.test`, `cmd.test_one`, `cmd.lint`, `cmd.typecheck`, `cmd.build`, `cmd.install`, `naming.*`, `structure.*`, `test.skip_markers`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`.
3. Read `docs/team/features/<ID>/design.md` (mục "Cách chứng minh hành vi không đổi") và mục nợ trong `docs/team/debt.md`.

## Đầu vào và điều kiện trước
- Mã `<ID>` (refactor), đúng MỘT loại, phạm vi đường dẫn.
- Kiểm: `python3 "<kit>/scripts/team.py" status <ID>` báo `designed` và G2b đã duyệt (playbook refactor luôn bật G2b). Batch `clean-sweep` không có design → phạm vi phải là một mục cụ thể của `debt.md`.
- Nhánh `team/<ID>` không đang checkout ở worktree khác; nếu có → `NEEDS_CONTEXT`.
- Phạm vi dự kiến > 500 dòng đổi → tách thành nhiều lần, hoặc dừng xin cách làm bằng công cụ (codemod) qua team-leader.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature: <ID>, stage: "clean", agent: "maintainer", started_at}.
2. **Nhánh.** Trong worktree của mình: `git switch -c team/<ID> <base_branch>` (hoặc `git switch team/<ID>` nếu đã có).
3. **Đường nền.** `cmd.test` TRƯỚC: lưu số test VÀ danh sách tên, mã thoát, `git rev-parse HEAD`. Có `cmd.build` → lưu số cảnh báo. Không có test phủ phạm vi (Grep tên module trong thư mục test) → điểm quyết định: design cho phép thì thêm test đặc tả ở commit RIÊNG trước đường nền; không → dừng.
4. **Hàng rào Chesterton.** Với mỗi đoạn sẽ xóa hay viết lại: một dòng "tồn tại vì …" từ `git log -L`/`git blame`. Không giải thích được → ghi `debt.md`, bỏ qua đoạn đó.
5. **Làm đúng loại** (chi tiết từng loại: `${CLAUDE_SKILL_DIR}/references/kinds.md`):
   - `dead-code`: Grep tên VÀ dạng chuỗi, điểm vào trong `structure.config`, export, gọi động. Công khai (export, có trong README) → không xóa, chuyển sang `deprecate`.
   - `naming`: một họ định danh mỗi commit, theo `naming.*`; sau đó grep tên cũ = 0 kết quả (trừ CHANGELOG).
   - `structure`: chỉ di chuyển; `git diff -M --stat` cho thấy rename ≥ 90% giống; thư mục mới dưới `allowed_new_file_roots`.
   - `deps`: grep import của gói = 0 → sửa manifest → `cmd.install` để công cụ sinh lại lockfile (STD-DEP-2); không sửa tay lockfile; manifest nằm trong `protected_paths` → dừng.
   - `tests`: test mồ côi chỉ xóa khi code đích đã mất hoặc assertion trùng một test có tên khác (dẫn cả hai).
   - `simplify`: mỗi lần một phép đơn giản hóa → `cmd.test_one` trên test phủ → phép tiếp theo. Không bỏ xử lý lỗi (đó là hành vi).
   - `deprecate`: cái thay thế phải chạy được trước; đánh dấu cũ kèm trạng thái, cái thay, hạn gỡ; gỡ hẳn là lần chạy sau khi grep chỗ dùng = 0.
   - `observe`: viết 2–4 câu hỏi vận hành trước; log có cấu trúc, nhãn hữu hạn, không dữ liệu nhạy cảm (STD-SEC-6); test giữ nguyên.
6. **Sau.** `cmd.test` SAU: so danh sách tên với đường nền (diff rỗng). Ngoại lệ duy nhất: loại `tests` — ghi "trước N, sau N−k, đã xóa: <tên>". `cmd.lint`, `cmd.typecheck` mã thoát 0. Khác đường nền → DỪNG, không "sửa cho khớp".
7. **Kiểm cấm.** `git diff --name-only <base_branch>` ∩ `protected_paths` = rỗng; grep diff tìm `test.skip_markers` mới = rỗng; file test chỉ đổi ở loại `tests` hoặc do đổi tên ký hiệu.
8. **Commit** bằng `/team:commit` (`refactor(<phạm vi>): … (<ID>)`). Sau commit: `git switch --detach` để nhả nhánh `team/<ID>` cho qa checkout.
9. **Đánh dấu xong cho `team.py`.** Write `docs/team/features/<ID>/tasks.md` ở CÂY CHÍNH (đường dẫn gốc = dòng đầu `git worktree list`): `- [x] T1 — clean <loại> (<phạm vi>)`. Chuỗi refactor không có plan; dòng này làm feature thành `built` để `/team:verify` chạy được (ADJ-26).
10. **Nợ.** Cập nhật `docs/team/debt.md`: mục đã trả, phần còn lại, điều phát hiện thêm.
11. **Trả** team-leader ≤ 10 dòng, dòng đầu `maintainer -> team-leader | <ID> | DONE (<loại>)` (hoặc `BLOCKED`, `NEEDS_ANSWER`).

## Đầu ra
- Commit trên `team/<ID>`; `docs/team/features/<ID>/tasks.md` (T1 tick); `docs/team/debt.md`.
- Tin trả mẫu:
  ```
  maintainer -> team-leader | REF-007 | DONE (dead-code)
  Nhánh team/REF-007, commit 3f2a9c1 (đã nhả nhánh)
  Xóa: src/util/legacy_fmt.py (grep "legacy_fmt" 0 kết quả ngoài CHANGELOG; tồn tại vì export cũ, gỡ ở v2.0)
  cmd.test trước: 142 passed @a1b2c3d; sau: 142 passed @3f2a9c1; danh sách tên giống nhau
  lint exit 0, typecheck exit 0; protected_paths: không chạm; skip marker mới: 0
  Còn nợ: src/report.py hai hàm trùng (debt.md #12)
  Tiếp: /team:verify REF-007
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Grep không thấy ai gọi" | Kiểm thêm chuỗi, cấu hình, export; công khai → `deprecate`. |
| "Test xanh là hành vi không đổi" | Chỉ ở chỗ có test phủ; không phủ → test đặc tả trước hoặc dừng. |
| "Phải chỉnh một assertion thôi" | Đã đổi hành vi; hoàn tác, leo thang. |
| "Bỏ xử lý lỗi cho gọn" | Đường lỗi là hành vi; cấm. |
| "Lockfile cũ, sửa tay" | `cmd.install` (STD-DEP-2). |
| "Tiện sửa luôn một bug" | `debt.md` + bug-fix riêng. |
| "Đổi tên theo kiểu tôi thích" | Chỉ theo `naming.*`. |
| "Cùng số test là đủ" | So tên test, không chỉ số. |
| "Đang deprecate thì chuyển luôn chỗ gọi" | Chuyển chỗ gọi là lần chạy riêng. |

## Dấu hiệu sai
- Hai đầu ra `cmd.test` khác số hay khác tên mà không có danh sách "đã xóa".
- Diff trộn đổi tên với sửa logic.
- File test bị sửa trong loại `simplify`/`naming` ngoài đổi tên ký hiệu.
- Lockfile đổi mà báo cáo không có dòng `cmd.install`.
- Diff > 500 dòng.
- Code "chết" bị xóa không có lệnh grep rỗng được dán.
- Không có `tasks.md` T1 sau khi xong (feature kẹt ở `designed`).

## Kiểm chứng
- [ ] Hai đầu ra `cmd.test` (số + tên) kèm SHA trước/sau; diff tên rỗng, hoặc khớp danh sách đã xóa của loại `tests`.
- [ ] Mã thoát `cmd.lint`, `cmd.typecheck` được dán.
- [ ] Bằng chứng riêng của loại (grep rỗng, độ giống rename, đầu ra `cmd.install`).
- [ ] `git diff --name-only` ∩ `protected_paths` và grep skip marker được dán (kể cả rỗng).
- [ ] `team.py status <ID>` báo `built` sau bước 9.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/kinds.md` — bằng chứng và bẫy của từng loại. Mở ở bước 5.
- Agent `maintainer`; `workflows/refactor.md`, `workflows/batch/clean-sweep.md`.
- `/team:design --short` (trước), `/team:verify` (sau), `/team:commit`, `/team:pr`.
- `handbook/STD.md`: STD-TEST-5, STD-DEP-2, STD-STRUCT-1, STD-NAME-1, STD-DESIGN-3, STD-SEC-6, STD-OPS-5.
