// AutoSubtitler page: picks the video, runs the speech worker, then hands the words to autosubs.py.

const $ = (id) => document.getElementById(id);
const SR = 16000;

let file = null;
let srtName = 'subtitles.srt';
let videoUrl = null;
let trackUrl = null;

// ---------- picking a file ----------
const drop = $('drop');
const input = $('file');

function pick(f) {
  if (!f) return;
  file = f;
  srtName = f.name.replace(/\.[^.]+$/, '') + '.srt';
  $('drop-title').textContent = f.name;
  $('drop-sub').textContent = `${(f.size / 1048576).toFixed(1)} MB · click to choose a different file`;
  drop.classList.add('has-file');
  $('go').disabled = false;
  hideError();
}
input.addEventListener('change', () => pick(input.files[0]));
['dragenter', 'dragover'].forEach((e) => drop.addEventListener(e, (ev) => { ev.preventDefault(); drop.classList.add('over'); }));
['dragleave', 'drop'].forEach((e) => drop.addEventListener(e, () => drop.classList.remove('over')));
drop.addEventListener('drop', (ev) => { ev.preventDefault(); pick(ev.dataTransfer.files[0]); });

// ---------- progress ----------
const ORDER = ['audio', 'download', 'vad', 'whisper', 'python'];
const WEIGHT = { audio: 5, download: 15, vad: 10, whisper: 62, python: 8 };

function setStage(stage) {
  const i = ORDER.indexOf(stage);
  document.querySelectorAll('#stages li').forEach((li) => {
    const j = ORDER.indexOf(li.dataset.stage);
    li.classList.toggle('done', j < i);
    li.classList.toggle('now', j === i);
  });
  setBar(stage, 0);
}
function setBar(stage, frac) {
  const i = ORDER.indexOf(stage);
  let pct = 0;
  for (let k = 0; k < i; k++) pct += WEIGHT[ORDER[k]];
  pct += WEIGHT[stage] * Math.max(0, Math.min(1, frac));
  $('bar-fill').style.width = pct.toFixed(1) + '%';
}
function show(step) {
  ['step-pick', 'step-run', 'step-done'].forEach((s) => { $(s).hidden = s !== step; });
}
function showError(msg) {
  const el = $('error');
  el.textContent = msg;
  el.hidden = false;
}
function hideError() { $('error').hidden = true; }

// ---------- audio ----------
async function readAudio(f) {
  const buf = await f.arrayBuffer();
  // Decoding with a 16 kHz context resamples for us (the PC tool does this with ffmpeg).
  const ctx = new OfflineAudioContext(1, 1, SR);
  let decoded;
  try {
    decoded = await ctx.decodeAudioData(buf);
  } catch {
    throw new Error("Your browser couldn't read the sound in this file. Does it have a sound track? Try an MP4 or a WAV.");
  }
  const n = decoded.length;
  const mono = new Float32Array(n);
  for (let c = 0; c < decoded.numberOfChannels; c++) {
    const ch = decoded.getChannelData(c);
    for (let i = 0; i < n; i++) mono[i] += ch[i] / decoded.numberOfChannels;
  }
  return mono;
}

// ---------- Python (Pyodide + autosubs.py) ----------
let pyReady = null;
function loadPython() {
  if (pyReady) return pyReady;
  pyReady = (async () => {
    if (!window.loadPyodide) {
      await new Promise((ok, bad) => {
        const s = document.createElement('script');
        s.src = 'vendor/pyodide/pyodide.js';
        s.onload = ok;
        s.onerror = () => bad(new Error('Could not load Python (Pyodide).'));
        document.head.appendChild(s);
      });
    }
    const py = await window.loadPyodide({ indexURL: new URL('vendor/pyodide/', location.href).href });
    const [autosubs, glue] = await Promise.all(
      ['autosubs/autosubs.py', 'py/web_glue.py'].map((p) => fetch(p).then((r) => {
        if (!r.ok) throw new Error(`Could not load ${p}`);
        return r.text();
      })),
    );
    py.FS.writeFile('/home/pyodide/autosubs.py', autosubs);
    py.FS.writeFile('/home/pyodide/web_glue.py', glue);
    py.runPython('import sys; sys.path.insert(0, "/home/pyodide"); import web_glue');
    return py;
  })();
  pyReady.catch(() => { pyReady = null; });
  return pyReady;
}

async function makeSrt(result, speech) {
  const py = await loadPython();
  const make = py.globals.get('web_glue').make_srt;
  try {
    return make(JSON.stringify(result), JSON.stringify(speech), $('terms').value, $('style').value);
  } finally {
    make.destroy();
  }
}

// ---------- speech worker ----------
let worker = null;
function runWorker(audio, model, lang) {
  if (!worker) worker = new Worker('asr-worker.js', { type: 'module' });
  return new Promise((resolve, reject) => {
    worker.onmessage = ({ data }) => {
      if (data.type === 'stage') setStage(data.stage);
      else if (data.type === 'progress') setBar(data.stage, data.total ? data.done / data.total : 0);
      else if (data.type === 'done') resolve(data);
      else if (data.type === 'error') reject(new Error(data.message));
    };
    worker.onerror = (e) => reject(new Error(e.message || 'The speech worker stopped.'));
    worker.postMessage({ type: 'run', audio, model, lang }, [audio.buffer]);
  });
}

// ---------- run ----------
$('go').addEventListener('click', async () => {
  if (!file) return;
  hideError();
  show('step-run');
  setStage('audio');
  const started = performance.now();
  try {
    loadPython(); // start fetching Python while the models work
    const audio = await readAudio(file);
    const seconds = audio.length / SR;
    const { result, speech } = await runWorker(audio, $('model').value, $('lang').value);
    setStage('python');
    const srt = await makeSrt(result, speech);
    if (!srt.trim()) throw new Error('No speech was found in this file, so there are no subtitles to write.');
    setBar('python', 1);
    finish(srt, seconds, (performance.now() - started) / 1000);
  } catch (err) {
    console.error(err);
    show('step-pick');
    showError(err.message || String(err));
    if (worker) { worker.terminate(); worker = null; }
  }
});

function finish(srt, seconds, took) {
  const count = (srt.match(/-->/g) || []).length;
  $('srt').value = srt.replace(/\r\n/g, '\n');
  $('done-note').innerHTML = `<strong>Done.</strong> ${count} subtitles for ${fmtLen(seconds)} of video, made in ${fmtLen(took)}.`;
  if (videoUrl) URL.revokeObjectURL(videoUrl);
  videoUrl = URL.createObjectURL(file);
  $('preview').src = videoUrl;
  updateTrack();
  show('step-done');
}

function fmtLen(s) {
  s = Math.round(s);
  return s < 60 ? `${s} s` : `${Math.floor(s / 60)} min ${s % 60} s`;
}

// Show the subtitles on the preview video (as WebVTT, which browsers understand).
function updateTrack() {
  const video = $('preview');
  video.querySelectorAll('track').forEach((t) => t.remove());
  if (trackUrl) URL.revokeObjectURL(trackUrl);
  const vtt = 'WEBVTT\n\n' + $('srt').value.replace(/(\d\d:\d\d:\d\d),(\d\d\d)/g, '$1.$2');
  trackUrl = URL.createObjectURL(new Blob([vtt], { type: 'text/vtt' }));
  const track = document.createElement('track');
  Object.assign(track, { kind: 'subtitles', label: 'Subtitles', srclang: $('lang').value === 'pl' ? 'pl' : 'en', src: trackUrl, default: true });
  video.appendChild(track);
  track.track.mode = 'showing';
}
$('srt').addEventListener('change', updateTrack);

$('download').addEventListener('click', () => {
  // Same file format as the PC tool: UTF-8 with Windows line endings.
  const text = $('srt').value.replace(/\r?\n/g, '\r\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type: 'application/x-subrip' }));
  a.download = srtName;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

$('again').addEventListener('click', () => {
  $('preview').pause();
  show('step-pick');
});

