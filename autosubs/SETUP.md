# Setting up the PC version (Windows)

The code in this folder is all you need from GitHub. The programs and AI models it uses are big
downloads, so they are not stored here. Put them in these folders next to `autosubs.py`:

```
autosubs/
  autosubs.py, Subtitle.bat, terms.txt, README.txt   <- from this repo
  bin/whisper-cpu/    whisper-cli.exe, whisper-vad-speech-segments.exe and their .dll files
  bin/ffmpeg/         ffmpeg.exe
  models/             ggml-large-v3-turbo-q5_0.bin, ggml-silero-v5.1.2.bin
```

1. **Python 3**: install it from [python.org](https://www.python.org/downloads/) and tick
   "Add python.exe to PATH". No extra packages are needed.
2. **whisper.cpp**: from the [whisper.cpp releases](https://github.com/ggml-org/whisper.cpp/releases),
   download the Windows x64 CPU build (`whisper-bin-x64.zip`) and unzip everything into `bin/whisper-cpu`.
   A GPU (Vulkan) build put in `bin/whisper-vulkan` is used first if it's there.
3. **ffmpeg**: download `ffmpeg-release-essentials.zip` from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
   and copy `bin/ffmpeg.exe` from it into `bin/ffmpeg`.
4. **Whisper model** (574 MB):
   [ggml-large-v3-turbo-q5_0.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin)
   into `models`.
5. **Speech detector** (1 MB):
   [ggml-silero-v5.1.2.bin](https://huggingface.co/ggml-org/whisper-vad/resolve/main/ggml-silero-v5.1.2.bin)
   into `models`.

Then drag a video onto `Subtitle.bat`. See `README.txt` for terms, settings and DaVinci Resolve.
