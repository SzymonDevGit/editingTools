# Third-party files in vendor/

These run in the visitor's browser and are served from this site, so nothing loads from a CDN.

| Folder | What | Licence |
| --- | --- | --- |
| `pyodide/` | [Pyodide](https://pyodide.org/) 0.26.4, Python compiled to WebAssembly | MPL-2.0 (Python itself: PSF licence) |
| `ort/` | [ONNX Runtime Web](https://github.com/microsoft/onnxruntime) WebAssembly build | MIT, Microsoft |
| `silero/` | [Silero VAD](https://github.com/snakers4/silero-vad) v5 model, from [@ricky0123/vad-web](https://github.com/ricky0123/vad) | MIT, Silero Team |
| `transformers/` | Licence for [Transformers.js](https://github.com/huggingface/transformers.js), bundled into `asr-worker.js` | Apache-2.0 |

The Whisper models (OpenAI, MIT licence) are downloaded from Hugging Face by the visitor's browser
when they first make subtitles, and are not stored in this repo.
