# 多版本和虚拟环境

!!! abstract

    Windows 下，使用 Python Launcher 管理多个版本的 Python，使用 venv 管理虚拟环境。

    尽管单独使用 conda（Anaconda、Miniconda）就能完成这些工作，但由于 conda 源中的包太少，经常要混用 `conda install` 和 `pip install` 让我很不爽，所以我选择用其他方案。

## Python 版本管理

电脑上需要安装多个版本的 Python，所以需要一个工具来做版本管理。一些常见的方案有：

- [pyenv](https://github.com/pyenv/pyenv)

    通过在环境变量 `Path` 的前面加一个 Shim Path，截获命令行中 python 相关的调用，实现多版本管理。**不支持 Windows。**

- [pyenv-win](https://github.com/pyenv-win/pyenv-win)

    pyenv 的 Windows 版。

- [Python Launcher](https://docs.python.org/3/using/windows.html#python-launcher-for-windows)

    官方为 Windows 系统提供的工具，直接被安装到系统目录。从 Python 3.3 开始，可以在安装 Python 时勾选安装。

这里我选择用 Python Launcher。

!!! tips

    1. 安装 Python 时，记得在自定义安装中勾选 py launcher。
    2. 不要把 Python 添加到环境变量 `Path` 中，避免混淆。

### 命令行中使用

统一使用 `py` 命令来调用 Python：

- `py` 使用默认的 Python 版本。
- `py -2` 使用 Python 2。
- `py -3` 使用 Python 3。
- `py -X.Y` 使用 Python X.Y。
- `py --list` 显示所有已安装的 Python 版本。
- 更多参数可以用 `py -h` 来查看。

举个例子，调用 Python 3.10 的 pip 安装依赖：

``` powershell
py -3.10 -m pip install -r requirements.txt
```

### 代码中指定版本

可以在 Python 文件前面指定版本：

=== "Python 2"

    ``` python
    #! python2

    print('Hello World!')
    ```

=== "Python 3"

    ``` python
    #! python3

    print('Hello World!')
    ```

=== "Python 3.10"

    ``` python
    #! python3.10

    print('Hello World!')
    ```

然后用下面的命令直接执行：

``` powershell
py script.py
```

## 虚拟环境

虚拟环境可以隔离项目的环境，避免污染全局。有时候不同项目会依赖同一个第三方库的不同版本，虚拟环境能很好地解决这个问题。一些常见的方案有：

- virtualenv

    功能强大，但不方便集中管理虚拟环境。支持 Python 2 和 3。

- virtualenv + virtualenvwrapper

    可以集中管理虚拟环境的 virtualenv，类似 conda。

- pipenv

    pip + virtualenv。

- venv

    Python 3.3 之后内置的官方库。**不支持旧版本的 Python。**

方便起见，我选择用 venv。一个项目一个虚拟环境，配合 Python Launcher 选择 Python 版本。

### 使用方法

在命令行中进入项目所在的目录，用指定版本的 Python 调用 venv。

例如，这里我用 Python 3.10 创建了一个叫 `env` 的虚拟环境：

``` powershell
py -3.10 -m venv env
```

创建完成后，项目中会多出一个文件夹（在这个例子中叫 `env`），里面存放着 Python、之后下载的 Package、其他和虚拟环境相关的文件。

激活环境：

``` powershell
.\env\Scripts\activate
```

然后就能正常使用了！可以放心地直接调用 python、pip。

退出环境：

``` powershell
deactivate
```

### 代码编辑器

VSCode 可以自动识别虚拟环境，不需要额外配置。其他的还没试过，估计也可以。

[^1]: [讲讲 Python Launcher 是什么鬼东西？ - 知乎](https://zhuanlan.zhihu.com/p/387109071)
[^2]: [Installing packages using pip and virtual environments — Python Packaging User Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
[^3]: [venv --- 创建虚拟环境 — Python 3.11.4 文档](https://docs.python.org/zh-cn/3/library/venv.html)
[^4]: [python多环境管理（venv与virtualenv） - doublexi - 博客园](https://www.cnblogs.com/doublexi/p/15783355.html)