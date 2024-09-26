---
slug: "240612012412"
date: 2024-06-12
---

# Go ldflags

- `-w` 去掉调试信息
- `-s` 去掉符号表
- `-X` 注入变量，编译时赋值

前两个一般一起用，可以减小构建后文件的大小。最后一个可以用来注入构建日期，工具链版本信息等。例如

``` bash
GoVersion=$(shell go version)
BuildTime=$(shell date "+%F %T")

go build -ldflags "-w -s \
-X 'github.com/pubgo/xxx/version.GoVersion=${GoVersion}' \
-X 'github.com/pubgo/xxx/version.BuildTime=${BuildTime}'"
```
