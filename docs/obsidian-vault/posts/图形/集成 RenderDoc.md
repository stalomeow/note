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
    RenderDoc() = default;
    ~RenderDoc() = default;

    void Load();
    void CaptureSingleFrame() const;
    uint32_t GetNumCaptures() const;
    std::tuple<int, int, int> GetVersion() const;
    std::string GetLibraryPath() const;

    bool IsLoaded() const { return m_Api != nullptr; }

private:
    RENDERDOC_API_1_5_0* m_Api = nullptr;
};
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
    int ret = RENDERDOC_GetAPI(eRENDERDOC_API_Version_1_5_0, reinterpret_cast<void**>(&m_Api));

    if (ret != 1)
    {
        m_Api = nullptr;
        DEBUG_LOG_ERROR("Failed to get RenderDoc API. Return Code: %d", ret);
        return;
    }

    m_Api->MaskOverlayBits(eRENDERDOC_Overlay_None, eRENDERDOC_Overlay_None); // 不显示 overlay
    m_Api->SetCaptureKeys(nullptr, 0);
}
```

在最后，调用 `MaskOverlayBits` 把 RenderDoc 左上角黑色的 Overlay 信息隐藏掉；调用 `SetCaptureKeys` 把默认的快捷键取消掉。

## 截帧

``` cpp
void RenderDoc::CaptureSingleFrame() const
{
    if (!IsLoaded())
    {
        return;
    }

    m_Api->TriggerCapture();

    if (m_Api->IsTargetControlConnected())
    {
        m_Api->ShowReplayUI();
    }
    else
    {
        m_Api->LaunchReplayUI(1, nullptr);
    }
}
```

调用这个方法后，会立即截一帧，然后打开 RenderDoc 窗口，就像 Unity 一样。

## 附加信息

获取截帧和版号信息。

``` cpp
uint32_t RenderDoc::GetNumCaptures() const
{
    if (!IsLoaded())
    {
        return 0;
    }

    return m_Api->GetNumCaptures();
}

std::tuple<int, int, int> RenderDoc::GetVersion() const
{
    if (!IsLoaded())
    {
        return std::make_tuple(0, 0, 0);
    }

    int verMajor = 0;
    int verMinor = 0;
    int verPatch = 0;
    m_Api->GetAPIVersion(&verMajor, &verMinor, &verPatch);
    return std::make_tuple(verMajor, verMinor, verPatch);
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
        m_RenderDoc.CaptureSingleFrame();
    }

    if (ImGui::BeginMenu("RenderDoc"))
    {
        if (ImGui::MenuItem("Capture", "Alt+C", nullptr, m_RenderDoc.IsLoaded()))
        {
            m_RenderDoc.CaptureSingleFrame();
        }

        ImGui::SeparatorText("Information");

        if (ImGui::BeginMenu("Library"))
        {
            ImGui::TextUnformatted(m_RenderDoc.GetLibraryPath().c_str());
            ImGui::EndMenu();
        }

        if (ImGui::BeginMenu("API Version"))
        {
            auto [major, minor, patch] = m_RenderDoc.GetVersion();
            ImGui::Text("%d.%d.%d", major, minor, patch);
            ImGui::EndMenu();
        }

        if (ImGui::BeginMenu("Num Captures"))
        {
            ImGui::Text("%d", m_RenderDoc.GetNumCaptures());
            ImGui::EndMenu();
        }

        ImGui::EndMenu();
    }

    ImGui::EndMainMenuBar();
}
```
