---
name: darkatlas-studio-doctor
description: "Skill 3/3 của bộ TikTok đã chuyên biệt cho kênh Dark Atlas Tales (profile_id darkatlas-us-states). Chẩn đoán hậu đăng TikTok Studio ở D+3 / D+7: khoá vệ sinh địa lý 48 h (kênh nhắm US; qualified_geo_pct ≥ 60–80 %, Views/Unique ≤ 2.0 qua tiktok_script_assembler.py fyp-diagnose), tách View Power và Money Power, mổ biểu đồ giữ chân theo từng beat của 03-TT-TIMELINE.csv và các mốc cố định của kênh (jumpscare, thẻ hook, thẻ tiêu đề, 'But here's the terrifying part', lộ mặt), hệ số co n/(n+5), quản trị HYPOTHESIS_LEDGER và xuất TT_DIAGNOSTIC_DELTA_V1 cho darkatlas-topic-studio / darkatlas-script-all-in-one. Dùng khi người dùng gửi ảnh/số TikTok Studio của một tập Dark Atlas."
---

# Dark Atlas Studio Doctor (`darkatlas-us-states` rev 1 · nền `tiktok-studio-doctor@4.0 BASE_RAW` · 22/11/2026)

Tiếng Việt với người dùng. Đầu vào: ảnh chụp/số TikTok Studio của 1 tập + `DA/EPxx/TT/out/03-TT-TIMELINE-<slug>.csv` (hoặc transcript thật `voice_milo_transcript.json` nếu đã render — **ưu tiên mốc giây thật**).
Bộ 3: [topic-studio](../darkatlas-topic-studio/SKILL.md) → [script](../darkatlas-script-all-in-one/SKILL.md) → **studio-doctor** (file này) → quay lại topic/script.

## 0) Hồ sơ kênh (tóm tắt, tự đủ)
`profile_id darkatlas-us-states` · vùng `US` (phụ CA/UK/AU) · en-US · nhánh `creator_rewards` 68–78 s · tư thế `DREAD_RULE` · giai đoạn `STAGE_1A_FOLLOWER_SPRINT` cho tới khi có số đo. Chưa có `MEASURED_BASELINE` Studio nào → mọi ngưỡng dưới đây là `HYPOTHESIS_TO_TEST` cho tới khi có ≥ 5 tập cùng tuổi D+7.

## 1) Khoá vệ sinh 48 h (đặc biệt quan trọng: người làm ở Việt Nam, kênh nhắm Mỹ)
- **Cấm** xem lặp từ máy/Wi-Fi của nhóm, cấm gửi link vào nhóm chat Việt Nam trong 48 h đầu; không VPN "giả Mỹ" để tự xem.
- `python3 -I ../darkatlas-script-all-in-one/scripts/tiktok_script_assembler.py fyp-diagnose --qualified-geo-pct <G> --views <V> --unique-viewers <U> --current-followers <F> --fol-per-k <R>`
  - `G < 60 %` (Locations: United States + CA/UK/AU) → hạt giống địa lý lệch: kiểm ngôn ngữ caption, giờ đăng (khung 19:00–23:00 giờ miền Đông/Trung Mỹ = 7:00–11:00 sáng hôm sau giờ VN), hashtag bang.
  - `Views/Unique > 2.0` → nghi tự xem lặp.
- Search queries TikTok gắn dưới video phải chứa **tên truyền thuyết hoặc "<state> legend"**; nếu gắn sai (ví dụ "horror animation") → siết chữ đầu "IN <STATE>," + SEO caption tập sau.

## 2) Sáu bước đọc 1 tập
1. Tách **View Power** (views, full %, ss/k, fol/k) và **Money Power** (Qualified Views, RPM) — chỉ so tập Dark Atlas với nhau (cùng 68–78 s).
2. Bốn cổng: `0–3s hold` (cổng jumpscare) · `avg_watch_s` & `watched_full_pct` · `ss_per_k = (shares+saves)/views×1000` · `fol_per_k`.
3. Tôn trọng nhịp lô; **không xoá đăng lại**; sửa ở tập kế.
4. Bị gắn *Ineligible/Unoriginal*: kênh vẽ 100 % bằng code → kháng nghị bằng 3 ảnh 1600×1000: (a) `render_epXX.py` + timestamp, (b) `stills.jpg`/timeline dựng, (c) `01-TT-SCRIPT` + `04-TT-MANIFEST` có `locked_at` trước giờ đăng.
5. Chấm ngang ở D+3 (sớm) và **chốt D+7**, phân vị `P(x)` trên các tập cùng tuổi (bỏ cột thiếu, không điền 0):
   `ViewPower = 0.40P(views) + 0.15P(full%) + 0.15P(avg_s) + 0.15P(ss/k) + 0.15P(fol/k)` · `MoneyPower = 0.50P(qual_views) + 0.20P(avg_s) + 0.30P(rpm)`.
6. Mỗi tập chỉ **1 `exploration_element`** (ghi trong Packet). Các biến thể hình bắt buộc (tiêu đề, camera, màu…) là nhận diện cảnh, không tính là biến thử nghiệm.

## 3) Mổ biểu đồ giữ chân theo mốc kênh
Ghép đường giữ chân với `03-TT-TIMELINE.csv` (beat_id, est_start_sec) **và** các mốc cố định:

| Mốc (≈ giây) | Gãy ở đây nghĩa là | Thuốc cho tập sau |
|---|---|---|
| 0–0,8 cold open | Vật thể câu "if" không rõ, tên bang không đọc kịp | chữ "IN <STATE>," to + vật thể hữu hình ngay khung 0 |
| 0,8–1,7 jumpscare | Mặt quái vật yếu/mờ, tiếng không phải của quái vật | lao vào full khung, chớp màu, tiếng quái vật 3 lớp + sub_boom |
| 5–9 thẻ hook | Câu lệnh dài/khó hiểu, màn đen quá lâu | lệnh ≤ 3 từ trên thẻ, ≤ 1,8 s |
| 10–16 thẻ tiêu đề | Tên lạ không có bản dịch/biệt danh | "They call her X. The <epithet>." + tiêu đề có chuyển động |
| 16–37 dữ kiện + legend | Giảng khô, không vật chứng | vật thể chứng cứ trong tranh, từ đỏ đúng giây |
| ~37–40 "But here's the terrifying part" | Đỉnh đến sớm hoặc lặp ý | leo thang mới thật sự (điều tệ nhất chưa nói) |
| 57–73 kết + lộ mặt | Câu kết recap, lộ mặt trễ/nhạt | câu đảo ngược nối về tiền đề, lộ mặt + SFX ≤ 0,75 s trước khi hết |

## 4) Thống kê mẫu nhỏ
Hiệu ứng co: `effect × n/(n+5)` (`--mean-with/--mean-without/--n-with/--n-without`); n < 4 mỗi nhánh = chỉ là hướng. Cỡ mẫu 80 % power: `fyp-diagnose --sigma-pts <σ> --delta-pts <Δ>`.

## 5) `HYPOTHESIS_LEDGER` (gạch ngang, không xoá)
Khởi tạo H1–H4 ở topic-studio (jumpscare → ret_3s; tên bang → ss/k; câu đảo ngược → full %; watchlist kill/blood → phân phối). Cập nhật: `OPEN` → `SUPPORTED (n, effect co)` / ~~`REJECTED`~~ kèm ngày và tập.

## 6) Xuất `TT_DIAGNOSTIC_DELTA_V1`
```yaml
schema_version: TT_DIAGNOSTIC_DELTA_V1
niche_profile_id: "darkatlas-us-states"
topic_id: "TT-00x"
episode_folder: "EPxx_<ten>"
age_checkpoint: "D+3 | D+7"
geo_and_hygiene: {qualified_geo_pct: null, views_per_unique: null, status: ""}
gates: {ret_3s: null, avg_watch_s: null, watched_full_pct: null, ss_per_k: null, fol_per_k: null, qualified_views: null, rpm_usd: null}
view_power_pct: null
money_power_pct: null
retention_breaks: []      # {at_s, beat_id, channel_marker, cause, fix_for_next}
hypothesis_updates: []    # {id, old_status, new_status, n, shrunk_effect}
next_episode_changes:     # đúng 1 exploration_element + các sửa lỗi
  exploration_element: ""
  script_fixes: []
  kit_fixes: []
```
