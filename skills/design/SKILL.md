---
name: design
description: Dùng khi spec đã duyệt cần thiết kế chi tiết (dữ liệu, API, luồng, quyền, migration, touchpoints, test plan) trước khi lập kế hoạch, hoặc khi refactor cần bản thiết kế ngắn chứng minh hành vi không đổi.
argument-hint: "<ID> [--short]"
context: fork
agent: team:designer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

# Thiết kế chi tiết

## Tổng quan
Skill này viết `design.md` đủ cụ thể để tech-lead chia task mà không phải đoán, dev biết chính xác file nào chạm, và qa biết kiểm từng tiêu chí bằng test nào. Skill chạy trong ngữ cảnh `designer` (fork). designer theo kiến trúc đã duyệt (dẫn mã ADR), theo quy ước code đang có, và không quyết luật nghiệp vụ. Chia task là việc của tech-lead (`/team:plan`); designer chỉ liệt kê touchpoints.

Thứ tự viết: hợp đồng trước luồng. Mọi hành vi quan sát được của một điểm vào công khai (mã lỗi, thông điệp, thứ tự, giá trị mặc định) đều là hợp đồng, vì sẽ có người phụ thuộc vào nó. Thêm vào thì an toàn hơn sửa; phá vỡ thì cần phiên bản mới và hướng dẫn di trú (STD-DESIGN-3).

`$ARGUMENTS`: mã `<ID>`; `--short` cho playbook refactor (mục 1, 7, 8 + cách chứng minh hành vi không đổi). `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Cỡ M/L sau analyze (và architect với cỡ L), trước `/team:plan`.
- Playbook `refactor` (`--short`), `data-migration` (mapping, rollback; G2b bật), `integration` (hợp đồng, retry, idempotency).
- qa trả `design-defect`: viết lại phần thiết kế sai, rồi plan/build lại phần bị ảnh hưởng.

Không dùng khi:
- Cỡ S: tiêu chí trong spec đủ cho một task → `/team:build` thẳng.
- Cần quyết cấu trúc nhiều module hay NFR mới → `/team:architect` trước.
- Câu hỏi là luật nghiệp vụ → `NEEDS_ANSWER` về team-leader, không đoán trong design.

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `structure.*` (`src`, `tests`, `allowed_new_file_roots`), `naming.*` (file, class, function, `test_file`), `protected_paths`, `cmd.test_one` (chỉ có chỗ thay `{file}`), `cmd.migrate`, `ui`.
2. Explore (câu hỏi cụ thể): kiểu lỗi đang dùng, kiểu phân trang, nơi kiểm quyền, cách đọc cấu hình, bố cục test hiện có, file và dữ liệu sẽ bị chạm. Tra cache trước: `bash "<kit>/scripts/explore-cache.sh" <thư mục>`; `HIT` → đọc file cache.
3. Read `docs/team/architecture.md` / `arch-impact.md` và ADR liên quan (cỡ L): ràng buộc của ADR là luật của design.

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/spec.md` (tiêu chí AC-n, NFR, DoD); `research.md` nếu có; `arch-impact.md`/`architecture.md` khi cỡ L hoặc playbook có architect.
- `--short` (refactor): `intake.md` + mục nợ trong `docs/team/debt.md` là đủ; chuỗi refactor không có spec (ADJ-26).
- Kiểm: `python3 "<kit>/scripts/team.py" status <ID>`; G1 bật mà chưa duyệt, hoặc có kiến trúc mà G2 chưa duyệt → dừng.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature, stage: "design", agent: "designer", started_at}.
2. **Giả định trước khi viết.** Liệt kê điều đang giả định. Giả định về nghiệp vụ → ghi `questions.md` (2–4 lựa chọn, khuyến nghị, hậu quả) và trả `NEEDS_ANSWER`. Giả định kỹ thuật ở chế độ decide → `## Assumptions decided by the team` (chọn gì / vì sao / phương án khác / sửa thế nào nếu sai).
3. **Mục 1 Bối cảnh:** vấn đề, phạm vi trong/ngoài (chép từ spec), mã ADR phải tuân.
4. **Mục 3 Hợp đồng (viết trước mục 2, 4):** mỗi điểm vào công khai: đầu vào, đầu ra, lỗi (một kiểu, theo code hiện có), phiên bản. Đánh dấu hành vi nào là hợp đồng. Đổi thì ưu tiên thêm trường tùy chọn; phá vỡ → phiên bản mới + hướng dẫn di trú (STD-DOC-7).
5. **Mục 2 Dữ liệu:** thực thể, trường, ràng buộc, chỉ mục theo cách truy cập; chủ sở hữu theo ADR. Không thêm trường "dự phòng" (STD-DESIGN-5).
6. **Mục 4 Luồng:** đường thuận và đường lỗi cho từng tiêu chí; mọi lời gọi ra ngoài có timeout (STD-ERR-5) và kết cục thành công / thất bại / không rõ.
7. **Tích hợp (playbook integration hoặc gọi API ngoài):** khóa idempotency suy từ ý định (không theo từng lần thử); giành quyền nguyên tử bằng ràng buộc duy nhất (không kiểm-rồi-chèn); cùng khóa khác nội dung → lỗi rõ ràng; chính sách cho bản trùng đang chạy; thời gian giữ khóa ≥ đường retry dài nhất. Chi tiết: `${CLAUDE_SKILL_DIR}/references/contracts.md`.
8. **Mục 5 Quyền:** kiểm đầu vào ở biên, kiểm quyền phía server (STD-SEC-4); phản hồi bên thứ ba coi là không tin cậy.
9. **Mục 6 Migration và rollback:** có `cmd.migrate` và đổi dữ liệu → lên, xuống, đối soát số lượng (STD-OPS-2, STD-OPS-3); bảng lớn chia lô; điều kiện kích hoạt rollback và tiêu chí thành công. designer chỉ lập kế hoạch; dev chạy trên bản sao, qa chạy lên/xuống/lên. Không có thay đổi dữ liệu → ghi "không có".
10. **Quan sát (STD-OPS-5):** một log hoặc metric cho mỗi đường mới quan trọng, không dữ liệu nhạy cảm — để `/team:release` chứng minh tính năng chạy trên prod.
11. **Mục 7 Touchpoints:** đường dẫn thật, "sửa" (Glob thấy file) hoặc "mới" (nằm dưới `structure.allowed_new_file_roots`); file test theo `structure.tests` và `naming.test_file`. Checkpoint máy: dán từng đường dẫn mới cạnh gốc cho phép mà nó khớp; không đường dẫn nào khớp `protected_paths`. Cột ghi chú nói vì sao chạm — không ghi số task.
12. **Mục 8 Test plan:** mỗi AC-n và mỗi NFR có "cách kiểm" → ≥ 1 dòng `tiêu chí | file test::tên | loại | đường lỗi/biên`. Tiêu chí có đầu vào → ít nhất một dòng biên hoặc lỗi (qa sẽ chạy nó). Lệnh chỉ nêu bằng tên khe (`cmd.test_one`), không gõ lệnh stack.
13. **`--short` (refactor):** mục 1, 7, 8 và mục "Cách chứng minh hành vi không đổi": `cmd.test` trước == sau (số test và tên test), lint/typecheck sạch, một loại dọn dẹp. Nơi không có test phủ → thêm test đặc tả (characterization) là task đầu, trước mọi thay đổi.
14. **Tự đối chiếu (điểm quyết định).** Mỗi mục dẫn mã ADR mình tuân. Design không thể thỏa tiêu chí nếu giữ ADR → `DESIGN_CONFLICT` về team-leader; không lặng lẽ đổi kiến trúc (STD-DESIGN-2).
15. **Viết** `docs/team/features/<ID>/design.md` từ `<kit>/templates/artifacts/design.md` (Write).
16. **Trả** team-leader ≤ 10 dòng, dòng đầu `designer -> team-leader | <ID> | DESIGNED` (hoặc `DESIGN_CONFLICT`, `NEEDS_ANSWER`).

## Đầu ra
- `docs/team/features/<ID>/design.md` (8 mục; `--short`: 1, 7, 8 + chứng minh hành vi không đổi); `questions.md` khi cần hỏi.
- Tin trả mẫu:
  ```
  designer -> team-leader | FEAT-014 | DESIGNED
  File: docs/team/features/FEAT-014/design.md (8 mục; tuân ADR-003, ADR-007)
  Touchpoints: 6 (4 sửa, 2 mới dưới src/auth/, tests/auth/ — thuộc allowed_new_file_roots); 0 trong protected_paths
  Hợp đồng: POST /otp/verify thêm mã lỗi OTP_EXPIRED (thêm, tương thích ngược)
  Dữ liệu: +1 cột otp_expires_at; migration 0007 lên/xuống + đối soát số hàng
  Test plan: 5/5 AC có test, 3 có đường lỗi/biên
  Giả định đã quyết: 1 (TTL đọc từ cấu hình); câu hỏi nghiệp vụ: 0. G2b tắt → Tiếp: /team:plan FEAT-014
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Viết luồng trước, API tính sau" | Hợp đồng (mục 3) trước luồng. |
| "Lỗi trả kiểu nào cũng được" | Một kiểu, theo code hiện có (Explore). |
| "Hành vi không ghi trong tài liệu thì chẳng ai dùng" | Liệt kê hành vi quan sát được là hợp đồng. |
| "Thêm phiên bản API song song cho chắc" | Thêm trường tùy chọn; phiên bản mới chỉ khi phá vỡ. |
| "Retry an toàn vì đã có header idempotency" | Khóa phải được lưu nguyên tử; thiết kế cả bản trùng đang chạy. |
| "Dev tự tìm file" | Đường dẫn thật trong touchpoints. |
| "Migration đơn giản, khỏi rollback" | Luôn có xuống và đối soát. |
| "Luật nghiệp vụ chắc là vậy" | `NEEDS_ANSWER`, không đoán. |
| "Thêm trường dự phòng" | Chỉ điều spec cần. |

## Dấu hiệu sai
- Điểm vào công khai không có danh sách lỗi.
- Touchpoint không tồn tại mà cũng không nằm dưới gốc cho phép; touchpoint khớp `protected_paths`.
- AC không có dòng test; dòng test ghi lệnh thay vì file test.
- Migration không có chiều xuống hay đối soát.
- Idempotency kiểu kiểm-rồi-chèn.
- Design chép lại kiến trúc thay vì dẫn mã ADR; design có số task.
- Luật nghiệp vụ được quyết trong design.

## Kiểm chứng
- [ ] Đủ mục (dán `grep -c '^## [1-8]\.' design.md`), hoặc 3 mục + chứng minh khi `--short`.
- [ ] Danh sách AC-n trong spec và trong test plan được dán, khớp nhau.
- [ ] Mỗi đường dẫn mới dán cạnh gốc cho phép; dòng "0 trong protected_paths".
- [ ] Tóm tắt Explore (quy ước lỗi, quyền, test) được dán làm căn cứ.
- [ ] Hợp đồng phá vỡ có phiên bản + dòng di trú, hoặc ghi "không có thay đổi phá vỡ".

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/contracts.md` — hợp đồng, lỗi, idempotency, migration theo lô, mẫu dòng test plan. Mở ở bước 4, 7, 9, 12.
- Agent `designer`; `<kit>/templates/artifacts/design.md`.
- `/team:architect` (trước, cỡ L), `/team:plan` (sau), `/team:clean` (refactor).
- `handbook/STD.md`: STD-DESIGN-1, STD-DESIGN-3, STD-DESIGN-5, STD-ERR-5, STD-SEC-4, STD-OPS-2, STD-OPS-3, STD-OPS-5.
