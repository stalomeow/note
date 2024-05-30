---
slug: "240427181327"
date: 2024-04-27
---

# GCHandle 与 IntPtr

`GCHandle` 与 `IntPtr` 可以相互转换，但是这个 `IntPtr` 不是某一个内部对象的地址，而是把 `handle` 的信息编码进了 `IntPtr`（native int）中。

例如，`GCHandle` 中的 `IsPinned` 私有方法是这样实现的：

``` csharp
// 注：handle 是一个 GCHandle
private static bool IsPinned(IntPtr handle)
{
    return ((nint)handle & 1) != 0;
}
```


