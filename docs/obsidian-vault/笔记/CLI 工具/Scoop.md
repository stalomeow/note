---
date: 2024-04-25T22:47:56
---

# Scoop

Windows 上一款开源的软件安装器，类似 macOS 的 Homebrew。用它装开发工具非常方便，环境变量也不需要自己配置了。

用一行 [[PowerShell]] 命令就能安装这个工具，具体看官网：[Scoop](https://scoop.sh/)

一些有自动更新功能的软件就别用 Scoop 装了。软件自动更新后，Scoop 这边是不知道的，版号就会错乱，可能导致一些神奇的 bug。这种软件建议直接官网安装，或者用 WinGet 装。

## Bucket

Bucket 相当于一类软件的集合，负责管理它们的版号和安装方式。Scoop 官方提供了很多个 Bucket，都在 GitHub 上和社区一起维护

- [ScoopInstaller/Main: 📦 The default bucket for Scoop. (github.com)](https://github.com/ScoopInstaller/Main)
- [ScoopInstaller/Extras: 📦 The Extras bucket for Scoop. (github.com)](https://github.com/ScoopInstaller/Extras)
- [ScoopInstaller/Versions: 📦 A Scoop bucket for alternative versions of apps. (github.com)](https://github.com/ScoopInstaller/Versions)
- 等等

官方提供了一个模板：[ScoopInstaller/BucketTemplate: Template Bucket for Scoop Installer (github.com)](https://github.com/ScoopInstaller/BucketTemplate)，我们可以用它创建自己的 Bucket。

## 多线程下载

先装 [[Aria2]]，然后 Scoop 就会用它多线程下载。

``` bash
scoop install aria2
```

如果下载速度反而慢了，用下面的命令关闭多线程下载。

``` bash
scoop config aria2-enabled false
```

## 常用命令

参考：

- [你需要掌握的Scoop技巧和知识 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/135278662)
- [Scoop - 最好用的 Windows 包管理器 - P3TERX ZONE](https://p3terx.com/archives/scoop-the-best-windows-package-manager.html)

### 更新

``` bash
# 检查哪些软件有更新
scoop status

# 更新 Scoop 自身
scoop update

# 更新某些 app
scoop update appName1 appName2

# 更新所有 app
scoop update *

# 禁止某程序更新
scoop hold <app>

# 允许某程序更新
scoop unhold <app>
```

### 清缓存

Scoop 默认会保留下载的安装包。

``` bash
# 查看所有的安装包缓存
scoop cache show

# 清除指定程序的安装包
scoop cache rm <app>

# 清除所有安装包缓存
scoop cache rm *
```

当软件被更新后 Scoop 会保留软件的旧版本。

``` bash
# 删除某软件的旧版本
scoop cleanup <app>

# 删除所有软件的旧版本
scoop cleanup *
```

加上 `-k` 参数可以同时删除旧版本和安装包。

``` bash
# 删除某软件的旧版本和安装包
scoop cleanup -k <app>

# 删除所有软件的旧版本和安装包
scoop cleanup -k *
```

### 切换软件版本

``` bash
scoop reset [app]@[version]
```

不写 `@[version]` 的话就切换到最新版。

### 查看软件信息

``` bash
# 列出已安装的 app
scoop list

# 显示某个 app 的信息
scoop info <app>

# 在浏览器中打开某 app 的主页
scoop home <app>
```

## 软件避坑

### MongoDB

`mongod` shim use `$dir\bin\mongod.cfg` as the default config file. To use a different config file, please run [^1]

``` powershell
$dir\bin\mongod.exe --config NEW_CONFIG_FILE
```

其中 `$dir` 是 `mongod` 的安装目录。

### Miktex

Scoop 现在使用 MIT 的镜像下载这个软件，国内速度非常慢，经常下载失败。这个镜像似乎还不让开代理访问。相关的内容：

- [(mik|la)tex: Use mirror link · ScoopInstaller/Main@cecb4a6 (github.com)](https://github.com/ScoopInstaller/Main/commit/cecb4a688b64a880a0f8330f6fbbea55aa5e19db)
- [[Bug]: Miktex 404 error on update · Issue #4680 · ScoopInstaller/Main (github.com)](https://github.com/ScoopInstaller/Main/issues/4680)

解决方法是自己去官网下载对应版本，然后替换 Scoop 的 cache 目录里的安装包。或者自己做一个 Bucket，用 SJTU 的镜像下载。

### Snipaste

必须装 `versions/snipaste-beta`。另外一个 `extras/snipaste` 很久没更新了，Win 11 上运行不了。

[^1]: [https://github.com/ScoopInstaller/Main/blob/5947087876e7d49221ad0b3293e56bf8402e64d6/bucket/mongodb.json#L14-L16](https://github.com/ScoopInstaller/Main/blob/5947087876e7d49221ad0b3293e56bf8402e64d6/bucket/mongodb.json#L14-L16)
