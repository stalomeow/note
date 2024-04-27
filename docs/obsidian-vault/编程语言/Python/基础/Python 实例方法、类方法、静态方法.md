---
slug: "240427173522"
date: 2024-04-27
---

# Python 实例方法、类方法、静态方法


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