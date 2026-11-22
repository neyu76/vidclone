---
name: darkatlas-topic-studio
description: "Skill 1/3 của bộ TikTok đã chuyên biệt cho kênh Dark Atlas Tales (series truyền thuyết kinh dị các bang Mỹ, 9:16, ~72 s, minh hoạ vector 2D vẽ bằng code, giọng Milo, profile_id darkatlas-us-states). Chọn đề tài tập mới từ SERIES_PLAN_US_STATES.md và nguồn ngoài, chạy 5-Axis Twin Check với các tập đã làm + video mẫu kênh gốc, kiểm SEO/từ bóp FYP bằng tiktok_script_assembler.py twin-seo-check, chấm Scorecard 100, kiểm nguồn dữ kiện thật, khoá Frame-0 (cảnh mở + jumpscare 0,8–1,7 s), chia 4 phần P01..P04 theo khuôn 10 nhịp và xuất TT_TOPIC_PACKET_V1 + START_COMMAND sang darkatlas-script-all-in-one. Dùng khi người dùng nói chọn đề tài, tập mới, TT-00x, săn topic, kiểm trùng cho Dark Atlas."
---

# Dark Atlas Topic Studio (`darkatlas-us-states` rev 1 · nền `tiktok-topic-studio@4.0 BASE_RAW` · 22/11/2026)

Trao đổi với người dùng bằng **tiếng Việt**; tên đề tài, hook, SEO, kịch bản bằng **tiếng Anh (Mỹ)**.
Bộ 3 skill: **topic-studio** (file này) → [darkatlas-script-all-in-one](../darkatlas-script-all-in-one/SKILL.md) → [darkatlas-studio-doctor](../darkatlas-studio-doctor/SKILL.md).
Sản xuất hình/âm thật vẫn theo skill [dark-atlas-tales-production](../dark-atlas-tales-production/SKILL.md) (`DA/` = `styles/dark-atlas-tales/dark_atlas/`).

---

## 0) `TIKTOK_NICHE_PROFILE` — Dark Atlas Tales (tự đủ, nhãn `Provenance`)

| Trục | Giá trị khoá | Nhãn |
|---|---|---|
| `profile_id` / `profile_revision` / `base_versions` | `darkatlas-us-states` / `1` / `tiktok-topic-studio@4.0 \| tiktok-script-all-in-one@4.0 \| tiktok-studio-doctor@4.0` | `OWNER_LOCKED` |
| Ngách | Truyền thuyết kinh dị dân gian theo **từng bang Mỹ** (series "If … in <STATE>… DON'T …"); series các nước là nhánh phụ | `OWNER_LOCKED` |
| Vùng FYP / địa lý hợp lệ | `target_fyp_region = US` (phụ: CA, UK, AU) · ngôn ngữ `en-US` | `OWNER_LOCKED` |
| Tư thế người nói | `OMNISCIENT_NARRATOR` — người kể giấu mặt, giọng nam trầm chậm (Sonic "Milo"), nói với "you" ở nhịp 1 và 9 | `OWNER_LOCKED` |
| Chân dung tâm lý (≥ 70 %) | Người Mỹ 16–34 lướt TikTok đêm khuya, thích "creepy local legend", câu hỏi thầm: **"Nơi mình (hoặc bang mình) có thứ gì đáng sợ mà mình chưa biết — và mình sẽ làm gì nếu gặp nó tối nay?"** | `HYPOTHESIS_TO_TEST` |
| Tư thế cảm xúc | `CUSTOM_SINGLE_POSTURE = DREAD_RULE` — sợ hãi có luật lệ: khán giả nhận **một quy tắc sinh tồn** để mang theo (đối chiếu: không phải Absolution/Elevation) | `OWNER_LOCKED` |
| Giai đoạn kênh | `STAGE_1A_FOLLOWER_SPRINT` (chưa có số đo Studio; cập nhật khi có `MEASURED_BASELINE`) | `HYPOTHESIS_TO_TEST` |
| Nhánh thời lượng | `creator_rewards` cố định theo định dạng kênh: **68–78 s**, đo được 140–150 wpm → `T_fast` (152 wpm) ≥ 62 s tự nhiên | `MEASURED_BASELINE` (V01–V03, EP02/04/05) |
| Chính sách sự thật | `FICTION_CREATIVE` cho phần truyền thuyết (luôn mở bằng "According to the legend" / "They say") + **`STRICT_NONFICTION` cho 1–2 dữ kiện thật** (năm, nơi, người ghi chép) có nguồn trong `SOURCES.md` | `OWNER_LOCKED` |
| Đơn vị đếm | `count_unit = words` · `rate_basis = MEASURED_SAMPLE` · `[145, 138, 152]` · 165–180 từ | `MEASURED_BASELINE` |
| Đường hình 9:16 | 1080×1920 vẽ hoàn toàn bằng Python (`engine.py`, `style.py`, `render_epXX.py`); không footage, không AI ảnh, không khung ngang viền mờ | `OWNER_LOCKED` |
| Cố định nhận diện | khuôn 10 nhịp · thẻ hook đen chữ đỏ · phụ đề Oswald in hoa từng từ có từ đỏ · giọng Milo · nhạc nền `us_bed_master_5min` · jumpscare mặt quái vật 0,8–1,7 s | `OWNER_LOCKED` |
| Thay đổi mỗi tập | thẻ tiêu đề, chuyển cảnh mềm, ngôn ngữ camera, bảng màu, cách lộ mặt, điểm nhấn thẻ hook, SFX đặc trưng — **không lặp 2 tập gần nhất** (bảng biến thể trong `references/quy_tac_san_xuat.md`) | `OWNER_LOCKED` |
| `identity_lock` | `UNSPECIFIED` cho nhân vật nạn nhân; truyền thuyết bản địa ghi đúng tên dân tộc, vẽ đúng mực, không máu | `OWNER_LOCKED` |

### 0.1. Lời đồn FYP bị bác bỏ (không thành luật)
Nhồi `#fyp #viral`; xoá đăng lại bản cắt sửa; thu nhỏ video ngang; "kinh dị phải có máu" (kênh **cấm máu**); "đổi mọi thứ mỗi tập để thử" (chỉ đổi **1 biến khám phá** `exploration_element`, các biến thể hình ở bảng biến thể là đổi *nhận diện cảnh*, không phải thử nghiệm phân phối).

### 0.2. `HYPOTHESIS_LEDGER` khởi tạo (sửa bằng gạch ngang, không xoá — quản trị ở studio-doctor)
| ID | Giả thuyết | Đo bằng | Trạng thái |
|---|---|---|---|
| H1 | Jumpscare mặt quái vật ở 0,8–1,7 s tăng `ret_3s` so với mở cảnh tĩnh | `ret_3s` EP04 v2/EP05 v2 vs v1 (nếu đăng) | OPEN |
| H2 | Tên bang ở chữ đầu tiên ("In New Mexico,") tăng chia sẻ cho người cùng bang (`ss_per_k`) | `ss_per_k`, comment nhắc bang | OPEN |
| H3 | Câu kết đảo ngược nối về tiền đề làm tăng `watched_full_pct` (vòng lặp) | `watched_full_pct`, rewatch | OPEN |
| H4 | Từ "kill/murder/blood" trong lời đọc làm giảm phân phối | so tập có/không | OPEN (watchlist mềm) |

---

## 1) Hai chế độ & phạm vi

- `ADAPT_SKILLS`: chỉ sửa bộ skill/profile, không mở đợt topic mới.
- `RUN_WORKFLOW`:
  - `CHAT_LLM_GO_MODE`: Shortlist 3–5 → người dùng chốt `TT-00x` → Twin + nguồn → Packet + `START_COMMAND` (mỗi bước chờ "go").
  - `AGENT_AUTONOMOUS_STEP_LOOP` (mặc định khi người dùng uỷ quyền "tự chọn"): chạy hết 7 pha, `decision_source = USER_DELEGATED`, `selection_status = DELEGATED_SELECTED`; chỉ hỏi khi thiếu biến cốt lõi (vùng FYP, ranh giới thật/hư cấu, ngân sách credit).
- Mã `TT-00x` ↔ thư mục tập `DA/EPxx_<ten>`: ghi cả hai trong Packet (`identity.topic_id` + `identity.episode_folder`).

---

## 2) Công cụ nghiên cứu (theo thứ tự có sẵn)

| Nhiệm vụ | Công cụ | Ghi chú |
|---|---|---|
| Outlier TikTok/Reels | `vidiq_instagram_tiktok_outlier_search` (5 cr), Apify `clockworks/tiktok-scraper` (`shouldDownloadVideos: false`) | **Nếu không có MCP**: ghi `outlier_references: []`, `evidence_confidence` ≤ `MODERATE_MIXED`, dùng danh sách "creepiest legend from every state" + tìm kiếm TikTok thủ công làm `OBSERVED_MARKET_EVIDENCE` yếu. Không bịa số view. |
| Dữ kiện thật | WebSearch (ưu tiên: bách khoa folklore, JSTOR/JAF, báo địa phương, Wikipedia có nguồn, NPS, trang bộ lạc) | Tách `Market Evidence` ≠ `Fact Evidence`. Câu nào chỉ có ở blog → không đưa vào lời đọc như sự thật. |
| Kênh mẫu | @darkatlastales V01–V03 (đã đo ở `references/dac_ta_phong_cach.md`) | Là đối thủ gần nhất cho Twin Check (nhất là V03 "LOOK AT HER FEET"). |

---

## 3) Bảy pha

### Pha 1 — Nguồn đề tài
1. Đọc `DA/SERIES_PLAN_US_STATES.md` (danh sách người dùng đã tự kiểm chứng = `OWNER_LOCKED` ưu tiên) + `DA/PROJECT_STATE.md`.
2. Thêm đề tài ngoài danh sách chỉ khi có lý do rõ (bang chưa làm, nguồn tốt) và đánh dấu `CANDIDATE_OUTSIDE_PLAN`.
3. Loại ngay: bang vừa làm ở 1 tập gần nhất; đề tài mà dữ kiện thật duy nhất là tin đồn vô căn cứ (ví dụ "dìm trẻ sơ sinh" ở hồ Pyramid — người dùng đã cấm).

### Pha 2 — Bản đồ tâm lý & 5-Axis Twin Check
- Mỗi ứng viên phải trả lời được câu hỏi thầm của chân dung (mục 0) bằng **một tình huống ban đêm cụ thể của "you"**.
- **5 trục** chấm 0 / 0,5 / 1 với **mọi tập đã làm (EP01, EP02, EP04, EP05…) + V01–V03 của kênh mẫu**:
  `Question` (tình huống "if you…") · `Stage` (bối cảnh/địa hình) · `Ladder` (bậc leo thang: lừa/đuổi/biến đổi/điềm báo) · `Payoff` (điều tệ nhất + câu đảo ngược) · `Look` (hình dạng quái vật + bảng màu chủ đạo).
  **≥ 3/5 hoặc trùng `Question + Payoff` = `TWIN [BLOCKER]`** → đổi Stage/Ladder/Payoff thật sự, không chỉ đổi chữ.
- Bảng trùng đã biết (cập nhật khi thêm tập):
  | Đề tài | Trùng với | Lý do |
  |---|---|---|
  | Water Babies (NV) | EP04 Kushtaka | Question "tiếng em bé khóc bên nước" + Payoff "dụ xuống nước" → BLOCKER nếu giữ nguyên |
  | Pukwudgie (MA), Ircenrraat (AK) | EP05 Nimerigar | Look "người tí hon", Ladder "tên độc/bắn lén" → cần đổi góc mạnh |
  | Bất kỳ "người phụ nữ bên đường xin giúp" | V03 kênh mẫu | Question + Stage + Look → BLOCKER |
- Chạy lexical twin + SEO + watchlist:
  ```bash
  python ../darkatlas-script-all-in-one/scripts/tiktok_script_assembler.py twin-seo-check \
    --candidate "<hook ứng viên>" --competitor "If She Asks You for Help on the Road... LOOK AT HER FEET" \
    --own-past "If a Man in a Fur Coat Throws Candy on Your Floor... DON'T GRAB IT" \
    --own-past "If You Hear a Baby Crying by the Water in Alaska... DON'T GO LOOKING" \
    --own-past "If You Hear Something Small Moving Between the Rocks in Wyoming... DON'T FOLLOW IT" \
    --seo-keywords "<legend name>, <state> legend, <state> urban legend"
  ```

### Pha 3 — Góc tiếp cận (khuôn kênh, không ép công thức ngoài)
- Container cố định: **10 nhịp** (mục 5). Động cơ leo thang chọn 1: `RULE_OR_DIE` (quy tắc sinh tồn) · `OMEN` (điềm báo người thân) · `MIMIC` (giả giọng/hình) · `HUNT` (bị săn) · `TEST` (bị thử thách). Không dùng lại động cơ của tập liền trước.
- Câu đảo ngược cuối phải **nối về tiền đề mở đầu** (vòng lặp TikTok).

### Pha 4 — Frame-0 (khớp năng lực kit)
4 thành tố tại 0,0 s trong kit hiện tại:
1. **Chuyển động:** cảnh mở có camera trôi + vật động (cold open, 0–0,85 s).
2. **Âm thanh:** lời đọc vào ngay 0,0 s ("In <STATE>, if…") + SFX môi trường; cú nhấn lớn là **jumpscare 0,8–1,7 s** (tiếng của chính quái vật, 3 lớp + `sub_boom`).
3. **Chữ Safe Zone:** phụ đề Oswald 84 px ở ~67,5 % chiều cao (y ≈ 1296, nằm trong y = 180–1480, x = 90–990): chữ đầu tiên = **"IN <STATE>,"** (tên bang tô đỏ) → đạt Mute Test về địa lý; thẻ hook đen chữ đỏ ở 5–9 s là câu lệnh.
4. **Vật thể hữu hình:** vật/tình huống của câu "if…" phải hiện ngay khung đầu (ngã tư, chiếc xích đu, lều trại…).
Kiểm thêm: tên tiêu đề ≤ 980 px; ảnh bìa vuông 1080×1080 giữa khung đọc được.

### Pha 5 — Scorecard 100 (chấm từng ứng viên, giữ bảng trong Packet)
(1) Tiền đề "if you… tonight" + Frame-0 + hook 3 lớp **30** · (2) Cầu thị trường & TikTok Search (tên truyền thuyết + bang) **20** · (3) Twin Check & Originality Delta so với tập cũ + V01–V03 **15** · (4) Độ thuần chân dung + thang leo thang không khoảng chết > 3 s **15** · (5) Khớp 68–78 s / 165–180 từ **10** · (6) Nguồn FACT có thật + dựng được bằng kit (vẽ được bằng code, ≥ 4 dấu hiệu bang, không máu, nhạy cảm văn hoá) **10**. Chọn điểm cao nhất ≥ 75.

### Pha 6 — Chia phần (4 phần cố định theo 10 nhịp)
| Phần | Nhịp | Thời điểm | Ngân sách từ |
|---|---|---|---|
| P01 | 1 "In <STATE>, if…" · 2 thẻ hook · 3 "Because…" · 4 "They call…" + thẻ tiêu đề | 0–16 s | 40–48 |
| P02 | 5 dữ kiện thật · 6 "According to the legend…" | 16–37 s | 44–52 |
| P03 | 7 "But here's the terrifying part." · 8 quy tắc/điểm yếu ("They say…") | 37–57 s | 40–50 |
| P04 | 9 "So if you're ever… tonight, don't…" · 10 "Because…" đảo ngược + lộ mặt | 57–73 s | 30–40 |
Tổng 165–180. Đỉnh cảm xúc (nhịp 7–8) rơi ở **52–70 %** thời lượng — trùng yêu cầu đỉnh 55–65 %.

### Pha 7 — Xuất `TT_TOPIC_PACKET_V1` (+ `START_COMMAND`)
Lưu ở `DA/EPxx_<ten>/TT/TT-00x_TT_TOPIC_PACKET_V1.yaml` (+ `SOURCES.md`). Schema giữ nguyên bản nền, các trường kênh điền sẵn:

```yaml
schema_version: TT_TOPIC_PACKET_V1
packet_spec_revision: "4.0"
identity:
  topic_id: "TT-00x"
  episode_folder: "EPxx_<ten>"          # thêm cho kênh
  slug: "<legend>-<state>"
  packet_revision: 1
  niche_profile_id: "darkatlas-us-states"
  profile_revision: 1
  base_versions: "tiktok-topic-studio@4.0 | tiktok-script-all-in-one@4.0 | tiktok-studio-doctor@4.0"
selection_and_scope:
  selection_status: ""        # USER_SELECTED | DELEGATED_SELECTED
  decision_source: ""         # USER_SELECTED | USER_DELEGATED
  execution_mode: ""          # CHAT_LLM_GO_MODE | AGENT_AUTONOMOUS_STEP_LOOP
  execution_scope: ""         # TOPIC_SHORTLIST_ONLY | PACKET_HANDOFF | FULL_SCRIPT_PIPELINE
  adaptation_route: "ORIGINAL_BUILD"
  readiness: ""               # READY_FOR_SCRIPT khi có nguồn + Twin CLEAR
  blockers_and_limitations: []
niche_and_psychological_avatar:
  niche_name: "US state horror folklore (Dark Atlas Tales)"
  content_archetype_and_story_engine: "10-beat legend + <RULE_OR_DIE|OMEN|MIMIC|HUNT|TEST>"
  brand_posture: "OMNISCIENT_NARRATOR"
  channel_stage: "STAGE_1A_FOLLOWER_SPRINT"
  target_person_and_inner_question: ""
  emotional_posture: "CUSTOM_SINGLE_POSTURE: DREAD_RULE"
  avatar_purity_check: ""
  target_fyp_region_and_qualified_geo: "US (CA/UK/AU secondary)"
  script_language: "en-US"
  format_track: "creator_rewards"
  fiction_and_fact_policy: "FICTION_CREATIVE legend + STRICT_NONFICTION fact anchors"
  identity_and_non_stereotype_lock: "UNSPECIFIED"
  exploration_element_tested: ""   # đúng 1 biến
angle_and_packaging_9x16:
  core_question_and_viewer_promise: ""
  concrete_stage_and_opening_object: ""
  unique_angle_familiar_plus_new: ""
  format_stack: {aaaa_or_story_engine: "", outer_container: "Dark Atlas 10-beat", inner_escalation_engine: ""}
  visual_hook_archetype_1_to_8: ""
  frame_0_four_elements: {motion_at_0s: "", audio_hit_at_0s: "", frame0_safezone_text: "IN <STATE>,", spoken_hook_what_plus_why: ""}
  hook_card_text: ""          # ≤ 3 từ in hoa, nền đen chữ đỏ
  tiktok_search_seo_keywords: []
  fyp_throttle_word_check: "PASS"
  spectacle_or_emotional_peak_at_55_65pct: ""
  ending_loop_or_part2_plan: "reversal line loops to the opening premise"
  episode_variations: {title_card: "", soft_transition: "", camera: "", grade: "", reveal: "", hook_accent: "", signature_sfx: []}
  state_markers_min4: []
runtime_and_part_budgets:
  target_seconds_range: "68-78 (T_fast >= 62.0)"
  voice_delivery_mode: "clean_voiceover"
  count_unit: "words"
  rate_basis: "MEASURED_SAMPLE"
  speaking_rate_center_min_max: [145, 138, 152]
  non_speech_budget_seconds: 0
  part_budgets_csv: ""         # ví dụ "46,48,46,35"
market_twin_and_source_governance:
  evidence_confidence: ""
  outlier_references: []
  five_axis_twin_check: {closest_matches_scored: [], verdict: ""}
  source_register: []
  claim_ledger: []             # FACT | CALC | LEGEND (they say) | CREATIVE
ordered_modular_outline:
  parts: []                    # P01..P04 như Pha 6
  open_loop_payoff_map: []
  voice_and_must_keep_constraints:
    voice_guide_summary: "Milo, calm and slow; short sentences; 'you' in beats 1 and 9; numbers spelled for TTS"
    user_must_keep: ["10-beat template", "black hook card red text", "jumpscare 0.8-1.7s with the creature's own sound", "no blood", ">=4 state markers"]
    strictly_do_not_copy: ["@darkatlastales scripts and titles", "Urban Legends for Every State scripts"]
```

`START_COMMAND` (dán ngay dưới Packet):
```text
Dùng $darkatlas-script-all-in-one ở AGENT_AUTONOMOUS_STEP_LOOP. Nhận TT_TOPIC_PACKET_V1 <đường dẫn>: init 4 phần theo part_budgets_csv,
chọn 3-5 hook (>=16/20) cho P01, viết tuần tự P01..P04 (mỗi phần 1 lượt + verify-part), opening-audit --p01-only, stitch-draft,
beat-audit, atlas-audit, QA 8 trục P0/P1, lock-export 4 file, rồi kit-scenes ra 05-TT-KIT-SCENES. Không chạy TTS/render.
```

---

## 4) Sau đăng
Không cày view từ máy/IP Việt Nam trong 48 h đầu (kênh nhắm US); không xoá đăng lại; đăng chéo Shorts/Reels từ file render gốc. Chẩn đoán ở `darkatlas-studio-doctor`.
