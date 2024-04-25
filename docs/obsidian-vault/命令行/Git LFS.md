---
slug: "240425232518"
date: 2024-04-25
---

# Git LFS

Git Large File Storage (LFS) 是 Git 的一个扩展。它可以将较大的二进制文件替换为较小的文本文件，然后把真实文件的内容保存在其他地方。

1. [下载](https://git-lfs.com/) 并安装 Git LFS。然后，运行下面的命令来为账号初始化：

    ``` bash
    git lfs install
    ```

    每个账号只需要运行一次。

2. 在 Git 仓库中运行下面的命令（或者直接编辑 .gitattributes），添加需要 Git LFS 管理的文件类型：

    ``` bash
    git lfs track "*.psd"
    ```

    接下来，要保证 .gitattributes 被追踪:

    ``` bash
    git add .gitattributes
    ```

    在任何时候都可以运行上面的命令，指定新的文件类型。然而，这个命令不会把之前匹配的文件转换到 Git LFS 中，比如其他分支里的文件，或者之前提交历史里的文件。

    如果还要转换之前的文件，需要使用 `git lfs migrate` 命令，并指定好参数。

现在，只要像以前一样使用 Git 就行了！例如，当前的分支是 `main`：

``` bash
git add file.psd
git commit -m "Add design file"
git push origin main
```

