---
date: 2024-11-26T13:14:47
publish: true
comments: true
permalink: wsl
aliases:
---

# WSL

Windows Subsystem for Linux (WSL) 可以方便地在 Windows 电脑上再运行一个 Linux 系统。

## WSL 1 vs WSL 2

具体区别：[Comparing WSL Versions | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。

- WSL 1 通过将 Linux 命令翻译为 Windows 命令实现。
- WSL 2 通过 Hyper-V 硬件虚拟化技术实现，运行了完整的 Linux 内核。

默认为 WSL 2。

## 命令

显示帮助

``` powershell
wsl --help
```

显示可安装的发行版本

``` powershell
wsl -l -o
```

``` powershell
以下是可安装的有效分发的列表。
使用 'wsl.exe --install <Distro>' 安装。

NAME                            FRIENDLY NAME
Ubuntu                          Ubuntu
Debian                          Debian GNU/Linux
kali-linux                      Kali Linux Rolling
Ubuntu-18.04                    Ubuntu 18.04 LTS
Ubuntu-20.04                    Ubuntu 20.04 LTS
Ubuntu-22.04                    Ubuntu 22.04 LTS
Ubuntu-24.04                    Ubuntu 24.04 LTS
OracleLinux_7_9                 Oracle Linux 7.9
OracleLinux_8_7                 Oracle Linux 8.7
OracleLinux_9_1                 Oracle Linux 9.1
openSUSE-Leap-15.6              openSUSE Leap 15.6
SUSE-Linux-Enterprise-15-SP5    SUSE Linux Enterprise 15 SP5
SUSE-Linux-Enterprise-15-SP6    SUSE Linux Enterprise 15 SP6
openSUSE-Tumbleweed             openSUSE Tumbleweed
```

安装 Ubuntu

``` powershell
wsl --install -d Ubuntu
```

删除已经安装的 Ubuntu

> 注意是 `--unregister`。`--uninstall` 是卸载 `wsl` 组件。

``` powershell
wsl --unregister Ubuntu
```

显示当前安装的发行版的详细信息

``` powershell
wsl --list -v
```

``` powershell
  NAME      STATE           VERSION
* Ubuntu    Stopped         2
```

## 文件管理

Windows 的 File Explorer 可以直接显示 Linux 的文件。Linux 中可以通过 `/mnt/c/Users/...` 路径访问 Windows 中的文件，但这种方式性能不太好。

## 软件

Ubuntu 安装以后，记得更新一下软件。第一个命令是更新本地软件包**列表**，第二个命令是升级系统中已安装的软件包。可以在每次安装软件前执行一下第一个命令，保证软件列表是新的。

``` bash
sudo apt update && sudo apt upgrade
```

可以安装 `build-essential` 快速配置 C/C++ 环境。

``` bash
sudo apt install build-essential
```

## 并行编译

使用 `cmake` 或 `Makefile` 时，不要直接用 `-j` 选项 [[GNU Make#并行|无限制并行]]，可能因为占用资源过多直接被系统 kill 掉。如果要并行的话，指定一个最大限制，例如 `-j2`。

## 其他

还有 GPU 加速（CUDA/DirectML）、VSCode 配置等，可以看微软文档：[Set up a WSL development environment | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)。

另外，Windows 上还可以用 `wsl` 命令直接执行 Linux 命令。

## 视频

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=1856395884&bvid=BV1tW42197za&cid=1630340704&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>
