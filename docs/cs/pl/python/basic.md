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
