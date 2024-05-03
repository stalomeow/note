---
slug: "240425224602"
date: 2024-04-25
---

# Windows 下使用 Makefile


基本上和正常 [[GNU Make]] 的使用方法一致，除了下面几点。

## Shell

在 Windows 上，make 默认还是会先找 sh 作为默认的 Shell。由于装 git 的时候，会附带一个 sh，所以 make 会拿 git 安装目录里的 sh 作为默认的 Shell。

个人觉得 git 自带的 sh 在 Windows 上不好用，所以要把 Shell 改成 `cmd`。在 Makefile 前面加一行

``` makefile
SHELL := cmd
```

如果要换成其他 Shell，比如 [[PowerShell]] 的话，必须写 `pwsh.exe`，后缀名不能省。

``` makefile
SHELL := pwsh.exe
```

make 会把 `$(SHELL)` 拼到环境变量 `Path` 后面，检查 Shell 文件是否存在，不存在的话就用默认的 sh。`cmd` 是被特殊对待的，不用加后缀名。但 `pwsh.exe` 不加 `.exe` 后缀的话就找不到了。


## 多行命令


