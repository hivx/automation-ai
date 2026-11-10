---
name: release
description: Dùng khi feature đã accepted, duyệt G4 và có As-Built, cần merge, gắn tag, đưa lên staging cho UAT, rồi lên prod khi người đã duyệt G5.
argument-hint: "<ID> [staging|prod]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(gh pr checks *) Bash(gh pr view *) Bash(git tag *) Bash(git log *)
---

# Phát hành có người duyệt

## Tổng quan
Skill này đưa một feature đã nghiệm thu lên staging, rồi lên prod — và không bao giờ lên prod khi thiếu dòng duyệt của người. Skill chạy trong phiên chính: team-leader kiểm điều kiện, chọn phiên bản, giữ cổng; devops (Agent `team:devops`) làm phần chạm hạ tầng: merge, tag, chạy lệnh deploy và smoke. Kit không tự deploy prod (SPEC §1): prod chỉ chạy sau `Approved-by-prod:`, bằng đúng lệnh/pipeline đã ghi và đã kiểm trong `docs/team/ci.md` (ADJ-24).

Ba điều không thương lượng: kế hoạch rollback có TRƯỚC khi deploy (STD-OPS-1); smoke đỏ là dừng và đề xuất rollback, không "giữ tạm"; G5 luôn là người.

`$ARGUMENTS`: mã `<ID>`; `staging` (mặc định) hoặc `prod`. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- `team.py status <ID>` báo `verified`, G4 đã duyệt, có `asbuilt.md` và PR đã mở (`/team:pr`).
- UAT trên staging xong và người đã thêm `Approved-by-prod:` → `/team:release <ID> prod`.
- Playbook `release` (ra phiên bản gom nhiều feature) hoặc `hotfix` (phần prod luôn cần người).

Không dùng khi:
- Chưa có As-Built hay CHANGELOG → `/team:asbuilt`.
- CI đỏ trên PR → `/team:ci fix`; không phát hành trên CI đỏ.
- Muốn đổi lệnh deploy hay viết script rollback → `/team:ci deploy-script` (PR riêng, có review).

## Tìm hiểu stack trước
1. Read `.team/profile.json`: `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer`, `ci.provider`, `protected_paths`.
2. Read `.team/config.json`: `base_branch`, `protected_branches`, `gates.G5_prod`, `approvers.G5_prod`.
3. Read `docs/team/ci.md` mục `## Deploy`: cách lên prod (job CI có environment bắt người duyệt, hoặc lệnh) và dòng `rollback: <lệnh đã kiểm>`. Profile không có khe deploy cho prod hay rollback (SPEC §8); hai lệnh này chỉ sống ở `docs/team/ci.md` (ADJ-24).
4. `deploy.staging` rỗng, hoặc `docs/team/ci.md` không có dòng rollback → DỪNG, lệnh tiếp: `/team:ci deploy-script`. Không bịa lệnh deploy.

## Đầu vào và điều kiện trước
Chạy và dán từng lệnh; một điều không đạt → dừng, in điều thiếu và lệnh sửa:
- `python3 "<kit>/scripts/team.py" status <ID>` → `verified`; G4 đã duyệt (hoặc tắt).
- `gh pr checks <số PR>` → mọi check xanh.
- `docs/team/features/<ID>/asbuilt.md` có; `CHANGELOG.md` có dòng `(<ID>)` dưới `## [Unreleased]`.
- Nợ sau G4 (K-35): mục `## Nợ sau G4` của `asbuilt.md` đã đóng, hoặc các mục "để /team:release kiểm" được chạy lại ở đây (devops chạy lệnh qa để lại) và xanh.
- `git diff --name-only <base_branch>...team/<ID>` không chạm `protected_paths` mà không có duyệt của người.
- `prod`: thêm điều kiện ở bước 8.

## Quy trình
1. **Ghi vị trí và lý do.** Write `.team/current.json` {feature, stage: "release", agent: "devops", started_at}; journal một câu: vì sao gọi devops, mục tiêu gì.
2. **Chọn phiên bản (điểm quyết định).** `git tag --sort=-v:refname | head -n 5` + nhóm trong mục CHANGELOG của feature: có Removed hay "phá vỡ" → tăng major; có Added → minor; chỉ Fixed/Security → patch. Dự án có quy ước khác (ghi trong `profile.notes` hoặc lịch sử CHANGELOG) thì theo quy ước. Ghi tag chọn và lý do vào journal.
3. **Kế hoạch rollback trước deploy.** Viết mục `## Rollback` trong `asbuilt.md` (team-leader được ghi `docs/team/**`): điều kiện kích hoạt (smoke đỏ; NFR trong spec bị vi phạm), lệnh (chép từ `docs/team/ci.md`), phần dữ liệu (dẫn dòng migration lên/xuống/lên trong `acceptance.md`), thời gian dự kiến. Không có lệnh rollback đã kiểm → không đi tiếp.
4. **Giao devops `deploy-staging`** (Agent `team:devops`), tin ≤ 10 dòng: mã, PR, tag đã chọn, lệnh `deploy.staging`/`deploy.smoke`, file `asbuilt.md`. devops làm:
   1. Merge PR đủ duyệt theo luật bảo vệ nhánh — không ép merge, không quyền admin.
   2. Đổi `## [Unreleased]` thành `## [<phiên bản>] - <YYYY-MM-DD>` trong CHANGELOG (trên nhánh merge), gắn tag, chỉ push tag (STD-GIT-3).
   3. Ghi phiên bản đang chạy trên staging TRƯỚC khi deploy (đích rollback).
   4. `deploy.staging` → `deploy.smoke`; dán mã thoát và đầu ra.
5. **Đọc kết quả devops.** Smoke xanh → bước 6. Smoke đỏ → devops ĐỀ XUẤT rollback về phiên bản ở bước 4.3; team-leader báo người, ghi journal; dừng. Không deploy lại "thử lần nữa".
6. **Điểm dừng UAT.** In cho người danh sách UAT = tiêu chí trong `spec.md` + mục "Cần làm gì" của release notes, và lệnh tiếp. Trạng thái dừng ở đây; skill kết thúc.
7. **Prod: điều kiện.** 20 dòng đầu `asbuilt.md` có `Approved-by-prod: <tên> <YYYY-MM-DD>` (có ngày). `approvers.G5_prod` không rỗng → tên phải nằm trong danh sách. Thiếu → DỪNG, in hướng dẫn duyệt G5. Không có ngoại lệ "gấp" — hotfix cũng vậy.
8. **Prod: kiểm lại trước khi chạm.** `gh pr checks` vẫn xanh trên commit đã tag; mục `## Rollback` có; `deploy.prod_requires_reviewer` true → cách lên prod phải là job CI có environment bắt người duyệt, hoặc người tự chạy lệnh; devops chỉ kích hoạt, không thao tác tay trên dữ liệu hay hạ tầng prod (STD-OPS-7).
9. **Giao devops `deploy-prod`**: kích hoạt đúng pipeline/lệnh trong `docs/team/ci.md` → `deploy.smoke` trên prod; dán mã thoát. Design có log/metric cho đường mới (STD-OPS-5) → dán một dòng chứng minh tính năng đang chạy.
10. **Smoke prod đỏ** → devops đề xuất rollback ngay (lệnh từ `## Rollback`); người quyết và chạy theo luật prod. Journal ghi sự cố; mở `docs/team/defects.md` nếu cần. Dừng.
11. **Xanh** → devops thêm dòng `Released: <tag> <YYYY-MM-DD>` vào `asbuilt.md` (mẫu đã chừa chỗ). Kiểm: `team.py status <ID>` báo `released`; `git tag -l <tag>` có.
12. **Journal và số liệu.** Một dòng journal: tag, staging/prod, smoke, thời gian; `bash "<kit>/scripts/log-run.sh" --skill release --result <released|staging|stopped>`.

## Đầu ra
- Tag phiên bản; `CHANGELOG.md` có mục phiên bản; mục `## Rollback` và dòng `Released:` trong `docs/team/features/<ID>/asbuilt.md`; journal.
- Tin cho người (staging xong):
  ```
  release FEAT-014 | staging xanh
  Tag: v1.5.0 (minor: Added 1 trong CHANGELOG). PR #87 đã merge, CI xanh.
  deploy.staging exit 0; deploy.smoke exit 0 ("12 checks ok")
  Rollback: về v1.4.2 bằng lệnh trong docs/team/ci.md (đã kiểm 2026-11-02)
  UAT: AC-1..AC-5 trong spec.md + đổi cấu hình OTP_TTL
  Tiếp: thêm `Approved-by-prod: <tên> <ngày>` vào asbuilt.md, rồi /team:release FEAT-014 prod
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Gấp, lên prod trước rồi duyệt sau" | Dừng, chờ `Approved-by-prod:` có ngày. |
| "Staging xanh thì prod chắc ổn" | Smoke prod vẫn chạy và dán. |
| "Smoke đỏ nhẹ, cứ giữ" | Dừng, đề xuất rollback, báo người. |
| "Rollback tính sau" | Không có lệnh rollback đã kiểm thì không deploy. |
| "Ép merge cho kịp" | Theo luật bảo vệ nhánh; thiếu duyệt thì chờ. |
| "UAT bỏ qua lần này" | Người quyết, không phải đội. |
| "Tự rollback prod cho nhanh" | devops đề xuất; người quyết và chạy (STD-OPS-7). |
| "Số phiên bản đoán đại" | Theo tag gần nhất + nhóm CHANGELOG. |
| "Lệnh deploy prod thì ai cũng biết" | Chỉ lệnh/pipeline ghi trong `docs/team/ci.md`; không có thì `/team:ci deploy-script`. |

## Dấu hiệu sai
- Tag được tạo trước khi CI xanh.
- Deploy prod mà header `asbuilt.md` không có `Approved-by-prod:` có ngày.
- CHANGELOG còn `[Unreleased]` cho feature đã có tag.
- "Smoke ok" không kèm mã thoát và đầu ra.
- Dòng `Released:` có mà `git tag -l <tag>` rỗng.
- `--force`, merge bằng quyền admin, push vào nhánh bảo vệ.
- Lệnh deploy không đến từ `deploy.*` hay `docs/team/ci.md`.
- Không có mục `## Rollback` trước lần deploy đầu.

## Kiểm chứng
- [ ] Đầu ra `team.py status <ID>` và `gh pr checks` được dán trước khi deploy.
- [ ] Mã thoát `deploy.staging` và `deploy.smoke` (và smoke prod khi lên prod) được dán.
- [ ] Prod: dòng `Approved-by-prod:` trích từ 20 dòng đầu `asbuilt.md`.
- [ ] `git tag -l <tag>` và dòng phiên bản trong CHANGELOG được dán.
- [ ] Mục `## Rollback` có lệnh, điều kiện kích hoạt, phần dữ liệu.
- [ ] Sau prod: `grep '^Released:' asbuilt.md` và `team.py status <ID>` báo `released`.

## Xem thêm
- Agent `devops`; `/team:ci deploy-script` (viết lệnh deploy/rollback/smoke), `/team:asbuilt` (trước), `/team:status`.
- `workflows/release.md`, `workflows/hotfix.md`; `docs/team/ci.md` (mục Deploy).
- `handbook/STD.md`: STD-OPS-1, STD-OPS-4, STD-OPS-5, STD-OPS-7, STD-CI-6, STD-GIT-3.
