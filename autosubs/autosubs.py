"""Make an .srt subtitle file next to a video, using Whisper (whisper.cpp) locally.

Usage: drag video files onto Subtitle.bat, or run
    python autosubs.py [--lang en|pl|auto] VIDEO [VIDEO ...]

Names and terms go in terms.txt next to this file.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

# ---- Settings you might want to change ------------------------------------

LANGUAGE = "en"          # "en", "pl", ... or "auto" (detects from the first 30 s)
MAX_LINE = 30            # characters per subtitle line (42 is the usual TV/film size)
MAX_LINES = 1            # lines per subtitle (2 for classic sentence-style subtitles)
MAX_WORDS = 6            # words per subtitle
MAX_DURATION = 4.0       # seconds a single subtitle may stay on screen (7 for sentence-style)
MIN_DURATION = 1.0       # seconds; short subtitles are stretched to this if there is room
PAUSE_BREAK = 0.7        # a pause this long (seconds) always starts a new subtitle
GAP = 0.05               # seconds left empty between back-to-back subtitles
DROP_SOUND_TAGS = True   # drop things like [Music] or (laughs)

# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "models", "ggml-large-v3-turbo-q5_0.bin")
FFMPEG = os.path.join(HERE, "bin", "ffmpeg", "ffmpeg.exe")
VAD_MODEL = os.path.join(HERE, "models", "ggml-silero-v5.1.2.bin")
VAD_EXE = os.path.join(HERE, "bin", "whisper-cpu", "whisper-vad-speech-segments.exe")
TERMS_FILE = os.path.join(HERE, "terms.txt")
# The first whisper build found is used, so a GPU build wins over the CPU one.
WHISPER_BUILDS = [
    ("GPU (Vulkan)", os.path.join(HERE, "bin", "whisper-vulkan", "whisper-cli.exe")),
    ("CPU", os.path.join(HERE, "bin", "whisper-cpu", "whisper-cli.exe")),
]


class Failed(Exception):
    pass


def fail(msg):
    raise Failed(msg)


def load_terms():
    """terms.txt: one term per line, or 'wrong => right' fix-ups. '#' starts a comment."""
    terms, fixes = [], []
    if not os.path.exists(TERMS_FILE):
        return terms, fixes
    with open(TERMS_FILE, encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "=>" in line:
                wrong, right = (p.strip() for p in line.split("=>", 1))
                if wrong and right:
                    fixes.append((wrong, right))
                    if right not in terms:
                        terms.append(right)
            else:
                for term in line.split(","):
                    term = term.strip()
                    if term and term not in terms:
                        terms.append(term)
    # Every term also forces its own spelling, so "scrapyard" becomes "Scrapyard".
    fixes += [(t, t) for t in terms]
    return terms, fixes


def apply_fixes(text, fixes):
    for wrong, right in fixes:
        text = re.sub(r"(?<!\w)" + re.escape(wrong) + r"(?!\w)", right, text, flags=re.IGNORECASE)
    return text


def run(cmd, **kw):
    return subprocess.run(cmd, check=False, **kw)


def extract_audio(video, wav):
    r = run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", video,
             "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])
    if r.returncode != 0 or not os.path.exists(wav):
        fail("ffmpeg could not read the audio from this file (does it have a sound track?).")


def find_speech(wav):
    """Return [(start, end), ...] in seconds where someone is talking, using the Silero VAD.

    It hears speech through game sound and music, which Whisper's own times don't handle well.
    """
    if not (os.path.exists(VAD_EXE) and os.path.exists(VAD_MODEL)):
        return []
    r = run([VAD_EXE, "-vm", VAD_MODEL, "-f", wav, "-vsd", "200", "-vp", "0", "-np"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
    found = re.findall(r"Speech segment \d+: start = ([\d.]+), end = ([\d.]+)", r.stdout + r.stderr)
    return [(float(a) / 100, float(b) / 100) for a, b in found]


def transcribe(wav, out_base, lang, prompt):
    for label, exe in WHISPER_BUILDS:
        if os.path.exists(exe):
            break
    else:
        fail("whisper-cli.exe not found in the bin folder.")
    print(f"Transcribing on {label} (language: {lang})...")
    # -dtw gives much better per-word times than whisper's default; it needs flash attention off.
    cmd = [exe, "-m", MODEL, "-f", wav, "-l", lang, "-t", str(max(1, (os.cpu_count() or 2) // 2)),
           "-dtw", "large.v3.turbo", "-nfa", "-ojf", "-of", out_base, "-pp", "-np"]
    if prompt:
        cmd += ["--prompt", prompt]
    r = run(cmd)
    if r.returncode != 0 or not os.path.exists(out_base + ".json"):
        fail(f"whisper-cli failed (exit code {r.returncode}).")
    with open(out_base + ".json", encoding="utf-8", errors="replace") as f:
        return json.load(f)


DTW_LAG = 0.23  # DTW marks a word ~0.23 s after it starts (measured against exact word times)


def words_from(result):
    """Join whisper's sub-word tokens into words with start/end times in seconds."""
    words = []
    for seg in result.get("transcription", []):
        seg_words = []
        for tok in seg.get("tokens", []):
            text = tok["text"]
            if text.startswith("[_") or not text:
                continue
            start, end = tok["offsets"]["from"] / 1000, tok["offsets"]["to"] / 1000
            if tok.get("t_dtw", -1) > 0:
                start = max(0.0, tok["t_dtw"] / 100 - DTW_LAG)
            if seg_words and not text.startswith(" "):
                w = seg_words[-1]
                w["text"] += text
                w["end"] = max(w["end"], end)
            else:
                seg_words.append({"text": text.strip(), "start": start, "end": end})
        seg_words = [w for w in seg_words if w["text"]]
        if not seg_words:
            continue
        # The DTW start times can overtake whisper's end times, so keep each word inside its slot.
        for a, b in zip(seg_words, seg_words[1:]):
            a["end"] = max(a["start"] + 0.1, min(a["end"], b["start"]))
        seg_words[-1]["end"] = max(seg_words[-1]["end"], seg_words[-1]["start"] + 0.3)
        # Whisper ends each segment at a sentence end; keep that so we can break there.
        seg_words[-1]["seg_end"] = True
        words.extend(seg_words)
    if DROP_SOUND_TAGS:
        words = drop_sound_tags(words)
    return words


def drop_sound_tags(words):
    out, depth = [], 0
    for w in words:
        opens = w["text"].count("[") + w["text"].count("(")
        closes = w["text"].count("]") + w["text"].count(")")
        if depth == 0 and opens and w["text"][0] in "[(":
            depth = opens - closes
            if depth <= 0 and w["text"][-1] in "])":
                depth = 0
            continue
        if depth > 0:
            depth -= closes - opens
            continue
        out.append(w)
    return out


def text_of(ws):
    return " ".join(w["text"] for w in ws)


def fits(ws):
    return (len(text_of(ws)) <= MAX_LINE * MAX_LINES and len(ws) <= MAX_WORDS
            and ws[-1]["end"] - ws[0]["start"] <= MAX_DURATION)


def paused(a, b, speech):
    """True if the speaker pauses between word a and word b."""
    if speech:
        return any(a["start"] < end and start <= b["start"] + 0.3 and start - end >= 0.3
                   for (_, end), (start, _) in zip(speech, speech[1:]))
    return b["start"] - a["end"] >= PAUSE_BREAK


def sentences(words, speech):
    """Split at sentence ends, whisper segment ends and pauses."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or w["text"][-1] in ".?!" or w.get("seg_end") or paused(w, nxt, speech):
            out.append(cur)
            cur = []
    return out


# A chunk shouldn't end on one of these ("look at the / Scrapyard theme")...
NO_END = set("a an the to of in on at for from with by into onto about my your his her its our their "
             "this that these those is are was were be been am i you we they he she it i'm you're "
             "we're they're it's can will would should could has have had do does did not very "
             "so and or but if than as".split())
# ...and is best started on one of these ("so the player has to").
GOOD_START = set("and but so or because then when which who that if while until".split())


def split_sentence(ws, speech=()):
    """Cut a sentence that is too long into even pieces, at commas, pauses and phrase edges."""
    if len(ws) == 1 or fits(ws):
        return [ws]
    total = len(text_of(ws))
    best, best_score = 1, None
    for i in range(1, len(ws)):
        a = len(text_of(ws[:i]))
        score = abs(a - total / 2)
        before, after = ws[i - 1]["text"], ws[i]["text"]
        if before[-1] in ",;:":
            score -= 15
        if before.lower().strip(",;:") in NO_END:
            score += 12
        if after.lower() in GOOD_START:
            score -= 6
        if speech and paused(ws[i - 1], ws[i], speech):
            score -= 15
        if best_score is None or score < best_score:
            best, best_score = i, score
    return split_sentence(ws[:best], speech) + split_sentence(ws[best:], speech)


def group_into_cues(words, speech):
    cues = []
    for s in sentences(words, speech):
        cues.extend(split_sentence(s, speech))
    # Join very short neighbours (like "Okay." "So.") when they fit together without a pause.
    merged = []
    for c in cues:
        if (merged and len(text_of(c)) < 10 and fits(merged[-1] + c)
                and not paused(merged[-1][-1], c[0], speech)):
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    return merged


def wrap(text):
    if len(text) <= MAX_LINE or MAX_LINES < 2:
        return text
    best, best_score = None, None
    for m in re.finditer(" ", text):
        a, b = text[:m.start()], text[m.start() + 1:]
        over = max(0, len(a) - MAX_LINE) + max(0, len(b) - MAX_LINE)
        # Fit first, then balance, with a small bonus for breaking after punctuation.
        score = over * 100 + abs(len(a) - len(b)) - (6 if a[-1] in ",.;:?!" else 0)
        if best_score is None or score < best_score:
            best, best_score = (a, b), score
    return "\n".join(best) if best else text


def snap(t, points, before, after):
    """Move t to the nearest point within [t-before, t+after], if any."""
    near = [p for p in points if t - before <= p <= t + after]
    return min(near, key=lambda p: abs(p - t)) if near else t


def in_speech(t, speech):
    return any(a <= t <= b for a, b in speech)


def fix_start(t, speech):
    # A subtitle can't start while nobody is talking: move it to where talking resumes.
    if speech and not in_speech(t, speech):
        later = [a for a, _ in speech if a > t]
        if later and later[0] - t <= 5:
            return later[0]
    return snap(t, [a for a, _ in speech], 0.3, 0.3)


def fix_end(t, start, speech):
    if speech and not in_speech(t, speech):
        earlier = [b for _, b in speech if start < b < t]
        if earlier:
            return earlier[-1]
    return snap(t, [b for _, b in speech], 0.3, 0.3)


def timed_cues(cues, speech, fixes):
    out = []
    for c in cues:
        # Whisper can drift by a second or more after music or silence, so line up with the speech.
        start = fix_start(c[0]["start"], speech)
        end = fix_end(c[-1]["end"], start, speech)
        end = max(end, start + 0.3)
        text = apply_fixes(text_of(c), fixes)
        out.append([start, end, wrap(text)])
    for i, cue in enumerate(out):
        if i + 1 == len(out):
            cue[1] = max(cue[1], cue[0] + MIN_DURATION)
            break
        nxt = out[i + 1][0]
        if not paused(cues[i][-1], cues[i + 1][0], speech):
            # Mid-sentence: hand straight over to the next chunk so the text doesn't flicker.
            cue[1] = nxt - GAP
        elif cue[1] - cue[0] < MIN_DURATION:
            cue[1] = cue[0] + MIN_DURATION
        cue[1] = max(cue[0] + 0.2, min(cue[1], nxt - GAP))
    return out


def srt_time(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(path, cues):
    if os.path.exists(path):
        old = os.path.splitext(path)[0] + ".old.srt"
        os.replace(path, old)
        print(f"(Kept the previous file as {os.path.basename(old)})")
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        for i, (start, end, text) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n\n")


def subtitle(video, lang, terms, fixes):
    print(f"\n=== {os.path.basename(video)} ===")
    started = time.time()
    tmp = tempfile.mkdtemp(prefix="autosubs_")
    try:
        wav = os.path.join(tmp, "audio.wav")
        extract_audio(video, wav)
        prompt = ", ".join(terms) + "." if terms else ""
        result = transcribe(wav, os.path.join(tmp, "out"), lang, prompt)
        words = words_from(result)
        if not words:
            print("No speech found, nothing written.")
            return
        speech = find_speech(wav)
        cues = group_into_cues(words, speech)
        cues = timed_cues(cues, speech, fixes)
        srt = os.path.splitext(video)[0] + ".srt"
        write_srt(srt, cues)
        print(f"Wrote {len(cues)} subtitles to {srt} in {time.time() - started:.0f} s")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", default=LANGUAGE, help="en, pl, auto, ... (default: %(default)s)")
    ap.add_argument("videos", nargs="+")
    args = ap.parse_args()
    for p in (MODEL, FFMPEG):
        if not os.path.exists(p):
            print(f"ERROR: Missing {p}")
            sys.exit(1)
    terms, fixes = load_terms()
    if terms:
        print("Terms:", ", ".join(terms))
    failed = 0
    for video in args.videos:
        if not os.path.isfile(video):
            print(f"\nSkipping {video}: not a file.")
            continue
        try:
            subtitle(os.path.abspath(video), args.lang, terms, fixes)
        except Failed as e:
            failed += 1
            print(f"ERROR: {e}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
