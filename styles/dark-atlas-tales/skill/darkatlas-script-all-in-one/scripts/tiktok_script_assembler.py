#!/usr/bin/env python3
"""
[DARK ATLAS TALES edition — profile_id darkatlas-us-states, profile_revision 1, base BASE_RAW v4.0, adapted 2026-11-22]
Channel defaults baked in (override with flags): English clean_voiceover by Sonic "Milo" (speed 1.05), count unit = words,
MEASURED rate 145 wpm (138-152), 165-180 words, 68-78 s, 10-beat template, 4 parts P01..P04.
Two channel subcommands added: atlas-audit (10-beat template / "..." / word-count / hook-card gate) and
kit-scenes (scene plan -> render_epXX.py T("word", n) anchors, shot-length gates, CHUNKS draft).

TikTok Multi-Niche Modular Script Assembler, Twin/SEO/FYP-Word Checker,
Opening Swipe/Contiguity Auditor & Post-Publish FYP Funnel Helper (v4.0 BASE_RAW)

Subcommands:
1) twin-seo-check : Audits candidate hooks/premises/captions against competitor & own past TikToks for Twin clone risk,
                    TikTok Search SEO keyword coverage, and FYP-throttled sensitive words.
2) init           : Initializes sequential multi-part writing state (TIKTOK_SCRIPT_STATE_V1) across 5 tracks:
                    - creator_rewards (1m05s-2m30s+, >=2 parts, enforces fast-rate >=62.0s above TikTok's 60s cliff)
                    - viral_short     (35-55s standalone loop, 1-2 parts, enforces slow-rate <=59.0s)
                    - serial_sub60    (35-55s Pre-10K Part 1/Part 2, 1-2 parts, enforces slow-rate <=59.0s)
                    - true_story      (30-180s first-person true story, enforces Anti-Fabrication & Natural Speech)
                    - extended_story  (3m00s-10m00s deep story/documentary, >=4 parts)
3) verify-part    : Enforces sequential P01..P0N verification, UTF-8 no-BOM, zero TTS emotion tags,
                    zero unresolved [GUESS]/[GỢI-Ý]/[CẦN HỎI] tags, natural-speech filter, and budget discipline.
4) opening-audit  : Audits 0-3s / 3-15s / 15-30s FYP windows for Beat-1 punch, sentence length, Frame-0 Safe-Zone text,
                    and 0-30s numeric/clock/scale anchors requiring 9:16 full-bleed visual contiguity or Data Cards.
5) beat-audit     : Audits spoken beat pacing (0 dead air >3s, beats exceeding max_beat_sec).
6) stitch-draft   : Stitches passed parts, exports P0k->P0(k+1) + FINAL->0.0s_LOOP seam anchors, and runs audits.
7) lock-export    : Verifies 100% lossless spoken token roundtrip + 60s cliff safety and exports matching 4-file bundle:
                    01-TT-SCRIPT, 02-TT-VOICE, 03-TT-TIMELINE.csv (for D+3/D+7 retention autopsy), 04-TT-MANIFEST.json.
8) fyp-diagnose   : Calculates Pre-10K follower sprint vs Post-10K Creator Rewards RPM math, 48h geo/IP data hygiene,
                    D+7 shrinkage effect n/(n+5), and two-arm statistical sample power.
"""

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FORBIDDEN_TAG_RE = re.compile(
    r"\[(sigh|laugh|gasp|whisper|pause|reset|cough|chuckle|cry|sob|breath|inhale|exhale|music|sfx)[^\]]*\]",
    re.IGNORECASE,
)
FORBIDDEN_PROSE_MARKERS_RE = re.compile(
    r"(https?://|\[HOOK[^\]]*\]|\[RE-HOOK[^\]]*\]|\[LOOP[^\]]*\]|\[CTA[^\]]*\]|\[SCENE[^\]]*\]|\[VISUAL[^\]]*\]|\[B-ROLL[^\]]*\]|\[DATA_CARD[^\]]*\])",
    re.IGNORECASE,
)
UNRESOLVED_EPISTEMIC_RE = re.compile(
    r"\[(GUESS|GỢI-Ý|GOI-Y|SUGGESTED_UNCONFIRMED|CẦN HỎI|CAN_HOI|NEEDS_CHECK)(?::[^\]]*)?\]",
    re.IGNORECASE,
)
AI_ESE_PUNCT_RE = re.compile(r"(—|→)")
SPEAKER_PREFIX_RE = re.compile(r"^([A-ZÀ-Ỹ0-9_][A-ZÀ-Ỹ0-9_ \-]{0,28}):\s+(.+)$")
CJK_CHAR_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])\s+")
NUMBER_OR_CLOCK_RE = re.compile(
    r"\b(\d{1,2}:\d{2}|\d+(?:[.,]\d+)?%?)\b",
    re.UNICODE,
)

CHANNEL_PROFILE = {
    "profile_id": "darkatlas-us-states",
    "profile_revision": 1,
    "base_versions": "tiktok-topic-studio@4.0 | tiktok-script-all-in-one@4.0 | tiktok-studio-doctor@4.0",
    "language": "en-US",
    "voice": "Sonic Voice Milo GUDYcgRAONiI1nXDcNQQ, eleven_v4, speed 1.05",
    "words_min": 165, "words_max": 180,
    "rate_center": 145.0, "rate_min": 138.0, "rate_max": 152.0,
    "duration_gate_s": [68.0, 78.0],
    "shots_gate": [26, 34], "mean_shot_gate_s": [2.1, 2.7], "max_shot_s": 5.0, "title_max_shot_s": 7.0,
    "jumpscare_window_s": [0.8, 1.7],
}

# Common FYP-throttled / policy-sensitive trigger words to rewrite naturally in spoken/on-screen copy
FYP_THROTTLE_WATCHLIST = {
    "tự tử": "nghĩ quẩn / bế tắc cùng cực",
    "giết": "đoạt mạng / hạ gục",
    "chết chóc": "thiệt mạng / mất mát",
    "lừa đảo": "bẫy tiền / chiêu trò",
    "cờ bạc": "đỏ đen",
    "suicide": "self-harm crisis / rock bottom",
    "kill yourself": "end it all",
    "scam": "money trap / shady scheme",
    "porn": "explicit content",
    # Dark Atlas horror watchlist (HYPOTHESIS_TO_TEST: soft warning only; legend narration may keep one if needed)
    "murder": "took his life / never came home",
    "murdered": "never came home",
    "blood": "dark stain (channel rule: no blood on screen or in words)",
    "bloody": "dark",
    "corpse": "the body / what was left",
    "kill": "end / take",
    "killed": "died / was taken",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_lf_utf8(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def count_units(text: str, unit_mode: str) -> int:
    if unit_mode == "non_space_chars":
        return len(re.sub(r"\s+", "", text))
    return len(re.findall(r"\S+", text, flags=re.UNICODE))


def tokenize_text(text: str, lang_mode: str = "auto") -> set[str]:
    cleaned = text.lower().strip()
    use_cjk = lang_mode == "cjk" or (lang_mode == "auto" and bool(CJK_CHAR_RE.search(cleaned)))
    if use_cjk:
        chars = re.sub(r"[\s\W_]+", "", cleaned, flags=re.UNICODE)
        if len(chars) <= 1:
            return {chars} if chars else set()
        bigrams = {chars[i : i + 2] for i in range(len(chars) - 1)}
        latin_nums = set(re.findall(r"[a-z0-9]+", cleaned))
        return bigrams | latin_nums
    return set(re.findall(r"[^\W_]+", cleaned, flags=re.UNICODE))


def jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    if not set_a or not set_b:
        return 0.0
    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


def scan_throttled_words(text: str) -> list[dict]:
    lowered = text.lower()
    hits = []
    for term, replacement in FYP_THROTTLE_WATCHLIST.items():
        if re.search(r"\b" + re.escape(term) + r"\b", lowered, flags=re.UNICODE):
            hits.append({"flagged_term": term, "safer_natural_alternative": replacement})
    return hits


def split_raw_chunks(part_text: str) -> list[str]:
    raw = normalize_lf_utf8(part_text)
    if "|" in raw:
        pieces = [re.sub(r"\s+", " ", p).strip() for p in raw.split("|")]
    else:
        pieces = [re.sub(r"\s+", " ", p).strip() for p in raw.split("\n") if p.strip()]
    return [p for p in pieces if p]


def parse_chunk_mode(chunk: str, mode: str) -> tuple[str, str, str]:
    if mode == "dialogue_scenes":
        m = SPEAKER_PREFIX_RE.match(chunk)
        if m:
            spk = m.group(1).strip()
            spoken = m.group(2).strip()
            return spk, f"{spk}: {spoken}", spoken
    return "NARRATOR", chunk, chunk


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def fyp_window_bucket(start_sec: float) -> str:
    if start_sec < 3.0:
        return "00_03s_FRAME0_SWIPE_GATE"
    if start_sec < 15.0:
        return "03_15s_PREMISE_ANCHOR"
    if start_sec < 30.0:
        return "15_30s_ESCALATION_ZONE"
    if start_sec < 60.0:
        return "30_60s_CLIFF_BRIDGE"
    return "60s_PLUS_REWARDS_ZONE"


def analyze_beats(
    spoken_chunks: list[str],
    unit_mode: str,
    rc: float,
    non_speech_sec: float,
    max_beat_sec: float,
) -> dict:
    beat_secs = [round(count_units(c, unit_mode) / rc * 60.0, 2) for c in spoken_chunks]
    spoken_total_sec = sum(beat_secs)
    total_est_sec = spoken_total_sec + non_speech_sec
    over_max = [
        {"beat_id": f"b{idx:03d}", "est_seconds": sec, "preview": spoken_chunks[idx - 1][:80]}
        for idx, sec in enumerate(beat_secs, start=1)
        if sec > max_beat_sec
    ]
    beats_per_10s = round((len(spoken_chunks) / total_est_sec * 10.0), 2) if total_est_sec > 0 else 0.0
    return {
        "total_beats": len(spoken_chunks),
        "first_beat_est_sec": beat_secs[0] if beat_secs else 0.0,
        "max_single_beat_est_sec": max(beat_secs) if beat_secs else 0.0,
        "avg_beat_est_sec": round(spoken_total_sec / len(beat_secs), 2) if beat_secs else 0.0,
        "spoken_beats_per_10s": beats_per_10s,
        "max_beat_threshold_sec": max_beat_sec,
        "beats_exceeding_threshold": over_max,
    }


def analyze_opening_fyp(
    spoken_chunks: list[str],
    unit_mode: str,
    rc: float,
    max_open_sentence_units: int,
    frame0_text: str | None,
) -> dict:
    cum_sec = 0.0
    text_0_15 = []
    text_0_30 = []
    beats_0_3 = 0
    beats_3_15 = 0
    beats_15_30 = 0
    first_beat_sec = 0.0

    for idx, chunk in enumerate(spoken_chunks):
        u = count_units(chunk, unit_mode)
        dur = (u / rc * 60.0) if rc > 0 else 0.0
        if idx == 0:
            first_beat_sec = round(dur, 2)
        start = cum_sec
        cum_sec += dur
        if start < 3.0:
            beats_0_3 += 1
        elif start < 15.0:
            beats_3_15 += 1
        elif start < 30.0:
            beats_15_30 += 1

        if start < 15.0:
            text_0_15.append(chunk)
        if start < 30.0:
            text_0_30.append(chunk)

    joined_15 = " ".join(text_0_15)
    joined_30 = " ".join(text_0_30)
    sents_15 = split_sentences(joined_15)
    sent_lengths = [count_units(s, unit_mode) for s in sents_15]
    long_sentences = [
        {"units": count_units(s, unit_mode), "sentence": s[:120]}
        for s in sents_15
        if count_units(s, unit_mode) > max_open_sentence_units
    ]

    has_question_or_curiosity_30s = ("?" in joined_30) or ("？" in joined_30)
    contiguity_anchors_30s = sorted(set(m.group(0) for m in NUMBER_OR_CLOCK_RE.finditer(joined_30)))
    throttled_hits_30s = scan_throttled_words(joined_30)

    frame0_clean = (frame0_text or "").strip()
    frame0_lines = [ln.strip() for ln in frame0_clean.splitlines() if ln.strip()] if frame0_clean else []
    frame0_status = "MISSING_SET_FRAME0_SAFEZONE_TEXT"
    if frame0_clean:
        if len(frame0_lines) <= 2 and count_units(frame0_clean, "words") <= 11:
            frame0_status = "PASS_SAFEZONE_MAX_2_LINES"
        else:
            frame0_status = "WARN_TOO_LONG_FOR_9X16_SAFEZONE"

    warnings = []
    if first_beat_sec > 4.5:
        warnings.append(f"Beat 1 is {first_beat_sec:.2f}s (>4.5s); split so Spoken Hook lands within 0-3.5s.")
    if long_sentences:
        warnings.append(
            f"{len(long_sentences)} sentence(s) in first 15s exceed {max_open_sentence_units} {unit_mode}; tighten for phone audio."
        )
    if frame0_status != "PASS_SAFEZONE_MAX_2_LINES":
        warnings.append(f"Frame-0 Safe-Zone overlay status: {frame0_status}.")
    if throttled_hits_30s:
        warnings.append(f"FYP throttle watchlist term(s) in first 30s: {throttled_hits_30s}")

    return {
        "first_beat_est_sec": first_beat_sec,
        "beats_in_windows": {
            "0_3s_swipe_gate": beats_0_3,
            "3_15s_premise": beats_3_15,
            "15_30s_escalation": beats_15_30,
        },
        "sentences_in_0_15s": len(sents_15),
        "avg_sentence_units_0_15s": round(sum(sent_lengths) / len(sent_lengths), 2) if sent_lengths else 0.0,
        "max_sentence_units_0_15s": max(sent_lengths) if sent_lengths else 0,
        "max_open_sentence_threshold": max_open_sentence_units,
        "long_sentences_0_15s": long_sentences,
        "question_in_0_30s": has_question_or_curiosity_30s,
        "contiguity_numeric_or_clock_anchors_0_30s": contiguity_anchors_30s,
        "fyp_throttle_watchlist_hits_0_30s": throttled_hits_30s,
        "frame0_safezone_text": frame0_clean or None,
        "frame0_safezone_status": frame0_status,
        "warnings": warnings,
    }


def cmd_twin_seo_check(args):
    candidates = [c for c in (args.candidate or []) if c.strip()]
    competitors = [r for r in (args.competitor or []) if r.strip()]
    own_past = [o for o in (args.own_past or []) if o.strip()]
    seo_keywords = [k.strip() for k in (args.seo_keywords or "").split(",") if k.strip()]

    if not candidates:
        sys.exit("[ERROR] Provide at least one --candidate hook/premise.")

    comp_sets = [(r, tokenize_text(r, args.lang)) for r in competitors]
    own_sets = [(o, tokenize_text(o, args.lang)) for o in own_past]
    seo_sets = [(kw, tokenize_text(kw, args.lang)) for kw in seo_keywords]

    results = []
    for cand in candidates:
        c_set = tokenize_text(cand, args.lang)
        max_comp_j = 0.0
        closest_comp = None
        for r_raw, r_set in comp_sets:
            j = round(jaccard_similarity(c_set, r_set), 4)
            if j > max_comp_j:
                max_comp_j = j
                closest_comp = r_raw

        max_own_j = 0.0
        closest_own = None
        for o_raw, o_set in own_sets:
            j = round(jaccard_similarity(c_set, o_set), 4)
            if j > max_own_j:
                max_own_j = j
                closest_own = o_raw

        max_j = max(max_comp_j, max_own_j)
        if max_j > 0.55:
            twin_verdict = "HIGH_TWIN_CLONE_RISK (>0.55 — change Stage, Escalation Ladder, or Twist!)"
        elif max_j >= 0.30:
            twin_verdict = "MODERATE_FAMILIAR_ANCHOR (0.30-0.55 — verify 5-Axis Twin score <= 2/5)"
        else:
            twin_verdict = "CLEAR_DISTINCT_WORDING (<0.30)"

        matched_seo = [kw for kw, kw_set in seo_sets if kw_set and kw_set.issubset(c_set)]
        missing_seo = [kw for kw, kw_set in seo_sets if kw_set and not kw_set.issubset(c_set)]
        throttle_hits = scan_throttled_words(cand)

        results.append(
            {
                "candidate": cand,
                "max_competitor_jaccard": max_comp_j,
                "closest_competitor": closest_comp,
                "max_own_past_jaccard": max_own_j,
                "closest_own_past": closest_own,
                "lexical_twin_verdict": twin_verdict,
                "tiktok_search_seo_matched": matched_seo,
                "tiktok_search_seo_missing": missing_seo,
                "fyp_throttle_watchlist_hits": throttle_hits,
            }
        )

    payload = {"lang_mode": args.lang, "candidates": results}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in results:
        print(
            f"[TT TWIN-SEO] '{r['candidate']}' -> MaxCompSim={r['max_competitor_jaccard']:.3f} | "
            f"Verdict={r['lexical_twin_verdict']} | SEOMatched={r['tiktok_search_seo_matched']} | "
            f"ThrottleHits={len(r['fyp_throttle_watchlist_hits'])}"
        )


def cmd_init(args):
    ws = Path(args.workspace)
    (ws / "PARTS").mkdir(parents=True, exist_ok=True)
    budgets = [int(x) for x in args.part_budgets.split(",") if x.strip()]
    if not budgets:
        sys.exit("[BLOCKER] --part-budgets must contain at least 1 positive integer.")

    if args.track == "creator_rewards" and len(budgets) < 2 and not args.allow_exception:
        sys.exit(
            "[ANTI-SINGLE-SHOT BLOCKER] Track 'creator_rewards' (1m05s-2m30s+) requires >= 2 modular parts "
            "(recommended 3-4 parts P01..P04) to prevent single-shot quality drop."
        )
    if args.track == "extended_story" and len(budgets) < 4 and not args.allow_exception:
        sys.exit("[ANTI-SINGLE-SHOT BLOCKER] Track 'extended_story' (3m-10m) requires >= 4 modular parts.")

    total_budget = sum(budgets)
    rc = float(args.rate)
    rmin = float(args.rate_min)
    rmax = float(args.rate_max)
    non_speech = max(0.0, float(args.non_speech_sec))

    spoken_center_sec = total_budget / rc * 60.0
    spoken_fast_sec = total_budget / rmax * 60.0
    spoken_slow_sec = total_budget / rmin * 60.0

    est_center_sec = spoken_center_sec + non_speech
    est_fast_sec = spoken_fast_sec + non_speech
    est_slow_sec = spoken_slow_sec + non_speech

    if args.track == "creator_rewards" and est_fast_sec < 62.0 and not args.allow_exception:
        sys.exit(
            f"[MONETIZATION BLOCKER] Track 'creator_rewards' requires fast-rate total duration >= 62.0s "
            f"(target >= 65.0s above TikTok's 60.0s cliff), but budget={total_budget} at r_max={rmax}/min "
            f"+ non_speech={non_speech:.1f}s yields only {est_fast_sec:.1f}s!"
        )
    if args.track in ("viral_short", "serial_sub60") and est_slow_sec > 59.0 and not args.allow_exception:
        sys.exit(
            f"[DURATION BLOCKER] Track '{args.track}' targets <60s, but budget={total_budget} at r_min={rmin}/min "
            f"+ non_speech={non_speech:.1f}s reaches {est_slow_sec:.1f}s."
        )
    if args.track == "true_story" and est_slow_sec > 178.0 and not args.allow_exception:
        sys.exit(f"[DURATION BLOCKER] Track 'true_story' slow-rate estimate {est_slow_sec:.1f}s exceeds 178s cap.")

    default_max_sent = 32 if args.count_unit == "non_space_chars" else 20
    max_open_sent = int(args.max_open_sentence_units) if args.max_open_sentence_units else default_max_sent

    parts_registry = {}
    for idx, b in enumerate(budgets, start=1):
        pid = f"P{idx:02d}"
        parts_registry[pid] = {
            "part_id": pid,
            "budget_units": b,
            "revision": 0,
            "file": None,
            "status": "PENDING",
            "actual_units": 0,
            "chunk_count": 0,
            "sha256": None,
            "first_sentence": None,
            "last_sentence": None,
        }

    state = {
        "schema": "TIKTOK_SCRIPT_STATE_V1",
        "niche_profile_id": CHANNEL_PROFILE["profile_id"],
        "assembler_version": "4.0",
        "topic_id": args.topic_id,
        "slug": args.slug,
        "track": args.track,
        "mode": args.mode,
        "count_unit": args.count_unit,
        "clean_tts": bool(args.clean_tts),
        "strict_natural_speech": bool(args.strict_natural_speech) or (args.track == "true_story"),
        "max_beat_sec": float(args.max_beat_sec),
        "max_open_sentence_units": max_open_sent,
        "frame0_text": args.frame0_text,
        "blueprint_version": 1,
        "script_version": 1,
        "current_workflow": "WF03_BLUEPRINT_LOCKED",
        "state": "BLUEPRINT_LOCKED",
        "rate_spec": {
            "rate_center_upm": rc,
            "rate_min_upm": rmin,
            "rate_max_upm": rmax,
            "rate_basis": args.rate_basis,
            "total_unit_budget": total_budget,
            "non_speech_budget_seconds": round(non_speech, 1),
            "planned_spoken_center_seconds": round(spoken_center_sec, 1),
            "planned_center_seconds": round(est_center_sec, 1),
            "planned_range_seconds": [round(est_fast_sec, 1), round(est_slow_sec, 1)],
        },
        "parts_expected": len(budgets),
        "parts_delivered": 0,
        "next_part": "P01",
        "parts_registry": parts_registry,
        "cumulative_units": 0,
        "cumulative_chunks": 0,
        "last_delivered_boundary": None,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        f"[TT INIT OK] {state_path} | Track={args.track} | Mode={args.mode} | Parts={len(budgets)} | "
        f"Budget={total_budget} {args.count_unit} + NonSpeech={non_speech:.1f}s "
        f"(~{est_center_sec:.1f}s, range {est_fast_sec:.1f}-{est_slow_sec:.1f}s)"
    )


def cmd_verify_part(args):
    ws = Path(args.workspace)
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    pid = args.part_id.upper()
    if pid not in state["parts_registry"]:
        sys.exit(f"[ERROR] Unknown part_id {pid}")

    idx = int(pid[1:])
    if idx > 1:
        prev_pid = f"P{idx - 1:02d}"
        if state["parts_registry"][prev_pid]["status"] != "SECTION_PASSED":
            sys.exit(f"[BLOCKER] Sequential discipline: cannot verify {pid} before {prev_pid} reaches SECTION_PASSED!")

    part_file = Path(args.file)
    raw_bytes = part_file.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        sys.exit(f"[BLOCKER] {part_file} contains UTF-8 BOM; save without BOM.")
    text = raw_bytes.decode("utf-8")

    if state.get("clean_tts", True):
        bad_tag = FORBIDDEN_TAG_RE.search(text)
        if bad_tag:
            sys.exit(f"[BLOCKER] Forbidden TTS emotion/SFX tag found in {pid}: {bad_tag.group(0)}")

    bad_marker = FORBIDDEN_PROSE_MARKERS_RE.search(text)
    if bad_marker:
        sys.exit(f"[BLOCKER] Technical marker/URL leaked into spoken prose of {pid}: {bad_marker.group(0)}")

    if not args.allow_guess:
        bad_epistemic = UNRESOLVED_EPISTEMIC_RE.search(text)
        if bad_epistemic:
            sys.exit(
                f"[ANTI-FABRICATION BLOCKER] Unresolved tag {bad_epistemic.group(0)} leaked into {pid}; "
                "confirm with user/source or hedge honestly before passing."
            )

    if state.get("strict_natural_speech") and not args.allow_ai_punct:
        bad_punct = AI_ESE_PUNCT_RE.search(text)
        if bad_punct:
            sys.exit(
                f"[NATURAL SPEECH BLOCKER] AI-ese punctuation '{bad_punct.group(0)}' detected in {pid}; "
                "rewrite as natural spoken phrases."
            )

    mode = state.get("mode", "clean_voiceover")
    if mode == "clean_voiceover":
        if re.search(r"^(PART\s+\d+|PHẦN\s+\d+|SECTION\s+\d+)\b", normalize_lf_utf8(text), re.IGNORECASE | re.MULTILINE):
            sys.exit(f"[BLOCKER] Section header leaked into clean spoken prose of {pid}.")

    raw_chunks = split_raw_chunks(text)
    if not raw_chunks:
        sys.exit(f"[BLOCKER] {pid} contains 0 spoken beats.")

    parsed = [parse_chunk_mode(c, mode) for c in raw_chunks]
    spoken_chunks = [p[2] for p in parsed]

    unit_mode = state["count_unit"]
    actual_units = count_units(" ".join(spoken_chunks), unit_mode)
    budget = state["parts_registry"][pid]["budget_units"]
    deviation_pct = ((actual_units - budget) / budget * 100.0) if budget else 0.0
    if abs(deviation_pct) > 22.0 and not args.allow_deviation:
        sys.exit(
            f"[NEEDS_REPAIR] {pid} spoken_units={actual_units} deviates {deviation_pct:+.1f}% from budget={budget}. "
            "Adjust pacing/detail before advancing to the next part."
        )

    was_locked = state.get("state") == "SCRIPT_LOCKED"
    if was_locked:
        state["script_version"] = int(state.get("script_version", 1)) + 1

    rec = state["parts_registry"][pid]
    rec["revision"] = int(args.revision)
    rec["file"] = str(part_file.resolve())
    rec["status"] = "SECTION_PASSED"
    rec["actual_units"] = actual_units
    rec["chunk_count"] = len(spoken_chunks)
    rec["sha256"] = sha256_bytes(raw_bytes)
    rec["first_sentence"] = parsed[0][1]
    rec["last_sentence"] = parsed[-1][1]

    passed_parts = [p for p in state["parts_registry"].values() if p["status"] == "SECTION_PASSED"]
    state["parts_delivered"] = len(passed_parts)
    state["cumulative_units"] = sum(p["actual_units"] for p in passed_parts)
    state["cumulative_chunks"] = sum(p["chunk_count"] for p in passed_parts)
    state["last_delivered_boundary"] = f"{pid}: {parsed[-1][1]}"

    pending = [k for k, v in sorted(state["parts_registry"].items()) if v["status"] != "SECTION_PASSED"]
    if pending:
        state["current_workflow"] = "WF04_WRITING"
        state["state"] = "WRITING"
        state["next_part"] = pending[0]
    else:
        state["current_workflow"] = "WF05_READY_FOR_QA"
        state["state"] = "DRAFT_COMPLETE"
        state["next_part"] = None

    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    lock_note = f" | [LOCK INVALIDATED -> v{state['script_version']}]" if was_locked else ""
    print(
        f"[TT PART PASSED] {pid} (R{rec['revision']}) | Units={actual_units}/{budget} ({deviation_pct:+.1f}%) | "
        f"Beats={len(spoken_chunks)} | Cumulative={state['cumulative_units']} | "
        f"Next={state['next_part'] or 'WF05_FLOW_AND_BEAT_AUDIT'}{lock_note}"
    )


def _collect_all_parts(state: dict):
    missing = [k for k, v in sorted(state["parts_registry"].items()) if v["status"] != "SECTION_PASSED"]
    if missing:
        sys.exit(f"[BLOCKER] Missing passed parts: {missing}")

    mode = state.get("mode", "clean_voiceover")
    part_master_blocks = []
    all_parsed_with_pid = []
    seam_pairs = []
    ordered_pids = sorted(state["parts_registry"].keys())

    for i, pid in enumerate(ordered_pids):
        rec = state["parts_registry"][pid]
        raw_chunks = split_raw_chunks(Path(rec["file"]).read_text(encoding="utf-8"))
        parsed = [parse_chunk_mode(c, mode) for c in raw_chunks]
        for p in parsed:
            all_parsed_with_pid.append((pid, p[0], p[1], p[2]))
        part_master_blocks.append("\n\n".join(p[1] for p in parsed))
        if i > 0 and parsed:
            prev_pid = ordered_pids[i - 1]
            prev_last = state["parts_registry"][prev_pid].get("last_sentence")
            seam_pairs.append({"seam": f"{prev_pid}->{pid}", "prev_closing": prev_last, "next_opening": parsed[0][1]})

    if all_parsed_with_pid:
        seam_pairs.append(
            {
                "seam": "FINAL->0.0s_LOOP_OR_PART2",
                "prev_closing": all_parsed_with_pid[-1][2],
                "next_opening": all_parsed_with_pid[0][2],
            }
        )
    return part_master_blocks, all_parsed_with_pid, seam_pairs


def cmd_opening_audit(args):
    ws = Path(args.workspace)
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if args.frame0_text is not None:
        state["frame0_text"] = args.frame0_text
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    mode = state.get("mode", "clean_voiceover")
    if args.p01_only:
        p01 = state["parts_registry"].get("P01")
        if not p01 or p01["status"] != "SECTION_PASSED":
            sys.exit("[BLOCKER] P01 must be SECTION_PASSED to run --p01-only opening-audit.")
        raw_chunks = split_raw_chunks(Path(p01["file"]).read_text(encoding="utf-8"))
        spoken_chunks = [parse_chunk_mode(c, mode)[2] for c in raw_chunks]
    else:
        _, all_parsed_with_pid, _ = _collect_all_parts(state)
        spoken_chunks = [x[3] for x in all_parsed_with_pid]

    rc = state["rate_spec"]["rate_center_upm"]
    threshold = (
        int(args.max_open_sentence_units)
        if args.max_open_sentence_units is not None
        else int(state.get("max_open_sentence_units", 20))
    )
    report = analyze_opening_fyp(spoken_chunks, state["count_unit"], rc, threshold, state.get("frame0_text"))
    audit_path = ws / f"{args.topic_id}_TT_OPENING_AUDIT_V{state['script_version']}.json"
    audit_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.strict and report["warnings"]:
        sys.exit(f"[OPENING FYP AUDIT BLOCKER] {report['warnings']}")

    print(
        f"[TT OPENING FYP AUDIT] Beat1={report['first_beat_est_sec']:.2f}s | "
        f"MaxSent0-15s={report['max_sentence_units_0_15s']}/{threshold} | "
        f"0-30sContiguityAnchors={report['contiguity_numeric_or_clock_anchors_0_30s']} | "
        f"Frame0={report['frame0_safezone_status']}"
    )


def cmd_beat_audit(args):
    ws = Path(args.workspace)
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    _, all_parsed_with_pid, _ = _collect_all_parts(state)
    spoken_chunks = [x[3] for x in all_parsed_with_pid]

    rc = state["rate_spec"]["rate_center_upm"]
    non_speech = float(state["rate_spec"].get("non_speech_budget_seconds", 0.0))
    threshold = float(args.max_beat_sec) if args.max_beat_sec is not None else float(state.get("max_beat_sec", 8.5))

    report = analyze_beats(spoken_chunks, state["count_unit"], rc, non_speech, threshold)
    audit_path = ws / f"{args.topic_id}_TT_BEAT_AUDIT_V{state['script_version']}.json"
    audit_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.strict and report["beats_exceeding_threshold"]:
        sys.exit(
            f"[BEAT AUDIT BLOCKER] {len(report['beats_exceeding_threshold'])} spoken beat(s) exceed "
            f"{threshold:.1f}s: {report['beats_exceeding_threshold']}"
        )
    print(
        f"[TT BEAT AUDIT] Beats={report['total_beats']} | FirstBeat={report['first_beat_est_sec']:.2f}s | "
        f"AvgBeat={report['avg_beat_est_sec']:.2f}s | MaxBeat={report['max_single_beat_est_sec']:.2f}s | "
        f"SpokenBeats/10s={report['spoken_beats_per_10s']:.2f} | OverThreshold={len(report['beats_exceeding_threshold'])}"
    )


def cmd_stitch_draft(args):
    ws = Path(args.workspace)
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))

    part_master_blocks, all_parsed_with_pid, seam_pairs = _collect_all_parts(state)
    spoken_chunks = [x[3] for x in all_parsed_with_pid]

    draft_text = "\n\n".join(part_master_blocks) + "\n"
    draft_path = ws / f"{args.topic_id}_TT_DRAFT_V{state['script_version']}.txt"
    draft_path.write_bytes(draft_text.encode("utf-8"))

    seams_path = ws / f"{args.topic_id}_TT_SEAM_ANCHORS_V{state['script_version']}.json"
    seams_path.write_text(json.dumps(seam_pairs, indent=2, ensure_ascii=False), encoding="utf-8")

    total_u = count_units(" ".join(spoken_chunks), state["count_unit"])
    rc = state["rate_spec"]["rate_center_upm"]
    rmin = state["rate_spec"]["rate_min_upm"]
    rmax = state["rate_spec"]["rate_max_upm"]
    non_speech = float(state["rate_spec"].get("non_speech_budget_seconds", 0.0))
    max_beat_sec = float(state.get("max_beat_sec", 8.5))
    open_thresh = int(state.get("max_open_sentence_units", 20))

    beat_report = analyze_beats(spoken_chunks, state["count_unit"], rc, non_speech, max_beat_sec)
    (ws / f"{args.topic_id}_TT_BEAT_AUDIT_V{state['script_version']}.json").write_text(
        json.dumps(beat_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    opening_report = analyze_opening_fyp(spoken_chunks, state["count_unit"], rc, open_thresh, state.get("frame0_text"))
    (ws / f"{args.topic_id}_TT_OPENING_AUDIT_V{state['script_version']}.json").write_text(
        json.dumps(opening_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    est_c = total_u / rc * 60.0 + non_speech
    est_f = total_u / rmax * 60.0 + non_speech
    est_s = total_u / rmin * 60.0 + non_speech
    print(
        f"[TT DRAFT STITCHED] {draft_path} | SpokenUnits={total_u} | Beats={len(spoken_chunks)} | "
        f"EstTotal={est_c:.1f}s (range {est_f:.1f}-{est_s:.1f}s) | "
        f"OverBeat={len(beat_report['beats_exceeding_threshold'])} | OpeningWarnings={len(opening_report['warnings'])}"
    )


def cmd_lock_export(args):
    ws = Path(args.workspace)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    state_path = ws / f"{args.topic_id}_TT_STATE_V1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))

    part_master_blocks, all_parsed_with_pid, seam_pairs = _collect_all_parts(state)
    spoken_chunks = [x[3] for x in all_parsed_with_pid]
    mode = state.get("mode", "clean_voiceover")

    master_prose = "\n\n".join(part_master_blocks) + "\n"
    if not args.allow_guess and UNRESOLVED_EPISTEMIC_RE.search(master_prose):
        sys.exit("[ANTI-FABRICATION BLOCKER] Unresolved epistemic tag remains in script; resolve before locking.")

    sep = " | " if args.voice_sep == "pipe" else "\n\n"
    voice_text = sep.join(spoken_chunks) + "\n"

    if mode == "clean_voiceover":
        tokens_master = re.findall(r"\S+", master_prose, flags=re.UNICODE)
    else:
        tokens_master = re.findall(r"\S+", " ".join(spoken_chunks), flags=re.UNICODE)
    tokens_voice = re.findall(r"\S+", " ".join(spoken_chunks), flags=re.UNICODE)
    if tokens_master != tokens_voice:
        sys.exit("[BLOCKER] Lossless Roundtrip failed: spoken token sequence mismatch between 01-TT-SCRIPT and 02-TT-VOICE!")

    total_u = count_units(" ".join(spoken_chunks), state["count_unit"])
    rc = state["rate_spec"]["rate_center_upm"]
    rmin = state["rate_spec"]["rate_min_upm"]
    rmax = state["rate_spec"]["rate_max_upm"]
    non_speech = float(state["rate_spec"].get("non_speech_budget_seconds", 0.0))

    est_center_sec = total_u / rc * 60.0 + non_speech
    est_fast_sec = total_u / rmax * 60.0 + non_speech
    est_slow_sec = total_u / rmin * 60.0 + non_speech

    if state["track"] == "creator_rewards" and est_fast_sec < 62.0 and not args.allow_exception:
        sys.exit(
            f"[MONETIZATION BLOCKER] Final draft fast-rate duration is {est_fast_sec:.1f}s "
            "(< 62.0s safety floor for TikTok Creator Rewards)! Expand middle escalation/proof before locking."
        )
    if state["track"] in ("viral_short", "serial_sub60") and est_slow_sec > 59.0 and not args.allow_exception:
        sys.exit(
            f"[DURATION BLOCKER] Final draft slow-rate duration is {est_slow_sec:.1f}s "
            f"(> 59.0s ceiling for sub-60s track '{state['track']}')!"
        )

    slug = state["slug"]
    script_file = out_dir / f"01-TT-SCRIPT-{slug}.txt"
    voice_file = out_dir / f"02-TT-VOICE-{slug}.txt"
    timeline_file = out_dir / f"03-TT-TIMELINE-{slug}.csv"
    manifest_file = out_dir / f"04-TT-MANIFEST-{slug}.json"

    master_bytes = master_prose.encode("utf-8")
    voice_bytes = voice_text.encode("utf-8")
    script_file.write_bytes(master_bytes)
    voice_file.write_bytes(voice_bytes)

    cum_sec = 0.0
    with timeline_file.open("w", encoding="utf-8", newline="\n") as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(
            [
                "beat_id",
                "part_id",
                "speaker",
                "fyp_window_bucket",
                "est_start_sec",
                "est_end_sec",
                "est_duration_sec",
                "units",
                "contiguity_anchors",
                "spoken_text",
            ]
        )
        for idx, (pid, spk, _, spoken) in enumerate(all_parsed_with_pid, start=1):
            u = count_units(spoken, state["count_unit"])
            dur = round(u / rc * 60.0, 2)
            start = round(cum_sec, 2)
            end = round(cum_sec + dur, 2)
            cum_sec += dur
            anchors = ";".join(sorted(set(m.group(0) for m in NUMBER_OR_CLOCK_RE.finditer(spoken))))
            writer.writerow(
                [
                    f"b{idx:03d}",
                    pid,
                    spk,
                    fyp_window_bucket(start),
                    f"{start:.2f}",
                    f"{end:.2f}",
                    f"{dur:.2f}",
                    u,
                    anchors,
                    spoken,
                ]
            )

    max_beat_sec = float(state.get("max_beat_sec", 8.5))
    open_thresh = int(state.get("max_open_sentence_units", 20))
    beat_report = analyze_beats(spoken_chunks, state["count_unit"], rc, non_speech, max_beat_sec)
    opening_report = analyze_opening_fyp(spoken_chunks, state["count_unit"], rc, open_thresh, state.get("frame0_text"))

    manifest = {
        "schema": "TIKTOK_LOCK_MANIFEST_V4",
        "niche_profile_id": CHANNEL_PROFILE["profile_id"],
        "profile_revision": CHANNEL_PROFILE["profile_revision"],
        "topic_id": state["topic_id"],
        "slug": slug,
        "track": state["track"],
        "mode": mode,
        "script_version": state["script_version"],
        "timing_status": "ESTIMATED",
        "count_unit": state["count_unit"],
        "total_spoken_units": total_u,
        "total_beats": len(spoken_chunks),
        "non_speech_seconds": non_speech,
        "estimated_center_seconds": round(est_center_sec, 1),
        "estimated_range_seconds": [round(est_fast_sec, 1), round(est_slow_sec, 1)],
        "creator_rewards_60s_safe": est_fast_sec >= 62.0 if state["track"] == "creator_rewards" else "NOT_APPLICABLE",
        "lossless_token_roundtrip": True,
        "seam_count": len(seam_pairs),
        "beat_pacing_summary": beat_report,
        "opening_fyp_audit": opening_report,
        "files": {
            "01_script": {"path": str(script_file.resolve()), "sha256": sha256_bytes(master_bytes)},
            "02_voice": {"path": str(voice_file.resolve()), "sha256": sha256_bytes(voice_bytes)},
            "03_timeline_csv": {"path": str(timeline_file.resolve()), "sha256": sha256_bytes(timeline_file.read_bytes())},
        },
        "locked_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    state["state"] = "SCRIPT_LOCKED"
    state["current_workflow"] = "WF06_SCRIPT_LOCKED"
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"[TT LOCK & EXPORT OK] v{state['script_version']} | Units={total_u} | "
        f"Est={est_center_sec:.1f}s (fast={est_fast_sec:.1f}s, slow={est_slow_sec:.1f}s) | "
        f"LosslessRoundtrip=PASS | Out={out_dir}"
    )


def cmd_fyp_diagnose(args):
    fol_per_k = float(args.fol_per_k)
    current_followers = int(args.current_followers)
    remaining_to_10k = max(0, 10000 - current_followers)
    views_to_10k = math.ceil(remaining_to_10k / fol_per_k * 1000.0) if fol_per_k > 0 and remaining_to_10k > 0 else 0

    qual_rate = float(args.qualified_rate_pct) / 100.0
    rpm = float(args.rpm_usd)
    est_qual_views_per_100k = int(round(100000 * qual_rate))
    est_rev_per_100k_usd = round(est_qual_views_per_100k / 1000.0 * rpm, 2)

    geo_status = "NOT_PROVIDED"
    if args.qualified_geo_pct is not None:
        geo_status = (
            "PASS_TARGET_GEO_CLEAN (>=60%)"
            if args.qualified_geo_pct >= 60.0
            else "WARN_GEO_DILUTED_BELOW_60PCT (check domestic Wi-Fi self-watch, off-market link sharing, or local language leak!)"
        )

    hygiene_ratio = None
    hygiene_status = "NOT_PROVIDED"
    if args.views is not None and args.unique_viewers is not None and args.unique_viewers > 0:
        hygiene_ratio = round(args.views / args.unique_viewers, 2)
        hygiene_status = (
            "CONTAMINATED_LOOP_WATCH_OVER_2.0 (stop self-watching from team devices!)"
            if hygiene_ratio > 2.0
            else "CLEAN_UNDER_2.0"
        )

    shrunk_effect = None
    sample_noise_flag = "NOT_PROVIDED"
    if (
        args.mean_with is not None
        and args.mean_without is not None
        and args.n_with is not None
        and args.n_without is not None
    ):
        n_min = min(int(args.n_with), int(args.n_without))
        raw_diff = float(args.mean_with) - float(args.mean_without)
        shrunk_effect = round(raw_diff * (n_min / (n_min + 5.0)), 3)
        sample_noise_flag = "LOW_SAMPLE_NOISE_N_UNDER_4" if n_min < 4 else "SUFFICIENT_DIRECTIONAL_SIGNAL"

    sigma = float(args.sigma_pts)
    delta = float(args.delta_pts)
    n_per_arm_80pwr = math.ceil(2.0 * ((1.96 + 0.84) * sigma / delta) ** 2) if delta > 0 else None

    report = {
        "monetization_and_sprint_math": {
            "current_followers": current_followers,
            "fol_per_k": fol_per_k,
            "estimated_views_needed_for_10k_followers": views_to_10k,
            "assumed_qualified_view_rate_pct": args.qualified_rate_pct,
            "assumed_rpm_usd": rpm,
            "est_revenue_per_100k_total_views_usd": est_rev_per_100k_usd,
        },
        "early_48h_fyp_data_hygiene": {
            "qualified_geo_share_pct": args.qualified_geo_pct,
            "geo_classification_status": geo_status,
            "views_per_unique_viewer": hygiene_ratio,
            "loop_contamination_status": hygiene_status,
        },
        "d7_feature_shrinkage_eval": {
            "shrunk_effect_n_over_n_plus_5": shrunk_effect,
            "sample_confidence": sample_noise_flag,
        },
        "retention_experiment_power": {
            "assumed_hold_sd_pts": sigma,
            "target_detectable_lift_pts": delta,
            "required_videos_per_arm_95ci_80power": n_per_arm_80pwr,
        },
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


# ======================= DARK ATLAS channel commands =======================
ATLAS_NORM = lambda w: "".join(c for c in w.lower() if c.isalnum())   # same normalisation as render_epXX.py T()


def _atlas_script_text(state: dict) -> str:
    _, all_parsed_with_pid, _ = _collect_all_parts(state)
    return " ".join(x[3] for x in all_parsed_with_pid)


def cmd_atlas_audit(args):
    """10-beat template gate for Dark Atlas (see darkatlas-script-all-in-one SKILL.md section 3)."""
    ws = Path(args.workspace)
    state = json.loads((ws / f"{args.topic_id}_TT_STATE_V1.json").read_text(encoding="utf-8"))
    text = _atlas_script_text(state)
    low = text.lower()
    words = re.findall(r"\S+", text)
    P = CHANNEL_PROFILE
    checks = []

    def add(name, ok, detail, level="P0"):
        checks.append({"check": name, "level": level, "pass": bool(ok), "detail": detail})

    add("word_count_165_180", P["words_min"] <= len(words) <= P["words_max"], f"{len(words)} words")
    ell = len(re.findall(r"\.\.\.|…", text))
    add("ellipsis_1_or_2", 1 <= ell <= 2, f'{ell} x "..." (before the hook command; optional 2nd before the climax line)')
    m = re.match(r"In ([A-Z][\w'\. ]+?),\s+if\b", text)
    add("beat1_In_STATE_if", bool(m), m.group(0) if m else text[:60])
    hook = None
    hm = re.search(r"(\.\.\.|…)\s*([^.!?]+[.!?])", text)
    if hm:
        hook = hm.group(2).strip()
        add("beat2_spoken_command_le_6_words", len(hook.split()) <= 6, hook)
        card = " ".join(hook.rstrip(".!?").split()[:3]).upper()
        add("hook_card_text_le_3_words", True, f"card suggestion: {card}. (EP04/05 shortened the spoken command on the card)", "P2")
        add("beat2_hook_is_imperative", hook.lower().startswith(("don't", "do not", "never", "keep", "look", "run", "pray", "stay", "close", "turn", "hide", "walk")), hook, "P1")
    else:
        add("beat2_spoken_command_le_6_words", False, "no '...' before a command")
    order = [
        ("beat3_because", r"\bbecause\b"),
        ("beat4_they_call", r"\bthey call (her|him|it|them)\b"),
        ("beat6_according_to_the_legend", r"\baccording to (one version of )?the legend\b"),
        ("beat7_terrifying_part", r"\bbut here's the terrifying part\b"),
        ("beat9_so_if_you", r"\bso,? if you\b"),
    ]
    pos = 0
    for name, rx in order:
        mm = re.search(rx, low[pos:])
        add(name, bool(mm), (low[pos + mm.start(): pos + mm.start() + 40] if mm else f"missing after char {pos}"))
        if mm:
            pos += mm.end()
    last_sent = split_sentences(text)
    tail = " ".join(last_sent[-2:]).lower() if last_sent else ""
    add("beat10_reversal_starts_because", "because" in tail, tail[:80])
    add("legend_marker_they_say_or_legend", ("they say" in low) or ("according to" in low), "supernatural claims framed as legend")
    add("no_ai_punct", not AI_ESE_PUNCT_RE.search(text), "no em dash / arrow", "P1")
    hits = scan_throttled_words(text)
    add("fyp_watchlist_soft", not hits, hits, "P2")
    p0_fail = [c for c in checks if c["level"] == "P0" and not c["pass"]]
    report = {"topic_id": args.topic_id, "words": len(words), "hook_card": hook, "checks": checks,
              "verdict": "PASS" if not p0_fail else "FAIL"}
    out = ws / f"{args.topic_id}_TT_ATLAS_AUDIT_V{state['script_version']}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    for c in checks:
        print(f"  {'PASS' if c['pass'] else 'FAIL'} [{c['level']}] {c['check']}: {c['detail']}")
    print(f"[ATLAS AUDIT] {report['verdict']} | words={len(words)} | hook_card={hook!r} | {out}")
    if p0_fail and args.strict:
        sys.exit("[ATLAS AUDIT BLOCKER] " + ", ".join(c["check"] for c in p0_fail))


def _caption_chunks(text: str) -> list[str]:
    """Draft CHUNKS like render_epXX.py: 1-4 words, break at punctuation, never end a chunk on a weak word
    (article/preposition/pronoun/'La'), so names and phrases stay together. The chunk right after the first '...'
    is the hook command (hidden '#', shown on the hook card)."""
    WEAK = {"a", "an", "the", "in", "of", "to", "at", "on", "for", "her", "his", "their", "your", "my", "la", "el",
            "called", "is", "are", "was", "and", "or", "but", "who", "who's", "you", "she", "he", "it", "they",
            "where", "if", "that", "by", "with", "from", "into", "just", "always", "never", "only", "very"}
    toks = re.findall(r"\S+", text)
    out, cur, hook_next, seen_ell = [], [], False, 0
    def flush(n=None):
        nonlocal cur, hook_next, seen_ell
        take, rest = (cur, []) if n is None else (cur[:n], cur[n:])
        chunk = " ".join(take)
        if hook_next:
            chunk = "#" + chunk
            hook_next = not re.search(r"[.!?]$", take[-1])
        if re.search(r"\.\.\.$|\u2026$", take[-1]):
            seen_ell += 1
            hook_next = hook_next or seen_ell == 1
        out.append(chunk)
        cur = rest
    for t in toks:
        cur.append(t)
        if re.search(r"[,.!?;:]$|\.\.\.$|\u2026$", t):
            flush()
        elif len(cur) >= 4:
            k = len(cur)
            if re.sub(r"[^\w']", "", cur[k - 1]).lower() in WEAK:   # move one dangling weak word to the next chunk
                k -= 1
            flush(k if k < len(cur) else None)
    if cur:
        flush()
    return out


def cmd_kit_scenes(args):
    """Scene plan (JSON list) -> kit anchors. Each scene: {id, anchor: 'first words of the scene', desc, kind?, split?}.
    kind: cold_open | jumpscare | hook_card | title | normal | reveal. Times are ESTIMATES from the measured rate until
    voice_milo_transcript.json exists; T("word", n) occurrences are exact because they come from the script words."""
    ws = Path(args.workspace)
    state = json.loads((ws / f"{args.topic_id}_TT_STATE_V1.json").read_text(encoding="utf-8"))
    text = _atlas_script_text(state)
    toks = re.findall(r"\S+", text)
    normed = [ATLAS_NORM(t) for t in toks]
    rc = float(state["rate_spec"]["rate_center_upm"])
    spoken_s = len(toks) / rc * 60.0
    pause_s = float(args.pause_budget_sec)
    voice_s = spoken_s + pause_s
    end_s = voice_s + 0.75
    t_word = lambda i: i / len(toks) * voice_s
    scenes = json.loads(Path(args.scenes).read_text(encoding="utf-8"))
    P = CHANNEL_PROFILE
    rows, cursor = [], 0
    for sc in scenes:
        if sc.get("kind") == "cold_open":
            rows.append(dict(sc, word_index=0, t_start=0.0, T_call="0"))
            continue
        if sc.get("kind") == "jumpscare":
            t0 = float(sc.get("t_start", 0.85))
            rows.append(dict(sc, word_index=None, t_start=t0, T_call=f"{t0}"))
            continue
        a = [ATLAS_NORM(w) for w in sc["anchor"].split()]
        hit = None
        for i in range(cursor, len(normed) - len(a) + 1):
            if normed[i:i + len(a)] == a:
                hit = i
                break
        if hit is None:
            sys.exit(f"[KIT-SCENES BLOCKER] anchor {sc['anchor']!r} of {sc['id']} not found after word {cursor} ({toks[cursor:cursor+6]})")
        occ = normed[: hit + 1].count(normed[hit])
        rows.append(dict(sc, word_index=hit, t_start=round(t_word(hit), 2), T_call=f'T("{normed[hit]}", {occ})'))
        cursor = hit + 1
    rows.sort(key=lambda r: r["t_start"])
    for i, r in enumerate(rows):
        r["t_end"] = round(rows[i + 1]["t_start"] if i + 1 < len(rows) else end_s, 2)
        r["dur"] = round(r["t_end"] - r["t_start"], 2)
    durs = [r["dur"] for r in rows]
    gates = []
    def gate(name, ok, detail):
        gates.append({"gate": name, "pass": bool(ok), "detail": detail})
    gate("shots_26_34", P["shots_gate"][0] <= len(rows) <= P["shots_gate"][1], len(rows))
    mean = sum(durs) / len(durs)
    gate("mean_shot_2.1_2.7", P["mean_shot_gate_s"][0] <= mean <= P["mean_shot_gate_s"][1], round(mean, 2))
    longs = [(r["id"], r["dur"]) for r in rows if r["dur"] > (P["title_max_shot_s"] if r.get("kind") == "title" else P["max_shot_s"])]
    gate("max_shot_le_5s_title_le_7s", not longs, longs or "ok")
    js = [r for r in rows if r.get("kind") == "jumpscare"]
    gate("jumpscare_in_0.8_1.7s", bool(js) and P["jumpscare_window_s"][0] <= js[0]["t_start"] <= P["jumpscare_window_s"][1], js[0]["t_start"] if js else "missing")
    hc = [r for r in rows if r.get("kind") == "hook_card"]
    gate("hook_card_5_9s", bool(hc) and 4.0 <= hc[0]["t_start"] <= 9.0, hc[0]["t_start"] if hc else "missing")
    tc = [r for r in rows if r.get("kind") == "title"]
    gate("title_card_present_dissolve_or_variant", bool(tc), tc[0]["t_start"] if tc else "missing")
    gate("est_duration_68_78", P["duration_gate_s"][0] <= end_s <= P["duration_gate_s"][1], round(end_s, 1))
    chunks = _caption_chunks(text)
    payload = {"topic_id": args.topic_id, "timing_status": "ESTIMATED_FROM_RATE (re-derive from voice_milo_transcript.json)",
               "est_voice_s": round(voice_s, 2), "est_end_s": round(end_s, 2), "pause_budget_s": pause_s,
               "scenes": rows, "gates": gates, "chunks_draft": chunks}
    slug = state["slug"]
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    jp = out_dir / f"05-TT-KIT-SCENES-{slug}.json"
    jp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [f"# 05 · Kit scene plan — {args.topic_id} {slug}", "",
          f"Timing ESTIMATED at {rc:.0f} wpm + {pause_s:.1f} s pauses → voice ≈ {voice_s:.1f} s, END ≈ {end_s:.1f} s. "
          "After TTS: re-run on the real transcript; the `T()` calls stay valid (occurrence counted on the script words).", "",
          "| # | id | kind | est start | est dur | kit anchor | words | what we SEE (motion in the shot) | camera / transition | SFX cue |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        wi = r.get("word_index")
        nxt = next((rr["word_index"] for rr in rows[i:] if rr.get("word_index") is not None), len(toks))
        words_txt = " ".join(toks[wi:nxt]) if wi is not None else "(no words: captions hidden)"
        md.append(f"| {i} | {r['id']} | {r.get('kind','normal')} | {r['t_start']:.2f} | {r['dur']:.2f} | `{r['T_call']}` | {words_txt} | {r.get('desc','')} | {r.get('camera','')} | {r.get('sfx','')} |")
    md += ["", "## Gates", ""] + [f"- {'PASS' if g['pass'] else 'FAIL'} {g['gate']}: {g['detail']}" for g in gates]
    md += ["", "## CHUNKS draft (paste into render_epXX.py; `#` = hidden while the hook card shows)", "", "```python",
           "CHUNKS = " + json.dumps(chunks, ensure_ascii=False), "```"]
    mp = out_dir / f"05-TT-KIT-SCENES-{slug}.md"
    mp.write_text("\n".join(md) + "\n", encoding="utf-8")
    for g in gates:
        print(f"  {'PASS' if g['pass'] else 'FAIL'} {g['gate']}: {g['detail']}")
    print(f"[KIT SCENES] {len(rows)} shots | mean {mean:.2f}s | END≈{end_s:.1f}s | {mp}")
    if args.strict and not all(g["pass"] for g in gates):
        sys.exit("[KIT-SCENES BLOCKER] gate(s) failed")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="TikTok Raw Suite v4.0 Deterministic CLI Engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ts = sub.add_parser("twin-seo-check", help="Check Twin lexical clone risk, TikTok Search SEO & FYP throttled words")
    p_ts.add_argument("--candidate", action="append", required=True, help="Candidate hook/premise/caption (repeatable)")
    p_ts.add_argument("--competitor", action="append", help="Competitor hook/title to check Twin risk against")
    p_ts.add_argument("--own-past", action="append", help="Own past video hook/title to avoid self-cloning")
    p_ts.add_argument("--seo-keywords", default="", help="Comma-separated TikTok Search SEO target phrases")
    p_ts.add_argument("--lang", choices=["auto", "space", "cjk"], default="auto")
    p_ts.add_argument("--json-out", help="Optional JSON output path")
    p_ts.set_defaults(func=cmd_twin_seo_check)

    p_init = sub.add_parser("init", help="Initialize sequential TikTok modular script state")
    p_init.add_argument("--workspace", required=True)
    p_init.add_argument("--topic-id", required=True)
    p_init.add_argument("--slug", required=True)
    p_init.add_argument(
        "--track",
        choices=["creator_rewards", "viral_short", "serial_sub60", "true_story", "extended_story"],
        default="creator_rewards",
    )
    p_init.add_argument("--mode", choices=["clean_voiceover", "dialogue_scenes"], default="clean_voiceover")
    p_init.add_argument(
        "--count-unit",
        choices=["words", "whitespace_words", "vietnamese_syllables", "non_space_chars"],
        default="words",
    )
    p_init.add_argument("--part-budgets", required=True, help="Comma-separated spoken unit budgets, e.g. 65,95,95,70")
    p_init.add_argument("--rate", default=CHANNEL_PROFILE["rate_center"], type=float)
    p_init.add_argument("--rate-min", default=CHANNEL_PROFILE["rate_min"], type=float)
    p_init.add_argument("--rate-max", default=CHANNEL_PROFILE["rate_max"], type=float)
    p_init.add_argument("--rate-basis", choices=["MEASURED_SAMPLE", "PLANNING_ASSUMPTION", "ASSUMED_PLANNING_RATE"], default="MEASURED_SAMPLE")
    p_init.add_argument("--non-speech-sec", default=0.0, type=float)
    p_init.add_argument("--max-beat-sec", default=8.5, type=float)
    p_init.add_argument("--max-open-sentence-units", type=int)
    p_init.add_argument("--frame0-text", help="Frame-0 Safe-Zone overlay text (max 2 lines)")
    p_init.add_argument("--clean-tts", action=argparse.BooleanOptionalAction, default=True)
    p_init.add_argument("--strict-natural-speech", action="store_true", help="Block em-dash and arrow symbols")
    p_init.add_argument("--allow-exception", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_vp = sub.add_parser("verify-part", help="Verify sequential part P0k")
    p_vp.add_argument("--workspace", required=True)
    p_vp.add_argument("--topic-id", required=True)
    p_vp.add_argument("--part-id", required=True)
    p_vp.add_argument("--file", required=True)
    p_vp.add_argument("--revision", default=1, type=int)
    p_vp.add_argument("--allow-deviation", action="store_true")
    p_vp.add_argument("--allow-guess", action="store_true")
    p_vp.add_argument("--allow-ai-punct", action="store_true")
    p_vp.set_defaults(func=cmd_verify_part)

    p_oa = sub.add_parser("opening-audit", help="Audit 0-3s / 3-15s / 15-30s FYP swipe gate & visual contiguity")
    p_oa.add_argument("--workspace", required=True)
    p_oa.add_argument("--topic-id", required=True)
    p_oa.add_argument("--p01-only", action="store_true")
    p_oa.add_argument("--frame0-text", help="Update Frame-0 Safe-Zone text")
    p_oa.add_argument("--max-open-sentence-units", type=int)
    p_oa.add_argument("--strict", action="store_true")
    p_oa.set_defaults(func=cmd_opening_audit)

    p_ba = sub.add_parser("beat-audit", help="Audit spoken beat durations")
    p_ba.add_argument("--workspace", required=True)
    p_ba.add_argument("--topic-id", required=True)
    p_ba.add_argument("--max-beat-sec", default=None, type=float)
    p_ba.add_argument("--strict", action="store_true")
    p_ba.set_defaults(func=cmd_beat_audit)

    p_sd = sub.add_parser("stitch-draft", help="Stitch passed parts & export seam anchors")
    p_sd.add_argument("--workspace", required=True)
    p_sd.add_argument("--topic-id", required=True)
    p_sd.set_defaults(func=cmd_stitch_draft)

    p_le = sub.add_parser("lock-export", help="Lock verified draft and export 4-file lossless 9:16 bundle")
    p_le.add_argument("--workspace", required=True)
    p_le.add_argument("--topic-id", required=True)
    p_le.add_argument("--out-dir", required=True)
    p_le.add_argument("--voice-sep", choices=["pipe", "newline"], default="pipe")
    p_le.add_argument("--allow-exception", action="store_true")
    p_le.add_argument("--allow-guess", action="store_true")
    p_le.set_defaults(func=cmd_lock_export)

    p_fd = sub.add_parser("fyp-diagnose", help="Post-publish FYP sprint/RPM, geo hygiene & D+7 shrinkage helper")
    p_fd.add_argument("--current-followers", type=int, default=0)
    p_fd.add_argument("--fol-per-k", type=float, default=5.0)
    p_fd.add_argument("--qualified-rate-pct", type=float, default=55.0)
    p_fd.add_argument("--rpm-usd", type=float, default=0.80)
    p_fd.add_argument("--qualified-geo-pct", type=float, help="Share of views from target qualified geo in pct")
    p_fd.add_argument("--views", type=int)
    p_fd.add_argument("--unique-viewers", type=int)
    p_fd.add_argument("--mean-with", type=float)
    p_fd.add_argument("--mean-without", type=float)
    p_fd.add_argument("--n-with", type=int)
    p_fd.add_argument("--n-without", type=int)
    p_fd.add_argument("--sigma-pts", type=float, default=8.0, help="Std dev of 3s/30s hold in percentage points")
    p_fd.add_argument("--delta-pts", type=float, default=5.0, help="Target detectable lift in percentage points")
    p_fd.add_argument("--json-out", help="Optional JSON output path")
    p_fd.set_defaults(func=cmd_fyp_diagnose)

    p_aa = sub.add_parser("atlas-audit", help="Dark Atlas 10-beat template / ellipsis / word-count / hook-card gate")
    p_aa.add_argument("--workspace", required=True)
    p_aa.add_argument("--topic-id", required=True)
    p_aa.add_argument("--strict", action="store_true")
    p_aa.set_defaults(func=cmd_atlas_audit)

    p_ks = sub.add_parser("kit-scenes", help="Scene plan JSON -> render_epXX.py T() anchors, shot gates, CHUNKS draft")
    p_ks.add_argument("--workspace", required=True)
    p_ks.add_argument("--topic-id", required=True)
    p_ks.add_argument("--scenes", required=True, help="JSON list of {id, anchor, kind, desc, camera, sfx}")
    p_ks.add_argument("--out-dir", required=True)
    p_ks.add_argument("--pause-budget-sec", type=float, default=0.0, help="Expected pauses not in the word rate (measured Milo: ~0)")
    p_ks.add_argument("--strict", action="store_true")
    p_ks.set_defaults(func=cmd_kit_scenes)

    return ap


if __name__ == "__main__":
    parser = build_parser()
    cli_args = parser.parse_args()
    cli_args.func(cli_args)
