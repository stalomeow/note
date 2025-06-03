---
date: 2024-04-25T22:45:29
publish: true
comments: true
permalink: power-shell
aliases:
---

# PowerShell

[PowerShell](https://github.com/PowerShell/PowerShell) 是一个基于 .NET 的跨平台 Shell。Windows 自带的 PowerShell（`powershell.exe`）是不跨平台的旧版，新版（`pwsh.exe`）需要自己安装。

## 安装

文档：[在 Windows 上安装 PowerShell - PowerShell | Microsoft Learn](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows)

推荐用包管理器安装，例如 WinGet，但是不推荐 [[Scoop]]。

> Since Scoop uses pwsh.exe internally, to update PowerShell Core itself, run `scoop update pwsh` from Windows PowerShell, i.e. powershell.exe. [^1]

## 配置文件

配置文件就是一个 PowerShell 脚本，每次 PowerShell 启动时它会被自动执行。`$PROFILE` 变量中保存了它的路径。

文档：[about Profiles - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles)

### 创建配置文件

第一次用的话，可能没有配置文件，需要手动创建。

``` powershell
New-Item -Path $PROFILE -Type File -Force
```

### 编辑配置文件

``` powershell
code $PROFILE
```

可以在配置文件最后加一个 `cls` 命令，清掉没用的信息。

### 重新加载配置

用 [Dot sourcing operator `.`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators#dot-sourcing-operator-) 重新执行一遍配置文件。

``` powershell
. $PROFILE
```

不要用 [Call operator `&`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.4#call-operator-)！它是在一个子作用域里执行脚本，脚本里的赋值不会影响全局。

## 增强编辑体验

使用 [PSReadLine](https://github.com/PowerShell/PSReadLine) 模块。在新的 PowerShell 中它已经被内置了，不用自己安装了。

### 查看键位

``` powershell
Get-PSReadLineKeyHandler
```

### 命令补全

我比较喜欢 copilot 那种 tab 补全，但是 PSReadLine 只是把你以前输入的相似内容提示给你，整行补全基本上没什么用。我选择退而求其次，按一下 tab 只向前补全一个单词。

在配置文件里加上

``` powershell
Set-PSReadLineKeyHandler -Key Tab -Function ForwardWord
```

## 主题美化

使用 [oh-my-posh](https://github.com/JanDeDobbeleer/oh-my-posh) 实现，但会使 PowerShell 启动变慢。文档：[Introduction | Oh My Posh](https://ohmyposh.dev/docs/)。

## gcm 命令

`gcm` 全称 [Get-Command](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-command)，类似以前 cmd 里的 `where` 命令和 linux 的 `which` 命令。获取所有 `xxx` 命令的方法：

``` powershell
gcm xxx -All
```

PowerShell 里的 `where` 指的是 [Where-Object](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/where-object)。如果要调用 cmd 的 where，需要用 `where.exe`。[^2]

## 环境变量

临时设置环境变量，语法和 cmd 的不一样。做 golang 交叉编译时常用。

``` powershell
$env:GOOS="linux"
$env:GOARCH="amd64"
```

读取环境变量

``` powershell
$env:GOOS
```

[^1]: [https://github.com/ScoopInstaller/Main/blob/2b4e2caea453c0ce0d5a6ccb7a05f3146e4c5131/bucket/pwsh.json#L7](https://github.com/ScoopInstaller/Main/blob/2b4e2caea453c0ce0d5a6ccb7a05f3146e4c5131/bucket/pwsh.json#L7)
[^2]: [在PowerShell中使用where命令查找文件-CSDN博客](https://blog.csdn.net/mighty13/article/details/119880762)
