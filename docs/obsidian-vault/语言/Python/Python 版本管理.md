---
date: 2024-04-27T16:25:21
publish: true
comments: true
permalink: python-version-control
aliases:
---

# Python 版本管理

电脑上需要安装多个版本的 Python，所以需要一个工具来做版本管理。一些常见的方案有：

- [pyenv](https://github.com/pyenv/pyenv)：通过在环境变量 `Path` 的前面加一个 Shim Path，截获命令行中 python 相关的调用，实现多版本管理。**不支持 Windows。**
- [pyenv-win](https://github.com/pyenv-win/pyenv-win)：Pyenv 的 Windows 版。
- [Python Launcher](https://docs.python.org/3/using/windows.html#python-launcher-for-windows)：官方为 Windows 系统提供的工具，直接被安装到系统目录。从 Python 3.3 开始，可以在安装 Python 时勾选安装。
- 用包管理器管理，例如 [[Scoop]]。

## 使用 Python Launcher

我是 Windows 系统，直接用 Python Launcher 了。

### 注意事项

- 安装 Python 时，记得在自定义安装中勾选 py launcher。
- 不要把 Python 添加到环境变量 `Path` 中，避免混淆。

### 命令行中使用

统一使用 `py` 命令来调用 Python：

- `py` 使用默认的 Python 版本。
- `py -2` 使用 Python 2。
- `py -3` 使用 Python 3。
- `py -X.Y` 使用 Python X.Y。
- `py --list` 显示所有已安装的 Python 版本。
- 更多参数可以用 `py -h` 来查看。

举个例子，调用 Python 3.10 的 pip 安装依赖：

``` bash
py -3.10 -m pip install -r requirements.txt
```

### 代码中指定版本

在 Python 文件的 [[Shebang]] 里指定版本。

- Python 2

    ``` python
    #! python2

    print('Hello World!')
    ```

- Python 3

    ``` python
    #! python3

    print('Hello World!')
    ```

- Python 3.10

    ``` python
    #! python3.10

    print('Hello World!')
    ```

然后用下面的命令直接执行：

``` bash
py script.py
```

## 参考

[讲讲 Python Launcher 是什么鬼东西？ - 知乎](https://zhuanlan.zhihu.com/p/387109071)
