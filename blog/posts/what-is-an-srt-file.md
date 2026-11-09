---
title: What is an SRT file? The subtitle format every editor understands
description: An SRT file is a plain text subtitle file with numbered lines and timings. Here's what's inside one, how to edit it, and how to make one for free.
order: 2
---
SRT (short for SubRip Text) is the most widely supported subtitle format there is. Video editors, YouTube, Vimeo, social media tools and media players like VLC all read it. If you only learn one subtitle format, learn this one.

## What's inside an SRT file

An SRT file is plain text. Open one in Notepad and you'll see blocks like this:

```
1
00:00:01,570 --> 00:00:02,720
and today I'm showing

2
00:00:02,770 --> 00:00:04,670
you my Teardown mod maker.
```

Each block has three parts:

1. **A number**, counting up from 1.
2. **The timing**: when the subtitle appears and when it disappears, as hours:minutes:seconds,milliseconds. Note the **comma** before the milliseconds, not a dot.
3. **The text**, on one or two lines.

A blank line separates one subtitle from the next.

## SRT vs other subtitle formats

- **WebVTT (.vtt)** is the web version. It looks almost the same but starts with the word `WEBVTT` and uses a dot before the milliseconds. Browsers use it for the `<track>` element.
- **ASS/SSA** supports fonts, colours and positions inside the file. It's popular for anime fansubs but less widely supported by editors.
- **Embedded captions** (CEA-608/708) live inside the video file itself, mostly for broadcast.

SRT has no styling of its own. That's a good thing when you edit: the editor applies one style to the whole subtitle track, so all your subtitles look consistent.

## How to edit an SRT file

Any text editor works. Keep the structure exactly as it is: number, timing line, text, blank line. If you change a time, keep the format `00:00:00,000`. Save the file as **UTF-8** so letters like ą, é or ß show correctly.

Most video editors also let you edit subtitle text right on the timeline after you import the file, which is easier for small fixes.

## How to make an SRT file for free

Typing out timings by hand is slow. [AutoSubtitler](/) listens to your video with Whisper and writes the whole .srt for you, timed to the words, in your browser and without uploading anything. Then [add it to your editor](/blog/free-subtitling-for-video/).
