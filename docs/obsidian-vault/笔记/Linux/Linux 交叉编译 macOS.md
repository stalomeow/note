---
date: 2024-11-26T20:08:12
---

# Linux 交叉编译 macOS

使用 [tpoechtrager/osxcross](https://github.com/tpoechtrager/osxcross) 实现。

## 安装

根据文档上的要求，安装基本工具。`python-is-python3` 是让 `python` 指向 `python3`。

``` bash
sudo apt update
sudo apt install clang cmake git patch python-is-python3 \
    libssl-dev lzma-dev libxml2-dev xz-utils \
    bzip2 cpio zlib1g-dev bash
```

clone `osxcross` 仓库。

``` bash
git clone https://github.com/tpoechtrager/osxcross.git
cd osxcross
```

## 打包 macOS SDK

根据 `osxcross` 文档上 PACKAGING THE SDK 的方法来做，挺麻烦的。可以直接用别人打包好的

- [joseluisq/macosx-sdks](https://github.com/joseluisq/macosx-sdks)
- [phracker/MacOSX-SDKs](https://github.com/phracker/MacOSX-SDKs)

我使用的是 `MacOSX15.1.sdk.tar.xz`，下载后放到 `osxcross/tarballs` 目录里。

## 构建

在 `osxcross` 目录执行

``` bash
./build.sh
```

构建成功后会生成 `target` 目录

``` bash
target/
├── bin
├── include
├── lib
├── libexec
├── SDK
├── share
└── toolchain.cmake
```

## 在 CMake 中使用

根据工具版本和目标架构设置环境变量。可以打开 `toolchain.cmake` 看这些环境变量是怎么被使用的。`OSXCROSS_SDK` 是 `target/SDK` 目录下的某个子目录名。

``` bash
export OSXCROSS_HOST=arm64-apple-darwin24.1
export OSXCROSS_TARGET_DIR=/home/stalo/workspace/osxcross/target
export OSXCROSS_TARGET=darwin24.1
export OSXCROSS_SDK=MacOSX15.1.sdk
```

使用 `cmake` 时指定 `toolchain.cmake`。

``` bash
-DCMAKE_TOOLCHAIN_FILE=/home/stalo/workspace/osxcross/target/toolchain.cmake
```

如果要从前面的 `arm64` 切到 `x86_64`，记得重新设置环境变量。

``` bash
export OSXCROSS_HOST=x86_64-apple-darwin24.1
```

最后，可以用 `lipo` 把两个架构的输出捆绑为一个。

``` bash
lipo -create arm64/mylib.dylib x86/mylib.dylib -output mylib.dylib
```

## 参考

- [如何在Linux下使用osxcross交叉编译Mac程序 | 我的个人知识库](https://www.wuliang142857.me/cpp/how-to-cross-compile-macos-app-in-linux.html)
