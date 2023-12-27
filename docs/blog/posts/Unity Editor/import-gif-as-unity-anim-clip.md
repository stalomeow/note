---
date: 2023-11-19
draft: true
authors:
  - stalomeow
categories:
  - Unity Editor
---

# 将 GIF 直接导入为 Animation Clip

<!-- more -->

``` cs
using System;
using System.Collections.Generic;
using UnityEngine;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.AssetImporters;

[ScriptedImporter(version: 2, exts: new[] { "ugif" }, overrideExts: new[] { "gif" })]
public class GIFImporter : ScriptedImporter
{
    [SerializeField] private bool m_Loop = true;
    [SerializeField] private string m_SpriteRendererPath = "";

    public override void OnImportAsset(AssetImportContext ctx)
    {
        using Image gif = Image.FromFile(ctx.assetPath);

        string gifName = Path.GetFileNameWithoutExtension(ctx.assetPath);
        PropertyItem frameDelayProp = GetFrameDelayProperty(gif);
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

    private static PropertyItem GetFrameDelayProperty(Image gif)
    {
        // PropertyTagFrameDelay
        return gif.PropertyItems.First(prop => prop.Id == 0x5100);
    }

    private static float GetFrameDelay(PropertyItem frameDelayProp, int frameIndex)
    {
        Span<byte> bytes = frameDelayProp.Value.AsSpan(frameIndex * 4, 4);
        int delay = ParseInt32(bytes); // 延迟时间，以 1/100 秒为单位
        return delay / 100.0f;
    }

    private static int ParseInt32(Span<byte> span)
    {
        byte b0 = span[0];
        byte b1 = span[1];
        byte b2 = span[2];
        byte b3 = span[3];
        return ((b3 << 24) | (b2 << 16) | (b1 << 8) | b0);
    }
}
```

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
