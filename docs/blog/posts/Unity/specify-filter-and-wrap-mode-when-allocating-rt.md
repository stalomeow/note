---
date: 2024-04-04T01:57:26
draft: false
authors:
  - stalomeow
categories:
  - Unity
---

# Allocate RT 时记得指定 `filterMode` 和 `wrapMode`

最近在 URP 里遇到的坑：C# 里申请了一张 RT

``` csharp
RenderingUtils.ReAllocateIfNeeded(ref m_RT, in desc);
```

在 Shader 里用 Inline Sampler State 采样它，实现了某个效果

``` hlsl
float3 color = SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_LinearClamp, uv).rgb;
```

打包测试发现 OpenGL ES 上效果不对。

<!-- more -->

## 原因

拿 RenderDoc 抓帧以后，发现在 DX11 上采样用的

|UVW|Minification & Magnification|
|:-:|:-:|
|ClampEdge|Linear|

这是正确的。但 OpenGL ES 上采样用的却是

|UVW|Minification & Magnification|
|:-:|:-:|
|Repeat|Point|

这组值刚好是 [`RenderingUtils.ReAllocateIfNeeded`](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/api/UnityEngine.Rendering.Universal.RenderingUtils.html#UnityEngine_Rendering_Universal_RenderingUtils_ReAllocateIfNeeded_UnityEngine_Rendering_RTHandle__UnityEngine_RenderTextureDescriptor__UnityEngine_FilterMode_UnityEngine_TextureWrapMode_System_Boolean_System_Int32_System_Single_System_String_) 方法中 `filterMode` 和 `wrapMode` 的默认值。

一查文档发现

!!! quote "Using sampler states"

    **Coupled textures and samplers**

    Most of the time when sampling textures in shaders, the texture sampling state should come from [texture settings](https://docs.unity3d.com/Manual/class-TextureImporter.html) – essentially, textures and samplers are coupled together. This is default behavior when using DX9-style shader syntax:

    ``` hlsl
    sampler2D _MainTex;
    // ...
    half4 color = tex2D(_MainTex, uv);
    ```

    Using sampler2D, sampler3D, samplerCUBE HLSL keywords declares both texture and sampler.

    Most of the time this is what you want, and is ==the only supported option on older graphics APIs (OpenGL ES)==. 

    ...

    **Separate textures and samplers**

    ...

    **Inline sampler states**

    ...

    ==Just like separate texture + sampler syntax, inline sampler states are not supported on some platforms. Currently they are implemented on Direct3D 11/12 and Metal.== [^1]

我试下来 Vulkan 似乎也没问题，至少最后的效果没问题。

## 结论

在 OpenGL ES 采样时用的是 RT 上的设置，`sampler_LinearClamp` 这种 Inline Sampler State 没用。

为了保证不同平台上效果一致，申请 RT 时加上 `filterMode` 和 `wrapMode`，和 Inline Sampler State 保持一致。或者干脆不用 Inline Sampler State，完全依靠 Texture Settings。

本文最前面的 C# 代码改成下面这样就能解决问题。

``` csharp
RenderingUtils.ReAllocateIfNeeded(ref m_RT, in desc, FilterMode.Bilinear, TextureWrapMode.Clamp);
```

[^1]: [Unity - Manual: Using sampler states](https://docs.unity3d.com/Manual/SL-SamplerStates.html)
