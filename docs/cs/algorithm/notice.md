# 注意事项

!!! abstract

    需要注意的一些细节。

## 两个整数的平均值

为了避免溢出，使用下面的方法：

- 向下取整：`#!cpp (hight - low) / 2 + low`。
- 向上取整：`#!cpp (hight - low + 1) / 2 + low`。
