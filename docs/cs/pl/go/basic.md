# Go 基础

!!! abstract

    记录一下 Go 的基础用法。

    参考：

    - [A Tour of Go](https://go.dev/tour/list)

    拓展阅读：

    - 类型写在标识符后面的原因：[Go's Declaration Syntax](https://go.dev/blog/declaration-syntax)
    - 异常处理：[Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
    - 关于切片：[Go Slices: usage and internals](https://go.dev/blog/slices-intro)

## Go 的生日

2009-11-10 23:00:00 UTC.

这是 Go Playground 的时间固定为它的原因 :)。

## Packages, variables, and functions.

Go 程序由包组成。从 `main` 包开始执行。

``` go
// 声明包
package main

// 导入包
// import "fmt"
// import "math"

// 通常使用 factored import 来导入多个包
import (
	"fmt"
	"math"
)

// func add(x int, y int) int {
// 	return x + y
// }

func add(x, y int) int {
	return x + y
}

func swap(x, y string) (string, string) {
	return y, x
}

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(add(42, 13))
}
```

只有大写字母开头的标识符才会被导出。
