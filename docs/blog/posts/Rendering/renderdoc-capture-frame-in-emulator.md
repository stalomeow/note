---
date: 2023-07-20
draft: false
authors:
  - stalomeow
categories:
  - Rendering
---

# 用 RenderDoc 和模拟器抓帧安卓手游

Windows 下，用 RenderDoc + 模拟器抓帧安卓手游。我使用的是 MuMu 模拟器安卓 12（版本：3.5.0）。

<!-- more -->

## Global Process Hook

1. 在 RenderDoc 顶部菜单栏点击 Tools/Settings，在 General 部分中找到 ^^Allow global process hooking - be careful!^^ 并勾选。
2. 在 RenderDoc 的 Launch Application 页面中，将模拟器可执行文件的路径填入 ^^Executable Path^^ 中，然后点击下面 Global Process Hook 部分的 ^^Enable Global Hook^^ 按钮（需要管理员权限）。
3. 如果之前打开了模拟器的话，退出模拟器。然后，用任务管理器检查，确保所有相关的进程都被关闭。

!!! danger "大坑 - Global Process Hook 开启后没有效果"

    RenderDoc 的 Global Process Hook 依赖 AppInit_DLLs 机制。[^1] [^2] 从 Windows 8 开始，当 SecureBoot 开启的时候，这个机制是被禁用的。[^3]

    <hr>
    <p style="font-size:large;font-weight:bold;">避坑方法</p>

    ++win+r++，输入 msinfo32，查看 ^^安全启动状态^^ 的值。如果是 ^^启用^^ 的话，需要重启电脑，在 BIOS 里关闭 SecureBoot。

## Connect To App

1. 打开模拟器，可以看到左上角显示 RenderDoc 的信息。
2. 在 RenderDoc 顶部菜单栏点击 File/Attach to Running Instance，选中 localhost 下面的模拟器核心程序，点击 Connect to app。
3. 可以正常抓帧了。

就不展示截图了，<del>怕游戏被封号 10 年</del>，怕被游戏公司的人找上门（x。

[^1]: [使用RenderDoc配合安卓模拟器抓帧手游 - 知乎](https://zhuanlan.zhihu.com/p/403453085)
[^2]: [用RenderDoc和安卓模拟器抓帧手游 | Kxn's eXercise Notes](https://blog.kangkang.org/post/504.html)
[^3]: [AppInit DLLs and Secure Boot - Win32 apps | Microsoft Learn](https://docs.microsoft.com/en-us/windows/win32/dlls/secure-boot-and-appinit-dlls)