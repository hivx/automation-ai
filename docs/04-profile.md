# 04 — Profile dự án (`.team/profile.json`)

Profile chứa mọi điều riêng của stack. Agent, skill và hook chỉ nhắc tên KHE, không ghi lệnh. File được commit.

| File | Vai trò |
|---|---|
| `templates/schemas/profile.schema.json` | Schema (JSON Schema draft-07) của profile |
| `templates/schemas/config.schema.json` | Schema của `.team/config.json` |
| `templates/project/team/config.json` | Config mặc định chép vào dự án lúc onboard |
| `profiles/_template.json` | Đủ mọi khe, giá trị rỗng, `notes` giải thích từng khe |
| `profiles/python.json`, `node-ts.json`, `go.json`, `java-maven.json`, `flutter.json` | Mặc định hợp lý theo stack; giá trị chưa chắc được ghi trong `notes` |
| `scripts/check-profile.py` | Kiểm một file theo schema: `scripts/check-profile.py <schema> <file>...` |

`/team:takeover` đề xuất profile kèm bằng chứng cho từng khe (`docs/team/profile-proposal.md`); `/team:onboard` ghi file sau khi người duyệt G0.

## Các khe
| Khe | Nghĩa | Ví dụ (minh họa, dự án Python) |
|---|---|---|
| `stack` | Tên stack chính | `"python"` |
| `language[]` | Ngôn ngữ dùng trong repo | `["python", "sql"]` |
| `cmd.install` | Cài phụ thuộc | `"pip install -e .[dev]"` |
| `cmd.build` | Build | `"python -m build"` |
| `cmd.test` | Toàn bộ test | `"pytest -q"` |
| `cmd.test_one` | **Bắt buộc.** Chạy test của một file, `{file}` là chỗ thay | `"pytest -q {file}"` |
| `cmd.lint` | Lint | `"ruff check ."` |
| `cmd.typecheck` | Kiểm kiểu | `"mypy src"` |
| `cmd.format` | Format một file | `"ruff format {file}"` |
| `cmd.run` | Chạy ứng dụng | `"python -m app"` |
| `cmd.migrate` | Chạy migration | `"alembic upgrade head"` |
| `formatters_by_ext{}` | Formatter theo đuôi file, dùng sau mỗi lần sửa | `{".py": "ruff format {file}"}` |
| `structure.src` | Thư mục mã nguồn | `"src"` |
| `structure.tests` | Thư mục test, hoặc `"colocated"` | `"tests"` |
| `structure.docs`, `structure.scripts`, `structure.config[]` | Nơi tài liệu, script, cấu hình | `"docs"`, `"scripts"`, `["pyproject.toml"]` |
| `structure.allowed_new_file_roots[]` | Danh sách ĐÓNG nơi được tạo file mới | `["src", "tests", "docs"]` |
| `naming.file`, `class`, `function`, `constant`, `test_file` | Quy ước đặt tên | `"snake_case"`, `"PascalCase"`, `"test_{name}.py"` |
| `naming.branch` | Mẫu nhánh | `"team/{id}-{slug}"` |
| `test.skip_markers[]` | Dấu bỏ qua test bị cấm dùng để cho xanh | `["@pytest.mark.skip", "xfail"]` |
| `protected_paths[]` | Không agent nào được sửa: secret, lockfile, thư viện vendored, cấu hình prod | `[".env*", "poetry.lock", "vendor/**"]` |
| `ci.provider`, `ci.runner`, `ci.setup[]` | Nền CI | `"github"`, `"ubuntu-latest"` |
| `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer` | Lệnh deploy staging, smoke test; prod luôn cần người | `true` |
| `ui` | Dự án có giao diện (bật qa dùng Playwright) | `false` |
| `tracker` | Nơi quản lý issue | `"github"` |
| `plugins.required[]`, `plugins.recommended[]` | Plugin cần/nên có; onboard chỉ in lệnh cài | — |
| `notes` | Khe → ghi chú một dòng; đánh dấu giá trị chưa chắc | `{"cmd.migrate": "Chưa chắc: ..."}` |
| `packages` | Monorepo: thư mục → profile ghi đè một phần | `{"web": {"stack": "node-ts"}}` |

## Luật
- `cmd.test_one` bắt buộc. Mọi lệnh chạy từ gốc repo.
- `{file}` là chỗ thay duy nhất.
- `allowed_new_file_roots` là danh sách đóng: ngoài danh sách thì hook chặn tạo file.
- Monorepo: profile gốc + `packages` ghi đè theo thư mục.
- Enum: `ci.provider` và `tracker` ∈ `github|gitlab|none`; `deploy.prod_requires_reviewer` chỉ nhận `true`.
- Không tự thêm khe mới; đề xuất qua `/team:feedback`. Schema có `additionalProperties: false` nên khe lạ bị báo lỗi.

## Thêm profile cho stack mới
1. Chép `profiles/_template.json` thành `profiles/<stack>.json` (tên tiếng Anh, kebab-case).
2. Điền mọi khe; khe không áp dụng để rỗng. Lệnh chưa chắc → ghi vào `notes`.
3. Thêm plugin LSP chính thức của ngôn ngữ (nếu có) vào `plugins.recommended`.
4. Chạy `scripts/check-profile.py templates/schemas/profile.schema.json profiles/<stack>.json`, rồi `scripts/validate.sh`.
