---
date: 2024-04-27T16:30:53
publish: true
comments: true
permalink: shebang
aliases:
---

# Shebang

Shebang（也称为 Hashbang）就是文本文件开头的 `#!`。类 Unix 操作系统的程序加载器会分析 Shebang 后的内容，将这些内容作为解释器指令，并调用该指令，并将载有 Shebang 的文件路径作为该解释器的参数。

## 语法

由 `#!` 开头，接数个空白字符（也可以没有），最后接解释器的绝对路径，用于调用解释器。在直接调用脚本时，调用者会利用 Shebang 提供的信息调用相应的解释器，从而使得脚本文件的调用方式与普通的可执行文件类似。

## 例子

以 `#!/bin/sh` 开头的文件在执行时会实际调用 `/bin/sh` 程序来执行。这行内容也是 shell 脚本的标准起始行。

## 参考

[Shebang - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/Shebang)
