---
slug: "240427172643"
date: 2024-04-27
---

# Python 装饰器

装饰器的 Parsing Expression Grammar (PEG)：

``` peg
named_expression:
    | assignment_expression
    | expression !':='

# 装饰器
decorators: ('@' named_expression NEWLINE )+
```

从语法上看，`@` 后面 ==几乎能跟各种表达式==。表达式的结果最后会被调用。

## 示例

### 装饰器写法

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

### 等价写法

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

## 使用 `functools.wraps()`

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

