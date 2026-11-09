AutoSubs: local Whisper subtitles for DaVinci Resolve (free)
============================================================

MAKE SUBTITLES
  Drag one or more video files onto Subtitle.bat.
  A .srt file with the same name appears next to each video.
  (Runs on the CPU: roughly as long as the video itself, so a 10 minute video takes about 11 minutes.)
  If a .srt already exists it is kept as NAME.old.srt.

NAMES AND TERMS
  Edit terms.txt. Each term is given to Whisper as a hint and its spelling/casing is forced in the output.
  For a word Whisper keeps mishearing, add a line like:  Simon => Szymon

IMPORT INTO DAVINCI RESOLVE (free)
  1. File > Import > Subtitle..., pick the .srt. It lands in the Media Pool.
  2. Drag it from the Media Pool onto the timeline, above the video, starting at the same point as the clip.
     Resolve adds a "Subtitle" track for it.
     (If your clip doesn't start at the very beginning of the timeline, line the subtitle clip up with the video clip's start.)
  3. Click the subtitle track to edit text or timing in the Inspector. Style for the whole track:
     select the track header > Inspector > Track tab (font, size, outline, position).
  4. Export: Deliver page > Subtitle Settings > tick "Export Subtitle", then
     "Burn into video" for captions baked into the picture, or "As a separate file" for YouTube-style captions.

SETTINGS
  Top of autosubs.py: language (English), and how big each subtitle is.
  Default is short one-line chunks: up to 6 words / 30 characters, timed to the words (within ~0.2 s).
  For classic sentence-style subtitles set MAX_LINE = 42, MAX_LINES = 2, MAX_WORDS = 20, MAX_DURATION = 7.0

FOLDERS
  bin\whisper-cpu  whisper.cpp (CPU build). A GPU build placed in bin\whisper-vulkan would be used first.
  bin\ffmpeg       ffmpeg, to pull the audio out of the video
  models           Whisper large-v3-turbo (q5_0) and the Silero speech detector used to line up the timing
