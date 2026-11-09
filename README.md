# edittools

Free video editing helpers by [szy.monster](https://szy.monster/). Live at **https://edittools.szy.monster/**.

## AutoSubtitler

Drop in a video and get an `.srt` subtitle file, timed to the words. It runs in your browser,
so the video is never uploaded.

```
video ──► sound track (16 kHz mono) ──┬─► Whisper    : the words, with a time for each
                                      └─► Silero VAD : exactly when someone is talking
                                                │
                              autosubs.py  ◄────┘   sentences → short chunks → line up with speech → fix names
                                   │
                                   ▼
                                 .srt
```

There are two versions, and both use the same [`autosubs/autosubs.py`](autosubs/autosubs.py) for
everything after the transcription:

| | Web page | PC version (`autosubs/`) |
| --- | --- | --- |
| Sound | browser audio decoder | ffmpeg |
| Words | Whisper base or small (Transformers.js, WebAssembly) | whisper.cpp, large-v3-turbo |
| Speech times | Silero VAD v5 (ONNX Runtime Web) | Silero VAD v5 (whisper.cpp) |
| Cutting, timing, terms, `.srt` | `autosubs.py` in Pyodide | `autosubs.py` |

The PC version: see [autosubs/README.txt](autosubs/README.txt) and [autosubs/SETUP.md](autosubs/SETUP.md).

## Files

- `index.html`, `style.css`, `app.js`: the page. `app.js` reads the sound, starts the worker, then runs
  `py/web_glue.py`, which imports `autosubs/autosubs.py` unchanged.
- `asr-worker.js`: built from `src/asr-worker.js` (Silero VAD + Whisper). Rebuild with `npm install && npm run build`.
- `vendor/`: Pyodide, the ONNX Runtime WebAssembly files and the Silero model, served from this site
  (see [vendor/NOTICES.md](vendor/NOTICES.md)). Only the Whisper model comes from Hugging Face,
  when someone first makes subtitles.
- `_headers`: makes the page cross-origin isolated so Whisper can use several CPU cores.
- `privacy.html`: privacy notice.

## Run it locally

Double-click `run-local.bat` (or run `python serve.py`) and open http://127.0.0.1:8000/.
`serve.py` sends the same headers as Cloudflare; a plain `python -m http.server` works too, but slower.

## Hosting

Cloudflare Workers, static assets only (`wrangler.jsonc`, `npx wrangler deploy`). Nothing is built on Cloudflare:
the built `asr-worker.js` and `vendor/` files are committed.
