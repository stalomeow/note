---
date: 2024-04-27T16:58:19
publish: true
comments: true
permalink: cleanly-uninstall-python-on-windows
aliases:
---

# Windows 下干净地卸载 Python

大致流程：

1. 卸载所有 pip 安装的 Package。
2. Windows 下卸载 Python 本体。

## 卸载所有 Package

先把全局安装的 Package 列表导出到文件，使用 [[Python 生成 requirements 的方法#`pip freeze`|pip freeze]]：

``` bash
pip freeze>python_modules.txt
```

全部删除：

``` bash
pip uninstall -r python_modules.txt -y
```

> -y 参数的意思是默认全部同意，这样就不用一直输入 y 了。

## 卸载 Python 本体

需要对应版本的 Python 安装程序。运行后，点击 Uninstall。完成后，手动删除 Python 安装目录中剩余的文件。

## 参考

- [如何快速卸载所有python包？ - 知乎](https://zhuanlan.zhihu.com/p/162698236)
- [python最详细的安装与完全卸载_python怎么卸载干净重新安装_无尽的沉默的博客-CSDN博客](https://blog.csdn.net/hgnuxc_1993/article/details/114675594)
