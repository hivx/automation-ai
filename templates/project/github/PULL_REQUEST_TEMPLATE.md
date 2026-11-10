## Feature
- Mã: <!-- FEAT-NNN / BUG-NNN / CHG-NNN -->
- Thiết kế: `docs/team/features/<ID>/design.md`
- As-Built: `docs/team/features/<ID>/asbuilt.md`
- Nghiệm thu: `docs/team/features/<ID>/acceptance.md` — Verdict: <!-- accepted / rework / design-defect -->

## Vì sao
<!-- vấn đề hoặc nhu cầu, một hai câu; dẫn spec.md -->

## Đổi gì
<!-- hành vi và file chính; khác thiết kế thì dẫn asbuilt.md -->

## Cách kiểm
<!-- lệnh đã chạy và đầu ra (mã thoát), lấy từ acceptance.md -->

## Review checklist (handbook/STD.md)
- [ ] 1. Làm đúng và đủ spec, không thừa (STD-DESIGN-5, STD-TEST-2)
- [ ] 2. Chỉ trong touchpoints; file mới đúng chỗ (STD-DESIGN-1, STD-STRUCT-1, STD-STRUCT-2)
- [ ] 3. Test hỏng trước; phủ biên và lỗi; không skip/xfail/only (STD-TEST-1, STD-TEST-8, STD-TEST-4)
- [ ] 4. Không sửa test cho khớp hành vi sai; test độc lập (STD-TEST-5, STD-TEST-6)
- [ ] 5. Xử lý lỗi; kiểm đầu vào; gọi ngoài có timeout (STD-ERR-1, STD-ERR-2, STD-ERR-5)
- [ ] 6. Không secret, không injection, có phân quyền (STD-SEC-1, STD-SEC-3, STD-SEC-4, STD-SEC-6)
- [ ] 7. Hợp đồng tương thích hoặc di trú lùi được (STD-DESIGN-3, STD-OPS-2)
- [ ] 8. Tên, cấu trúc, phong cách theo profile; không code chết (STD-NAME-1, STD-NAME-2, STD-STYLE-4, STD-STYLE-5)
- [ ] 9. Phụ thuộc mới có lý do (STD-DEP-1, STD-DEP-3, STD-DEP-5)
- [ ] 10. Commit, nhánh, PR đúng chuẩn; tài liệu đi cùng (STD-NAME-4, STD-NAME-5, STD-GIT-1, STD-DOC-2)
