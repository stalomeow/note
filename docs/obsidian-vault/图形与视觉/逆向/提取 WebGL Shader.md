---
date: 2024-11-04T20:30:04
publish: true
comments: true
permalink: extract-webgl-shader
aliases:
---

# 提取 WebGL Shader

一键提取 WebGL Shader 的代码，来自 [https://github.com/greggman/dump-all-the-shaders/tree/master](https://github.com/greggman/dump-all-the-shaders/tree/master)。

``` js
(function(global) {
  'use strict';

  function wrap(className) {
    if (!className) {
      return;
    }
    className.prototype.compileShader = (function(origFn) {
      return function(shader) {
        origFn.call(this, shader);
        console.log("---[ shader from JavaScript ] ---\n", this.getShaderSource(shader));
        const ext = this.getExtension('WEBGL_debug_shaders');
        if (ext) {
          console.log("---[ shader passed to GPU driver ] ---\n", ext.getTranslatedShaderSource(shader));
        }
      };
    }(className.prototype.compileShader));
  }

  wrap(global.WebGLRenderingContext);
  wrap(global.WebGL2RenderingContext);
}(this));
```

在控制台里执行这个代码。当有 Shader 被编译时，就会在控制台输出 Shader 的源代码。
