---
date: 2024-08-20T23:53:05
slug: renderdoc-integration
categories:
  - 图形渲染
  - 逆向
  - RenderDoc
draft: false
comments: true
---

# 集成 RenderDoc

<!-- more -->

实现像 Unity 一样，直接从自己程序里调起 RenderDoc 截帧的功能。参考文档：[In-application API — RenderDoc documentation](https://renderdoc.org/docs/in_application_api.html)。

## 引入头文件

在 RenderDoc 的安装目录里，有 `renderdoc_app.h`，复制进项目即可。然后，写一个类简单封装一下。

``` cpp
class RenderDoc final
{
public:
    static bool IsLoaded();
    static void Load();
    static void CaptureSingleFrame();
    static uint32_t GetNumCaptures();
    static std::tuple<int32_t, int32_t, int32_t> GetVersion();
    static std::string GetLibraryPath();
};
```

cpp 文件里

``` cpp
static RENDERDOC_API_1_5_0* g_Api = nullptr;
```

## 加载

==在创建图形设备前==，枚举常用的 RenderDoc 安装位置，动态加载安装目录里的 `renderdoc.dll`。

``` cpp
std::string RenderDoc::GetLibraryPath() const
{
    // 常用安装位置，可以多枚举几个
    return "C:\\Program Files\\RenderDoc\\renderdoc.dll";
}
```

如果 `LoadLibrary` 前，`renderdoc.dll` 已经被加载，说明用户是用 RenderDoc 启动 App 的，就不需要再手动 load 了。

``` cpp
bool RenderDoc::IsLoaded()
{
    return g_Api != nullptr;
}

void RenderDoc::Load()
{
    if (IsLoaded())
    {
        return;
    }

    // 如果使用 RenderDoc 启动 App 的话，不重复加载 dll
    HMODULE hModule = GetModuleHandleA("renderdoc.dll");

    if (!hModule)
    {
        hModule = LoadLibraryA(GetLibraryPath().c_str());
    }

    if (!hModule)
    {
        DEBUG_LOG_ERROR("Failed to load RenderDoc library");
        return;
    }

    auto RENDERDOC_GetAPI = reinterpret_cast<pRENDERDOC_GetAPI>(GetProcAddress(hModule, "RENDERDOC_GetAPI"));
    int ret = RENDERDOC_GetAPI(eRENDERDOC_API_Version_1_5_0, reinterpret_cast<void**>(&g_Api));

    if (ret != 1)
    {
        g_Api = nullptr;
        DEBUG_LOG_ERROR("Failed to get RenderDoc API. Return Code: %d", ret);
        return;
    }

    g_Api->MaskOverlayBits(eRENDERDOC_Overlay_None, eRENDERDOC_Overlay_None); // 不显示 overlay
    g_Api->SetCaptureKeys(nullptr, 0);
}
```

在最后，调用 `MaskOverlayBits` 把 RenderDoc 左上角黑色的 Overlay 信息隐藏掉；调用 `SetCaptureKeys` 把默认的快捷键取消掉。

## D3D12 调试层

在做 D3D12 开发时，我们通常会开启 D3D12 的调试层，但 RenderDoc 默认情况下禁用了 API Validation 和 Debug Output，使得 D3D12 的调试层失去作用。

在加载 RenderDoc 后，调用下面的方法可以解决。[^1]

``` cpp
g_Api->SetCaptureOptionU32(eRENDERDOC_Option_APIValidation, 1);
g_Api->SetCaptureOptionU32(eRENDERDOC_Option_DebugOutputMute, 0);
```

另外，RenderDoc 会使 `ID3D12InfoQueue1` 失去作用，因为它只提供了一个 dummy 的实现。[^2]

``` cpp
// give every impression of working but do nothing.
// Just allow the user to call functions so that they don't
// have to check for E_NOINTERFACE when they expect an infoqueue to be there
struct DummyID3D12InfoQueue : public ID3D12InfoQueue1
{
    // ...
}
```

RenderDoc 会使 D3D12 的调试层变得不完整，它本身又有一些额外的开销，所以不建议每次启动应用时都加载 RenderDoc。

可以像 Unity 一样，提供一个加载按钮，但是加载 RenderDoc 后需要重新创建图形设备，整个过程是比较麻烦的。也可以提供一个命令行参数 `-load-renderdoc`，仅在有该参数的情况下加载 RenderDoc，修改 VisualStudio 调试器的启动参数就行。

## 截帧

``` cpp
void RenderDoc::CaptureSingleFrame()
{
    if (!IsLoaded())
    {
        return;
    }

    g_Api->TriggerCapture();

    if (g_Api->IsTargetControlConnected())
    {
        g_Api->ShowReplayUI();
    }
    else
    {
        g_Api->LaunchReplayUI(1, nullptr);
    }
}
```

调用这个方法后，会立即截一帧，然后打开 RenderDoc 窗口，就像 Unity 一样。

## 附加信息

获取截帧和版号信息。

``` cpp
uint32_t RenderDoc::GetNumCaptures()
{
    if (!IsLoaded())
    {
        return 0;
    }

    return g_Api->GetNumCaptures();
}

std::tuple<int32_t, int32_t, int32_t> RenderDoc::GetVersion()
{
    if (!IsLoaded())
    {
        return std::make_tuple(0, 0, 0);
    }

    int verMajor = 0;
    int verMinor = 0;
    int verPatch = 0;
    g_Api->GetAPIVersion(&verMajor, &verMinor, &verPatch);
    return std::make_tuple(static_cast<int32_t>(verMajor), static_cast<int32_t>(verMinor), static_cast<int32_t>(verPatch));
}
```

## 快捷键和 UI

这部分用 ImGui 实现，使用快捷键 `Alt+C` 就能截帧。

![[Pasted image 20240824233322.png|UI 效果]]

``` cpp
if (ImGui::BeginMainMenuBar())
{
    if (ImGui::Shortcut(ImGuiMod_Alt | ImGuiKey_C, ImGuiInputFlags_RouteAlways))
    {
        RenderDoc::CaptureSingleFrame();
    }

    if (ImGui::BeginMenu("RenderDoc"))
    {
        if (ImGui::MenuItem("Capture", "Alt+C", nullptr, RenderDoc::IsLoaded()))
        {
            RenderDoc::CaptureSingleFrame();
        }

        ImGui::SeparatorText("Information");

        if (ImGui::BeginMenu("Library"))
        {
            ImGui::TextUnformatted(RenderDoc::GetLibraryPath().c_str());
            ImGui::EndMenu();
        }

        if (ImGui::BeginMenu("API Version"))
        {
            auto [major, minor, patch] = RenderDoc::GetVersion();
            ImGui::Text("%d.%d.%d", major, minor, patch);
            ImGui::EndMenu();
        }

        if (ImGui::BeginMenu("Num Captures"))
        {
            ImGui::Text("%d", RenderDoc::GetNumCaptures());
            ImGui::EndMenu();
        }

        ImGui::EndMenu();
    }

    ImGui::EndMainMenuBar();
}
```

[^1]: [d3d debug runtime doesn't work with RenderDoc? · Issue #418 · baldurk/renderdoc (github.com)](https://github.com/baldurk/renderdoc/issues/418)
[^2]: [renderdoc/renderdoc/driver/d3d12/d3d12_device.h at v1.x · baldurk/renderdoc (github.com)](https://github.com/baldurk/renderdoc/blob/v1.x/renderdoc/driver/d3d12/d3d12_device.h)
