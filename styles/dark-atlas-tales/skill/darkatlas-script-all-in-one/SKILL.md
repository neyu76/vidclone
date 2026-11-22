---
name: darkatlas-script-all-in-one
description: "Skill 2/3 của bộ TikTok đã chuyên biệt cho kênh Dark Atlas Tales (profile_id darkatlas-us-states). Nhận TT_TOPIC_PACKET_V1 từ darkatlas-topic-studio rồi viết kịch bản tiếng Anh 165–180 từ theo khuôn 10 nhịp, CẤM VIẾT 1 HƠI: 4 phần P01..P04 viết tuần tự qua scripts/tiktok_script_assembler.py (init → verify-part từng phần → opening-audit → stitch-draft → beat-audit → atlas-audit → QA 8 trục P0/P1/P2 → lock-export), chọn 3–5 hook (≥16/20), đồng bộ Hình–Lời với năng lực vẽ thật của kit (render_epXX.py, T('word', n), CHUNKS/RED, split, jumpscare, thẻ hook, thẻ tiêu đề) và xuất 01-TT-SCRIPT, 02-TT-VOICE, 03-TT-TIMELINE.csv, 04-TT-MANIFEST.json + 05-TT-KIT-SCENES. Dùng khi viết kịch bản tập mới, làm START_COMMAND, sửa kịch bản đã khoá cho Dark Atlas."
---

# Dark Atlas Script All-in-One (`darkatlas-us-states` rev 1 · nền `tiktok-script-all-in-one@4.0 BASE_RAW` · 22/11/2026)

Tiếng Việt với người dùng; lời đọc, phụ đề, tiêu đề **tiếng Anh Mỹ**. Bộ 3: [topic-studio](../darkatlas-topic-studio/SKILL.md) → **script** (file này) → [studio-doctor](../darkatlas-studio-doctor/SKILL.md).
Sau khi khoá kịch bản, sản xuất (giọng → transcript → dựng → SFX → mix → QA 11 chỉ số) theo [dark-atlas-tales-production](../dark-atlas-tales-production/SKILL.md). **Skill này dừng ở kịch bản + phân cảnh, không gọi TTS, không render.**

---

## 0) `TIKTOK_CHANNEL_PROFILE` (cấp kênh, tự đủ)

| Mục | Giá trị | Nhãn |
|---|---|---|
| `profile_id` | `darkatlas-us-states` rev 1 | `OWNER_LOCKED` |
| Shortform DNA | lời vào 0,00 s; cold open 0–0,85 s; **jumpscare 0,8–1,7 s** (mặt quái vật lao vào ống kính, chớp màu 2 khung, rung, ẩn phụ đề); thẻ hook đen chữ đỏ 5–9 s; thẻ tiêu đề 10–16 s (dissolve 0,27 s hoặc biến thể); 27–34 cắt / 72 s, cảnh TB 2,1–2,7 s, dài nhất ≤ 5 s (tiêu đề ≤ 7 s); kết ~0,75 s sau chữ cuối | `MEASURED_BASELINE` |
| Avatar & tư thế | người Mỹ 16–34 lướt đêm; `DREAD_RULE` (sợ có luật lệ) | `HYPOTHESIS_TO_TEST` / `OWNER_LOCKED` |
| Vertical Voice Guide (5 thành tố) | (1) giọng Milo trầm, chậm, đều, speed 1.05, 140–150 wpm; (2) câu ngắn ≤ 20 từ, tối đa 1 mệnh đề phụ; (3) "you" ở nhịp 1 và 9, ngôi thứ ba ở giữa; (4) "..." chỉ 1–2 chỗ (trước câu lệnh hook; tuỳ chọn trước câu thoại cao trào); (5) số viết bằng chữ khi Milo phải đọc đúng ("fourteen inches", "two hundred years") — năm có thể để số ("1827") | `MEASURED_BASELINE` |
| "Data card" của kênh | Kênh **không dùng thẻ dữ liệu đồ hoạ**; con số/năm/địa danh được hiện bằng **vật thể trong tranh** (tờ báo có ngày tháng, sổ tay nhà dân tộc học, thước đo "14 inches", tấm biển bang, bia mộ, đồng hồ) + **từ đỏ trong phụ đề**. Quy tắc nền "30–40 % Data Cards" thay bằng: *mọi FACT/số/năm/địa danh nói ra trong 0–30 s phải có vật thể diegetic hoặc từ đỏ đúng giây phát âm* | `OWNER_LOCKED` (thay luật nền) |
| Safe Zone | phụ đề tâm ~67,5 % chiều cao (y≈1296 @1920), 1–4 từ/cụm, ≤ 2 dòng ~16 ký tự; không vật trắng/đỏ sau vùng 60–75 % chiều cao | `MEASURED_BASELINE` |
| Kết | câu đảo ngược nối về tiền đề (Seamless Loop) + lộ mặt; không recap, không CTA | `OWNER_LOCKED` |

---

## 1) CẤM VIẾT 1 HƠI — vòng lặp tác tử (mặc định)

Workspace tập: `DA/EPxx_<ten>/TT/` (PARTS/, state, audits). Đầu ra khoá: `DA/EPxx_<ten>/TT/out/`. `A=styles/dark-atlas-tales/skill/darkatlas-script-all-in-one/scripts/tiktok_script_assembler.py` (chạy `python3 -I`).

```bash
# 1) Blueprint + khoá vách đá 60 s (mặc định kênh: words, 145/138/152 wpm MEASURED_SAMPLE)
python3 -I $A init --workspace <ws> --topic-id TT-00x --slug <slug> --track creator_rewards --mode clean_voiceover \
  --count-unit words --part-budgets "46,48,46,35" --frame0-text "IN <STATE>," --strict-natural-speech
# 2) Mỗi lượt tool = 1 phần. P01 trước, có 3-5 hook đã chấm:
python3 -I $A verify-part --workspace <ws> --topic-id TT-00x --part-id P01 --file <ws>/PARTS/P01.txt
python3 -I $A opening-audit --workspace <ws> --topic-id TT-00x --p01-only
# 3) P02, P03, P04 — mỗi phần một lượt riêng, đọc lại phần trước + Scene-State Delta trước khi viết
# 4) Ghép + kiểm:
python3 -I $A stitch-draft --workspace <ws> --topic-id TT-00x
python3 -I $A beat-audit  --workspace <ws> --topic-id TT-00x
python3 -I $A atlas-audit --workspace <ws> --topic-id TT-00x --strict
python3 -I $A opening-audit --workspace <ws> --topic-id TT-00x
# 5) QA 8 trục (mục 4) → sửa P0/P1 trong PARTS/ + verify-part --revision r+1 → khoá:
python3 -I $A lock-export --workspace <ws> --topic-id TT-00x --out-dir <ws>/out
# 6) Phân cảnh khớp kit:
python3 -I $A kit-scenes --workspace <ws> --topic-id TT-00x --scenes <ws>/scenes.json --out-dir <ws>/out --strict
```
Cấm: ghi nhiều phần trong 1 file/1 lượt, sinh cả bài rồi cắt. Định dạng PARTS: **mỗi dòng = 1 beat** (1 câu hoặc 1 vế ngắn), UTF-8 không BOM, không thẻ `[pause]`/`[SFX]`, không tiêu đề phần. Sửa sau khi khoá: sửa `PARTS/P0k.txt` → `verify-part --revision <r+1>` → chạy lại 4–6.

---

## 2) Viết từng phần theo khuôn 10 nhịp

| Phần | Nhịp & khuôn câu | Hình phải có (kit) |
|---|---|---|
| **P01** (40–48 từ) | 1 `In <STATE>, if <a specific night situation> ...` · 2 `<COMMAND>.` (≤ 6 từ nói; thẻ ≤ 3 từ) · 3 `Because <shocking reason>. <twist sentence>.` · 4 `They call <her/him/it/them> <NAME>. <Translation/epithet>.` | cold open có vật thể của câu "if"; jumpscare 0,8–1,7 s; thẻ hook đen chữ đỏ + accent biến thể; thẻ tiêu đề kiểu biến thể của tập |
| **P02** (44–52) | 5 dữ kiện thật 1–2 câu (năm/nơi/người ghi) **có nguồn** · 6 `According to the legend, <appearance + method>. <Rule A>. <Rule B>.` | vật thể chứng cứ (tờ báo, sổ, ảnh, bia, biển) ≥ 2 dấu hiệu bang; nhân vật quái vật lần đầu (chưa lộ hẳn mặt) |
| **P03** (40–50) | 7 `But here's the terrifying part.` + chi tiết tệ nhất + leo thang (tuỳ chọn `..."<câu thoại>"`) · 8 `They say <only one thing> <saves/stops> you. <What happens next>.` | cảnh chân dung nạn nhân có thở/run; cảnh quy tắc (vật thể của quy tắc) |
| **P04** (30–40) | 9 `So if you're ever <viewer's situation> tonight, <imperative>. <Imperative>.` · 10 `Because <reframe>. <final twist that loops to beat 1>.` | trở lại bối cảnh mở đầu (loop) → lộ mặt theo biến thể, SFX nhấn, hết ~0,75 s sau chữ cuối |

**Scene-State Delta**: mỗi phần đổi ≥ 1 biến (`INFORMATION` → `DANGER` → `RULE` → `PROXIMITY`). **Continuity ledger**: tên, ngôi (her/him/it/them), màu áo, đạo cụ, giờ trong đêm phải khớp xuyên suốt.

### 2.1. Chọn 3–5 hook cho P01 (cổng 20 điểm, chọn bản ≥ 16)
5 tiêu chí × 0–4: *Mute Test* (chữ "IN <STATE>," + vật thể hữu hình đọc được khi tắt tiếng) · *What + Why* (tình huống + lệnh trong ≤ 7 s) · *Nguy cơ cá nhân* ("you", tonight) · *Câu hỏi mở kéo qua 15–30 s* ("Because…" chưa giải hết) · *0 % mùi AI*. Diệt 4 hook killer: mở bằng năm ("In 1910…"), thuật ngữ khô, rao bán, khoe kênh. Lưu bảng chấm vào `<ws>/TT-00x_HOOK_DRAFTS.md`.

### 2.2. Diệt văn AI & sự thật
- Cấm `—`, `→`, "not X but Y" lặp, liệt kê 3 vế đối xứng, "Have you ever wondered…", triết lý cuối bài.
- Mọi chi tiết siêu nhiên mở bằng "According to the legend / They say / In one version". Dữ kiện thật chỉ dùng điều có trong `SOURCES.md`; chi tiết chỉ thấy ở blog → không nói như sự thật.
- Watchlist FYP (mềm): kill/killed/murder/blood/corpse/suicide → ưu tiên "died", "never came home", "was taken". Walking Sam: không nhắc tự tử thật, có dòng 988.
- Truyền thuyết bản địa/di dân: nói rõ tên dân tộc/nguồn gốc (Tlingit, Shoshone, Paiute, Hispano New Mexico, Guatemala/Mexico…), không chế giễu, không bịa tập tục.

---

## 3) Đồng bộ Hình–Lời với năng lực thật của kit ("Nói gì hình hiện nấy")

Kit vẽ được (đã chứng minh ở EP02/04/05, có thể chép hàm): trời đêm + trăng quầng, núi nhiều lớp + sương, sa mạc/vách đá, bờ biển + nước gợn, nhà trại/kho thóc/nhà gỗ, nội thất có nến/bếp, lều + đèn, nhân vật phẳng 2 tông (chân dung, nghiêng, bóng), quái vật cách điệu (mắt sáng, răng, không máu), cờ bay, tờ báo/sổ tay chữ thật (Gelasio/Kalam), bụi/tàn lửa/tuyết/mưa tên, đèn quét, chớp, rung, whip-pan, dissolve, motion blur, `split()` thêm cắt, phụ đề từng từ có từ đỏ.
Quy tắc ghép:
- Mỗi cảnh gắn vào **một từ** của lời đọc; trong `render_epXX.py` dùng `T("word", n)` (n = lần xuất hiện thứ n của từ đã chuẩn hoá chữ-số, ví dụ `don't` → `dont`). `kit-scenes` tính sẵn n từ kịch bản — **dùng đúng giá trị nó in ra**, sau TTS chỉ cần kiểm transcript khớp kịch bản (`check_transcript.py`).
- 30–33 cảnh (kể cả jumpscare và split); không cảnh nào > 5 s trừ tiêu đề; mỗi cảnh có camera chuyển động + ≥ 1 chuyển động nhỏ.
- Từ đỏ (`RED`): tên bang, tên quái vật, số/năm, danh từ chủ chốt, động từ nguy hiểm — 25–35 từ/tập.
- `scenes.json` mỗi phần tử: `{"id","anchor":"<các từ đầu cảnh>","kind":"cold_open|jumpscare|hook_card|title|normal|reveal","desc","camera","sfx"}`.

---

## 4) Kiểm toán Bước 5.4 + QA 8 trục (/100, P0 = chặn khoá, P1 = phải sửa, P2 = ghi chú)

1. **Frame-0 + 3–5 hook (≥ 16/20) + vật thể hữu hình** (20) — P0 nếu không có hook ≥ 16.
2. **Sự thật & Twin & watchlist** (20) — P0: FACT không nguồn, Twin BLOCKER; P1: watchlist.
3. **Đồng bộ Hình–Lời 9:16** (10) — P0: FACT/số trong 0–30 s không có vật thể/từ đỏ.
4. **10 nhịp đủ + đỉnh 52–70 % + 0 khoảng chết > 3 s + DREAD_RULE** (15) — P0: `atlas-audit` FAIL.
5. **Nhân quả, continuity, Scene-State Delta** (10) — P1.
6. **Toán thời lượng**: 165–180 từ, ước tính 68–78 s, `T_fast` ≥ 62 s (15) — P0.
7. **Giọng điện thoại tự nhiên + Safe Zone** (5) — P1: câu > 20 từ trong 0–15 s, ký tự AI.
8. **Gói lossless** 01/02/03/04 (+05 kit) (5) — P0: roundtrip FAIL.
Mối nối: đọc `TT-00x_TT_SEAM_ANCHORS_V*.json` (P01→P02… và FINAL→0.0s_LOOP: câu cuối phải gọi lại tiền đề, không "Recap cliff", không "follow for part 2"). Lưu bảng QA ở `<ws>/out/TT-00x_QA_REPORT.md`.

### Gói xuất
`01-TT-SCRIPT-<slug>.txt` (bản master, đoạn = beat) · `02-TT-VOICE-<slug>.txt` (lời đọc, `|` giữa beat — khi đưa vào `script.txt` của tập thì thay `|` bằng xuống dòng/đoạn) · `03-TT-TIMELINE-<slug>.csv` (dải giây ước tính, dùng cho studio-doctor) · `04-TT-MANIFEST-<slug>.json` · `05-TT-KIT-SCENES-<slug>.md/.json` (bảng cảnh + `T()` + gates + CHUNKS draft). Sau khi người dùng duyệt: chép lời vào `DA/EPxx/script.txt`, `TITLE.txt` theo mẫu "If … in <State>… DON'T …".

### Mẫu lệnh
```text
Dùng $darkatlas-script-all-in-one. Nhận TT_TOPIC_PACKET_V1 <đường dẫn>, chạy AGENT_AUTONOMOUS_STEP_LOOP P01..P04 qua tiktok_script_assembler.py,
chọn 3-5 hook >=16/20, opening-audit, beat-audit, atlas-audit, QA 8 trục rồi lock-export + kit-scenes. Không chạy TTS/render.
```
