---
date: 2024-11-04T14:51:19
publish: true
comments: true
permalink: python-basics
aliases:
---

# Python 基础

## 对象拷贝

导入内置模块 `copy`。

- 浅拷贝：`y = copy.copy(x)`。
- 深拷贝：`y = copy.deepcopy(x)`。

列表浅拷贝也可以用切片：`y = x[::]`。

## 实例方法、类方法、静态方法

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

## 守护线程

如果线程的 `daemon=True`，那么它就是一个「守护线程」。守护线程（Daemon Thread）不会阻止 Python 程序的退出，就像 C# 中的 Background Thread。

在创建线程时，如果不显式指定，`daemon` 的值默认是 `None`，表示使用创建它的线程的 `daemon` 的值。

> 守护线程在程序关闭时会突然关闭。他们的资源（例如已经打开的文档，数据库事务等等）可能没有被正确释放。如果你想你的线程正常停止，设置他们成为非守护模式并且使用合适的信号机制，例如：[`Event`](https://docs.python.org/zh-cn/3/library/threading.html#threading.Event)。[^1]

## 在文件前面添加内容

``` python
with open(file, 'r+', encoding='utf8') as fp:
    text = fp.read()
    fp.seek(0)
    fp.write('foo\n' + text)
```

### 常见错误

``` python
with open(file, 'r+', encoding='utf8') as fp:
    fp.seek(0)
    fp.write('foo\n') # 会把文件开头的部分覆盖掉！
```

## 装饰器

装饰器的 Parsing Expression Grammar (PEG)：

``` peg
named_expression:
    | assignment_expression
    | expression !':='

# 装饰器
decorators: ('@' named_expression NEWLINE )+
```

从语法上看，`@` 后面 ==几乎能跟各种表达式==。表达式的结果最后会被调用。

### 示例

#### 装饰器写法

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

#### 等价写法

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

### 使用 `functools.wraps()`

使用 `functools.wraps()` 可以保留被装饰函数的信息。

``` python
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print('Calling decorated function')
        return f(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')
```

- `example.__name__`: `'example'`。
- `example.__doc__`: `'Docstring'`。

不用 `functools.wraps()` 的话，

- `example.__name__`: `'wrapper'`。
- `example.__doc__`: `''`。

这篇文章深入地介绍了原理：[Python functools.wraps 深入理解 - 知乎](https://zhuanlan.zhihu.com/p/45535784)。

[^1]: [threading --- 基于线程的并行 — Python 3.11.5 文档](https://docs.python.org/zh-cn/3/library/threading.html#thread-objects)
