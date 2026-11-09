---
title: Import free SRT subtitles into Premiere Pro
description: Make subtitles for free with Whisper and import the SRT into Premiere Pro as a caption track. Then style it and export burned-in or as a sidecar file.
order: 11
editor: Premiere Pro
---
Premiere Pro has its own Speech to Text, but it depends on your plan, your version and your language packs. If you'd rather use Whisper, or you want the same subtitles in several programs, make an .srt file for free and import it.

## 1. Make the SRT

Open [AutoSubtitler](/), drop in your video, and press **Make subtitles**. Check the preview, fix any words, then **Download .srt**. The video stays on your computer.

For an edited sequence, export a quick draft of the whole sequence and subtitle that, so the times match the sequence from the very first frame.

## 2. Import it

Use **File › Import** (or drag the .srt into the Project panel), just like a video clip. Premiere recognises it as a captions file.

## 3. Add it to the sequence

Drag the captions file from the Project panel onto the timeline. Premiere puts it on a caption track above your video. Line its start up with the start of the clip it belongs to.

## 4. Edit and style

- Open **Window › Text**. The **Captions** tab lists every subtitle, so you can fix words there.
- Select a caption and use the **Essential Graphics** panel (or Properties, in newer versions) to change the font, size, background and position. To apply it to all captions, save the look as a **track style**.

## 5. Export

In the export settings, open the **Captions** section:

- **Burn Captions Into Video** draws them into the picture.
- **Create Sidecar File** exports an .srt next to the video, for YouTube or Vimeo.

## Tips

- Premiere sometimes asks for the caption format when importing. Subtitles (SRT) is the right choice.
- Short one-line chunks, the default in AutoSubtitler, suit vertical video. For interviews, switch to **Classic two-line sentences** under **More options** before you make the file.

See also: [what's inside an SRT file](/blog/what-is-an-srt-file/).
