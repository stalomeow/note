---
slug: "20240421203108"
date: 2024-04-21
---

# 优化迭代和协程的 GC 

主要涉及 foreach、yield、Coroutine 的 GC 优化。不对 Unity 2022 LTS 以下的版本负责。

## for 和 foreach

对数组来说，foreach 会被编译器转成 for，两者没什么区别。对于其他集合，foreach 的本质就是 `GetEnumerator()` 获取迭代器，然后不断 `MoveNext()` 并获取 `Current`。

用 foreach 前，先检查一下 `GetEnumerator()` 的返回值类型。如果迭代器本身不是值类型，或者返回时会装箱的话，每次用 foreach 都会创建一个新的迭代器对象，产生 GC Alloc。这种情况尽量用 for。

像平时常用的 `List<T>`、`Dictionary<TKey, TValue>` 的迭代器都是值类型的，可以放心用 foreach。

## 不滥用 yield

在 C# 中，用 `yield` 语句可以快速实现 `IEnumerator<T>`、`IEnumerable<T>`。但是，这种方式生成的迭代器、集合都是引用类型的，对 foreach 不友好。

> 就算编译器生成值类型迭代器，因为方法返回的类型是 `IEnumerator<T>`，所以返回时也会装箱，还不如直接生成为引用类型。

如果迭代器比较常用的话，还是应该自己手写一个值类型的版本，并且声明一个返回该类型迭代器的 `GetEnumerator()` 方法（扩展方法也行）。

## 协程和 UniTask

在 Unity 里，协程本质就是个迭代器，用 `yield` 语句来编写。每次开启一个协程都会 new 新的迭代器对象，产生 GC Alloc。

UniTask 是基于 async/await 来实现的，可以替代协程。对于 async method，在 Release 模式下，编译器生成的 state machine 是值类型的。在此基础上，UniTask 又做了很多优化，使得它的 GC Alloc 很低，可以认为是 0 GC。
