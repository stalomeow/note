---
date: 2024-09-29
slug: "240929141530"
---

# ANSI 字符集

ANSI 字符集，也叫 ANSI code pages、Windows code pages。[^1]

## 历史

在 Unicode 还没被广泛应用时，不同国家和地区有自己的一套字符集和编码方式，例如 ASCII、GB2312、Shift JIS 等。为了将 Windows 全球化，微软搞出了 Code pages。它会根据当前电脑系统的 Active code page 选择具体的字符集和编码，不同国家和地区的 Active code page 通常不一样。

在命令行输入 `chcp` 可以查看当前的 Active code page，简体中文是 936，对应 `ANSI/OEM Simplified Chinese (PRC, Singapore); Chinese Simplified (GB2312)`。[^2] 换句话说，在简体中文的电脑里，ANSI 相当于 GB2312。

## 问题

如果两台电脑的 Active code page 不一样，那么它们的 ANSI 底层使用的字符集和编码是不同的，用一台电脑打开另一台电脑上的 ANSI 文件就可能会乱码。

## 替代方案

Unicode 不会出现上面的问题，所以建议使用 Unicode 替代 ANSI。Windows 上的 Unicode 默认指 UTF-16 编码，不是 Unicode 字符集。采用 Unicode 字符集相关编码保存文件时，必须加上 BOM，否则系统读取文件时会当 ANSI 处理。

可以使用 WinAPI 中的 [`MultiByteToWideChar`](https://learn.microsoft.com/en-us/windows/win32/api/stringapiset/nf-stringapiset-multibytetowidechar) 和 [`WideCharToMultiByte`](https://learn.microsoft.com/en-us/windows/win32/api/stringapiset/nf-stringapiset-widechartomultibyte) 实现 UTF-16 与 ANSI/UTF-8 的相互转换。

[^1]: [Code Pages - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/intl/code-pages)
[^2]: [Code Page Identifiers - Win32 apps | Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/Intl/code-page-identifiers)
