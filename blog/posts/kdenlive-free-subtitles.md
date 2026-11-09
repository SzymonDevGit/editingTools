---
title: Free subtitles in Kdenlive with a Whisper SRT
description: Kdenlive can import SRT subtitles onto its subtitle track. Make the SRT free in your browser with Whisper, import it, style it and render.
order: 15
editor: Kdenlive
---
Kdenlive has a dedicated subtitle track, and newer versions can even run Whisper themselves, if you install the Python packages it needs. If you'd rather not set that up, or want to subtitle on a different computer from the one you edit on, make the SRT in your browser and import it.

## 1. Make the SRT

Open [AutoSubtitler](/), drop in your video and press **Make subtitles**. Download the .srt. Nothing is uploaded, and there's nothing to install.

## 2. Import it into Kdenlive

Choose **Project › Subtitles › Import Subtitle File…**, pick the .srt, and check the encoding (UTF-8) and offset in the dialog. The subtitles land on the subtitle track at the top of the timeline.

## 3. Edit

Double-click a subtitle on the subtitle track to edit its text, or drag its edges to change the timing. The subtitle editor window lets you step through them one by one.

## 4. Style

The subtitle track's style settings control the font, size, colour, outline and position for the whole track.

## 5. Render

When you render, the subtitles on the subtitle track are drawn into the picture. To deliver them as a separate file too, use **Project › Subtitles › Export Subtitle File…** or keep the original .srt from step 1.

## Tips

- If the subtitles are offset, check where your clip starts. Subtitles are timed from the start of the video you made them from.
- For long recordings of talks, switch to **Classic two-line sentences** under **More options** in AutoSubtitler before making the file.

Also free and open source: [Shotcut](/blog/shotcut-free-subtitles/).
