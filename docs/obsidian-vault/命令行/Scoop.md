---
slug: "240425224756"
date: 2024-04-25
---

# Scoop

Windows 上一款开源的包管理器，类似 macOS 的 Homebrew。用它装开发工具非常方便，环境变量也不需要自己配置了。

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


## 常用命令


参考：

- [你需要掌握的Scoop技巧和知识 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/135278662)
- [Scoop - 最好用的 Windows 包管理器 - P3TERX ZONE](https://p3terx.com/archives/scoop-the-best-windows-package-manager.html)

### 清缓存

``` bash
# 查看所有已下载的缓存信息
scoop cache show

# 清除指定程序的下载缓存
scoop cache rm <app>

# 清除所有缓存
scoop cache rm *

# 删除某软件的旧版本
scoop cleanup <app>

# 删除全局安装的某软件的旧版本
scoop cleanup <app> -g

# 删除过期的下载缓存
scoop cleanup <app> -k
```

## 避坑

### MongoDB

`mongod` shim use `$dir\bin\mongod.cfg` as the default config file. To use a different config file, please run [^1]

``` powershell
$dir\bin\mongod.exe --config NEW_CONFIG_FILE
```

其中 `$dir` 是 `mongod` 的安装目录。

### Miktex




[^1]: [https://github.com/ScoopInstaller/Main/blob/5947087876e7d49221ad0b3293e56bf8402e64d6/bucket/mongodb.json#L14-L16](https://github.com/ScoopInstaller/Main/blob/5947087876e7d49221ad0b3293e56bf8402e64d6/bucket/mongodb.json#L14-L16)




