---
date: 2024-11-18T23:12:01
publish: true
comments: true
permalink: cpp-primer
aliases:
---

# C++ Primer

## 基本类型和变量

- 0 开头的整数是八进制
- word 是储存的基本单元
- 内置类型的变量不会被默认初始化，值是未知的
- 使用 `extern` 声明变量

    ``` cpp
    extern int i;     // 只是声明变量 i，没定义变量 i
    extern int i = 1; // 声明并定义变量 i
    int i;            // 声明并定义变量 i
    int i = 1;        // 声明并定义变量 i
    ```
