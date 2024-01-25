---
date: 2023-10-07
draft: true
authors:
  - stalomeow
categories:
  - Unity
---

# IL Post-Process

有时候需要在程序集编译完成后修改里面的 IL 代码。这里主要记录一下把这个步骤插入到 Unity 编译管线中的方法。

修改 IL 使用 Mono.Cecil。Package Manager 里安装 `com.unity.nuget.mono-cecil`。

<!-- more -->

## 法一：CompilationPipeline API

这个方法偶尔会有 AccessViolation 错误，但总体用下来还是可以的。推荐同时提供自动和手动两种模式。

CompilationPipeline API 是有文档的，使用起来不难。它的编译完成事件是在 Domain Reload 前调用的。

## 法二：ILPostProcessor

这个方法 Unity 在 ECS 和 Burst Compiler 中有使用。

!!! warning "风险警告"

    截至 2023 年 9 月，这依然是一个未公开的 feature，没有文档。Unity 可能会在未来修改它的 API 和功能。[^1]

[^1]: [How does Unity do CodeGen and why can't I do it myself? - Unity Forum](https://forum.unity.com/threads/how-does-unity-do-codegen-and-why-cant-i-do-it-myself.853867/#post-5646937)