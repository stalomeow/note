# MSBuild cpp csharp

## MSVC utf8 问题

MSVC 是通过文件前面的 BOM 来识别 Unicode 编码的，如果没有 BOM 就使用 Windows 系统默认的编码方式。[^1] 如果使用没有 BOM 的 UTF-8 编码保存代码文件，编译时必须加上 `/utf-8` 参数。

[^1]: [/utf-8 (Set source and execution character sets to UTF-8) | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/utf-8-set-source-and-executable-character-sets-to-utf-8?view=msvc-170)
