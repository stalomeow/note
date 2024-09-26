---
slug: "240427173631"
date: 2024-04-27
---

# Python 守护线程

如果线程的 `daemon=True`，那么它就是一个「守护线程」。守护线程（Daemon Thread）不会阻止 Python 程序的退出，就像 C# 中的 Background Thread。

在创建线程时，如果不显式指定，`daemon` 的值默认是 `None`，表示使用创建它的线程的 `daemon` 的值。

> 守护线程在程序关闭时会突然关闭。他们的资源（例如已经打开的文档，数据库事务等等）可能没有被正确释放。如果你想你的线程正常停止，设置他们成为非守护模式并且使用合适的信号机制，例如：[`Event`](https://docs.python.org/zh-cn/3/library/threading.html#threading.Event)。[^1]

[^1]: [threading --- 基于线程的并行 — Python 3.11.5 文档](https://docs.python.org/zh-cn/3/library/threading.html#thread-objects)
