---
date: 2023-06-24
draft: false
authors:
  - stalomeow
categories:
  - Python
---

# 卸载 Python

<del>从入门到卸载跑路。</del> 卸载的大致流程：

1. 卸载所有 pip 安装的 Package。
2. Windows 下卸载 Python 本体。

<!-- more -->

## 卸载所有 Package

先把安装的 Package 的列表导出到文件：

``` powershell
pip freeze>python_modules.txt
```

再一次性全部删除：

``` powershell
pip uninstall -r python_modules.txt -y
```

> -y 参数的意思是默认全部同意，这样就不用一直输入 y 了。

## 卸载 Python 本体（Windows）

需要对应版本的 Python 安装程序。运行后，点击 Uninstall。完成后，手动删除 Python 安装目录中剩余的文件。

[^1]: [如何快速卸载所有python包？ - 知乎](https://zhuanlan.zhihu.com/p/162698236)
[^2]: [python最详细的安装与完全卸载_python怎么卸载干净重新安装_无尽的沉默的博客-CSDN博客](https://blog.csdn.net/hgnuxc_1993/article/details/114675594)