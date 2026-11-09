"""Runs Szymon's autosubs.py inside the browser (Pyodide).

The PC tool calls ffmpeg, whisper-cli and the Silero VAD itself. On the web page those three
steps happen in JavaScript (the browser's audio decoder, Whisper in WebAssembly, Silero in
WebAssembly), then everything after that is the unchanged code from autosubs/autosubs.py:
splitting into sentences and short chunks, lining the times up with the speech, the terms.txt
fix-ups and writing the .srt.
"""

import json
import os

import autosubs

# Subtitle styles from autosubs/README.txt.
STYLES = {
    "short": dict(MAX_LINE=30, MAX_LINES=1, MAX_WORDS=6, MAX_DURATION=4.0),
    "sentence": dict(MAX_LINE=42, MAX_LINES=2, MAX_WORDS=20, MAX_DURATION=7.0),
}
TERMS_PATH = "/tmp/terms.txt"
SRT_PATH = "/tmp/subtitles.srt"


def make_srt(result_json, speech_json, terms_text, style):
    for name, value in STYLES.get(style, STYLES["short"]).items():
        setattr(autosubs, name, value)
    with open(TERMS_PATH, "w", encoding="utf-8") as f:
        f.write(terms_text or "")
    autosubs.TERMS_FILE = TERMS_PATH
    terms, fixes = autosubs.load_terms()

    words = autosubs.words_from(json.loads(result_json))
    if not words:
        return ""
    speech = [tuple(s) for s in json.loads(speech_json)]
    cues = autosubs.group_into_cues(words, speech)
    cues = autosubs.timed_cues(cues, speech, fixes)

    if os.path.exists(SRT_PATH):
        os.remove(SRT_PATH)
    autosubs.write_srt(SRT_PATH, cues)
    with open(SRT_PATH, encoding="utf-8", newline="") as f:
        return f.read()
