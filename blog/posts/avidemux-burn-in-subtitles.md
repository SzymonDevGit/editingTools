---
title: Burn subtitles into a video with Avidemux, free
description: Avidemux is a tiny free video tool that can burn SRT subtitles into a video with a filter. Make the SRT free with Whisper, then burn it in.
order: 23
editor: Avidemux
---
Avidemux is a small free video tool for quick cuts and conversions. It's not a full editor, but its **subtitle filter** burns an SRT file into the picture. That's handy when you just want a captioned copy of a video.

## 1. Make the SRT

Open [AutoSubtitler](/), drop in your video and press **Make subtitles**. Download the .srt. Nothing is uploaded.

## 2. Open the video in Avidemux

Open the video with **File › Open**. If you want to trim it, do it after making the subtitles from the trimmed file, or the times will be shifted.

## 3. Add the subtitle filter

1. Set **Video Output** (on the left) to an encoder such as **Mpeg4 AVC (x264)**. Filters don't work in **Copy** mode, because the picture has to be re-encoded to draw the subtitles.
2. Click **Filters** under Video Output.
3. In the **Subtitles** group, add the **SSA/ASS/SRT** subtitle filter and pick your .srt file.
4. Use the preview to check the subtitles show and are in sync.

## 4. Save

Pick an output format (MP4 Muxer is a safe choice), set **Audio Output** to Copy, and choose **File › Save**. The new file has the subtitles burned in.

## Tips

- Avidemux uses a plain subtitle style. For styled captions, use an editor like [Shotcut](/blog/shotcut-free-subtitles/) or [DaVinci Resolve](/blog/davinci-resolve-free-subtitles/).
- If accented letters look wrong, make sure the .srt is UTF-8. AutoSubtitler always saves it that way.

Similar tool: [HandBrake](/blog/handbrake-burn-in-subtitles/).
