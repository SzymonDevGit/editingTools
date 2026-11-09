// Speech work for AutoSubtitler, run off the main thread so the page stays responsive.
//  1. Silero VAD finds where someone is talking (same model as the PC tool's ggml-silero-v5.1.2).
//  2. Whisper (transformers.js, ONNX on WebAssembly) turns each stretch of speech into words with times.
// The words go back to the page in whisper.cpp's JSON shape, so autosubs.py can read them unchanged.
//
// Build: npm run build  (bundles this file into /asr-worker.js)

import * as ort from 'onnxruntime-web/wasm';
import { pipeline, env } from '@huggingface/transformers';

const SR = 16000;
const ORT_DIR = new URL('vendor/ort/', self.location.href).href;
const SILERO_URL = new URL('vendor/silero/silero_vad_v5.onnx', self.location.href).href;

// Keep everything we ship on our own site; only the Whisper model itself comes from Hugging Face.
ort.env.wasm.wasmPaths = {
  mjs: ORT_DIR + 'ort-wasm-simd-threaded.mjs',
  wasm: ORT_DIR + 'ort-wasm-simd-threaded.wasm',
};
ort.env.wasm.numThreads = self.crossOriginIsolated ? Math.min(8, navigator.hardwareConcurrency || 4) : 1;
env.backends.onnx.wasm.wasmPaths = ort.env.wasm.wasmPaths;
env.allowLocalModels = false;

const post = (type, data = {}) => self.postMessage({ type, ...data });

// ---- Silero VAD -----------------------------------------------------------
// Settings match the PC tool's call: whisper-vad-speech-segments -vsd 200 -vp 0
const VAD = {
  threshold: 0.5,          // whisper.cpp default
  minSpeechMs: 250,        // whisper.cpp default
  minSilenceMs: 200,       // -vsd 200
  speechPadMs: 0,          // -vp 0
};
const FRAME = 512, CONTEXT = 64;

let sileroSession = null;

async function speechProbs(audio) {
  if (!sileroSession) {
    const buf = await (await fetch(SILERO_URL)).arrayBuffer();
    sileroSession = await ort.InferenceSession.create(buf);
  }
  const sr = new ort.Tensor('int64', BigInt64Array.from([BigInt(SR)]), []);
  let state = new ort.Tensor('float32', new Float32Array(2 * 128), [2, 1, 128]);
  let context = new Float32Array(CONTEXT);
  const probs = [];
  const n = Math.ceil(audio.length / FRAME);
  for (let i = 0; i < n; i++) {
    const frame = new Float32Array(FRAME);
    frame.set(audio.subarray(i * FRAME, (i + 1) * FRAME));
    const input = new Float32Array(CONTEXT + FRAME);
    input.set(context, 0);
    input.set(frame, CONTEXT);
    context = frame.slice(-CONTEXT);
    const out = await sileroSession.run({
      input: new ort.Tensor('float32', input, [1, input.length]), state, sr,
    });
    state = out.stateN;
    probs.push(out.output.data[0]);
    if (i % 200 === 0) post('progress', { stage: 'vad', done: i, total: n });
  }
  return probs;
}

// Silero's get_speech_timestamps(), returned in seconds.
function speechSegments(probs, totalSamples) {
  const { threshold, minSpeechMs, minSilenceMs, speechPadMs } = VAD;
  const neg = Math.max(threshold - 0.15, 0.01);
  const minSpeech = SR * minSpeechMs / 1000;
  const minSilence = SR * minSilenceMs / 1000;
  const pad = SR * speechPadMs / 1000;
  const segs = [];
  let triggered = false, cur = null, tempEnd = 0;
  probs.forEach((p, i) => {
    const pos = i * FRAME;
    if (p >= threshold && tempEnd) tempEnd = 0;
    if (p >= threshold && !triggered) { triggered = true; cur = { start: pos }; return; }
    if (p < neg && triggered) {
      if (!tempEnd) tempEnd = pos;
      if (pos - tempEnd < minSilence) return;
      cur.end = tempEnd;
      if (cur.end - cur.start > minSpeech) segs.push(cur);
      cur = null; tempEnd = 0; triggered = false;
    }
  });
  if (cur && totalSamples - cur.start > minSpeech) { cur.end = totalSamples; segs.push(cur); }
  return segs.map(s => [
    Math.max(0, s.start - pad) / SR,
    Math.min(totalSamples, s.end + pad) / SR,
  ]);
}

// ---- Whisper ----------------------------------------------------------------
let asr = null, asrModel = null;

async function loadWhisper(model) {
  if (asr && asrModel === model) return asr;
  const files = {};
  asr = await pipeline('automatic-speech-recognition', model, {
    device: 'wasm',
    dtype: 'q8',
    progress_callback: (p) => {
      if (p.status === 'progress' && p.total) {
        files[p.file] = [p.loaded, p.total];
        const vals = Object.values(files);
        post('progress', {
          stage: 'download',
          done: vals.reduce((a, v) => a + v[0], 0),
          total: vals.reduce((a, v) => a + v[1], 0),
        });
      }
    },
  });
  asrModel = model;
  return asr;
}

// Group the speech into pieces of at most ~28 s (Whisper hears 30 s at a time).
function pieces(speech, duration) {
  if (!speech.length) return [[0, duration]];
  const out = [];
  let [a, b] = speech[0];
  for (const [s, e] of speech.slice(1)) {
    if (e - a <= 28) b = e;
    else { out.push([a, b]); [a, b] = [s, e]; }
  }
  out.push([a, b]);
  return out.map(([s, e]) => [Math.max(0, s - 0.3), Math.min(duration, e + 0.3)]);
}

async function transcribe(audio, speech, lang) {
  const duration = audio.length / SR;
  const parts = pieces(speech, duration);
  const transcription = [];
  for (let i = 0; i < parts.length; i++) {
    post('progress', { stage: 'whisper', done: i, total: parts.length });
    const [s, e] = parts[i];
    const clip = audio.subarray(Math.floor(s * SR), Math.ceil(e * SR));
    const opts = { task: 'transcribe', return_timestamps: 'word' };
    if (lang !== 'auto') opts.language = lang;
    if (e - s > 30) { opts.chunk_length_s = 30; opts.stride_length_s = 5; }
    const res = await asr(clip, opts);
    // One whisper.cpp-style segment per piece: each word becomes a token that starts with a space.
    const tokens = (res.chunks || [])
      .filter(w => w.text && w.text.trim())
      .map(w => {
        const from = (s + (w.timestamp[0] ?? 0)) * 1000;
        const to = (s + (w.timestamp[1] ?? w.timestamp[0] ?? 0)) * 1000;
        return { text: ' ' + w.text.trim(), offsets: { from: Math.round(from), to: Math.round(Math.max(to, from)) }, t_dtw: -1 };
      });
    if (tokens.length) transcription.push({ tokens });
  }
  post('progress', { stage: 'whisper', done: parts.length, total: parts.length });
  return { transcription };
}

self.onmessage = async ({ data }) => {
  // 'speech' only runs the speech detector (handy for checking timing problems).
  if (data.type === 'speech') {
    try {
      post('done', { speech: speechSegments(await speechProbs(data.audio), data.audio.length) });
    } catch (err) {
      post('error', { message: String(err && err.message || err) });
    }
    return;
  }
  if (data.type !== 'run') return;
  try {
    const { audio, model, lang } = data;
    post('stage', { stage: 'download' });
    try {
      await loadWhisper(model);
    } catch (err) {
      console.error(err);
      throw new Error("Couldn't download the Whisper model from Hugging Face. Check your internet connection, "
        + 'or whether a browser extension or network filter is blocking huggingface.co. (' + (err && err.message || err) + ')');
    }
    post('stage', { stage: 'vad' });
    const speech = speechSegments(await speechProbs(audio), audio.length);
    post('stage', { stage: 'whisper' });
    const result = await transcribe(audio, speech, lang);
    post('done', { result, speech });
  } catch (err) {
    post('error', { message: String(err && err.message || err) });
  }
};
