---
date: 2024-05-01T01:33:47
---

# Windows 全局钩子

实现全局钩子需要写一个 dll 和一个 exe。

由于进程的地址空间是相互隔离的，发生事件的进程不能调用其他进程地址空间的钩子函数，所以把钩子函数写在一个 dll 里，在事件发生时，系统会把这个 dll 加载进发生事件的进程，使它能够调用钩子函数。exe 只负责安装和卸载钩子。

## dll 实现

### 共享数据段

全局钩子的句柄需要放在 [[DLL 进程间共享数据|dll 的共享数据段]] 里，保证所有进程加载的 dll 共享一个全局钩子句柄。

``` c
#pragma data_seg(".shared")
    HHOOK hHook = NULL;
#pragma data_seg()

#pragma comment(linker, "/SECTION:.shared,RWS")
```

### 钩子函数

看文档根据具体的情况实现，这里以 `ShellProc` 为例。

``` c
LRESULT CALLBACK ShellProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    if (nCode == HSHELL_LANGUAGE)
    {
        // 处理 HSHELL_LANGUAGE
    }

    // ...

    return CallNextHookEx(hHook, nCode, wParam, lParam);
}
```

最后要调用 ` CallNextHookEx `！

### 安装和卸载函数

这两个方法要导出给 exe 用。同样要根据文档和需求指定不同的参数。

``` c
void __declspec(dllexport) Install(HINSTANCE hinstDLL)
{
    if ((hHook = SetWindowsHookEx(WH_SHELL, ShellProc, hinstDLL, 0)))
    {
        // ...
    }
}

void __declspec(dllexport) Uninstall(HINSTANCE hinstDLL)
{
    if (hHook && UnhookWindowsHookEx(hHook))
    {
        hHook = NULL;
    }
}
```

文档：[SetWindowsHookExA function (winuser.h) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexa)

## exe 实现

### 安装和卸载钩子

加载 dll 后，调用 dll 里导出的安装函数。

``` c
// 加载 dll
if (!(hinstDLL = LoadLibrary(TEXT("my-dll.dll"))))
{
    return;
}

InstallHook = (InstallerFunc)GetProcAddress(hinstDLL, "Install");
UninstallHook = (InstallerFunc)GetProcAddress(hinstDLL, "Uninstall");

if (!InstallHook || !UninstallHook)
{
    return;
}

InstallHook(hinstDLL);
```

上面 `InstallerFunc` 的定义

``` c
typedef void (*InstallerFunc)(HINSTANCE hinstDLL);
```

程序结束后，调用卸载函数。

``` c
UninstallHook(hinstDLL);
FreeLibrary(hinstDLL);
```

### 消息循环

``` c
MSG msg;
BOOL bRet;
while ((bRet = GetMessage(&msg, NULL, 0, 0)) != 0)
{
    // GetMessage() 返回 -1 表示出错，返回 0 表示 WM_QUIT 消息
    if (bRet == -1)
    {
        return Dispose(4);
    }

    TranslateMessage(&msg);
    DispatchMessage(&msg);
}
```

### 防多开

dll 里的 `hHook` 变量是所有进程共享的，多个进程同时写可能出现竞争。需要 [[Windows 程序防多开|避免 exe 被多开]]。
