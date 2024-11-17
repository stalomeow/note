---
date: 2024-10-20T01:10:44
slug: linear-color-space-rendering
draft: false
comments: true
---

# 在 Linear Color Space 中渲染

<!-- more -->

ImGui 目前所有操作都是在 sRGB 空间进行的，不支持 Linear Color Space。[^1] 考虑到透明混合的问题，不能直接把 ImGui 传入 Shader 的颜色转到 Linear 空间，否则在不同 Color Space 下 ImGui 看上去不一致，尤其是它的 Color Picker。

注意到 ImGui 只有一张 Texture，在不使用 [Colorful Glyphs/Emojis](https://github.com/ocornut/imgui/blob/master/docs/FONTS.md#using-colorful-glyphsemojis) 时，这张 Texture 的 RGB 全是 1，这意味着我们既可以把它当作 Linear 颜色，也可以把它当作 sRGB 颜色。我引擎的 Texture 在被 Shader 采样后得到的都是 Linear 颜色，所以不妨把 ImGui 的 Texture 当成 Linear 的。

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
