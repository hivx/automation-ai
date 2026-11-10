# Đo chất lượng skill và agent (Bước 4)

Nguồn số: `python3 scripts/kit-metrics.py --json` trên commit `e24f0ed` (đếm thân, bỏ frontmatter; tiếng Việt đếm theo âm tiết). Cột "Chuẩn tài liệu F1" so với câu chữ của tài liệu yêu cầu (skill hay nạp < 200 từ, skill khác < 500). Cột "Chuẩn P7" so với chuẩn mà repo đang dùng (≤ 400 với skill hay nạp; 1.200–2.500 với skill khác; 600–1.200 với agent). Bước 4 của prompt nghiệm thu cũng lấy chuẩn ≤ 400.

| Mục | Lớp | Chữ (thân) | Mục có/yêu cầu | Dòng tự bào chữa | Dấu hiệu sai | Ô kiểm chứng | Mô tả: tiền tố / độ dài | references/ | Lệnh stack ghi cứng | Chuẩn P7 | Chuẩn tài liệu F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agent:analyst | agent | 957 | 10/10 | 8 | 4 | — | OK / 119 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:architect | agent | 866 | 10/10 | 7 | 4 | — | OK / 140 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:coach | agent | 965 | 10/10 | 7 | 4 | — | OK / 144 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:designer | agent | 833 | 10/10 | 7 | 4 | — | OK / 133 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:dev | agent | 959 | 10/10 | 9 | 6 | — | OK / 143 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:devops | agent | 838 | 10/10 | 7 | 4 | — | OK / 146 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:maintainer | agent | 830 | 10/10 | 7 | 4 | — | OK / 149 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:qa | agent | 924 | 10/10 | 9 | 5 | — | OK / 129 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:researcher | agent | 844 | 10/10 | 7 | 4 | — | OK / 132 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:reviewer | agent | 946 | 10/10 | 9 | 6 | — | OK / 128 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:team-leader | agent | 1105 | 10/10 | 9 | 6 | — | OK / 164 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:tech-lead | agent | 945 | 10/10 | 9 | 6 | — | OK / 130 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| agent:writer | agent | 857 | 10/10 | 7 | 4 | — | OK / 165 | 0 | 0 | đạt | — (tài liệu không đặt trần cho agent) |
| skill:analyze | full | 1589 | 10/10 | 10 | 8 | 6 | OK / 112 | 1 | 0 | đạt | vượt (<500) |
| skill:architect | full | 1430 | 10/10 | 9 | 7 | 5 | OK / 187 | 1 | 0 | đạt | vượt (<500) |
| skill:asbuilt | full | 1526 | 10/10 | 9 | 7 | 6 | OK / 157 | 1 | 0 | đạt | vượt (<500) |
| skill:audit-kit | full | 1326 | 10/10 | 9 | 6 | 5 | OK / 169 | 1 | 0 | đạt | vượt (<500) |
| skill:build | full | 1503 | 10/10 | 10 | 8 | 6 | OK / 136 | 1 | 0 | đạt | vượt (<500) |
| skill:ci | full | 1348 | 10/10 | 9 | 7 | 6 | OK / 125 | 1 | 0 | đạt | vượt (<500) |
| skill:clean | full | 1362 | 10/10 | 9 | 7 | 5 | OK / 173 | 1 | 0 | đạt | vượt (<500) |
| skill:commit | full | 1501 | 10/10 | 12 | 7 | 6 | OK / 82 | 2 | 0 | đạt | vượt (<500) |
| skill:design | full | 1506 | 10/10 | 9 | 7 | 5 | OK / 202 | 1 | 0 | đạt | vượt (<500) |
| skill:feedback | always | 263 | 4/4 | 6 | — | — | OK / 103 | 0 | 0 | đạt | vượt (<200) |
| skill:handbook | always | 389 | 4/4 | 6 | — | — | OK / 84 | 0 | 0 | đạt | vượt (<200) |
| skill:intake | always | 326 | 4/4 | 6 | — | — | OK / 78 | 0 | 0 | đạt | vượt (<200) |
| skill:make-agent | full | 1356 | 10/10 | 9 | 6 | 5 | OK / 172 | 1 | 0 | đạt | vượt (<500) |
| skill:make-skill | full | 1427 | 10/10 | 9 | 7 | 5 | OK / 170 | 1 | 0 | đạt | vượt (<500) |
| skill:onboard | full | 1249 | 10/10 | 9 | 7 | 5 | OK / 161 | 1 | 0 | đạt | vượt (<500) |
| skill:plan | full | 1315 | 10/10 | 10 | 7 | 6 | OK / 150 | 1 | 0 | đạt | vượt (<500) |
| skill:pr | full | 1443 | 10/10 | 11 | 7 | 6 | OK / 131 | 1 | 0 | đạt | vượt (<500) |
| skill:release | full | 1363 | 10/10 | 9 | 8 | 6 | OK / 135 | 0 | 0 | đạt | vượt (<500) |
| skill:research | full | 1550 | 10/10 | 9 | 7 | 5 | OK / 185 | 1 | 0 | đạt | vượt (<500) |
| skill:retro | full | 1446 | 10/10 | 9 | 7 | 5 | OK / 196 | 1 | 0 | đạt | vượt (<500) |
| skill:run | always | 321 | 4/4 | 6 | — | — | OK / 110 | 0 | 0 | đạt | vượt (<200) |
| skill:session | full | 1272 | 10/10 | 9 | 7 | 5 | OK / 189 | 1 | 0 | đạt | vượt (<500) |
| skill:status | always | 281 | 4/4 | 6 | — | — | OK / 80 | 0 | 0 | đạt | vượt (<200) |
| skill:takeover | full | 1514 | 10/10 | 10 | 7 | 6 | OK / 135 | 1 | 0 | đạt | vượt (<500) |
| skill:using-team | always | 395 | 4/4 | 6 | — | — | OK / 138 | 0 | 0 | đạt | vượt (<200) |
| skill:verify | full | 1551 | 10/10 | 13 | 10 | 6 | OK / 118 | 1 | 0 | đạt | vượt (<500) |

## Tóm tắt
| Nhóm | Số | Trung vị chữ | Đạt chuẩn P7 | Đạt chữ theo tài liệu F1 |
|---|---|---|---|---|
| Skill nạp thường xuyên | 6 | 323.5 | 6/6 | 0/6 (< 200) |
| Skill khác | 20 | 1436.5 | 20/20 | 0/20 (< 500) |
| Agent | 13 | 924 | 13/13 | — |

So với bộ tham khảo (`docs/research/reference-kits.md`): trung vị SKILL.md của addyosmani/agent-skills là 1.985 chữ, obra/superpowers 1.246; trung vị agent của wshobson/agents là 951, VoltAgent 901. Kit đang ở mức 1.436,5 chữ với skill khác và 924 với agent, đếm theo âm tiết. Mọi skill có `description` bắt đầu bằng "Dùng khi", dài < 500 ký tự. Mọi agent có `description` bắt đầu bằng "Giao khi", dài ≤ 300. Không có lệnh stack ghi cứng.

Kết luận cho REQ-F1 (ngân sách chữ): theo câu chữ của tài liệu thì 0/26 skill đạt, vì sau P7 cả 26 đều vượt 200/500. Theo chuẩn P7 và chuẩn của Bước 4 thì 39/39 đạt. Về độ sâu (bảng tự bào chữa, dấu hiệu sai, đòi bằng chứng), 39/39 đạt chuẩn P7.
