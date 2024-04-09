---
date: 2024-03-26T00:01:38
draft: false
authors:
  - stalomeow
categories:
  - Math
  - Web Front-end
---

# 个人常用的 MathJax Macro

简化 TeX 的编写，长期更新。

<!-- more -->

参考文档：[Defining TeX macros — MathJax 3.2 documentation](https://docs.mathjax.org/en/latest/input/tex/macros.html#defining-tex-macros)。

## 代码

``` js
macros: {
    abs: [String.raw`\left | #1 \right |`, 1],
    coloneq: String.raw`\mathrel{\vcenter{:}}=`,
    ddx: [String.raw`\frac{\mathrm{d}#2}{\mathrm{d}#1}`, 2, 'x'],
    dddx: [String.raw`\dfrac{\mathrm{d}#2}{\mathrm{d}#1}`, 2, 'x']
}
```
