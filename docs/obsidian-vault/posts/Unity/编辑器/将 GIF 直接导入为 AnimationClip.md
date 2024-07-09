---
date: 2023-11-19T11:57:34
slug: unity-import-gif-as-anim-clip
categories:
  - Unity
  - 编辑器工具
draft: false
comments: true
---

# 将 GIF 直接导入为 AnimationClip

<!-- more -->

写一个 `ScriptedImporter`，让 Unity 把 GIF 动图直接导入为 `AnimationClip`。这个 `AnimationClip` 通过控制 `SpriteRenderer.m_Sprite` 来实现帧动画。


## 导出 GIF 的关键帧图片

读取 GIF 用 `System.Drawing.Image` 实现。

- 获取 GIF 的帧数：`Image.GetFrameCount(FrameDimension.Time)`。

- 导出第 $i$ 帧的图片：

    1. `Image.SelectActiveFrame(FrameDimension.Time, i)` 激活第 $i$ 帧。
    2. `Image.Save(ms, ImageFormat.Png)` 保存到名为 `ms` 的 `Stream` 中。
    3. 创建 `Texture2D` 和 `Sprite`。

## 获取每个关键帧的持续时间

根据微软的文档，`Image.PropertyItems` 中 `Id==0x5100` 的属性保存的是 `FrameDelay`。[^1] 类型是 `uint[]` [^2]，长度为 GIF 的帧数。`FrameDelay[i]` 表示第 $i$ 帧图片停留的时间，单位是 $10^{-2}$ 秒。

然而，实际上 `PropertyItem.Value` 的类型是 `byte[]`，我们需要自己把 4 个 `byte` 转成 1 个 `uint`。这就涉及到字节序的问题，可是文档上没提到字节序相关的问题。我猜是和当前系统架构有关，所以就直接用 `BitConverter` 做转换了。

## C# 创建 AnimationClip

因为要操作的是 `SpriteRenderer.m_Sprite`，所以需要创建 `PPtrCurve` (object reference curve)。然后用 `AnimationUtility.SetObjectReferenceCurve` 把一组 `ObjectReferenceKeyframe` 关键帧和 `PPtrCurve` 关联，加进 `AnimationClip` 中。

## 完整代码

因为 Unity 默认支持 `.gif` 扩展名（但图片不能动），所以需要在 Inspector 上手动切换到自己的 Importer，有点麻烦。为了方便，可以把扩展名改成 `.ugif`。

### `GIFImporter.cs`

``` cs
using System;
using System.Collections.Generic;
using UnityEngine;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using UnityEditor;
using UnityEditor.AssetImporters;

[ScriptedImporter(version: 4, exts: new[] { "ugif" }, overrideExts: new[] { "gif" })]
public class GIFImporter : ScriptedImporter
{
    [SerializeField] private bool m_Loop = true;
    [SerializeField] private string m_SpriteRendererPath = "";

    public override void OnImportAsset(AssetImportContext ctx)
    {
        using Image gif = Image.FromFile(ctx.assetPath);

        string gifName = Path.GetFileNameWithoutExtension(ctx.assetPath);
        PropertyItem frameDelayProp = gif.GetPropertyItem(0x5100);
        int frameCount = gif.GetFrameCount(FrameDimension.Time);

        using MemoryStream ms = new();
        List<ObjectReferenceKeyframe> keyframes = new();
        float elapsedTime = 0;

        for (int i = 0; i < frameCount; i++)
        {
            ms.Seek(0, SeekOrigin.Begin);
            gif.SelectActiveFrame(FrameDimension.Time, i);
            gif.Save(ms, ImageFormat.Png);

            // Texture
            Texture2D texture = new Texture2D(gif.Width, gif.Height);
            texture.name = $"{gifName}_frame_{i}_texture";
            texture.LoadImage(ms.ToArray());
            ctx.AddObjectToAsset(texture.name, texture);

            // Sprite
            Rect spriteRect = new Rect(0, 0, texture.width, texture.height);
            Sprite sprite = Sprite.Create(texture, spriteRect, new Vector2(0.5f, 0.5f));
            sprite.name = $"{gifName}_frame_{i}_sprite";
            ctx.AddObjectToAsset(sprite.name, sprite);

            // Animation Clip
            keyframes.Add(new ObjectReferenceKeyframe
            {
                time = elapsedTime,
                value = sprite
            });
            elapsedTime += GetFrameDelay(frameDelayProp, i);
        }

        AnimationClip clip = new AnimationClip();
        var binding = EditorCurveBinding.PPtrCurve(m_SpriteRendererPath, typeof(SpriteRenderer), "m_Sprite");
        AnimationUtility.SetObjectReferenceCurve(clip, binding, keyframes.ToArray());
        AnimationUtility.SetAnimationClipSettings(clip, new AnimationClipSettings()
        {
            startTime = 0,
            stopTime = elapsedTime,
            loopTime = m_Loop
        });

        ctx.AddObjectToAsset($"{gifName}_animation_clip", clip);
        ctx.SetMainObject(clip);
    }

    private static float GetFrameDelay(PropertyItem frameDelayProp, int frameIndex)
    {
        Span<byte> bytes = frameDelayProp.Value.AsSpan(frameIndex * 4, 4);
        uint delay = BitConverter.ToUInt32(bytes); // 延迟时间，以 1/100 秒为单位
        return delay / 100.0f;
    }
}
```

### `GIFImporterEditor.cs`

``` cs
using UnityEditor;
using UnityEditor.AssetImporters;

[CustomEditor(typeof(GIFImporter))]
public class GIFImporterEditor : ScriptedImporterEditor
{
    private SerializedProperty m_Loop;
    private SerializedProperty m_SpriteRendererPath;

    public override void OnEnable()
    {
        base.OnEnable();

        m_Loop = serializedObject.FindProperty("m_Loop");
        m_SpriteRendererPath = serializedObject.FindProperty("m_SpriteRendererPath");
    }

    public override void OnDisable()
    {
        m_Loop = null;
        m_SpriteRendererPath = null;

        base.OnDisable();
    }

    public override void OnInspectorGUI()
    {
        serializedObject.Update();
        {
            EditorGUILayout.PropertyField(m_Loop);
            EditorGUILayout.PropertyField(m_SpriteRendererPath);

            EditorGUILayout.HelpBox("填入 SpriteRenderer 所在物体相对于 Animator 所在物体的路径，就是 Transform.Find 用的路径。如果在同一个物体上就空着。", MessageType.Info);
        }
        serializedObject.ApplyModifiedProperties();
        ApplyRevertGUI();
    }
}
```

[^1]: [Property item descriptions - Win32 apps](https://learn.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-constant-property-item-descriptions#propertytagframedelay)
[^2]: [Image property tag type constants (Gdiplusimaging.h) - Win32 apps](https://learn.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-constant-image-property-tag-type-constants)
