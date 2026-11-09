---
title: Free subtitling for video: make accurate subtitles without paying
description: How to subtitle a video for free with Whisper. Make an .srt file in your browser, then add it to any editor or YouTube. No sign-up, no upload.
order: 1
---
Most "free" subtitle tools turn out to have a catch: a watermark, a five-minute limit, or an account that wants your card details. You don't need any of that. The speech recognition that paid tools use, OpenAI's Whisper, is free and open source, and it runs fine on an ordinary computer.

This guide shows the quickest free route from a video to finished subtitles.

## What you need

- Your video (MP4, MOV, WebM, or even just an MP3 or WAV of the sound).
- A recent version of Chrome, Edge or Firefox.
- The video editor or platform you want the subtitles in. Nearly all of them accept an **.srt file**, which is the standard subtitle format.

## Step 1: make the .srt file

1. Open [AutoSubtitler](/).
2. Drop your video onto the page. It is opened by your browser and is never uploaded anywhere.
3. Pick the language and press **Make subtitles**.
4. When it's done, play the preview to check it, fix any words in **Edit the subtitles**, and press **Download .srt**.

The first time, your browser downloads the Whisper model (about 80 MB) and keeps it, so later videos start straight away.

## Step 2: add the subtitles to your video

Every editor has its own menu for this. We have a short guide for each:

- [DaVinci Resolve](/blog/davinci-resolve-free-subtitles/)
- [Premiere Pro](/blog/premiere-pro-free-subtitles/)
- [Final Cut Pro](/blog/final-cut-pro-free-subtitles/)
- [CapCut](/blog/capcut-srt-subtitles/)
- [Shotcut](/blog/shotcut-free-subtitles/) and [Kdenlive](/blog/kdenlive-free-subtitles/)
- [Filmora](/blog/filmora-srt-subtitles/) and [Vegas Pro](/blog/vegas-pro-srt-subtitles/)
- [YouTube](/blog/youtube-upload-srt-subtitles/), and [HandBrake](/blog/handbrake-burn-in-subtitles/) or [Avidemux](/blog/avidemux-burn-in-subtitles/) to burn them into the picture
- Lesser-known editors: [Lightworks](/blog/lightworks-srt-subtitles/), [OpenShot](/blog/openshot-free-subtitles/), [VSDC Free Video Editor](/blog/vsdc-free-video-editor-subtitles/) and [Kapwing](/blog/kapwing-srt-subtitles/)

## Why the timing is good

A subtitle that appears half a second early looks wrong. AutoSubtitler uses two models: Whisper writes down the words, and a second model, Silero, marks exactly when someone is speaking. Each subtitle is then moved onto real speech, so nothing flashes up during silence or music. Long sentences are cut into short chunks at natural breaks, which is easier to read on a phone.

## Is it really free?

Yes. There's no account, no watermark and no length limit. It runs on your own computer, so there's no server bill to pass on to you. The code is [open source on GitHub](https://github.com/SzymonDevGit/editingTools).

## Tips for better subtitles

- **Clear sound wins.** Whisper copes with background music, but a voice close to the microphone is always more accurate.
- **Add names under More options.** Names and brand words are where speech recognition slips most. Type them in once and their spelling is fixed in every subtitle.
- **Pick the accurate model for hard audio.** It's a bigger download (about 250 MB) but makes fewer mistakes with accents and fast talk.
