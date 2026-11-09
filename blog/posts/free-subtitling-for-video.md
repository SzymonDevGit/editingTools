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

## Free subtitling tools compared

There are a few honest free options. Each suits a different job:

- **AutoSubtitler (this site)**: Whisper in your browser. It's free with no limits, works offline after the first model download, and gives you an .srt for any editor. It's slower than a server on old computers.
- **YouTube's automatic captions**: free, but only for videos you upload to YouTube. They often take hours to appear and get names wrong. You can download them, but only from your own videos.
- **Your editor's built-in captions**: convenient where they're included. In DaVinci Resolve they need the paid Studio version, in Premiere Pro they depend on your plan, and in CapCut and Filmora they often need credits or a subscription.
- **Typing them yourself**: free and exact, but it takes several times longer than the video.

For most people, the quickest free route is to let Whisper write the first draft and spend a few minutes fixing it.

## Frequently asked questions

**Is there a time limit?** No. The only limit is your computer's memory and patience: a long video takes a while, because the work happens on your own machine. For long recordings, the [Windows version](https://github.com/SzymonDevGit/editingTools/tree/main/autosubs) is faster.

**Does my video get uploaded?** No. Your browser reads the video and does all the work on your computer. The only download is the Whisper model itself, from Hugging Face, the first time you use it.

**Which languages work?** English and Polish are in the menu, and **Detect language** handles most of the languages Whisper knows, including Spanish, German, French, Italian and Portuguese. Accuracy is best for widely spoken languages. See the [Polish guide](/blog/polish-subtitles-free/) for tips on harder languages.

**How accurate is it?** On clear speech, Whisper gets the large majority of words right, and timing is matched to the speech. Names, slang and heavy background noise cause most of the mistakes. Add names under **More options**, and use the **Accurate model** for difficult audio.

**Can I translate the subtitles?** Not in AutoSubtitler yet. YouTube can auto-translate uploaded captions for viewers. See [uploading an SRT to YouTube](/blog/youtube-upload-srt-subtitles/).

**What format do I get?** A standard [.srt file](/blog/what-is-an-srt-file/), in UTF-8. Every major editor and video platform accepts it.

**Does it work on a phone?** It runs in mobile browsers, but phones have less memory and get warm, so a laptop or desktop is much quicker.
