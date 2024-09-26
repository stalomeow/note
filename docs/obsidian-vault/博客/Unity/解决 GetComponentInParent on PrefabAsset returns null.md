---
date: 2023-05-26T09:07:48
slug: unity-get-component-in-parent-on-prefab-asset-returns-null
categories:
  - Unity
draft: false
comments: true
---

# 解决 GetComponentInParent on PrefabAsset returns null

<!-- more -->

如果一个 `GameObject` 是 **PrefabAsset**（仅指 Project Window 里的 Prefab 对象，Hierarchy 里的不算）

- 直接对它调用 `GetComponentInParent<T>()` 永远会返回 `null`，必须要用 `GetComponentInParent<T>(true)`。
- 其他有 `includeInactive` 参数的 `GetComponentXXX` 方法同上。
- 没有 `includeInactive` 参数的方法，比如 `GetComponent<T>()`，可以直接使用。

## 问题原因

这个时候 `GameObject` 是 Inactive 的（就算 Inspector 上的勾是勾上的，它也是 Inactive 的）。示例代码：

``` csharp
protected UIPage FindUIPage(SerializedProperty property)
{
    var component = property.serializedObject.targetObject as Component;
    Assert.IsNotNull(component);

    GameObject go = component.gameObject;

    Debug.Log(PrefabUtility.IsPartOfPrefabAsset(go)); // -> True
    Debug.Log(go.activeInHierarchy);                  // -> False
    Debug.Log(go.activeSelf);                         // -> True

    Debug.Log(go.GetComponentInParent<UIPage>(/* false */)); // -> Null
    Debug.Log(go.GetComponentInParent<UIPage>(true));        // -> Not Null

    return go.GetComponentInParent<UIPage>(true);
}
```

## 这不是一个 Bug

有人 2020 年在 Unity Issue Tracker 上提过这个问题 [^1]，但 Unity 反馈说它与 2019 年的 GetComponentInParent has no override for getting inactive objects [^2] 问题重复（严格来说，应该是 overload 而不是 override），说明这大概率不是一个 Bug，Unity 就是这样设计的。

## By the way

`GameObject` 上的 `GetComponentInParent` 从 2020.1.X 开始有 `includeInactive` 参数，但当时 Unity 忘记在 `Component` 上定义这个重载了，所以 2021.2.X 开始 `Component` 上才有。[^3]

[^1]: [GetComponentInParent is returning null when the GameObject is a prefab - Unity Issue Tracker](https://issuetracker.unity3d.com/issues/getcomponentinparent-is-returning-null-when-the-gameobject-is-a-prefab)
[^2]: [GetComponentInParent has no override for getting inactive objects - Unity Issue Tracker](https://issuetracker.unity3d.com/issues/getcomponentinparent-has-no-override-for-inactive-objects)
[^3]: [Component.GetComponentInParent doesn't have an overload for getting components of inactive objects - Unity Issue Tracker](https://issuetracker.unity3d.com/issues/component-dot-getcomponentinparent-doesnt-have-an-overload-for-getting-components-of-inactive-objects)
