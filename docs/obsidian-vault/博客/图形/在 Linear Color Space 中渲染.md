---
date: 2024-10-20T01:10:44
slug: linear-color-space-rendering
draft: false
comments: true
---

# 在 Linear Color Space 中渲染

为了计算更准确，现在都在 Linear [[色彩空间]] 做渲染。自己写引擎时，要相应地做一些处理。

<!-- more -->

## RTV

建议所有中间的临时 RTV 都不带 `_SRGB` 后缀，最后的 Back Buffer RTV 使用 `DXGI_FORMAT_*_SRGB`。这样中间所有内容都在 Linear 空间，只在 Present 前进行一次 Gamma 校正。

## Texture

像 Unity 一样提供一个 `sRGB` 选项，然后使用 DirectXTex 提供的 `CREATETEX_FLAGS` 进行 sRGB 配置。

``` cpp
// https://github.com/microsoft/DirectXTex/wiki/CreateTexture
// The CREATETEX_SRGB flag provides an option for working around gamma issues with content
// that is in the sRGB or similar color space but is not encoded explicitly as an SRGB format.
// This will force the resource format be one of the of DXGI_FORMAT_*_SRGB formats if it exist.
// Note that no pixel data conversion takes place.
// The CREATETEX_IGNORE_SRGB flag does the opposite;
// it will force the resource format to not have the _*_SRGB version.
CREATETEX_FLAGS createFlags;

if constexpr (GfxSettings::GetColorSpace() == GfxColorSpace::Linear)
{
    createFlags = m_IsSRGB ? CREATETEX_FORCE_SRGB : CREATETEX_IGNORE_SRGB;
}
else
{
    // shader 中采样时不进行任何转换
    createFlags = CREATETEX_IGNORE_SRGB;
}

GFX_HR(CreateTextureEx(device, m_MetaData, D3D12_RESOURCE_FLAG_NONE, createFlags, &m_Resource));
```

## Color

我们平时说的颜色值、Editor 里配置的颜色都是 sRGB 空间的。从外部向 Shader 传入颜色时（例如 Material Constant Buffer），需要将颜色从 sRGB 空间转到 Linear 空间。

## ImGui

ImGui 目前所有操作都是在 sRGB 空间进行的，不支持 Linear Color Space。[^1] 考虑到透明混合的问题，不能直接把 ImGui 传入 Shader 的颜色转到 Linear 空间，否则在不同 Color Space 下 ImGui 看上去不一致，尤其是它的 Color Picker。

注意到 ImGui 只有一张 Texture，在不使用 [Colorful Glyphs/Emojis](https://github.com/ocornut/imgui/blob/master/docs/FONTS.md#using-colorful-glyphsemojis) 时，这张 Texture 的 RGB 全是 1，这意味着把它当成 Linear 颜色变换到 sRGB 或者反过来结果都一样。我引擎的 Texture 在被 Shader 采样后得到的都是 Linear 颜色，所以不妨把 ImGui 的 Texture 当成 Linear Texture。

修改 ImGui 的 Pixel Shader，把 Texture 的采样结果变换到 sRGB 空间，使得 ImGui 依旧在 sRGB 空间渲染。

``` hlsl
struct PS_INPUT
{
  float4 pos : SV_POSITION;
  float4 col : COLOR0;
  float2 uv  : TEXCOORD0;
};
SamplerState sampler0 : register(s0);
Texture2D texture0 : register(t0);

float LinearToSRGB1(float x)
{
    return (x < 0.0031308) ? (12.92 * x) : (1.055 * pow(x, 1.0 / 2.4) - 0.055);
}
float3 LinearToSRGB3(float3 x)
{
    return float3(LinearToSRGB1(x.r), LinearToSRGB1(x.g), LinearToSRGB1(x.b));
}
float4 main(PS_INPUT input) : SV_Target
{
  float4 tex_col = texture0.Sample(sampler0, input.uv);
  float4 out_col = input.col * float4(LinearToSRGB3(tex_col.rgb), tex_col.a);
  return out_col;
}
```

等 ImGui 渲染完成后，将 sRGB 颜色转到 Linear 空间，同时 Blit 到 Back Buffer（sRGB RTV）。

``` cpp
void GameEditor::DrawImGuiRenderGraph(GfxDevice* device, int32_t renderTargetId)
{
    auto builder = m_ImGuiRenderGraph->AddPass("DrawImGui");

    GfxRenderTextureDesc desc = device->GetBackBuffer()->GetDesc();
    desc.Format = m_ImGuiRtvFormat;

    builder.CreateTransientTexture(renderTargetId, desc);
    builder.SetRenderTargets(renderTargetId);
    builder.ClearRenderTargets(ClearFlags::Color);

    builder.SetRenderFunc([=](RenderGraphContext& context)
    {
        ImGui::Render();
        ImGui_ImplDX12_RenderDrawData(ImGui::GetDrawData(), context.GetD3D12GraphicsCommandList());
    });
}

void GameEditor::BlitImGuiToBackBuffer(GfxDevice* device, int32_t srcTextureId, int32_t backBufferId)
{
    auto builder = m_ImGuiRenderGraph->AddPass("BlitImGuiToBackBuffer");

    builder.ImportTexture(backBufferId, device->GetBackBuffer());
    builder.SetRenderTargets(backBufferId);

    TextureHandle srcTexture = builder.ReadTexture(srcTextureId, ReadFlags::PixelShader);

    builder.SetRenderFunc([=](RenderGraphContext& context)
    {
        m_BlitImGuiMaterial->SetTexture("_SrcTex", srcTexture.Get());
        context.DrawMesh(GetFullScreenTriangleMesh(), m_BlitImGuiMaterial.get());
    });
}
```

``` hlsl
float4 c = _SrcTex.Sample(sampler_SrcTex, input.uv);

#ifdef MARCH_COLORSPACE_GAMMA
    return c;
#else
    return SRGBToLinear(c);
#endif
```

[^1]: [sRGB and linear color spaces · Issue #578 · ocornut/imgui (github.com)](https://github.com/ocornut/imgui/issues/578)
