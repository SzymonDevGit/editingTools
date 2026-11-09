---
title: Free Polish subtitles for video, made with Whisper
description: Make Polish subtitles (napisy) for a video for free. Whisper handles Polish well; here's how to get the spelling and names right.
order: 4
---
Polish is harder for speech recognition than English. Words change their endings, there are many diacritics (ą, ć, ę, ł, ń, ó, ś, ź, ż), and fast speech runs words together. Whisper still handles Polish well, and you can make Polish subtitles for free in your browser.

## How to make Polish subtitles

1. Open [AutoSubtitler](/) and drop in your video.
2. Set the language to **Polish**. Don't leave it on detect if you know the language: forcing it avoids the odd English sentence in the middle.
3. Choose the **Accurate model** for Polish. It's a bigger download, but it makes noticeably fewer mistakes with Polish endings than the fast one.
4. Press **Make subtitles**, check the preview, and download the .srt.

## Get names and words right

Whisper often "anglicises" Polish names. For example, it can hear *Szymon* as *Simon*. Open **More options** and add a line for each fix:

```
Szymon
Simon => Szymon
```

The first line makes sure the name is always spelled and capitalised the same way. The second line replaces a word Whisper keeps mishearing. Changes only apply to whole words, and capitals don't matter.

## Make sure the letters show correctly

The .srt is saved as UTF-8, which keeps ą, ę and the rest. Most editors read UTF-8 without any fuss. If you ever see characters like Ä… instead of ą, the program has read the file in the wrong encoding. Look for an encoding or "character set" option when importing and pick UTF-8.

## Short or sentence-style subtitles?

Polish words are long, so short one-line chunks can feel choppy. Under **More options**, try **Classic two-line sentences** for interviews and talking-head videos, and keep **Short one-line chunks** for fast social media edits.

Next: [add the subtitles in your editor](/blog/free-subtitling-for-video/).
