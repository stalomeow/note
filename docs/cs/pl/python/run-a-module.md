# 执行一个模块

!!! abstract

    用 Python 直接执行一个模块。

## 命令

``` powershell
python -m module-name
```

`module-name` 就是模块的名称（没有 `.py` 扩展名），也可以是包名，比如 `pip`。如果是包的话，会执行包里的 `__main__` 模块。

## 和直接执行文件的区别

主要是 `sys.path` 不同。Python 按照 `sys.path` 中的路径顺序来搜索程序中 import 的模块和包。

直接执行文件 `python script.py`，会将脚本文件所在的目录添加到 `sys.path`。

执行一个模块 `python -m module`，会将当前执行命令的路径添加到 `sys.path`。

## 应用

``` title="包的目录结构"
package1/
	|-- __init__.py
	|-- mod1.py
package2/
	|-- __init__.py
	|-- run.py
```

假设，在 `run.py` 中 import 了 `mod1.py`。

直接执行 `python run.py` 是不行的，会提示找不到 `package1`。

在 `package2` 所在的目录执行 `python -m package2.run` 是可以的。

## `__init__.py` 和 `__main__.py`

``` title="包的目录结构"
pkg/
    |-- __init__.py
    |-- __main__.py
```

### 直接执行文件夹

``` powershell
python pkg
```

只有 `__main__.py` 被执行。

- `#!python __name__`：`#!python '__main__'`。
- `#!python __package__`：`#!python ''`。
- `#!python sys.argv[0]`：`#!python 'pkg'`。
- `__main__.py` 所在的目录（`pkg` 文件夹的路径）被加进 `#!python sys.path`。

### 模块方式执行

``` powershell
python -m pkg
```

先执行 `__init__.py`，再执行 `__main__.py`。

- `__init__.py`：
    - `#!python __name__`：`#!python 'pkg'`。
    - `#!python __package__`：`#!python 'pkg'`。
    - `#!python sys.argv[0]`：`#!python '-m'`。
- `__main__.py`：
    - `#!python __name__`：`#!python '__main__'`。
    - `#!python __package__`：`#!python 'pkg'`。
    - `#!python sys.argv[0]`：`__main__.py` 文件的路径。
- 执行命令时的路径被加进 `#!python sys.path`。


[^1]: [python -m 和 python 直接运行的区别 - Joseph_Chuh - 博客园](https://www.cnblogs.com/josephchuh/p/9209695.html#:~:text=%3E%3E%3E%20python%20xxx.py%20%23%20%E7%9B%B4%E6%8E%A5%E8%BF%90%E8%A1%8C%20%3E%3E%3E%20python%20-m,%E7%9B%B8%E5%BD%93%E4%BA%8Eimport%EF%BC%8C%E5%8F%AB%E5%81%9A%E5%BD%93%E5%81%9A%E6%A8%A1%E5%9D%97%E6%9D%A5%E5%90%AF%E5%8A%A8%20%E4%B8%BB%E8%A6%81%E5%8C%BA%E5%88%AB%E5%9C%A8%E4%BA%8E%20sys.path%20%E4%B8%8D%E5%90%8C%20%E7%9B%B4%E6%8E%A5%E8%BF%90%E8%A1%8C%E4%BC%9A%E5%B0%86%E8%AF%A5%E8%84%9A%E6%9C%AC%E6%89%80%E5%9C%A8%E7%9B%AE%E5%BD%95%E6%B7%BB%E5%8A%A0%E8%87%B3%20sys.path%20%E5%BD%93%E5%81%9A%E6%A8%A1%E5%9D%97%E5%90%AF%E5%8A%A8%E5%88%99%E4%BC%9A%E5%B0%86%E5%BD%93%E5%89%8D%E8%BF%90%E8%A1%8C%E5%91%BD%E4%BB%A4%E7%9A%84%E8%B7%AF%E5%BE%84%E6%B7%BB%E5%8A%A0%E8%87%B3%20sys.path)
[^2]: [Python入门之——Package内的__main__.py和__init__.py 51CTO博客](https://blog.51cto.com/feishujun/5513660)
[^3]: [1. 命令行与环境 — Python 3.11.4 文档](https://docs.python.org/zh-cn/3/using/cmdline.html#cmdoption-m)
