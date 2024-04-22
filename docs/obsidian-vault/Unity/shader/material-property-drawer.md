# Material Property Drawer

!!! abstract

    列举内置的 `MaterialPropertyDrawer` 和自定义实现的方法。

    参考：

    - [Unity - Scripting API: MaterialPropertyDrawer](https://docs.unity3d.com/2022.3/Documentation/ScriptReference/MaterialPropertyDrawer.html)
    - [Shader笔记——自定义Material面板 - 简书](https://www.jianshu.com/p/a1f5ecb7706d)

## 内置 Drawer & Decorator

都声明在 [Editor/Mono/Inspector/MaterialPropertyDrawer.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Editor/Mono/Inspector/MaterialPropertyDrawer.cs) 文件中。

### Toggle

### ToggleOff

### KeywordEnum

### Enum

### PowerSlider

### IntRange

### Space

### Header

## 自定义 Drawer & Decorator

> Note that for performance reasons, EditorGUILayout functions are not usable with MaterialPropertyDrawers.

## 内置 Property Flags

### HideInInspector

### PerRendererData

### NoScaleOffset

### Normal

### HDR

### Gamma

### NonModifiableTextureData
