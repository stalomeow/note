---
date: 2024-11-04T18:10:47
---

# Unity 常用 Render State 属性 UI

有时候想把 `ZTest`、`Cull` 等属性暴露到面板中配置，避免重复写相似的 Shader。这里直接把常用的都整理出来。

## Properties

``` shaderlab
[Header(Option)]
[Enum(UnityEngine.Rendering.CullMode)] _CullMode("Cull Mode", float) = 2
[Enum(UnityEngine.Rendering.ColorWriteMask)] _ColorMask("Color Mask", Float) = 15
[Enum(Off, 0, On, 1)] _ZWriteMode("ZWrite Mode", float) = 1
[Enum(UnityEngine.Rendering.CompareFunction)] _ZTestMode("ZTest Mode", Float) = 4

[Header(Blend)]
[Enum(UnityEngine.Rendering.BlendOp)] _BlendOp("Blend Op", Float) = 0
[Enum(UnityEngine.Rendering.BlendMode)] _SrcBlend("Src Blend", Float) = 1
[Enum(UnityEngine.Rendering.BlendMode)] _DstBlend("Dst Blend", Float) = 0

[Header(Stencil)]
[IntRange] _StencilRef("Stencil Ref", Range(0, 255)) = 0
[IntRange] _StencilReadMask("Stencil ReadMask", Range(0, 255)) = 255
[IntRange] _StencilWriteMask("Stencil WriteMask", Range(0, 255)) = 255
[Enum(UnityEngine.Rendering.CompareFunction)] _StencilComp("Stencil Comp", Float) = 8
[Enum(UnityEngine.Rendering.StencilOp)] _StencilPass("Stencil Pass", Float) = 0
[Enum(UnityEngine.Rendering.StencilOp)] _StencilFail("Stencil Fail", Float) = 0
[Enum(UnityEngine.Rendering.StencilOp)] _StencilZFail("Stencil ZFail", Float) = 0
```

建议自己写一个 `MaterialPropertyDrawer` 绘制 `_ColorMask`。因为 `ColorWriteMask` 是一个 Flags，但是 `[Enum(UnityEngine.Rendering.ColorWriteMask)]` 只能绘制成普通 Enum，无法组合多个值。

## Commands

相关文档：[ShaderLab: commands](https://docs.unity3d.com/Manual/shader-shaderlab-commands.html)。

``` shaderlab
Cull [_CullMode]
ColorMask [_ColorMask]
ZWrite [_ZWriteMode]
ZTest [_ZTestMode]

BlendOp [_BlendOp]
Blend [_SrcBlend] [_DstBlend]

Stencil
{
    Ref [_StencilRef]
    ReadMask [_StencilReadMask]
    WriteMask [_StencilWriteMask]
    Comp [_StencilComp]
    Pass [_StencilPass]
    Fail [_StencilFail]
    ZFail [_StencilZFail]
}
```

## Enum

相关的枚举都声明在 [Runtime/Export/Graphics/GraphicsEnums.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Runtime/Export/Graphics/GraphicsEnums.cs) 里。

下面的表基于 Unity 2023.3.0b5 的代码。

### BlendMode

|Name|Value|
|:-|:-|
|Zero|0|
|One|1|
|DstColor|2|
|SrcColor|3|
|OneMinusDstColor|4|
|SrcAlpha|5|
|OneMinusSrcColor|6|
|DstAlpha|7|
|OneMinusDstAlpha|8|
|SrcAlphaSaturate|9|
|OneMinusSrcAlpha|10|

### BlendOp

|Name|Value|
|:-|:-|
|Add|0|
|Subtract|1|
|ReverseSubtract|2|
|Min|3|
|Max|4|
|LogicalClear|5|
|LogicalSet|6|
|LogicalCopy|7|
|LogicalCopyInverted|8|
|LogicalNoop|9|
|LogicalInvert|10|
|LogicalAnd|11|
|LogicalNand|12|
|LogicalOr|13|
|LogicalNor|14|
|LogicalXor|15|
|LogicalEquivalence|16|
|LogicalAndReverse|17|
|LogicalAndInverted|18|
|LogicalOrReverse|19|
|LogicalOrInverted|20|
|Multiply|21|
|Screen|22|
|Overlay|23|
|Darken|24|
|Lighten|25|
|ColorDodge|26|
|ColorBurn|27|
|HardLight|28|
|SoftLight|29|
|Difference|30|
|Exclusion|31|
|HSLHue|32|
|HSLSaturation|33|
|HSLColor|34|
|HSLLuminosity|35|

### CompareFunction

|Name|Value|
|:-|:-|
|Disabled|0|
|Never|1|
|Less|2|
|Equal|3|
|LessEqual|4|
|Greater|5|
|NotEqual|6|
|GreaterEqual|7|
|Always|8|

### CullMode

|Name|Value|
|:-|:-|
|Off|0|
|Front|1|
|Back|2|

### ColorWriteMask

|Name|Value (Flags)|
|:-|:-|
|Alpha|1|
|Blue|2|
|Green|4|
|Red|8|
|All|15|

### StencilOp

|Name|Value|
|:-|:-|
|Keep|0|
|Zero|1|
|Replace|2|
|IncrementSaturate|3|
|DecrementSaturate|4|
|Invert|5|
|IncrementWrap|6|
|DecrementWrap|7|

## 参考

- [Shader面板上常用的一些内置枚举UI - 知乎](https://zhuanlan.zhihu.com/p/93194054)。
