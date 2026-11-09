---
title: Free subtitles in OpenShot using an SRT from Whisper
description: OpenShot adds subtitles with its Caption effect. Make the subtitles free in your browser with Whisper, then paste them into OpenShot.
order: 21
editor: OpenShot
---
OpenShot is a simple, free, open-source editor for Windows, Mac and Linux. It doesn't open .srt files directly. Instead, it has a **Caption** effect, which reads a list of timed lines very like an SRT. Whisper can write that list for you, for free.

## 1. Make the subtitles

Open [AutoSubtitler](/), drop in your video and press **Make subtitles**. When it's done, open **Edit the subtitles** and copy all the text, or download the .srt and open it in Notepad.

## 2. Add the Caption effect

1. In OpenShot, open the **Effects** tab and drag **Caption** onto your video clip on the timeline.
2. Select the clip, then open the effect's **Properties**.
3. Paste your subtitles into the **Caption Text** field.

OpenShot's caption format uses a dot before the milliseconds (`00:00:01.570`) where SRT uses a comma (`00:00:01,570`). If your captions don't show, replace the commas in the timing lines with dots. This is the same change that turns SRT into [WebVTT](/blog/what-is-an-srt-file/).

## 3. Style

In the Caption effect's properties you can set the font, size, colour, background, position and fade. These apply to every subtitle in the effect.

## 4. Export

**File › Export Video** renders the captions into the picture. For YouTube, also upload the .srt separately, so viewers can switch subtitles off: see [how to upload an SRT to YouTube](/blog/youtube-upload-srt-subtitles/).

## Tips

- The Caption effect sits on one clip. Times count from the start of that clip, so subtitle the clip itself, not a longer video it was cut from.
- For a long video made of many clips, it's often easier to export the edit first and then [burn the subtitles in with HandBrake](/blog/handbrake-burn-in-subtitles/).
