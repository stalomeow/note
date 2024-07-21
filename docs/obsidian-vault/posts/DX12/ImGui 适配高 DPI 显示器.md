---
date: 2024-07-21T23:42:26
slug: imgui-handle-high-dpi
categories:
  - ImGui
  - 图形渲染
draft: false
comments: true
---

# ImGui 适配高 DPI 显示器

<!-- more -->

## DPI

DPI 全称 Dots per inch，即每英寸的点数，对于显示器来说就是每英寸的像素数量。

## Display Scale Factor

早期的显示器基本都是 96 DPI 的，所以那时候的应用程序 UI 都是以 96 DPI 为标准的。现在显示器的 DPI 普遍比 96 高，这意味着同样大小的显示器，像素数量变多了。早期的应用程序放到现在的显示器上，尽管占用的像素数量和以前一样，但是显示器的像素密度大了，所以看上去应用程序的界面变小了。

为了解决上面的问题，Windows 引入了一个 Display Scale Factor，一般是显示器 DPI 除以基准值 96 的结果。

![[Pasted image 20240722000504.png|显示缩放]]

Windows 会骗应用程序说 DPI 还是 96，让它以 `WindowSize / DisplayScaleFactor` 的大小绘制界面，然后 Windows 再把界面放大 `DisplayScaleFactor` 倍。但是这样会导致界面变的不清晰。

## DPI 感知

就是自己处理 DPI，不让 Windows 缩放。在应用启动时，调用 API 设置 Per-Monitor (V2) DPI Awareness。[SetProcessDpiAwarenessContext function (winuser.h) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiawarenesscontext)。

``` cpp
SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
```

> ImGui 提供了 `ImGui_ImplWin32_EnableDpiAwareness()`，但是我这里调用它以后显示有问题。

利用 ImGui 的 API 可以方便地拿到缩放值（Display Scale Factor）。

``` cpp
float dpiScale = ImGui_ImplWin32_GetDpiScaleForHwnd(m_WindowHandle);
```

初始化导入字体时，将字体占用的像素大小改为：96 DPI 下的基准值乘上 `dpiScale`。

``` cpp
ImGuiIO& io = ImGui::GetIO();
// ...
io.Fonts->AddFontFromFileTTF("...", 15.0f * dpiScale);
```

在窗体消息函数里，收到 `WM_DPICHANGED`（DPI 变化）时，重新加载字体，应用新的缩放，再设置窗体大小。[WM_DPICHANGED message (WinUser.h) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/hidpi/wm-dpichanged)。

``` cpp
case WM_DPICHANGED:
{
    float dpiScale = ImGui_ImplWin32_GetDpiScaleForHwnd(m_WindowHandle);
    auto& io = ImGui::GetIO();
    io.Fonts->Clear();
    io.Fonts->AddFontFromFileTTF("...", 15.0f * dpiScale);
    io.Fonts->Build();
    ImGui_ImplDX12_InvalidateDeviceObjects();

    RECT* const prcNewWindow = (RECT*)lParam;
    SetWindowPos(hWnd,
        NULL,
        prcNewWindow->left,
        prcNewWindow->top,
        prcNewWindow->right - prcNewWindow->left,
        prcNewWindow->bottom - prcNewWindow->top,
        SWP_NOZORDER | SWP_NOACTIVATE);
    return 0;
}
```

在运行时，修改字体以后，先调用 `io.Fonts->Build()` 在 CPU 上重新构建字体图集，然后调用 `ImGui_ImplDX12_InvalidateDeviceObjects()` 强制重新创建 GPU 上的资源。一开始初始化时不需要调用这两个函数，因为那时候什么缓存都没有，必须重新创建。


## 参考

[High DPI Desktop Application Development on Windows - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)
