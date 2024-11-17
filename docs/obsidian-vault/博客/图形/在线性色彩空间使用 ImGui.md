---
date: 2024-10-20T01:10:44
slug: imgui-in-linear-color-space
draft: false
comments: true
---

# 在线性色彩空间使用 ImGui

ImGui 目前所有操作都是用非线性颜色做的，不支持线性色彩空间。[^1] 考虑到透明混合的问题，不能直接对 ImGui 传入 Shader 的颜色去 Gamma 校正，否则 ImGui 显示的颜色和原来不一致，尤其是它的 Color Picker。

<!-- more -->

为了显示效果一致，只能让 ImGui 继续使用非线性颜色。

注意到 ImGui 只有一张 Texture，在不使用 [Colorful Glyphs/Emojis](https://github.com/ocornut/imgui/blob/master/docs/FONTS.md#using-colorful-glyphsemojis) 时，这张 Texture 的 RGB 全是 1，这意味着我们既可以把它当作线性颜色，也可以把它当作非线性颜色。我引擎的 Texture 在被 Shader 采样后得到的都是线性颜色，所以直接修改 ImGui 的 Pixel Shader，在 Texture 采样后加一个 Gamma 校正。这样，我引擎的 Texture 的颜色就成非线性颜色了，ImGui 的 Texture 颜色不变。

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

等 ImGui 渲染完成后，再做一次去 Gamma 校正，同时 Blit 到 Back Buffer（sRGB RTV）。

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
