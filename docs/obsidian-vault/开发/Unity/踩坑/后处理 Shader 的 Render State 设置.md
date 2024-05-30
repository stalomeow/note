---
slug: "240427224423"
date: 2024-04-27
---

# 后处理 Shader 的 Render State 设置

后处理 Shader 或者一些 Blit 用的 Shader，一定要记得加下面几行！

``` shaderlab
Cull Off
ZTest Always
ZWrite Off
```

不加的话在**某些平台**绘制不了，会被剔除！比如 MuMu 模拟器上，我就遇到过这个问题。
