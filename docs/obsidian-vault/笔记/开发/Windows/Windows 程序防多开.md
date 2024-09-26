---
slug: "240503200030"
date: 2024-05-03
---

# Windows 程序防多开

在 Windows 上保证一个程序只有一个实例，禁止多开。

## 用 Mutex 实现

这个是比较常用的方法。程序启动时，创建一个命名的 Mutex，如果之前就存在，那么说明多开了，直接退出。

文档：[CreateMutexA function (synchapi.h) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexa)

``` c
HANDLE hMutex = CreateMutex(NULL, FALSE, TEXT("MyUniqueMutexName"));

// 创建失败
if (hMutex == NULL)
{
    return;
}

// 如果已经有一个实例在运行，则退出
if (GetLastError() == ERROR_ALREADY_EXISTS)
{
    // 释放 Mutex
    CloseHandle(hMutex);
    return;
}

// 程序的逻辑 ...

// 结束后释放 Mutex
CloseHandle(hMutex);
```

`CreateMutex` 返回内核对象的句柄，用完以后要调用 `CloseHandle` 释放它，减少内核对象的引用计数。

`ReleaseMutex` 是释放 Mutex 的所有权。这里只判断 Mutex 是否存在，不管所有权，所以不需要用这个函数。
