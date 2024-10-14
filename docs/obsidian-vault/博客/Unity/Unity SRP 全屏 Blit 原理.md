---
date: 2024-10-13T10:36:33
slug: unity-srp-fullscreen-blit
categories:
  - Universal RP
  - Unity
  - 图形渲染
draft: false
comments: true
---

# Unity SRP 全屏 Blit 原理

<!-- more -->

一般我们做 Blit 用的都是两个三角形，或者一个 Quad。SRP 只用了一个三角形。

![[Pasted image 20241014124509.png|示例图]]

三角形顶点的齐次坐标是在 Vertex Shader 里根据 Vertex ID 计算的。三角形 Mesh 中 `v0`、`v1`、`v2` 三个顶点的坐标可以随便给。

源码：[Graphics/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl at master · Unity-Technologies/Graphics (github.com)](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl)。

``` hlsl
// Generates a triangle in homogeneous clip space, s.t.
// v0 = (-1, -1, 1), v1 = (3, -1, 1), v2 = (-1, 3, 1).
float2 GetFullScreenTriangleTexCoord(uint vertexID)
{
#if UNITY_UV_STARTS_AT_TOP
    return float2((vertexID << 1) & 2, 1.0 - (vertexID & 2));
#else
    return float2((vertexID << 1) & 2, vertexID & 2);
#endif
}

float4 GetFullScreenTriangleVertexPosition(uint vertexID, float z = UNITY_NEAR_CLIP_VALUE)
{
    // note: the triangle vertex position coordinates are x2 so the returned UV coordinates are in range -1, 1 on the screen.
    float2 uv = float2((vertexID << 1) & 2, vertexID & 2);
    float4 pos = float4(uv * 2.0 - 1.0, z, 1.0);
#ifdef UNITY_PRETRANSFORM_TO_DISPLAY_ORIENTATION
    pos = ApplyPretransformRotation(pos);
#endif
    return pos;
}
```
