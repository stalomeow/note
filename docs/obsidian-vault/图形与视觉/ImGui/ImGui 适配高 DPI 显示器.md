---
date: 2024-07-21T23:42:26
publish: true
comments: true
permalink: imgui-handle-high-dpi
aliases:
---

# ImGui 适配高 DPI 显示器

为了解决高 [[DPI|DPI]] 显示器下 ImGui 字体模糊的问题，ImGui 提供了 `ImGui_ImplWin32_EnableDpiAwareness()`，但是我这里调用它以后显示有问题，所以我只能用 `SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)` 自己处理。

## 字体缩放

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

在运行时，修改字体以后，先调用 `io.Fonts->Build()` 在 CPU 上重新构建字体图集，然后调用 `ImGui_ImplDX12_InvalidateDeviceObjects()` 强制重新创建 GPU 上的资源。一开始初始化时不需要调用这两个函数，因为那时候什么缓存都没有，ImGui 会自动构建。

---

理论上，应该再加上

``` cpp
ImGui::GetStyle().ScaleAllSizes(dpiScale);
```

但实际上，Style 里不少参数都是整数，每次 Scale 之后都会进行取整，多次 Scale 就会积累很多误差，因此我个人不推荐。
