---
date: 2024-05-04T01:31:41
---

# GNU Make

这个工具可以用来自动化一些流程，比如编译流程。相关资料：

- 官网（可以下到源码）：[Make - GNU Project - Free Software Foundation](https://www.gnu.org/software/make/)
- 官方手册：[GNU Make Manual - GNU Project - Free Software Foundation](https://www.gnu.org/software/make/manual/)
- 中文教程（网页 +PDF）：[跟我一起写Makefile — 跟我一起写Makefile 1.0 文档 (seisman.github.io)](https://seisman.github.io/how-to-write-makefile/index.html)

## 打印调试信息

在用 `make` 命令时加上 `-d` 选项就能打印调试信息。

``` bash
make -d
```

## 忽略错误

一般情况下，只要一条命令出错 make 就会停下来。在命令前加 `-` 表示在它出错时直接忽略，继续执行。

``` bash
-mkdir dir
```

## 只用一个 Shell 执行所有命令

默认情况下，每行命令都在一个单独的 Shell 里执行。在 Makefile 的任意位置加一个 `.ONESHELL` 目标，就能让多行命令都在一个 Shell 里执行。

即在 Makefile 里加一行

``` makefile
.ONESHELL:
```

这个时候，如果不希望在 Shell 上打印原始命令的话，只要第一行命令开头加一个 `@` 就行，不需要再每行都加了。

## 自动变量

|  符号  |      含义       |
| :--: | :-----------: |
| `$@` |     目标文件      |
| `$<` |    第一个依赖文件    |
| `$^` |    所有依赖文件     |
| `$?` | 所有内容发生变化的依赖文件 |

## Windows Shell

在 Windows 上，make 默认还是会先找 sh 作为默认的 Shell。由于装 [[Git|git]] 的时候，会附带一个 sh，所以 make 会拿 git 安装目录里的 sh 作为默认的 Shell。

个人觉得 git 自带的 sh 在 Windows 上不好用，所以要把 Shell 改成 `cmd`。在 Makefile 前面加一行

``` makefile
SHELL := cmd
```

如果要换成其他 Shell，比如 [[PowerShell]] 的话，必须写绝对路径或者带扩展名的 `pwsh.exe`。

``` makefile
SHELL := pwsh.exe
```

指定了 `SHELL` 后，make 会按下面的流程检查它是否存在

1. 把 `$(SHELL)` 当绝对路径，直接检查文件是否存在
2. 把 `$(SHELL)` 拼到环境变量 `Path` 后面，然后逐个检查对应文件是否存在

不存在的话就用默认的 sh。`cmd` 是被特殊对待的，不用加扩展名，但 `pwsh.exe` 不加 `.exe` 的话就找不到了。
