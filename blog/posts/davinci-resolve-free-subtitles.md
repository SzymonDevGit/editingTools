---
title: Free subtitles for DaVinci Resolve: make an SRT and import it
description: The free version of DaVinci Resolve has no automatic subtitles, but it imports SRT files. Make one for free with Whisper and add it in four steps.
order: 10
editor: DaVinci Resolve
---
Automatic subtitles in DaVinci Resolve are a **Studio** feature, which is the paid version. The free version can still import, edit, style and export subtitles. All it needs is an .srt file, and you can make that for free.

## 1. Make the subtitle file

Open [AutoSubtitler](/), drop in your video (or the rendered timeline), and press **Make subtitles**. When it's done, press **Download .srt**. Nothing is uploaded: it all runs in your browser.

Tip: if your timeline is an edit of several clips, render a quick low-quality version of the whole timeline first and subtitle that. The times then match the timeline exactly.

## 2. Import the SRT

In Resolve, go to **File › Import › Subtitle…** and pick the .srt. It appears in the Media Pool.

## 3. Put it on the timeline

Drag the subtitle file from the Media Pool onto the timeline, above the video, starting at the same point as the clip. Resolve creates a **Subtitle** track for it.

If your clip doesn't start at the very beginning of the timeline, slide the subtitle clip so its start lines up with the video clip's start.

## 4. Style and edit

- Click a subtitle on the track to change its text or timing in the **Inspector**.
- To style the whole track (font, size, outline, background, position), select the **track header**, then open **Inspector › Track**.

## 5. Export

On the **Deliver** page, open **Subtitle Settings** and tick **Export Subtitle**. Then choose:

- **Burn into video** for captions drawn into the picture, which is best for social media.
- **As a separate file** for YouTube-style captions that viewers can switch on and off.

Not sure which? See [burned-in vs separate subtitles](/blog/burned-in-vs-separate-subtitles/).

## Why not type them by hand?

Resolve's subtitle track is great for fixing a few words, but typing out a 10-minute video with timings takes hours. Letting Whisper write the first draft and correcting it in Resolve takes minutes.

Doing lots of videos? The [Windows version of AutoSubtitler](https://github.com/SzymonDevGit/editingTools/tree/main/autosubs) uses the biggest Whisper model and subtitles a whole folder of clips when you drag them onto it.
