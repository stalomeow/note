# FFmpeg

!!! abstract

    记一下平时会用到的命令。

    > FFmpeg 是一个开放源代码的自由软件，可以执行音频和视频多种格式的录影、转换、串流功能，包含了 libavcodec —— 这是一个用于多个项目中音频和视频的解码器函式库，以及 libavformat —— 一个音频与视频格式转换函式库。

## 视频转 GIF

```
ffmpeg -ss 30 -t 3 -i input.mp4 \
    -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 output.gif
```
