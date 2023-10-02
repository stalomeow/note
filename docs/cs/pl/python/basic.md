# Python 基础

!!! abstract

    都是非常基础的东西。持续更新。

## @classmethod 和 @staticmethod

``` python
class A(object):
    # 实例方法，第一个参数 self 的值为当前的对象
    def m1(self, n):
        print("self:", self)

    # 类方法，第一个参数 cls 的值为当前的类
    @classmethod
    def m2(cls, n):
        print("cls:", cls)
        print(cls()) # 创建当前类的对象

    # 静态方法，没有特殊的参数
    @staticmethod
    def m3(n):
        pass
```

## int 和 bytes 相互转换

- `#!python int.to_bytes(self, length, byteorder, *, signed=False)`。
    - `length`: 字节数量。
    - `byteorder`: 字节序（`#!python 'little'` 或 `#!python 'big'`）。
    - `signed`: 是否为有符号整数。
    - 返回 `#!python bytes`。

- `#!python @classmethod int.from_bytes(cls, bytes, byteorder, *, signed=False)`。
    - `bytes`: 字节。
    - `byteorder`: 字节序（`#!python 'little'` 或 `#!python 'big'`）。
    - `signed`: 是否为有符号整数。
    - 返回 `#!python int`。

## 字符和 Unicode 码相互转换

- 字符转 Unicode：`#!python ord('a')`。
- Unicode 转字符：`#!python chr(97)`。

## 对象拷贝

导入内置模块 `copy`。

- 浅拷贝：`#!python y = copy.copy(x)`。
- 深拷贝：`#!python y = copy.deepcopy(x)`。

列表浅拷贝也可以用切片：`#!python y = x[::]`。

## 时间相关

=== "毫秒级时间戳"

    ``` python
    # Unix 时间戳（Unix epoch, Unix time, POSIX time 或 Unix timestamp）
    # 是从 1970 年 1 月 1 日（UTC/GMT 的午夜）开始所经过的秒数，不考虑闰秒。

    import time

    # 当前时间的毫秒级时间戳
    print(int(time.time() * 1000))
    ```

=== "时间差"

    ``` python
    from datetime import datetime

    time1 = datetime.now()
    time2 = datetime.now()

    # 打印时间差（毫秒）
    print((time2 - time1).total_seconds() * 1000)
    ```

## 遍历文件夹

``` python
import os

for root, dirs, files in os.walk(r'.', topdown=False):
    for name in dirs:
        print(os.path.join(root, name))

    for name in files:
        print(os.path.join(root, name))
```

- `root`: 当前文件夹的路径。
- `dirs`: 当前文件夹中的子文件夹列表（不包括子文件夹的子文件夹）。
- `files`: 当前文件夹中的文件列表。
- `topdown`: 如果为 `True`，则从上往下遍历，否则从下往上遍历。默认为 `True`。

## 在文件前面添加内容

=== "正确方式"

    ``` python
    with open(file, 'r+', encoding='utf8') as fp:
        text = fp.read()
        fp.seek(0)
        fp.write('foo\n' + text)
    ```

=== "常见错误"

    ``` python
    with open(file, 'r+', encoding='utf8') as fp:
        fp.seek(0)
        fp.write('foo\n') # 会把文件开头的部分覆盖掉！
    ```

## 守护线程 (Daemon Thread)

如果线程的 `#!python daemon=True`，那么它就是一个「守护线程」。守护线程不会阻止 Python 程序的退出，就像 C# 中的 Background Thread。

在创建线程时，如果不显式指定，`daemon` 的值默认是 `#!python None`，表示使用创建它的线程的 `daemon` 的值。

> 守护线程在程序关闭时会突然关闭。他们的资源（例如已经打开的文档，数据库事务等等）可能没有被正确释放。如果你想你的线程正常停止，设置他们成为非守护模式并且使用合适的信号机制，例如：[`Event`](https://docs.python.org/zh-cn/3/library/threading.html#threading.Event)。[^1]

一些语言中线程的分类：

- C#：Foreground Thread 和 Background Thread。
- Java：User Thread 和 Daemon Thread。
- Python: Non-Daemon Thread 和 Daemon Thread。

前一种在 Alive 的情况下会阻止程序退出，后一种不会。

## 装饰器

``` peg title="Parsing Expression Grammar (PEG)"
named_expression:
    | assignment_expression
    | expression !':='

# 装饰器
decorators: ('@' named_expression NEWLINE )+ 
```

从语法上看，`@` 后面几乎能跟各种表达式。表达式的结果最后会被调用。

??? example "示例，看完就会写各种装饰器了"

    === "装饰器写法"

        ``` python
        # 无参
        @test1
        def func1():
            pass

        # 无参
        @test2()
        def func2():
            pass

        # 有参
        @test3(...)
        def func3():
            pass

        # 少见的写法
        @A()+B()
        def func4():
            pass
        ```

    === "等价写法"

        ``` python
        # 无参
        def func1():
            pass
        func1 = test1(func1)

        # 无参
        def func2():
            pass
        func2 = test2()(func2)

        # 有参
        def func3():
            pass
        func3 = test3(...)(func3)

        # 少见的写法
        def func4():
            pass
        func4 = (A()+B())(func4)
        ```

[^1]: [threading --- 基于线程的并行 — Python 3.11.5 文档](https://docs.python.org/zh-cn/3/library/threading.html#thread-objects)
