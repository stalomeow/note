# Python 基础

!!! abstract

    都是非常基础的东西。持续更新。

## 字符和 Unicode 码相互转换

- 字符转 Unicode：`#!python ord('a')`。
- Unicode 转字符：`#!python chr(97)`。

## 对象拷贝

用内置模块 `copy`。

- 浅拷贝：`#!python y = copy.copy(x)`。
- 深拷贝：`#!python y = copy.deepcopy(x)`。

列表浅拷贝也可以用切片：`#!python y = x[::]`。

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
