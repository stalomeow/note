# IL Post-Process

!!! abstract

    有时候需要在程序集编译完成后修改里面 IL 代码。

    修改 IL 使用 Mono.Cecil。在 Package Manager 里安装 `com.unity.nuget.mono-cecil`。

    这里主要记录一下把修改 IL 的步骤插入到 Unity 编译管线中的方法。

## 法一：CompilationPipeline API


## 法二：ILPostProcessor

这个方法 Unity 在 ECS 和 Burst Compiler 中有使用。

!!! warning "风险警告"

    截至 2023 年 9 月，这依然是一个未公开的 feature，没有文档。Unity 可能会在未来修改它的 API 和功能。


