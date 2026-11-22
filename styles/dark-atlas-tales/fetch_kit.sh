#!/usr/bin/env bash
# Restore the large files of the Dark Atlas kit that are not in git (music WAV masters, episode sfx.wav, the 3 approved
# videos in video_mau/) from the kit zip on Google Drive. Needs network access to drive.usercontent.google.com.
# Usage: styles/dark-atlas-tales/fetch_kit.sh [DRIVE_FILE_ID]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ID="${1:-14jO5Kk1QWOZxeb--xqu9vKMYajXqho9m}"   # DarkAtlas_US_States_Kit_2026-11-21.zip
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
curl -fSL -o "$TMP/kit.zip" "https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t"
unzip -q "$TMP/kit.zip" -d "$TMP"
SRC="$TMP/DarkAtlas_US_States_Kit"
( cd "$SRC" && find dark_atlas -name '*.wav' -print0 | while IFS= read -r -d '' f; do mkdir -p "$HERE/$(dirname "$f")"; [ -e "$HERE/$f" ] || cp "$f" "$HERE/$f"; done )
mkdir -p "$HERE/video_mau"; for v in "$SRC"/video_mau/*.mp4; do [ -e "$HERE/video_mau/$(basename "$v")" ] || cp "$v" "$HERE/video_mau/"; done
echo "restored WAV masters + video_mau/ into $HERE"
