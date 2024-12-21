---
date: 2024-04-27T16:45:05
---

# Python 虚拟环境

虚拟环境可以隔离项目的环境，避免污染全局。有时候不同项目会依赖同一个第三方库的不同版本，虚拟环境能很好地解决这个问题。一些常见的方案有：

- `virtualenv`：功能强大，但不方便集中管理虚拟环境。支持 Python 2 和 3。
- `virtualenv` + `virtualenvwrapper`：可以集中管理虚拟环境的 `virtualenv`，类似 conda。
- `pipenv`：`pip` + `virtualenv`。
- `venv`：Python 3.3 之后内置的官方库。**不支持旧版本的 Python。**

## `venv`

方便起见，我选择用 `venv`。一个项目一个虚拟环境。

### 使用方法

在命令行中进入项目所在的目录，用指定版本的 Python 调用 `venv`。

例如，这里我用 Python 3.10 创建了一个叫 `env` 的虚拟环境：

``` bash
py -3.10 -m venv env
```

创建完成后，项目中会多出一个文件夹（在这个例子中叫 `env`），里面存放着 Python、之后下载的 Package、其他和虚拟环境相关的文件。

激活环境：

``` bash
.\env\Scripts\activate
```

然后就能正常使用了！可以放心地直接调用 python、pip。

退出环境：

``` bash
deactivate
```

### 代码编辑器

VSCode 可以自动识别 `venv`，不需要额外配置。其他的还没试过，估计也可以。

## 参考

- [Installing packages using pip and virtual environments — Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
- [venv --- 创建虚拟环境 — Python 3.11.4 文档](https://docs.python.org/zh-cn/3/library/venv.html)
- [python多环境管理（venv与virtualenv） - doublexi - 博客园](https://www.cnblogs.com/doublexi/p/15783355.html)
