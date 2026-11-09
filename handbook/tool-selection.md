# Chọn công cụ: hook, script, rule, skill hay agent

Dùng bảng này trước khi thêm bất cứ thứ gì vào kit hoặc vào `.claude/` của dự án. Đi từ trên xuống, dừng ở dòng đầu tiên khớp.

## Bảng quyết định
| # | Nếu việc cần... | Dùng | Vì sao |
|---|---|---|---|
| 1 | Xảy ra 100%, không được sai | hook + script (và `permissions.deny` nếu là chặn quyền) | Máy chạy luôn; LLM có thể bỏ qua văn bản (STD mức 3) |
| 2 | Tính toán hoặc đọc dữ liệu | script | Tất định, rẻ, không tốn token |
| 3 | Kiến thức tĩnh gắn với một loại đường dẫn | rule có `paths:` trong `.claude/rules/` | Chỉ nạp khi chạm file khớp |
| 4 | Quy trình nhiều bước, có điểm kiểm | skill | Nạp khi gọi; bước, điểm dừng, bằng chứng |
| 5 | Cần ngữ cảnh, bộ tool hoặc model riêng | agent | Ngữ cảnh sạch, quyền hẹp, model phù hợp |

Luật phụ: điều gì viết được thành hook thì KHÔNG viết thành rule.

## Ví dụ
| Việc | Chọn | Ghi chú |
|---|---|---|
| Chặn sửa file `.env` | hook PreToolUse + `permissions.deny` | Dòng 1; khe `protected_paths` |
| Biết lệnh test của dự án | khe `cmd.test_one` trong profile, script đọc ra | Dòng 2; không ghi lệnh vào skill/agent |
| Tính feature đang ở giai đoạn nào | script (`team.py status`) | Dòng 2; trạng thái tính từ artifact |
| Format file sau mỗi lần sửa | hook PostToolUse gọi script đọc `formatters_by_ext` | Dòng 1 |
| Cách viết migration trong repo này | rule có `paths:` trỏ thư mục migration | Dòng 3; chỉ nạp khi chạm migration |
| Quy ước test của thư mục test | rule có `paths:` trỏ `structure.tests` | Dòng 3 |
| Chạy nghiệm thu | skill `verify` | Dòng 4; nhiều bước, cần dán đầu ra |
| Tiếp nhận dự án theo tầng | skill `takeover` | Dòng 4; có ngân sách mỗi tầng, điểm dừng |
| Review trong ngữ cảnh sạch | agent `reviewer` | Dòng 5; không thấy hội thoại của dev, model mạnh |
| Đọc nhiều file để tìm chỗ sửa | agent `Explore` có sẵn | Dòng 5; giữ ngữ cảnh chính gọn |
| Cấm push nhánh bảo vệ | hook PreToolUse(Bash) + `permissions.deny` | Dòng 1; KHÔNG viết thành rule |

## Dấu hiệu chọn sai
- **Rule lẽ ra là hook:** rule viết "không bao giờ", "luôn luôn", "bắt buộc" về một thao tác tool nhận diện được (sửa đường dẫn, lệnh git). Chuyển thành hook.
- **Skill chỉ là văn xuôi:** skill không có bước đánh số, không điểm kiểm, không đòi bằng chứng. Viết lại thành quy trình hoặc chuyển thành rule.
- **Agent cho việc 2 phút:** gọi agent cho việc một lệnh hay một lần đọc file. Làm tại chỗ hoặc dùng script.
- **Script gọi LLM để "đánh giá":** tính toán phải tất định. Phần cần phán đoán đưa cho agent.
- **Kiến thức viết hai nơi:** một rule và một skill cùng nói một điều. Giữ một nơi, nơi kia trỏ tới.
- **Ghi lệnh stack vào skill/agent/hook:** luôn đọc từ khe `cmd.*`.
