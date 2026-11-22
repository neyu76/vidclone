# TT-001 La Mala Hora — Bước 5.4 + QA 8 trục (script_version 1, 22/11/2026)

Nguồn kiểm: `TT-001_TT_ATLAS_AUDIT_V1.json` (PASS strict), `TT-001_TT_BEAT_AUDIT_V1.json` (0 beat > 8,5 s, max 4,97 s), `TT-001_TT_OPENING_AUDIT_V1.json` (0 cảnh báo, strict), `TT-001_TT_SEAM_ANCHORS_V1.json`, `TT-001_HOOK_DRAFTS.md`, `../SOURCES.md`.

| # | Trục | Điểm | Mức lỗi còn lại | Ghi chú |
|---|---|---|---|---|
| 1 | Frame-0 + 3–5 hook (≥ 16/20) + vật thể hữu hình | 19/20 | — | H1 19/20; "IN NEW MEXICO," ở chữ đầu; ngã tư + áo đen ở khung 0; jumpscare 0,85 s |
| 2 | Sự thật, Twin, watchlist | 18/20 | P2 | F1–F3 có nguồn; phần siêu nhiên đều mở "According to the legend"/"They say"/"One woman…"; Twin CLEAR (V03 1,5/5); 0 từ watchlist. Trừ: chưa có số đo thị trường (không có vidIQ/Apify) |
| 3 | Đồng bộ Hình–Lời 9:16 | 9/10 | P2 | 0–30 s không có số; FACT "descansos" (~20 s) có thánh giá trắng trong tranh + từ đỏ DESCANSOS; kênh không dùng data card (luật kênh thay thế) |
| 4 | 10 nhịp, đỉnh, khoảng chết, tư thế | 14/15 | — | đủ 10 nhịp (atlas-audit); "But here's the terrifying part" ở từ 98/178 = **55 %**, chuyện người vợ 60–70 %; max beat 4,97 s < 8,5; DREAD_RULE giữ đến hết |
| 5 | Nhân quả, continuity, Scene-State Delta | 9/10 | P2 | P01 INFORMATION → P02 TRUST/RULE → P03 DANGER (sang người thân) → P04 RULE+LOOP; vị trí xuất hiện thống nhất "crossroads / where two roads meet"; "her/she" của người vợ và của bà ở câu 19–20 đọc hiểu được nhờ hình (người vợ trong tranh) |
| 6 | Toán thời lượng & vách 60 s | 14/15 | P2 | 178 từ (165–180); ước tính 73,7 s (70,3–77,4); `T_fast` 70,3 ≥ 62. Nếu Milo đọc > 78 s → `fit_voice.py`, không tạo lại giọng |
| 7 | Giọng tự nhiên + Safe Zone | 5/5 | — | 0 dấu —/→; câu dài nhất 0–15 s = 20 từ (ngưỡng 20); câu lệnh "keep walking." 2 từ |
| 8 | Gói lossless 4 file (+05 kit) | 5/5 | — | `lock-export` roundtrip PASS (xem manifest) |
| | **Tổng** | **93/100** | **P0 = 0 · P1 = 0** | |

## Lỗi đã sửa trước khi khoá (nhật ký)
| Lúc | Lỗi | Mức | Sửa | Kiểm lại |
|---|---|---|---|---|
| P01 R1 | Beat 1 ước tính 9,1 s (một dòng 22 từ) | P1 | tách 4 beat, giữ nguyên chữ (R2) | opening-audit: Beat1 1,24 s, 0 cảnh báo |
| Bản 1 | 180 từ → `T_slow` 78,3 s > 78 | P1 | P02 bỏ "small" | 178 từ, `T_slow` 77,4 s |
| Bản 1 | P03 "on an empty road" mâu thuẫn P02 "where two roads meet" | P1 | "at a crossroads" (R2) | continuity OK |

## Mối nối (seam anchors)
- P01→P02 "The evil hour." → "Her story is told…" (từ tên sang nguồn gốc, OK).
- P02→P03 "She doesn't have to." → "But here's the terrifying part." (mở vòng: vậy bà làm gì).
- P03→P04 "…rolling across the road." → "So if you're walking home alone tonight," (về lại tình huống của you).
- FINAL→0.0 s "…who's not coming home." → "In New Mexico, if you're walking home alone…" (**vòng lặp khít**, không recap, không CTA).

## P2 để theo dõi (không chặn)
- Đo lại `wpm` thật sau TTS; nếu Milo nghỉ nhiều ở các dòng tách, `fit_voice.py --keep` giữ 0,6 s trước "keep walking." và trước "at that exact hour."
- `check_transcript.py`: whisper dễ nghe sai "La Mala Hora", "descansos", "Hispanic".
- Biểu tượng Zia chỉ trên biển đường bang (tôn trọng Zia Pueblo).
