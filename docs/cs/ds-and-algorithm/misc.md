# 杂项

!!! abstract

    需要注意的一些细节。

## 两个整数的平均值

为了避免溢出，使用下面的方法：

- 向下取整：`#!cpp (hight - low) / 2 + low`。
- 向上取整：`#!cpp (hight - low + 1) / 2 + low`。

## 递归三要素

1. **确定递归函数的参数和返回值：** 确定哪些参数是递归的过程中需要处理的，那么就在递归函数里加上这个参数，并且还要明确每次递归的返回值是什么进而确定递归函数的返回类型。
2. **确定终止条件：** 写完了递归算法, 运行的时候，经常会遇到栈溢出的错误，就是没写终止条件或者终止条件写的不对，操作系统也是用一个栈的结构来保存每一层递归的信息，如果递归没有终止，操作系统的内存栈必然就会溢出。
3. **确定单层递归的逻辑：** 确定每一层递归需要处理的信息。在这里也就会重复调用自己来实现递归的过程。