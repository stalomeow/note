---
date: 2025-03-31T23:27:18
publish: true
comments: true
permalink: hlsl-bilinear-and-gather
aliases:
---

# HLSL Bilinear 和 Gather

## Bilinear

大致的代码如下，在算纹理坐标时有 0.5 的偏移

``` hlsl
float4 bilinear(Texture2D tex, float2 uv)
{
    float2 texSize;  
    tex.GetDimensions(texSize.x, texSize.y);

    float2 i;
    float2 t = modf(uv * texSize - 0.5, i);

    // 为了看起来更清晰，这里没考虑边界情况
    float4 p1 = lerp(tex[int2(i.x, i.y)], tex[int2(i.x + 1, i.y)], t.x);
    float4 p2 = lerp(tex[int2(i.x, i.y + 1)], tex[int2(i.x + 1, i.y + 1)], t.x);
    return lerp(p1, p2, t.y);
}
```

## Gather

可以一条指令获取用于 Bilinear 的四个纹素，但是每个纹素只能选择 RGBA 一个通道的值，结果会被打包进一个 `float4` 中。打包方式如下图所示，X 是左下角的纹素，然后按逆时针排列。

![[Pasted image 20250331235725.png|打包方式]]

`Gather` 方法只能用于最高级别的 Mip，参数是一个 Sampler 和一个 UV。Sampler 的话，只有 Addressing Mode 会被用到，就是 Repeat/Clamp/... 这个设置。UV 的话，注意 Bilinear 采样时 0.5 的偏移，可以参考前面的代码，确保给定的 UV 能获取到想要的四个纹素。

## 参考

- [Wojtek Sterna - Blog: DirectX 11, HLSL, GatherRed](https://wojtsterna.blogspot.com/2018/02/directx-11-hlsl-gatherred.html)
- [Texture2D::Texture2D Gather methods - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/texture2d-gather)
- [gather4 (sm5 - asm) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/gather4--sm5---asm-)
- [Provide extensive functions for Gather() · Issue #35 · microsoft/hlsl-specs](https://github.com/microsoft/hlsl-specs/issues/35)
- [shaders - Bilinear filtering: Selecting pixels to interpolate between - Game Development Stack Exchange](https://gamedev.stackexchange.com/questions/69601/bilinear-filtering-selecting-pixels-to-interpolate-between)
