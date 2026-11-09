---
title: Free subtitles in Final Cut Pro with an SRT file
description: Make an SRT for free in your browser, then import it into Final Cut Pro as captions. How to edit, style and export them.
order: 12
editor: Final Cut Pro
---
Final Cut Pro has imported SRT captions since version 10.4.1. Recent versions can also transcribe speech on Apple silicon Macs. If you're on an Intel Mac, need a language it doesn't support, or just want Whisper's accuracy, an .srt file is the free way in.

## 1. Make the SRT

Open [AutoSubtitler](/) in Safari, Chrome or Firefox, drop in your video and press **Make subtitles**. Download the .srt when it's done. Your video isn't uploaded anywhere.

## 2. Import the captions

In Final Cut Pro, choose **File › Import › Captions…**, select the .srt, and pick the clip or timeline position to attach them to. When it asks for a role, choose **SRT** and the language.

The captions appear as a caption lane above the primary storyline.

## 3. Edit and style

- Double-click a caption to change its text.
- Drag its ends in the caption lane to change its timing.
- Use the **Captions inspector** for formatting.

SRT captions can carry basic styling, such as bold and colour, and their position.

## 4. Export

- To share a video with captions burned in, choose **File › Share**, pick a destination, and select **Burn in captions** with the SRT role.
- To export the captions as a separate file, select them and choose **File › Export Captions**.

## Tips

- If Final Cut shows the captions out of sync, check that they're attached to the right clip, and that the timeline starts at 00:00:00:00.
- Speech recognition struggles with names. Add yours under **More options** in AutoSubtitler before you make the file, and they'll be spelled correctly throughout.

Read next: [burned-in vs separate subtitles](/blog/burned-in-vs-separate-subtitles/).
