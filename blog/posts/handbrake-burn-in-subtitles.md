---
title: Burn subtitles into a video for free with HandBrake
description: Don't need a full editor? Make an SRT for free with Whisper, then burn it into the picture with HandBrake, a free open-source video converter.
order: 19
editor: HandBrake
---
Sometimes you don't need an editor at all, just a video with subtitles baked in, ready to post. HandBrake, the free open-source video converter, can burn an .srt file into the picture in a few clicks.

## 1. Make the SRT

Open [AutoSubtitler](/), drop in your video and press **Make subtitles**. Download the .srt. Your video stays on your computer.

## 2. Open the video in HandBrake

Open HandBrake (free for Windows, Mac and Linux from handbrake.fr) and open your video as the **Source**.

## 3. Add the subtitles

1. Go to the **Subtitles** tab.
2. Choose **Import Subtitle** (or **Add › Import SRT** on some versions) and pick the .srt.
3. Tick **Burn In** for that subtitle track.
4. Check the **character code** is UTF-8, so letters with accents show correctly.

## 4. Export

Choose a preset (the **Fast 1080p30** preset is fine for social media), pick where to save it, and press **Start Encode**. The new video has the subtitles drawn into the picture.

## Keep them separate instead

If you leave **Burn In** unticked and save as MKV, the subtitles are kept as a separate track that players like VLC can switch on and off. For MP4, players support this less consistently.

## Tips

- HandBrake uses a plain white subtitle style. For styled, animated captions, use an editor such as [CapCut](/blog/capcut-srt-subtitles/) or [DaVinci Resolve](/blog/davinci-resolve-free-subtitles/).
- Short one-line chunks, the AutoSubtitler default, are easier to read when burned in on a phone screen.

Read next: [burned-in vs separate subtitles](/blog/burned-in-vs-separate-subtitles/).
