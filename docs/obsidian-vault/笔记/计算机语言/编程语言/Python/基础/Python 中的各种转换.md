---
slug: "240427171634"
date: 2024-04-27
---

# Python 中的各种转换

## int 和 bytes 相互转换

- `int.to_bytes(self, length, byteorder, *, signed=False)`。
    - `length`: 字节数量。
    - `byteorder`: 字节序（`'little'` 或 `'big'`）。
    - `signed`: 是否为有符号整数。
    - 返回 `bytes`。
- `@classmethod int.from_bytes(cls, bytes, byteorder, *, signed=False)`。
    - `bytes`: 字节。
    - `byteorder`: 字节序（`'little'` 或 `'big'`）。
    - `signed`: 是否为有符号整数。
    - 返回 `int`。

## 字符和 Unicode 码相互转换

- 字符转 Unicode：`ord('a')`。
- Unicode 转字符：`chr(97)`。
