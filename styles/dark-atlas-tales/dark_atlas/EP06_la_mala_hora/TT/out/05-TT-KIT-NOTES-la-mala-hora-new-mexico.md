# 05 · Kit notes — TT-001 / EP06 La Mala Hora (đi kèm 05-TT-KIT-SCENES)

Trạng thái: kịch bản **khoá v1**, chưa TTS, chưa render. Các bước dưới đây chỉ chạy **sau khi người dùng duyệt kịch bản + báo giá SFX**.

## 1. Chép kịch bản vào thư mục tập
`02-TT-VOICE` dùng `|` giữa các beat → `script.txt` cần đoạn văn thường:
```bash
cd styles/dark-atlas-tales/dark_atlas/EP06_la_mala_hora
sed 's/ | /\n/g' TT/out/02-TT-VOICE-la-mala-hora-new-mexico.txt > script.txt
```
(Milo đọc mỗi dòng như một câu; nếu nghỉ quá nhiều thì nối các dòng của cùng một câu bằng dấu cách trước khi TTS.)

## 2. Dựng `tools/render_ep06.py` từ `render_ep05.py`
- `EP = os.path.join(ROOT, "EP06_la_mala_hora")`; đọc `style.json` của tập (khoá màu đã có).
- Cảnh = bảng 05-TT-KIT-SCENES (33 cảnh, `T("word", n)` đã đếm sẵn trên chữ của kịch bản — sau TTS chỉ cần `check_transcript.py` = OK).
- Hàm chép được: `desert_sky`/`milky_way`/`fg_layer`/`dust_items_factory` (EP05, đổi màu tím chàm), trăng + quầng (style.py), nhà/nội thất + nến (EP02), cờ/biển (EP02), chân dung run/thở (EP05 `camper_portrait`), jumpscare (EP05 `S0J`), quét đèn (EP05 reveal), dissolve 0,27 s.
- Hàm mới cần vẽ: `la_mala_hora(P, x, feet, h, back=True|False, turn=0..1)` (rebozo đen phủ đầu, váy dài, ánh tím viền, mắt trắng đục, răng mảnh, không máu) · `crossroads(top_down=False)` · `descanso(P, x, y, s, flowers)` · `adobe_church_twin_towers` · `ristra(P, x, y, n)` · `zia_route_sign` (biểu tượng chỉ trên biển) · `wall_clock(P, x, y, r, hh=12, mm=0)` · `dark_mass_rolling(lt)` · `shadow_wipe` (chuyển cảnh mềm của tập: bóng khăn choàng quét ngang khung, ~0,3 s).
- Camera tập: trượt ngang dài (lateral) + đẩy rất chậm; không dập dềnh (EP04), không góc sát đất/whip mũi tên (EP05).

## 3. Từ đỏ gợi ý (`RED`, 27 từ)
```python
RED = {"MEXICO,", "ALONE", "MIDNIGHT,", "BLACK", "CROSSROADS...", "NEXT.", "MALA", "HORA.", "EVIL", "HISPANIC", "DESCANSOS",
       "DIED.", "LEGEND,", "MEET.", "TOUCHES", "TERRIFYING", "DIE.", "LOVE", "CROSSROADS.", "HUSBAND", "EXACT", "HOUR.",
       "HUMAN.", "SHAPE", "STOP,", "BACK.", "HOME."}
```
Lưu ý dùng điều kiện như EP05 để chỉ tô từ trong đúng cụm (ví dụ "ALONE" ở cả 2 chỗ là chủ đích; "HOME." chỉ ở câu cuối).

## 4. Biến thể tập (ghi vào bảng biến thể khi tập được duyệt)
| Thẻ tiêu đề | Chuyển cảnh mềm | Camera | Màu | Lộ mặt | Thẻ hook | SFX đặc trưng |
|---|---|---|---|---|---|---|
| Nến trên descanso tắt, khói thành chữ LA MALA HORA | Wipe bằng bóng khăn choàng đi ngang | Trượt ngang dài + đẩy rất chậm | Tím chàm gần đơn sắc + đỏ ristra | Quay đầu chậm ở ngã tư | Bóng bà đi ngang thẻ, chữ chập chờn | Chuông nhà thờ điểm giờ · tiếng thở khàn của bà · khăn choàng sột soạt |

## 5. Báo giá SFX riêng (Magnific `audio_sfx_generate`, 5 credit/giây) — CHỜ DUYỆT
| File (`assets/sfx/ep06_la_mala_hora/`) | Mô tả prompt (EN) | Giây | Credit |
|---|---|---|---|
| `mala_hora_breath_rasp.mp3` | "slow raspy exhale of a ghostly old woman, close, distorted, low whisper tail, no words" (jumpscare 3 lớp + lộ mặt) | 3 | 15 |
| `church_bell_toll_single.mp3` | "single deep toll of an old adobe church bell at midnight, long natural decay, distant desert air" | 3 | 15 |
| `rebozo_rustle_gravel.mp3` | "heavy dark shawl fabric rustling in wind, slow footsteps on dry gravel road" | 2 | 10 |
| | | **8 s** | **40 credit** |
Thư viện `horror/` dùng lại: wind_night_loop, drone_low_loop, sub_boom, riser_tension, whispers, heartbeat_loop, breath_fear_man_a/b, breath_fear_woman_a, gasp_a, swallow_nervous, creature_growl, stinger_jumpscare. Cú hù mở đầu **chỉ dùng tiếng của bà** (3 lớp gốc/−4/+5 + sub_boom), không tiếng hét người.

## 6. Tiêu đề đăng (nháp cho TITLE.txt)
```
If You See a Woman in Black at a Crossroads in New Mexico… KEEP WALKING

In New Mexico's Hispanic communities they tell of La Mala Hora, the evil hour. She never touches you. She comes to tell you who's not coming home. 🌙
#darkatlas #lamalahora #newmexico #urbanlegend #folklore #scarystories #crossroads
```

## 7. Sau TTS (nhắc lại quy trình kit)
`transcribe.py` → `check_transcript.py` (dễ sai: "La Mala Hora", "descansos", "Hispanic") → nếu > 78 s hoặc > 152 wpm: `fit_voice.py --keep "<giây trước 'keep'>:0.6,<giây trước 'at that exact hour'>:0.6" --cap 0.33 --tempo 0.97` → chạy lại `kit-scenes` (thời gian thật từ transcript) → stills 30+ mốc → render → `sfx_cues.json` → mix `--bed us_bed_master_5min.wav` → `qa_full.py` 11/11.
