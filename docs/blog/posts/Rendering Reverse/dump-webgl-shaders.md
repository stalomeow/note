---
date: 2023-06-18
draft: false
authors:
  - stalomeow
categories:
  - Rendering Reverse
---

# 提取 WebGL Shaders

一键提取 WebGL Shaders 的代码。

<!-- more -->

控制台里执行下面的代码。[^1]

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

当有 Shader 被编译时，就会在控制台输出 Shader 的源代码。

[^1]: [https://github.com/greggman/dump-all-the-shaders/tree/master](https://github.com/greggman/dump-all-the-shaders/tree/master)