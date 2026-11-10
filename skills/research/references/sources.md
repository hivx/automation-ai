# Nguồn, trích dẫn, độ tin cậy

## Thứ bậc nguồn
| Hạng | Nguồn | Dùng cho |
|---|---|---|
| 1 | Docs chính thức của đúng phiên bản (reference, guide) | mọi khẳng định về API, cấu hình, giới hạn |
| 2 | Changelog, release notes, migration guide, blog chính thức của dự án | thay đổi giữa phiên bản, deprecate |
| 3 | Chuẩn (RFC, W3C, MDN) | giao thức, định dạng, trình duyệt |
| 4 | Bảng tương thích, issue tracker chính thức (trạng thái lỗi đã xác nhận) | lỗi đã biết, nền tảng hỗ trợ |
| — | Blog cá nhân, hỏi đáp cộng đồng, tóm tắt AI, trí nhớ | chỉ để tìm hướng; không bao giờ là nguồn của khẳng định |

## Cách trích
- URL đầy đủ tới trang/mục (anchor), kèm `(truy cập YYYY-MM-DD)`.
- Khẳng định khó thấy hay gây tranh cãi: trích một câu nguyên văn, ngắn.
- Khẳng định không tìm được nguồn: ghi `UNVERIFIED` ngay sau câu; liệt kê ở cuối mục trả lời.
- Hai nguồn mâu thuẫn: ghi cả hai, nói nguồn nào áp cho phiên bản đang dùng và vì sao.

## Độ tin cậy
| Mức | Khi nào |
|---|---|
| cao | nguồn hạng 1–2 của đúng phiên bản trả lời trực tiếp; POC (nếu có) xác nhận |
| trung bình | nguồn hạng 1–2 nhưng khác phiên bản minor, hoặc phải suy từ hai nguồn |
| thấp | chỉ hạng 3–4, có `UNVERIFIED`, hoặc phiên bản không xác định được |

## Mẫu bảng `--upgrade`
| Thay đổi phá vỡ | Nguồn | File bị ảnh hưởng (Explore) | Bước di trú | Rủi ro |
|---|---|---|---|---|
| `connect()` bỏ tham số `timeout` | <URL#breaking> | src/db/pool.py:12, src/jobs/sync.py:40 | dùng `options.timeout` | thấp |

Mỗi dòng cỡ một task 2–5 phút; dòng quá lớn → tách.

## Mẫu bảng `--integration`
| Mục | Giá trị | Nguồn |
|---|---|---|
| Xác thực | OAuth2 client credentials, token 1 giờ | <URL> |
| Giới hạn | 100 yêu cầu/phút/khóa; vượt → 429 + `Retry-After` | <URL> |
| Idempotency | header `Idempotency-Key`, giữ 24 giờ | <URL> |
| Sandbox | có, dữ liệu reset hằng ngày | <URL> |
| Lỗi | JSON `{code, message}`; 5xx nên retry có backoff | <URL> |
| Phân trang | cursor | <URL> |
| Timeout khuyến nghị | 10 giây | <URL> hoặc `UNVERIFIED` |
