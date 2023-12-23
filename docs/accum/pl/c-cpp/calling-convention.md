# 函数调用约定

!!! abstract

    两种常见的 C/C++ 函数调用约定：`__stdcall`、`__cdecl`。

    <hr>

    <small><i>高中博客的遗产。</i></small>

当一个函数被调用时，参数会被传递给这个函数，返回值会被返回给调用者。函数调用约定主要约束了三件事：

1. 参数传递顺序。
2. 堆栈维护职责。
3. 名称修饰约定。

## __stdcall

| |实现|
|:-|:-|
|参数传递顺序|从右向左|
|堆栈维护职责|被调用的函数从堆栈中弹出自己的参数|
|名称修饰约定|`_` 作为名称的前缀，名称后跟 `@` 符号和所有参数占用的字节数（十进制）|

??? example "名称修饰约定的例子"

    ``` c
    int32_t __stdcall func(int32_t a, double b);
    ```

    修饰后的名称为 `_func@12`。

Win32 API 函数绝大部分都是采用 `__stdcall` 调用约定的。`WINAPI` 其实也只是 `__stdcall` 的一个别名而已。

``` c
#define WINAPI __stdcall
```

!!! warning "注意"

    由于该调用约定是被调用方清理堆栈，因此编译器会对 `vararg` 函数使用 `__cdecl`。

## __cdecl

| |实现|
|:-|:-|
|参数传递顺序|从右向左|
|堆栈维护职责|调用函数从堆栈中弹出参数|
|名称修饰约定|`_` 作为名称的前缀，但导出使用 C 链接的 `__cdecl` 函数时除外|

`__cdecl` 是 C Declaration 的缩写，是 C/C++ 程序的默认调用约定。

!!! warning "注意"

    由于堆栈由调用方清理，因此它可以执行 `vararg` 函数，但该调用约定创建的可执行文件比 `__stdcall` 更大，因为它要求每个函数调用都包含堆栈清理代码。

[^1]: [Calling Conventions | Microsoft Learn](https://docs.microsoft.com/en-us/cpp/cpp/calling-conventions)
[^2]: [函数调用约定_百度百科](https://baike.baidu.com/item/%E5%87%BD%E6%95%B0%E8%B0%83%E7%94%A8%E7%BA%A6%E5%AE%9A/3306047?fr=aladdin)