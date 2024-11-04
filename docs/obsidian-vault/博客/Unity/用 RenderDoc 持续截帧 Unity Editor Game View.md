---
date: 2024-04-02T21:42:47
slug: unity-editor-renderdoc-tool
draft: false
comments: true
---

# 用 RenderDoc 持续截帧 Unity Editor Game View

某些渲染 bug 只会持续很短的时间，手动抓帧根本抓不到。Unity 在 `UnityEditorInternal` 命名空间下，提供了 [`RenderDoc.BeginCaptureRenderDoc`](https://github.com/Unity-Technologies/UnityCsReference/blob/d2eb9c0352229c0268d47ca0efa69e14b5d180f8/Editor/Mono/RenderDoc/RenderDoc.bindings.cs#L32) 和 [`RenderDoc.EndCaptureRenderDoc`](https://github.com/Unity-Technologies/UnityCsReference/blob/d2eb9c0352229c0268d47ca0efa69e14b5d180f8/Editor/Mono/RenderDoc/RenderDoc.bindings.cs#L34C28-L34C47) 方法。可以用它们对 Game View 持续截帧。

<!-- more -->

## 代码

随便给的快捷键：

- Alt+Shift+B 开始截帧
- Alt+Shift+E 结束截帧

为了防止和其他快捷键冲突，所以给得比较反人类。不过用的频率比较低，所以可以接受。

同时开多个 Game View 可能有问题，一个都不开必有问题。

``` csharp
using System;
using UnityEditor;
using UnityEditor.ShortcutManagement;
using UnityEditorInternal;
using UnityEngine;

public static class RenderDocUtils
{
    [Shortcut("RenderDocUtils/BeginCaptureGameView", KeyCode.B, ShortcutModifiers.Alt | ShortcutModifiers.Shift)]
    public static void BeginCaptureGameView()
    {
        RenderDoc.BeginCaptureRenderDoc(GetActiveGameView());
        Debug.Log("RenderDoc capture started");
    }

    [Shortcut("RenderDocUtils/EndCaptureGameView", KeyCode.E, ShortcutModifiers.Alt | ShortcutModifiers.Shift)]
    public static void EndCaptureGameView()
    {
        RenderDoc.EndCaptureRenderDoc(GetActiveGameView());
        Debug.Log("RenderDoc capture ended");
    }

    private static EditorWindow GetActiveGameView()
    {
        Type type = typeof(SceneView).Assembly.GetType("UnityEditor.GameView");
        return EditorWindow.GetWindow(type);
    }
}
```
