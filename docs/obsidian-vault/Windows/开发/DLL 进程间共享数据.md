---
slug: "240503184542"
date: 2024-05-03
---

# DLL 进程间共享数据

==这个方法仅限 MSVC。== 参考：[How do I share data in my DLL with an application or with other DLLs? | Microsoft Learn](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-2008/h90dkhs0(v=vs.90)?redirectedfrom=MSDN)

多个进程加载同一个 dll，dll 中的全局变量是不共享的。进程 A 对 dll 中全局变量的修改与进程 B 的修改是互不影响的。

可以用 `#pragma data_seg` 声明一个命名数据段来打破这个限制。把需要共享的变量声明在这个数据段中。变量在声明时 ==必须初始化== ！否则不会被放在命名数据段中。之后再用 `#pragma comment` 告诉链接器，这个数据段是可读（R）、可写（W）、共享（S）的。

``` c
#pragma data_seg(".shared")
    HHOOK hHook = NULL;
#pragma data_seg()

#pragma comment(linker, "/SECTION:.shared,RWS")
```

上面的代码声明了一个叫 `.shared` 的 RWS 命名数据段，里面有一个 `hHook` 变量。


