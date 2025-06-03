---
date: 2024-11-04T20:26:00
publish: true
comments: true
permalink: embed-bilibili-video-in-webpage
aliases:
---

# 网页中嵌入 b 站视频

## 常用的播放器参数

参考：[https://www.sunzhongwei.com/video-websites-embed-bilibili-iframe-code-video-disable-play-automatically](https://www.sunzhongwei.com/video-websites-embed-bilibili-iframe-code-video-disable-play-automatically)。

|参数名|说明|取值|
|:-|:-|:-|
|`cid`|-|-|
|`aid`|AV 号|-|
|`bvid`|BV 号|-|
|`t`|从几秒开始播放|秒数|
|`page`|选集里的第几个视频，默认 `1`|序号，从 `1` 开始|
|`autoplay`|是否自动播放，默认开启|`0 / 1`|
|`danmuku`|是否开启弹幕，默认开启|`0 / 1`|

## 播放器适应页面宽度

参考：[https://sunete.github.io/tutorial/bilibili-video-adapts-to-the-width/](https://sunete.github.io/tutorial/bilibili-video-adapts-to-the-width/)。

### CSS

``` css
.responsive-video-container {
    position: relative;
    margin-bottom: 1em;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
    max-width: 100%;
}

.responsive-video-container iframe,
.responsive-video-container object,
.responsive-video-container embed {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
```

### HTML

``` html
<div class="responsive-video-container">
    <!-- bilibili 播放器 iframe -->
</div>
```
