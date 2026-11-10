---
name: asbuilt
description: Dùng khi feature đã accepted và duyệt G4, cần As-Built, release notes, mục CHANGELOG, cập nhật README/tài liệu người dùng và nội dung PR trước khi phát hành.
argument-hint: "<ID> [--audience user|dev|client]"
context: fork
agent: team:writer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Ghi lại cái đã giao

## Tổng quan
Skill này ghi lại cái ĐÃ giao — không phải cái định làm — cho người đọc phù hợp. Nó chạy trong ngữ cảnh `writer` (fork), sau khi qa ra `Verdict: accepted` và người duyệt G4. Đầu ra gồm bốn thứ: `asbuilt.md` so từng mục thiết kế với code thật; release notes cho người đọc được nêu; một mục CHANGELOG dưới `## [Unreleased]`; và `pr-body.md` mà `/team:pr` dùng nguyên văn.

Nguyên tắc: mỗi câu viết ra phải truy được về một dòng trong `acceptance.md` (AC-n) hoặc một đoạn trong `diff.patch`. Không có nguồn thì không viết. As-Built cũng là nơi đóng phần DoD "sau G4" mà qa đã ghi chủ (K-35).

`$ARGUMENTS`: mã `<ID>`, tùy chọn `--audience` (mặc định `user`). `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- `team.py status <ID>` báo `verified` và G4 đã duyệt (hoặc G4 tắt).
- `/team:release` báo thiếu As-Built, CHANGELOG hay tài liệu người dùng.
- Sau một vòng rework đã accepted lại: viết lại As-Built cho commit mới.

Không dùng khi:
- Chưa accepted → `/team:verify`. As-Built viết trước nghiệm thu là đoán.
- Việc chỉ là tài liệu (playbook `docs-only`, `client-docs`): team-leader giao thẳng writer theo playbook, không có diff để so.
- Muốn sửa code cho khớp tài liệu → đó là rework, không phải As-Built.

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `structure.docs` (nơi tài liệu người dùng), `cmd.*` (mọi lệnh hiện cho người đọc chép từ đây, không gõ theo trí nhớ), `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `gates.G4_uat`.
3. Mẫu PR của dự án: `.github/PULL_REQUEST_TEMPLATE.md` (nếu có) — `pr-body.md` điền đúng các mục của nó; không có thì dùng `<kit>/templates/project/github/PULL_REQUEST_TEMPLATE.md`.
4. Định dạng CHANGELOG hiện có: Read 30 dòng đầu `CHANGELOG.md` (Keep a Changelog hay kiểu riêng). Theo kiểu đã có; chưa có file thì tạo theo Keep a Changelog. `CHANGELOG.md` ở gốc luôn được tạo (K-05).

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/spec.md`, `design.md` (cỡ M/L), `acceptance.md`, `review-NN.md`, `tasks.md`.
- `docs/team/features/<ID>/diff.patch` — do `/team:build` ghi ở bước cuối (Write). Thiếu hoặc rỗng → trả `NEEDS_CONTEXT`, nêu "cần diff.patch từ /team:build".
- Kiểm: `python3 "<kit>/scripts/team.py" status <ID>` báo `verified`; `grep -E '^Verdict: accepted$' acceptance.md` đúng một dòng. Không đạt → dừng, trả lại.
- G4 bật: 20 dòng đầu `acceptance.md` có `Approved-by: <tên> <YYYY-MM-DD>`. Không có → dừng; không viết As-Built cho bản chưa được người nhận.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature, stage: "asbuilt", agent: "writer", started_at}.
2. **Gom nợ sau G4 của qa.** Grep `acceptance.md` tìm các dòng "chủ: writer, sau G4" và lệnh kiểm qa để lại. Mỗi dòng thành một việc của lần chạy này. Checkpoint: số việc gom được ghi ra; cuối cùng số việc đóng phải bằng.
3. **Bảng thiết kế ↔ thực tế.** Với từng mục của `design.md` (8 mục) và từng dòng touchpoints: Grep đường dẫn trong `diff.patch`, đọc đoạn đổi, rồi ghi một dòng `mục | đúng thiết kế / khác: … | file:line | lý do`. Lý do chỉ lấy từ `review-NN.md`, ghi chú trong `tasks.md`, dòng `DESIGN_CONFLICT`; không có thì ghi "lý do: không ghi nhận" — không bịa. File có trong diff mà không có trong touchpoints → một dòng riêng, dẫn `review-NN` đã chấp nhận nó. Cỡ S không có `design.md`: so với tiêu chí trong `spec.md`. Cách đọc diff và mẫu dòng: `${CLAUDE_SKILL_DIR}/references/writing-rules.md`.
4. **Điểm quyết định — hành vi ngoài spec.** Diff có hành vi không có trong `spec.md` hay `acceptance.md` (endpoint mới, cờ cấu hình mới, thay đổi mặc định) → DỪNG, trả team-leader (cần analyst `--amend` hoặc người quyết). Không mô tả nó như tính năng.
5. **Release notes** cho người đọc trong `--audience`: đổi gì, ai bị ảnh hưởng, cần làm gì (đổi cấu hình, cửa sổ migration, phiên bản API mới — lấy từ design mục 3 và 6). Mỗi câu dẫn AC-n hoặc file. Thuật ngữ nội bộ (task, review, STD) chỉ nằm trong As-Built, không trong release notes.
6. **CHANGELOG.** Edit `CHANGELOG.md`: thêm dòng dưới `## [Unreleased]` theo nhóm Added / Changed / Deprecated / Removed / Fixed / Security; mỗi dòng một thay đổi người dùng thấy được, kết thúc bằng mã feature `(<ID>)`. Thay đổi phá vỡ → nhóm Changed/Removed và trỏ hướng dẫn di trú. KHÔNG đổi `[Unreleased]` thành số phiên bản — việc đó của `/team:release`.
7. **Tài liệu người dùng.** Grep README và `structure.docs` tìm tên lệnh, cờ, hành vi vừa đổi; sửa đúng các đoạn đó, viết ở thì hiện tại ("lệnh X xuất Y"), không viết lịch sử thay đổi. Lệnh hiện cho người đọc chép từ giá trị `cmd.*`. README đã đúng → ghi "README: không đổi (grep `<chuỗi>` khớp hành vi AC-n)".
8. **pr-body.md.** Write `docs/team/features/<ID>/pr-body.md` theo mẫu PR: `## Feature` (mã, đường dẫn design/asbuilt/acceptance, Verdict), `## Vì sao` (dẫn spec), `## Đổi gì` (hành vi + file chính; khác thiết kế thì dẫn As-Built), `## Cách kiểm` (lệnh + mã thoát chép từ `acceptance.md`, không tạo khẳng định mới), rồi Review checklist của mẫu. `/team:pr` grep đúng bốn tiêu đề này.
9. **Đóng nợ sau G4.** Với mỗi việc ở bước 2: làm xong rồi chạy lại lệnh kiểm qa để lại (chỉ lệnh chỉ-đọc như `grep`); ghi kết quả vào mục `## Nợ sau G4` của `asbuilt.md`. Lệnh cần chạy code → ghi "để /team:release kiểm".
10. **Viết `asbuilt.md`** từ `<kit>/templates/artifacts/asbuilt.md` (Write): bảng bước 3, release notes, mục CHANGELOG đã thêm, mục nợ sau G4. Giữ chỗ cho `Approved-by-prod:` trong 20 dòng đầu; KHÔNG tự điền nó, không viết `Released:` (devops viết sau prod).
11. **Kiểm cuối.** `git status --short`: chỉ `docs/**`, `CHANGELOG.md`, `README.md` đổi (role-policy của writer). Grep `pr-body.md` bốn tiêu đề; grep CHANGELOG có `(<ID>)`.
12. **Trả** team-leader ≤ 10 dòng, dòng đầu `writer -> team-leader | <ID> | ASBUILT` (hoặc `NEEDS_CONTEXT`, `NEEDS_ANSWER`).

## Đầu ra
- `docs/team/features/<ID>/asbuilt.md`, `docs/team/features/<ID>/pr-body.md`.
- `CHANGELOG.md` (mục dưới `[Unreleased]`); `README.md` hoặc file dưới `structure.docs` khi hành vi đổi.
- Tin trả mẫu:
  ```
  writer -> team-leader | FEAT-014 | ASBUILT
  File: docs/team/features/FEAT-014/{asbuilt,pr-body}.md, CHANGELOG.md, docs/auth.md
  So thiết kế: 8 mục + 6 touchpoints; khác 1 (mục 3: mã lỗi 409→422, src/auth/otp.py:41, lý do review-02)
  CHANGELOG: Added 1, Changed 1 dưới [Unreleased] (FEAT-014)
  Nợ sau G4 từ acceptance: 2/2 đóng (CHANGELOG, docs/auth.md)
  Cần người đọc lại: release notes mục "Cần làm gì" (đổi cấu hình OTP_TTL)
  Tiếp: /team:pr FEAT-014
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Code đúng thiết kế, ghi một dòng là đủ" | Bảng đủ từng mục thiết kế và từng touchpoint; mỗi dòng có `file:line`. |
| "Lý do khác thiết kế chắc là vì hiệu năng" | Chỉ lấy lý do từ `review-NN`, `tasks.md`; không có thì "không ghi nhận". |
| "Release notes viết kỹ thuật cho nhanh" | Viết cho người đọc trong `--audience`; chi tiết kỹ thuật ở As-Built. |
| "Ghi luôn tính năng sắp làm cho đủ ý" | Chỉ cái có trong diff và acceptance. |
| "README chắc vẫn đúng" | Grep chuỗi hành vi đổi; ghi kết quả grep. |
| "Gõ lệnh cài đặt theo trí nhớ" | Chép giá trị `cmd.*` trong profile. |
| "Đổi luôn `[Unreleased]` thành 1.4.0" | Việc của `/team:release` (devops). |
| "Thêm `Approved-by-prod:` cho đủ thủ tục" | Chỉ người điền (G5 luôn là người). |
| "Diff có endpoint mới, mô tả như tính năng" | Hành vi ngoài spec → dừng, trả team-leader. |

## Dấu hiệu sai
- Bảng thiết kế ↔ thực tế ít dòng hơn số mục thiết kế cộng số touchpoints.
- Dòng "khác" không có `file:line` hoặc đoạn diff làm căn cứ.
- Câu release notes không truy được về AC-n hay file nào.
- Dòng CHANGELOG thiếu mã feature; `[Unreleased]` đã bị đổi thành số phiên bản.
- README nhắc một lệnh không có trong `cmd.*`.
- `pr-body.md` thiếu một trong bốn tiêu đề; mục "Cách kiểm" có lệnh không có trong `acceptance.md`.
- writer viết `Released:` hay `Approved-by-prod:`; file bị ghi ngoài `docs/**`, `CHANGELOG.md`, `README.md`.

## Kiểm chứng
- [ ] Dán `grep -E '^Verdict: accepted$' acceptance.md` (một dòng) và dòng `Approved-by:` của G4 (khi G4 bật).
- [ ] Bảng thiết kế ↔ thực tế: số dòng = mục thiết kế + touchpoints; mỗi dòng "khác" có đoạn diff trích.
- [ ] Đoạn diff của `CHANGELOG.md` dưới `## [Unreleased]` được dán, có `(<ID>)`.
- [ ] Mỗi dòng "chủ: writer, sau G4" của qa có kết quả đóng trong `## Nợ sau G4`.
- [ ] `grep -cE '^## (Feature|Vì sao|Đổi gì|Cách kiểm)$' pr-body.md` = 4 được dán.
- [ ] `git status --short` chỉ có file trong vùng ghi của writer.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/writing-rules.md` — đọc diff theo mục thiết kế, mẫu dòng bảng, nhóm CHANGELOG, quy tắc câu có nguồn. Mở ở bước 3 và 5.
- Agent `writer`; `<kit>/templates/artifacts/asbuilt.md`; mẫu PR `<kit>/templates/project/github/PULL_REQUEST_TEMPLATE.md`.
- `/team:verify` (trước), `/team:pr` (dùng `pr-body.md`), `/team:release` (đổi `[Unreleased]` thành phiên bản, kiểm lại nợ sau G4).
- `handbook/STD.md`: STD-DOC-1, STD-DOC-2, STD-DOC-3, STD-SEC-6, STD-GIT-7.
