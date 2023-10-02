# 编译 UE4 源码

!!! abstract

    记录一下编译 UE4 源码的流程和遇到的坑。

    - UE 源码版本：4.27.2。
    - IDE：Visual Studio 2022。
    - 操作系统：Windows 11。

## IDE 和必要负载

只装一个 VS2022 会有一些问题：

- UE4 源码中 GitDependencies、MemoryProfiler2 项目用了 .NET Framework 4.5。这个太老了，从 VS2022 开始就不支持了，会弹警告。
- 在编译 UE4 源码的时候，如果用了比 VS2019 高的版本，Output 窗口会打印警告。

最好是额外安装一个 VS2019，勾选上 .NET Framework 4.5 和其他必要的负载。然后可以用 VS2019 也可以用 VS2022。VS2022 这时候也支持 .NET Framework 4.5 了，而且编译 UE4 的时候会自动使用 VS2019 的工具链。

需要的负载：

- .NET Framework 4.5（VS2022 没有）和 4.6.2。UE4 里大部分 C# 项目用的是 4.6.2，少数几个用的 4.5。
- Windows 10 SDK (10.0.18362.0)。高版本可能会报错！[^1]
- 使用 C++ 的游戏开发。
- 使用 C++ 的桌面开发。
- 通用 Windows 平台开发。

## 下载源码

把 Epic Games 账号和 GitHub 账号关联，然后会收到加入他们 GitHub 组织的邀请。加入组织后就能访问到 UE 的源码。

推荐自己 Fork 一下，然后 Clone 到本地。这样方便修改源码。

``` bash title="Git 命令"
git clone -b 4.27 https://github.com/stalomeow/UnrealEngine.git "文件夹名称"
```

至少要预留 150G 的磁盘空间，后面还要编译。

## 编译构建

按官方的 README 做，大致流程：

1. 执行 Setup.bat。可以在命令行加个 `--threads=20` 参数，多线程下载。[^2]
2. 执行 GenerateProjectFiles.bat。
3. 双击 UE4.sln，进入 VS。
4. 构建 UE4 项目，配置是 Development Editor，目标平台 Win64。
5. 等着...
6. 在 UE4 项目上右键，点击 Set as Startup Project，设置成启动项。
7. 在 UE4 项目上右键，点击 Debug/Start New Instance，启动新实例。快捷键是 ++f5++。

## 游戏项目

源码版的 UE4 创建完游戏项目以后就会自动退出。需要进到游戏项目的根目录，双击 solution 文件，在 VS 里运行。

刚创建完的游戏项目，直接打开 uproject 也会报错。按刚才的方法，在 VS 里运行过一次后就没事了。

[^1]: [virtual reality - Compilation errors while building Oculus' Unreal Engine - Stack Overflow](https://stackoverflow.com/questions/72304385/compilation-errors-while-building-oculus-unreal-engine)
[^2]: [UE4源码版编译流程 - 知乎](https://zhuanlan.zhihu.com/p/366392529)