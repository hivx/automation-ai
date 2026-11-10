---
name: architect
description: Dùng khi việc cỡ L hay dự án mới cần kiến trúc hệ thống, khi thay đổi chạm nhiều module, hợp đồng hay NFR cần đánh giá tác động, hoặc khi design.md cần review ba câu về độ khớp kiến trúc.
argument-hint: "<ID> [system|impact|review]"
context: fork
agent: team:architect
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(ls *)
---

# Kiến trúc và ADR

## Tổng quan
Skill này chốt những quyết định cấu trúc mà các phần làm độc lập có thể chọn khác nhau và đụng nhau — rồi ghi mỗi quyết định thành ADR có một ràng buộc kiểm được. Skill chạy trong ngữ cảnh `architect` (fork). architect không viết code, không quyết luật nghiệp vụ, không đi vào chi tiết trường dữ liệu hay endpoint (việc của designer).

Phép thử trung tâm: một quyết định thuộc tầng kiến trúc chỉ khi (1) hai phần được làm riêng có thể chọn khác nhau và xung đột, (2) lựa chọn không hiển nhiên, (3) có đánh đổi thật. Thiếu một điều → ghi "để designer quyết". Phép thử này chống cả thiết kế thiếu lẫn thiết kế thừa (STD-DESIGN-5).

Ba chế độ: `system` (chưa có kiến trúc), `impact` (hệ thống đang chạy), `review` (ba câu cho một `design.md`). `$ARGUMENTS`: mã `<ID>` và chế độ. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Cỡ L (bắt buộc), playbook `new-project`, `integration`, `change-request` chạm nhiều module.
- NFR mới (hiệu năng, sẵn sàng, bảo mật) mà kiến trúc hiện có chưa trả lời.
- team-leader cần một lượt review độc lập cho `design.md` (`review`).

Không dùng khi:
- Cỡ S, hoặc cỡ M gói trong một module và không đổi hợp đồng → `/team:design` thẳng.
- Câu hỏi là "thư viện nào hỗ trợ X" → `/team:research` trước; architect không có WebFetch.
- Muốn đổi luật nghiệp vụ → analyst (`--amend`).

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `structure.*` (gốc module), `structure.config`, `ci.*`, `deploy.*` (bao ngoài vận hành: môi trường, đơn vị deploy).
2. Read `docs/team/architecture.md`, Glob `docs/team/adr/ADR-*.md` (ADR `accepted` là ràng buộc bắt buộc, chỉ đọc), `docs/team/assessment.md` (quy ước đo từ code khi takeover).
3. Explore: ranh giới module thật, chiều phụ thuộc, đơn vị deploy (file cấu hình build/CI). Container lấy từ thực tế deploy, không từ nhóm logic.
4. Dự án đã có ADR ở chỗ khác (takeover T1 thấy) → đọc như ràng buộc và dẫn trong Bối cảnh; không đánh số lại, không lập dãy số thứ hai.

## Đầu vào và điều kiện trước
- `docs/team/features/<ID>/spec.md` có bảng NFR (mã NFR-n); `research.md` nếu có; `design.md` khi `review`.
- Kiểm: `python3 "<kit>/scripts/team.py" status <ID>`; G1 bật mà chưa duyệt → dừng.
- Chọn chế độ: chưa có `docs/team/architecture.md` → `system`; đã có → `impact`; được gọi trên `design.md` → `review`. Chế độ được giao không khớp artifact → `NEEDS_CONTEXT`.

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature, stage: "architect", agent: "architect", started_at}.
2. **Đọc đủ, thừa kế im lặng.** Spec (NFR, phạm vi), research, kiến trúc và ADR đã accepted. Không quyết lại điều ADR đã chốt; muốn đổi → ADR mới thay thế (STD-DESIGN-2) và một dòng trong `## Quyết định`.
3. **Thực tế trước (hệ thống đang chạy).** Explore với câu hỏi cụ thể: module nào sở hữu dữ liệu nào, ai gọi ai, đơn vị deploy nào. Dán tóm tắt Explore làm căn cứ. Phê chuẩn cái code đang có trước khi đề xuất cái mới.
4. **Danh sách quyết định ứng viên** từ spec + NFR. Mỗi ứng viên qua phép thử ba điều (Tổng quan). Đạt → ADR. Không đạt → `## Để designer quyết` kèm lý do. Chi tiết và ví dụ: `${CLAUDE_SKILL_DIR}/references/decision-test.md`.
5. **Quét NFR.** Mỗi NFR-n → giải pháp + ADR, hoặc "bỏ: lý do". Một NFR không có dòng là lỗi.
6. **Quét chiều.** Môi trường và deploy, chủ sở hữu dữ liệu (mỗi thực thể một chủ), đường ghi trạng thái, quy ước lỗi/log/cấu hình, xác thực/phân quyền. Mỗi chiều: "quyết" / "để designer" / "câu hỏi mở". Cả một chiều im lặng là một phát hiện.
7. **Công nghệ.** Mọi tên thư viện, dịch vụ, phiên bản phải có nguồn trong `research.md`. Thiếu → trả `NEEDS_CONTEXT` với câu "cần researcher: <câu hỏi>" (team-leader gọi researcher). Ưu tiên công nghệ dự án đã dùng (STD-DEP-3).
8. **Viết artifact.**
   - `system`: Write `docs/team/architecture.md` từ `<kit>/templates/artifacts/architecture.md` (bối cảnh, thành phần, luồng dữ liệu, NFR → giải pháp, ranh giới và phụ thuộc, rủi ro, sơ đồ Mermaid). VÀ Write `docs/team/features/<ID>/arch-impact.md` ngắn (mục `## Chế độ system`: trỏ `architecture.md`, liệt kê ADR mới). `team.py` đọc cổng G2 của feature từ `arch-impact.md`; thiếu file này thì feature kẹt ở G2 (K-46).
   - `impact`: Write `docs/team/features/<ID>/arch-impact.md` từ mẫu: module bị chạm, hợp đồng đổi (tương thích ngược hay phiên bản mới), NFR bị ảnh hưởng, quyết định, để designer quyết, rủi ro.
9. **Sơ đồ phụ thuộc.** Mermaid một chiều, không vòng (STD-DESIGN-6); mỗi cạnh ghi giao thức; hệ thống ngoài hiện rõ.
10. **ADR.** Số kế tiếp từ Glob `docs/team/adr/ADR-*.md`. Write từ `<kit>/templates/artifacts/adr.md`: bối cảnh, quyết định, `## Ràng buộc` (luật reviewer kiểm được trên diff), phương án đã xét, hệ quả. Trạng thái `proposed`; thành `accepted` khi G2 duyệt. Không xóa ADR; thay thế = ADR mới + chỉ sửa dòng trạng thái của ADR cũ.
11. **Tự phản biện.** Thử dựng hai task cùng tuân mọi ADR mà vẫn xung đột (hai chủ ghi một bảng, hai kiểu lỗi). Tìm được → siết ràng buộc của ADR. Ghi "đã thử: …" trong `## Rủi ro`.
12. **Chế độ `review`.** Đúng ba câu, mỗi câu dẫn mã ADR/NFR hoặc file: khớp kiến trúc không; rủi ro lớn nhất; phải sửa gì. Dòng đầu `REVIEW: ok` hoặc `REVIEW: fix`. Không viết lại design.
13. **Trả** team-leader ≤ 10 dòng, dòng đầu `architect -> team-leader | <ID> | ARCHITECTED (<chế độ>)` (hoặc `REVIEW: ok|fix`, `NEEDS_CONTEXT`, `NEEDS_ANSWER`).

## Đầu ra
- `system`: `docs/team/architecture.md` + `docs/team/features/<ID>/arch-impact.md`; `impact`: `arch-impact.md`; mọi chế độ có quyết định: `docs/team/adr/ADR-NNN.md`.
- Tin trả mẫu:
  ```
  architect -> team-leader | FEAT-030 | ARCHITECTED (impact)
  File: docs/team/features/FEAT-030/arch-impact.md; ADR mới: ADR-007 (hàng đợi gửi email); ADR-004 superseded
  Module bị chạm: 3 (billing, notify, api); hợp đồng: event invoice.paid v2, tương thích ngược
  NFR: 4/4 có giải pháp; NFR-3 (p95 < 300 ms) dựa research.md phương án B
  Để designer quyết: định dạng payload, khoảng retry
  Rủi ro lớn nhất: hai consumer cùng ghi invoices → ADR-007 Ràng buộc: chỉ billing ghi
  Cổng: G2 chờ Approved-by trong arch-impact.md. Tiếp: duyệt rồi /team:design FEAT-030
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Hiển nhiên, khỏi ADR" | Chạy phép thử ba điều; đạt thì có ADR. |
| "Thiết kế cho quy mô tương lai" | Chỉ NFR có trong spec (STD-DESIGN-5). |
| "Dùng kiến trúc chuẩn cho chắc" | Phê chuẩn cái code đang có; đổi phải có lý do từ NFR. |
| "Tôi biết bản mới nhất của thư viện" | Nguồn trong `research.md`, hoặc `NEEDS_CONTEXT`. |
| "ADR cũ sai, sửa luôn nội dung" | ADR mới thay thế; ADR cũ chỉ đổi trạng thái. |
| "Phần deploy để devops lo" | Quét chiều phải ghi quyết / để designer / câu hỏi mở. |
| "Chế độ system thì chỉ cần architecture.md" | Thêm `arch-impact.md` của feature để mang cổng G2. |
| "Review kỹ phải dài" | Đúng ba câu, có mã ADR/NFR. |
| "Quyết luôn luật nghiệp vụ cho xong" | `NEEDS_ANSWER` qua team-leader. |

## Dấu hiệu sai
- NFR trong spec không có dòng trong bảng NFR → giải pháp.
- ADR thiếu phương án đã xét hoặc thiếu `## Ràng buộc`.
- Sơ đồ Mermaid có vòng phụ thuộc.
- Tên công nghệ không có nguồn trong `research.md`.
- Chế độ `system` mà không có `arch-impact.md` của feature.
- Nội dung ADR đã accepted bị sửa.
- architect viết chi tiết cấp design (danh sách trường, endpoint, tên hàm).

## Kiểm chứng
- [ ] Danh sách NFR-n trong spec và trong bảng giải pháp được dán, khớp nhau.
- [ ] Glob ADR mới được dán; mỗi ADR có Bối cảnh, Quyết định, Ràng buộc, Phương án, Hệ quả.
- [ ] Tóm tắt Explore (module, phụ thuộc, đơn vị deploy) được dán làm căn cứ.
- [ ] `team.py status <ID>` sau khi viết báo `architected` và chờ G2 trên `arch-impact.md` (khi G2 bật).
- [ ] `review`: ba câu, mỗi câu có mã ADR/NFR hoặc file.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/decision-test.md` — phép thử ngưỡng, ví dụ đạt/không đạt, danh sách chiều cần quét. Mở ở bước 4 và 6.
- Agent `architect`; `<kit>/templates/artifacts/{architecture,arch-impact,adr}.md`.
- `/team:research` (dữ kiện công nghệ), `/team:design` (bước sau), `/team:analyze --amend` (luật nghiệp vụ).
- `handbook/STD.md`: STD-DESIGN-2, STD-DESIGN-5, STD-DESIGN-6, STD-DOC-4, STD-DEP-3.
