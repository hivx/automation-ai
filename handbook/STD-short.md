<!-- GENERATED — do not edit; run scripts/gen-handbook-short.py -->
# STD-short — bản rút gọn của handbook/STD.md

## Quy tắc mức 2–3 (mức trong ngoặc)
- STD-STRUCT-1 (3) Chỉ tạo file mới dưới các thư mục trong `structure.allowed_new_file_roots`.
- STD-STRUCT-2 (2) Đặt mã nguồn trong `structure.src` và test trong `structure.tests` (hoặc cạnh mã khi giá trị là `colocated`).
- STD-STRUCT-3 (2) Theo bố cục module sẵn có; không tạo thư mục hay tầng song song cho cùng một mục đích.
- STD-STRUCT-4 (3) Không sửa trong `.git/`, thư mục sinh ra khi build hoặc thư mục vendored.
- STD-STRUCT-5 (2) Giữ mỗi file một trách nhiệm chính; tách file khi nó gánh hai mục đích không liên quan.
- STD-STRUCT-6 (3) Chạy kiểm cấu trúc trước khi kết thúc một task build.
- STD-STRUCT-7 (2) Đặt script tiện ích trong `structure.scripts` và file cấu hình ở các vị trí `structure.config`.
- STD-NAME-1 (2) Đặt tên file theo `naming.file`.
- STD-NAME-2 (2) Đặt tên lớp/kiểu, hàm, hằng theo `naming.class`, `naming.function`, `naming.constant`.
- STD-NAME-3 (3) Đặt tên file test theo `naming.test_file`.
- STD-NAME-4 (3) Đặt tên nhánh `team/<ID>-<slug>`.
- STD-NAME-5 (3) Viết commit message dạng `type(scope): description (<ID>)`.
- STD-NAME-6 (2) Dùng tên nói lên ý nghĩa nghiệp vụ; không viết tắt ngoài `docs/team/glossary.md`.
- STD-NAME-7 (2) Giữ một quy ước đặt tên trong một module; không trộn hai quy ước.
- STD-STYLE-1 (3) Định dạng mọi file đã sửa bằng formatter của profile.
- STD-STYLE-2 (3) Để `cmd.lint` sạch trước khi commit.
- STD-STYLE-3 (3) Để `cmd.typecheck` sạch khi profile có khe này.
- STD-STYLE-4 (2) Theo phong cách sẵn có của file đang sửa; không đổi phong cách hàng loạt trong PR tính năng.
- STD-STYLE-5 (2) Không để code chết, code bị comment-out hay log gỡ lỗi trong diff.
- STD-STYLE-7 (2) Không tắt một luật lint/typecheck tại chỗ mà không ghi lý do ngay cạnh.
- STD-DESIGN-1 (2) Chỉ sửa trong touchpoints của task; cần sửa ngoài thì dừng và báo `DESIGN_CONFLICT`.
- STD-DESIGN-2 (2) Theo kiến trúc và ADR đã duyệt; đổi kiến trúc phải có ADR mới.
- STD-DESIGN-3 (2) Giữ hợp đồng API công khai tương thích ngược; phá vỡ thì có phiên bản mới và hướng dẫn di trú.
- STD-DESIGN-4 (2) Tái sử dụng logic đã có thay vì viết trùng.
- STD-DESIGN-5 (2) Chọn giải pháp đơn giản nhất đáp ứng spec; không thêm tính năng hay điểm mở rộng chưa được yêu cầu.
- STD-DESIGN-6 (2) Giữ phụ thuộc giữa các module một chiều; không tạo vòng phụ thuộc.
- STD-DESIGN-7 (2) Đọc giá trị thay đổi theo môi trường từ cấu hình; không ghi cứng trong code.
- STD-TEST-1 (2) Viết test hỏng trước khi sửa code (bắt buộc với bug-fix) và dán đầu ra đỏ.
- STD-TEST-2 (2) Phủ mỗi tiêu chí nghiệm thu bằng ít nhất một test tự động hoặc một bước kiểm có đầu ra.
- STD-TEST-3 (3) Chạy `cmd.test_one` cho test đã đổi trước khi xong task và `cmd.test` trước khi gộp.
- STD-TEST-4 (3) Không dùng skip, xfail hay only để cho xanh — vi phạm là blocker.
- STD-TEST-5 (2) Không sửa assertion cho khớp hành vi sai; chỉ đổi test khi spec đổi.
- STD-TEST-6 (2) Viết test độc lập và lặp lại được: không phụ thuộc thứ tự chạy, giờ thật hay mạng ngoài.
- STD-TEST-7 (2) Ghi test chập chờn vào `docs/team/debt.md` và sửa; không tắt nó.
- STD-TEST-8 (2) Kiểm cả trường hợp biên và đường lỗi, không chỉ đường thuận.
- STD-ERR-1 (2) Không nuốt lỗi; mỗi chỗ bắt lỗi phải xử lý, thêm ngữ cảnh rồi ném tiếp, hoặc ghi rõ vì sao bỏ qua.
- STD-ERR-2 (2) Kiểm tra đầu vào tại ranh giới hệ thống (API, form, file, message).
- STD-ERR-3 (2) Không lộ chi tiết nội bộ (stack trace, truy vấn, đường dẫn) trong thông báo lỗi cho người dùng.
- STD-ERR-4 (2) Ghi log lỗi đủ ngữ cảnh để lần lại (mã yêu cầu, thực thể) và không ghi dữ liệu nhạy cảm.
- STD-ERR-5 (2) Gọi dịch vụ ngoài với timeout, số lần thử lại có giới hạn và thao tác idempotent khi thử lại.
- STD-ERR-6 (2) Dừng ngay lúc khởi động khi cấu hình thiếu hoặc sai; không chạy tiếp với mặc định ngầm.
- STD-ERR-7 (2) Chạy thao tác nhiều bước trên dữ liệu trong transaction hoặc có bước bù trừ.
- STD-GIT-1 (2) Một task một PR nhỏ; khi task được gộp vào nhánh feature, task là một commit riêng review được độc lập.
- STD-GIT-2 (2) Giữ commit nhỏ và nguyên tử; mỗi commit build được và qua test.
- STD-GIT-3 (3) Chỉ push nhánh `team/*`.
- STD-GIT-4 (3) Không force-push và không viết lại lịch sử đã push.
- STD-GIT-5 (2) Không commit file sinh ra, kết quả build hay file riêng của máy; khai chúng trong file ignore.
- STD-GIT-6 (2) Cập nhật từ `config.base_branch` trước khi mở PR; giải xung đột mà không làm mất thay đổi của người khác.
- STD-GIT-7 (2) Viết mô tả PR gồm: vì sao, đổi gì, cách kiểm, mã feature/task.
- STD-CI-1 (3) Chạy lint, typecheck và test của profile trên mọi PR.
- STD-CI-2 (3) Không merge khi CI đỏ.
- STD-CI-3 (2) Không xóa, tắt hay nới một bước kiểm để CI xanh.
- STD-CI-5 (2) Lấy secret từ kho secret của nền CI; không ghi secret trong file workflow.
- STD-CI-6 (3) Mọi lần deploy prod cần một người duyệt.
- STD-CI-7 (2) Ghim phiên bản runner và công cụ để pipeline lặp lại được.
- STD-DOC-1 (2) Có thiết kế trước khi làm và As-Built sau khi làm (thuộc DoD).
- STD-DOC-2 (2) Cập nhật README hoặc tài liệu người dùng trong cùng PR khi hành vi người dùng thấy thay đổi.
- STD-DOC-3 (2) Thêm mục CHANGELOG cho mọi thay đổi được phát hành.
- STD-DOC-4 (2) Ghi mọi quyết định kiến trúc thành ADR có bối cảnh, phương án và hệ quả.
- STD-DOC-7 (2) Mô tả đầu vào, đầu ra và lỗi của mọi API công khai.
- STD-SEC-1 (3) Không commit secret và không chạm `protected_paths`.
- STD-SEC-2 (3) Không đọc file `.env*` hay file secret; dùng biến môi trường được cấp.
- STD-SEC-3 (2) Tham số hóa hoặc escape mọi truy vấn và lệnh dựng từ dữ liệu bên ngoài.
- STD-SEC-4 (2) Kiểm xác thực và phân quyền phía server cho mọi thao tác trên dữ liệu được bảo vệ.
- STD-SEC-6 (2) Không ghi mật khẩu, token hay dữ liệu cá nhân vào log, artifact hay journal.
- STD-SEC-7 (2) Mã hóa dữ liệu nhạy cảm khi truyền và khi lưu theo yêu cầu của spec.
- STD-DEP-1 (2) Ghi lý do cho mỗi phụ thuộc mới trong design hoặc PR (giấy phép, bảo trì, kích thước).
- STD-DEP-2 (3) Không sửa tay lockfile; chỉ cập nhật qua `cmd.install` hoặc trình quản lý gói.
- STD-DEP-3 (2) Không thêm thư viện cho phần việc dưới 50 dòng code.
- STD-DEP-4 (2) Ghim phiên bản phụ thuộc theo cách của hệ sinh thái; không dùng phiên bản trôi nổi cho prod.
- STD-DEP-5 (2) Không thêm phụ thuộc có lỗ hổng nghiêm trọng đã biết hoặc giấy phép không tương thích.
- STD-DEP-6 (2) Nâng cấp phụ thuộc chính trong PR riêng, sau khi đọc changelog về thay đổi phá vỡ.
- STD-OPS-1 (2) Có kế hoạch rollback đã kiểm cho mọi thay đổi được deploy.
- STD-OPS-2 (2) Viết migration đảo ngược được và chạy thử cả chiều lên lẫn chiều xuống.
- STD-OPS-3 (2) Chạy thử migration dữ liệu trên bản sao và đối soát số lượng trước khi chạy thật.
- STD-OPS-4 (3) Chạy smoke test sau mỗi lần deploy.
- STD-OPS-5 (2) Thêm log hoặc metric đủ để biết tính năng mới chạy đúng ở prod.
- STD-OPS-7 (3) Không để agent thao tác trực tiếp trên dữ liệu hay hạ tầng prod.

## Review checklist (10)
1. Diff làm đúng và đủ spec cùng tiêu chí của task, không thừa (STD-DESIGN-5, STD-TEST-2).
2. Chỉ sửa trong touchpoints; file mới nằm đúng chỗ (STD-DESIGN-1, STD-STRUCT-1, STD-STRUCT-2).
3. Có test hỏng trước; test phủ biên và đường lỗi; không có skip/xfail/only (STD-TEST-1, STD-TEST-8, STD-TEST-4).
4. Không sửa test cho khớp hành vi sai; test độc lập, lặp lại được (STD-TEST-5, STD-TEST-6).
5. Lỗi được xử lý; đầu vào được kiểm tại ranh giới; gọi ngoài có timeout (STD-ERR-1, STD-ERR-2, STD-ERR-5).
6. Không secret, không injection, có phân quyền, không lộ dữ liệu nhạy cảm (STD-SEC-1, STD-SEC-3, STD-SEC-4, STD-SEC-6).
7. Hợp đồng API và dữ liệu tương thích, hoặc có di trú đảo ngược được (STD-DESIGN-3, STD-OPS-2).
8. Tên, cấu trúc, phong cách theo profile; không code chết (STD-NAME-1, STD-NAME-2, STD-STYLE-4, STD-STYLE-5).
9. Phụ thuộc mới có lý do và đáng giá (STD-DEP-1, STD-DEP-3, STD-DEP-5).
10. Commit, nhánh, PR đúng chuẩn; tài liệu đi cùng thay đổi (STD-NAME-4, STD-NAME-5, STD-GIT-1, STD-DOC-2).

## Acceptance checklist (6)
1. Mỗi tiêu chí nghiệm thu: chạy lệnh thật, dán đầu ra, kết luận đạt hay không (STD-TEST-2).
2. `cmd.test`, `cmd.lint`, `cmd.typecheck` xanh trên nhánh feature (STD-TEST-3, STD-STYLE-2, STD-STYLE-3).
3. Diff không thêm dấu bỏ qua test nào trong `test.skip_markers` (STD-TEST-4).
4. Migration chạy lên rồi xuống thành công; dữ liệu đối soát khớp (STD-OPS-2, STD-OPS-3).
5. DoD đủ: As-Built, README/tài liệu, CHANGELOG (STD-DOC-1, STD-DOC-2, STD-DOC-3).
6. Diff không chạm `protected_paths` và không chứa secret (STD-SEC-1).

## Finding format
Mỗi phát hiện một dòng:
`severity | STD | file:line | description | fix`
- `severity` ∈ `blocker` (chặn merge), `major` (phải sửa trong task này), `minor`.
- Chỉ liệt kê blocker và major. Gộp mọi minor vào một dòng cuối: `minor | — | — | <n> điểm nhỏ: ... | tùy dev`.
- Mỗi phát hiện có đúng một mã STD; không có mã thì không phải phát hiện.
