---
date: 2024-04-25T23:18:55
publish: true
comments: true
permalink: ffmpeg
aliases:
---

# FFmpeg

FFmpeg 是一个开放源代码的自由软件，可以执行音频和视频多种格式的录影、转换、串流功能，包含了 libavcodec —— 这是一个用于多个项目中音频和视频的解码器函式库，以及 libavformat —— 一个音频与视频格式转换函式库。

## 截图

在视频第 4.5 秒处截一张图。

``` bash
ffmpeg -i input.mp4 -ss 4.500 -frames:v 1 -update 1 output.png
```

将 `-ss` 放在 `-i` 前面，速度会快一点，但可能不准。[^1] `-update 1` 表示 `output.png` 文件名中不包含 `%03d` 这类格式化符号。[^2]

> `-ss` position (*input/output*)
>
> When used as an input option (before `-i`), seeks in this input file to position. Note that in most formats it is not possible to seek exactly, so `ffmpeg` will seek to the closest seek point before position. When transcoding and `-accurate_seek` is enabled (the default), this extra segment between the seek point and position will be decoded and discarded. When doing stream copy or when `-noaccurate_seek` is used, it will be preserved.
>
> When used as an output option (before an output url), decodes but discards input until the timestamps reach position.
>
> position must be a time duration specification, see [(ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual](https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax).

## 视频转 GIF

``` bash
ffmpeg -ss 30 -t 3 -i input.mp4 \
    -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 output.gif
```

[^1]: [ffmpeg Documentation Main-options](https://ffmpeg.org/ffmpeg.html#Main-options)
[^2]: [ffmpeg Documentation Options-77](https://www.ffmpeg.org/ffmpeg-all.html#Options-77)
