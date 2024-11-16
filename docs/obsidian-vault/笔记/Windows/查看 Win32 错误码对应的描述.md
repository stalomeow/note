---
date: 2024-05-01T01:04:26
---

# 查看 Win32 错误码对应的描述

Win32 的错误码，即 [GetLastError()](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror) 的返回值。在代码里可以用 [FormatMessage](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-formatmessage) 函数获取对应的描述，但有些 app 在打日志的时候只打印了错误码，所以需要一种更方便的方式来获取描述。

以错误码 1603 为例。

## net helpmsg 命令

这个方法的缺点：错误码必须是十进制。

``` powershell
net helpmsg 1603
```

结果是

```
安装时发生严重错误
```

## Win32Exception

这个方法只能在 [[PowerShell]] 里用。错误码可以是任意进制的。

``` powershell
[ComponentModel.Win32Exception] 1603
```

这行命令做了一个 [类型转换](https://learn.microsoft.com/en-us/powershell/scripting/lang-spec/chapter-06?view=powershell-7.4#618-net-conversion)。本质上是将 1603 作为参数 new 了一个 [Win32Exception Class (System.ComponentModel)](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.win32exception) 对象。结果是

```
NativeErrorCode : 1603
ErrorCode       : -2147467259
TargetSite      :
Message         : 安装时发生严重错误
Data            : {}
InnerException  :
HelpLink        :
Source          :
HResult         : -2147467259
StackTrace      :
```
