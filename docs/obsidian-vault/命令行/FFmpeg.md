---
slug: "240425231855"
date: 2024-04-25
---

# FFmpeg


FFmpeg 是一个开放源代码的自由软件，可以执行音频和视频多种格式的录影、转换、串流功能，包含了 libavcodec —— 这是一个用于多个项目中音频和视频的解码器函式库，以及 libavformat —— 一个音频与视频格式转换函式库。

## 截图

在视频第 4.5 秒处截一张图。

``` bash
ffmpeg -i input.mp4 -ss 4.500 -vframes 1 output.png
```

## 视频转 GIF

``` bash
ffmpeg -ss 30 -t 3 -i input.mp4 \
    -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 output.gif
```
