---
slug: "240427180904"
date: 2024-04-27
---

# CSharp 弱引用


当程序可以访问一个对象时，如果 GC 不能回收该对象，那么可以认为程序持有该对象的**强引用**。C# 中默认的引用方式就是强引用。下面的代码先创建了一个对象，然后建立了对它的强引用并记为 `obj`。

``` csharp
var obj = new object();
```

**弱引用**允许程序访问对象，同时也允许 GC 回收这个对象。可以用

- [`WeakReference`](https://learn.microsoft.com/en-us/dotnet/api/system.weakreference)
- [`WeakReference<T>`](https://learn.microsoft.com/en-us/dotnet/api/system.weakreference-1)
- [`GCHandle`](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.gchandle)

来创建弱引用。下面的代码创建了对 `obj` 引用的对象的弱引用。

- `WeakReference`

    ``` csharp
    var weakRef = new WeakReference(obj);

    // do something ...
    ```

- `GCHandle`

    ``` csharp
    var gcHandle = GCHandle.Alloc(obj, GCHandleType.Weak);

    // do something ...

    gcHandle.Free(); // 一定要记得 Free！
    ```

---

- 弱引用和强引用可以同时存在。
- 当强引用不存在时，对象就有资格被 GC 回收。
- 在使用弱引用指向的对象前，需要检查这个对象是否存活。

``` csharp
object target = weakRefOrGCHandle.Target; // 尝试重新建立强引用

if (target is null)
{
    // 弱引用指向的对象已经被 GC 回收了，所以重新创建一个
    target = new object();
    weakRefOrGCHandle.Target = target;
}
else
{
    // 弱引用指向的对象还没被 GC 回收，可以直接使用
}

// do something ...
```

---

在使用 `WeakReference` 时，不要像下面这样写

``` csharp
if (weakRef.IsAlive)
{
    object target = weakRef.Target;

    // do something ...
}
```

有可能在 `if` 的条件判断完成后对象被 GC 回收了，这时 `target` 的值为 `null`。

## 短弱引用 vs. 长弱引用

一般来说，对象有四种状态：

1. 活跃状态。
2. 终结器排队等待执行。
3. 终结器执行完成，等待下一次 GC。
4. 被 GC 回收，彻底没了。

通常，对象处于状态 1。当一次 GC 发生时，假设一个对象被认为是垃圾，

- 如果它有终结器且终结器需要被执行，则进入状态 2。
- 如果它被上一种对象强引用（包括直接和间接），它也进入状态 2。
- 其余情况，直接进入状态 4。

处于状态 2 的对象，在终结器被执行完成后，会进入状态 3。等到下一次 GC 发生时，会尝试回收处于状态 3 的对象，如果成功，使之进入状态 4，否则回到状态 1。

- 当一个对象处于状态 2 时，它处于一种假死的状态。这时对象中的数据是无法预测的，因为它可能引用了已经处于状态 3 的对象（在本次 GC 中也是垃圾，并且终结器较早执行）。

- 在调用终结器前的那一刻，对象会复活（Resurrection），允许（终结器里的）程序访问。

- 一个对象的终结器默认只执行一次。换言之，复活的对象相当于没有终结器（除非程序里强制重新执行）。

关于终结器和复活，会另外写一篇文章，此处不继续展开。

- 短弱引用（Short Weak Reference）
- 一旦引用指向的对象离开状态 1，这个引用就无效了（`Target` 属性返回值变成 `null`）。即使对象复活，该引用也无效。
- 长弱引用（Long Weak Reference）
- 当对象进入状态 4 时，引用才失效。

`WeakReference` 默认创建的是短弱引用，如果要创建长弱引用，需要在构造函数中将 `trackResurrection` 设置为 `true`。

`GCHandle` 必须要在构造函数中手动指定类型才能创建弱引用：

- `GCHandleType.Weak`：短弱引用。
- `GCHandleType.WeakTrackResurrection`：长弱引用。

### 尽量不要使用长弱引用

- 对象中的数据可能在某个时间点变得无法预测，这也许会导致一些错误。
- Unity IL2CPP 不支持！！！

## 注意事项

- 不要对小对象使用弱引用。创建弱引用需要占用额外的空间，这可能比小对象本身占用的空间都大。
- 当一个对象占用的空间很大，但是很容易被重新创建时，可以使用弱引用。
- 能不用就别用。

## WeakReference 的实现

`WeakReference` 实际上是用 `GCHandle` 实现的。

在一般的 .NET 实现中，`WeakReference` 对象本身会被 GC 特殊对待。下面这段话是源码中 `~WeakReference()` 方法里的注释。

> While WeakReference is formally a finalizable type, the finalizer does not actually run.
> Instead the instances are treated specially in GC when scanning for no longer strongly-reachable finalizable objects.
>
> Unlike WeakReference&lt;T&gt; case, the instance could be of a derived type and in such case it is finalized via a finalizer. [^1]

在 Unity 的 IL2CPP 中，`WeakReference` 是一个非托管对象。创建时直接 `malloc`，然后靠引用计数来管理，当引用计数归零时直接 `free`。具体代码在 IL2CPP 目录下 `libil2cpp/vm/WeakReference.cpp` 文件中。

## GCHandle 的实现

这里只简单谈谈 Unity IL2CPP 中短弱引用 `GCHandle` 的实现，具体代码在 IL2CPP 目录下 `libil2cpp/gc/GCHandle.cpp` 及其头文件中。

IL2CPP 在非托管内存里维护了四个列表，用来保存四个类型的 `GCHandle`。

``` cpp
enum GCHandleType
{
    HANDLE_WEAK,
    HANDLE_WEAK_TRACK,
    HANDLE_NORMAL,
    HANDLE_PINNED
};

typedef struct
{
    uint32_t  *bitmap;
    void* *entries;
    uint32_t   size;
    uint8_t    type;
    uint32_t     slot_hint : 24;/* starting slot for search */
    /* 2^16 appdomains should be enough for everyone (though I know I'll regret this in 20 years) */
    /* we alloc this only for weak refs, since we can get the domain directly in the other cases */
    uint16_t  *domain_ids;
} HandleData;

/* weak and weak-track arrays will be allocated in malloc memory
 */
static HandleData gc_handles[] =
{
    {NULL, NULL, 0, HANDLE_WEAK, 0},
    {NULL, NULL, 0, HANDLE_WEAK_TRACK, 0},
    {NULL, NULL, 0, HANDLE_NORMAL, 0},
    {NULL, NULL, 0, HANDLE_PINNED, 0}
};
```

`HandleData` 事实上就是一个同类型 `GCHandle` 的列表。

- `type` 表示 `GCHandle` 的类型，对应 `GCHandleType`。
- `entries` 是一个指针数组，用于保存 `GCHandle.Target` 对象的地址。
- `size` 保存了 `entries` 数组的长度，它满足表达式 $32 \cdot 2^n$ ， $n$ 是一个自然数。每次扩容， $n$ 递增。
- `bitmap` 也是一个数组，用二进制状态压缩的方法记录 `entries` 中每一个位置的使用情况。
- `slot_hint` 用于快速在 `entries` 数组中找空位。
- `domain_ids` 暂时不需要管<del>（没看见它被用过）</del>。

创建 `Weak GCHandle` 的大致流程（伪代码）：

``` cpp
static uint32_t alloc_weak_handle(Il2CppObject *obj, bool track_resurrection)
{
    HandleData *handles = &gc_handles[track_resurrection ? HANDLE_WEAK_TRACK : HANDLE_WEAK];

    // ...

    uint32_t slot = find_empty_entry_index(handles->entries);

    // ...

    handles->entries[slot] = obj;

    // ...

    if (obj)
    {
        GarbageCollector::AddWeakLink(&(handles->entries[slot]), obj, track_resurrection);
    }

    // ...

    return (slot << 3) | (handles->type + 1);
}
```

最后的返回值 [[GCHandle 与 IntPtr|把信息编码进一个整数中]]。另外，为了保证 `IntPtr.Zero` 是一个无效的 `GCHandle`，`(slot << 3) | (handles->type + 1)` 表达式中才对 `type` 加一。 

`GarbageCollector` 里的方法大多依赖于 GC 的实现。下面以 Unity 使用的 BoehmGC 为例。

- `GarbageCollector::AddWeakLink` 会在内部的 `GC_dl_hashtbl`（GC disappearing-link hashtable）中添加一个新的 `disappearing_link`，把 `&(handles->entries[slot])` 与 `obj` 关联起来。当 `obj` 被回收以后，`handles->entries[slot]` 保存的地址也会被 GC 修改为非法值。

- 尝试访问弱引用指向的对象时，会调用 `GarbageCollector::GetWeakLink` 来拿到 `handles->entries[slot]` 里保存的地址。如果这个地址是非法值，那么会返回 `NULL`。

- 删除弱引用时，会调用 `GarbageCollector::RemoveWeakLink` 删除 GC 内部保存的 `disappearing_link`，然后回收 `GCHandle` 在 `gc_handles` 里占用的那个 `entry`（但不释放）。

## 参考

- [Weak References - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/weak-references)
- [System.WeakReference internals and side-effects : Reed Copsey, Jr.](http://reedcopsey.com/2009/07/08/systemweakreference-internals-and-side-effects/)
- [WeakReference implementation in .NET - Stack Overflow](https://stackoverflow.com/questions/1095492/weakreference-implementation-in-net)
- [WeakReference understanding - Stack Overflow](https://stackoverflow.com/questions/10928329/weakreference-understanding)
- [Prefer WeakReference<T> to WeakReference - Philosophical Geek](http://www.philosophicalgeek.com/2014/08/14/prefer-weakreferencet-to-weakreference/)
- [Short vs. Long Weak References and Object Resurrection - Philosophical Geek](http://www.philosophicalgeek.com/2014/08/20/short-vs-long-weak-references-and-object-resurrection/)
- [Practical uses of WeakReference - Philosophical Geek](http://www.philosophicalgeek.com/2014/09/03/practical-uses-of-weakreference/)
- [Garbage Collection: Automatic Memory Management in the Microsoft .NET Framework - MSDN Magazine](https://learn.microsoft.com/en-us/archive/msdn-magazine/2000/november/garbage-collection-automatic-memory-management-in-the-microsoft-net-framework)
- [c#--泛型-弱引用 - 知乎](https://zhuanlan.zhihu.com/p/348542890)

[^1]: [WeakReference - .NET Source Browser](https://source.dot.net/#System.Private.CoreLib/src/libraries/System.Private.CoreLib/src/System/WeakReference.cs,198)
