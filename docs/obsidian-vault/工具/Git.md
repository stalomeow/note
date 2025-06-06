---
date: 2024-04-25T23:19:39
publish: true
comments: true
permalink: git
aliases:
---

# Git

## 配置

设置 Commit 时的用户名：

``` bash
git config --global user.name "[name]"
```

设置 Commit 时的邮箱：

``` bash
git config --global user.email "[email address]"
```

启用有帮助的彩色命令行输出：

``` bash
git config --global color.ui auto
```

## gitattribute

> 模板：[gitattributes/gitattributes](https://github.com/gitattributes/gitattributes)

修改 `.gitattribute` 和 `.gitignore` 后，记得取消跟踪所有文件，再重新 `git add .` 应用新配置。方法在后文有提到。

### Line endings

- [cross platform - What's the strategy for handling CRLF (carriage return, line feed) with Git?](https://stackoverflow.com/questions/170961/whats-the-strategy-for-handling-crlf-carriage-return-line-feed-with-git)
- [Configuring Git to handle line endings](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)

使用 `git` 的 `autocrlf` 功能处理 line endings，但最好不要依赖全局的 `core.autocrlf` 配置，而是在 `.gitattribute` 里指定。不同用户的全局配置不同，而 `.gitattribute` 中的配置会覆盖全局的 `core.autocrlf`，避免意外的错误。

``` bash
# Set the default behavior, in case people don't have core.autocrlf set.
# Auto detect text files and perform LF normalization
*        text=auto
```

还可以对一些特殊文件使用固定的 line endings。

``` bash
# Declare files that will always have CRLF line endings on checkout.
*.sln text eol=crlf
```

### Linguist

> 文档：[linguist/docs/overrides.md](https://github.com/github-linguist/linguist/blob/main/docs/overrides.md)

在 `.gitattributes` 文件中配置仓库的语言统计，例如显式指定文件使用的编程语言、将文件标记为 `generated` 等。

``` bash
# Example of a `.gitattributes` file which reclassifies `.rb` files as Java:
*.rb linguist-language=Java

# Use the `linguist-generated` attribute to mark or unmark paths as generated.
Api.elm linguist-generated
```

## 分支

### 创建

> [Branch from a previous commit using Git - Stack Overflow](https://stackoverflow.com/questions/2816715/branch-from-a-previous-commit-using-git)

用 commit hash 创建分支：

``` bash
git branch branch_name <commit-hash>
```

用符号引用（symbolic reference）创建分支：

``` bash
git branch branch_name HEAD~3
```

创建分支并切换：

``` bash
git checkout -b branch_name <commit-hash or HEAD~3>
```

### 推送

将分支推送到远程：

``` bash
git push origin local_branch_name:remote_branch_name
```

本地关联远程分支（这样 push 或 pull 时不需要再指定分支）：

``` bash
git branch --set-upstream-to=origin/remote_branch_name local_branch_name
```

将本地分支推送到远程，同时本地关联远程分支（本地和远程的分支都叫 branch_name）：

``` bash
git push -u origin branch_name
```

### 删除

> 删除本地分支前，先切到其他分支。

删除本地分支，如果分支没被合并则不允许删除：

``` bash
git branch -d branch_name
```

强制删除本地分支，不管是否被合并：

``` bash
git branch -D branch_name
```

删除远程分支：

``` bash
git push origin -d branch_name
```

推送空分支到远程，也能删除远程分支：

``` bash
git push origin :branch_name
```

删除远程分支后，更新本地分支列表（`-p` 即 `--prune`）：

``` bash
git fetch -p
```

### 重命名

重命名本地分支：

``` bash
git branch -m old_name new_name
```

## HEAD 引用

HEAD 文件通常是一个符号引用（symbolic reference），指向目前所在的分支。 所谓符号引用，表示它是一个指向其他引用的指针。

> [git HEAD / HEAD^ / HEAD~ 的含义 - 个人文章 - SegmentFault 思否](https://segmentfault.com/a/1190000022506884)

- HEAD 指向当前所在分支提交至仓库的最新一次的 commit。
- `~` 是用来在当前提交路径上回溯的修饰符。

    HEAD~{n} 表示当前所在的提交路径上的前 n 个提交（n >= 0）：

    - `HEAD = HEAD~0`
    - `HEAD~ = HEAD~1`
    - `HEAD~~ = HEAD~2`
- `^` 是用来切换**父级**提交路径的修饰符。

    当我们始终在一个分支比如 dev 开发/提交代码时，每个 commit 都只会有一个父级提交，就是上一次提交，但当并行多个分支开发，feat1, feat2, feat3，完成后 merge feat1 feat2 feat3 回 dev 分支后，此次的 merge commit 就会有多个父级提交。

    ``` python
    # 当前提交
    HEAD = HEAD~0 = HEAD^0

    # 主线回溯
    HEAD~1 = HEAD^   # 主线的上一次提交
    HEAD~2 = HEAD^^  # 主线的上二次提交
    HEAD~3 = HEAD^^^ # 主线的上三次提交

    # 如果某个节点有其他分支并入
    HEAD^1   # 主线提交（第一个父提交）
    HEAD^2   # 切换到了第2个并入的分支并得到最近一次的提交
    HEAD^2~3 # 切换到了第2个并入的分支并得到最近第 4 次的提交
    HEAD^3~2 # 切换到了第3个并入的分支并得到最近第 3 次的提交

    # ^{n} 和 ^ 重复 n 次的区别 
    HEAD~1 = HEAD^
    HEAD~2 = HEAD^^
    HEAD~3 = HEAD^^^

    # 切换父级
    HEAD^1~3 = HEAD~4 
    HEAD^2~3 = HEAD^2^^^
    HEAD^3~3 = HEAD^3^^^
    ```

### Windows CMD 中的坑

在 Windows CMD 中，`^` 是转义符。输入单个 `^` 的话，命令行就会在下一行问 `More?` 让你继续输入需要转义的内容。`^^` 才会被识别为 `^`。

要想让 git 正确识别 `HEAD^`，需要输入 `HEAD^^` 或者用双引号包裹 `"HEAD^"`。换 powershell、git bash 也行。

## 路径大小写不敏感

> [解决 Git 不区分大小写导致的文件冲突问题 - 千古壹号 - 博客园 (cnblogs.com)](https://www.cnblogs.com/qianguyihao/p/15906060.html)

Git 默认不区分路径大小写，[[不同操作系统的文件路径规则|类似 Windows]]。比如把 `Test` 改名为 `test` 是没用的，Git 认为没有发生变化。

可以设置

``` bash
git config core.ignorecase false
```

让 Git 区分大小写，但是不推荐，我遇到过问题：执行这条命令后，把 `Test` 改名为 `test` 再提交，远程仓库里同时存在 `Test` 和 `test`，但是本地仓库里只有 `test`。

上面的问题只能用最朴素的办法来解决：

1. 把 `Test` 改名为 `Test1`
2. 提交
3. 把 `Test1` 改名为 `test`
4. 提交

## Sync Fork

> [How to sync your fork with the original repository](https://ljvmiranda921.github.io/notebook/2021/11/12/sync-your-fork/)

直接在 GitHub 上点 `Sync Fork` 有可能产生一个新的 Commit，污染提交记录。下面用 Rebase 来同步，保证干净的提交记录。

1. 添加原来的远程库，可以起名为 `fork`：

    ``` bash
    git remote add fork https://github.com/com/original/original.git
    ```

2. 拉取原来的远程库的信息：

    ``` bash
    git fetch fork
    ```

3. 切到需要同步的本地分支，然后 rebase：

    ``` bash
    git checkout branch_name
    git rebase fork/main
    ```

4. 强制推送至云端：

    ``` bash
    git push origin +branch_name
    ```

    `+` 是强制推送的意思，也可以用下面的方法：

    ``` bash
    git push -f origin branch_name
    ```

## Squash Merge

将多个提交合并成一个，然后 Merge，需要自己再写一个 Commit：

``` bash
git merge --squash another_branch
git commit -m "message here"
```

## 合并冲突

首先，把 VS Code 设置成 Merge 和 Diff 的工具，方便我们使用。在 pwsh 中输入下面的命令。[^1] 在 pwsh 中 `$` 是变量的前缀，需要使用单引号避免字符串中 `$REMOTE` 等被解析成变量。

``` powershell
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
```

当合并发生冲突时，输入下面的命令启动 VS Code 解决冲突

``` powershell
git mergetool
```

解决冲突后，默认会把带有冲突标记的原始文件保存到扩展名为 `.orig` 的文件中。可以通过设置关闭这个功能 [^2]

``` powershell
git config --global mergetool.keepBackup false
```

然后，继续完成合并

``` powershell
git merge --continue
```

如果要取消合并，可以输入

``` powershell
git merge --abort
```

## 删除中间几个 Commit

使用交互式 Rebase 来删除中间的 Commit：

``` bash
git rebase -i <commit-hash>
```

这行命令会先在编辑器中打开一个文件，在文件中可以给不想要的 Commit 标记上 drop，然后保存关闭文件。之后 git 会执行 Rebase，删掉标记了 drop 的 Commit。

## 取消跟踪所有文件

在不删除文件的条件下，取消跟踪所有文件。之后可以重新 `git add .`。

``` bash
git rm -r --cached .
```

## Pull

`git pull` 是 `git fetch` + `git merge`。

## 撤销

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?aid=559048463&bvid=BV1ne4y1S7S9&cid=861329934&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
</div>

## 常用工作流

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?aid=561005338&bvid=BV19e4y1q7JJ&cid=846391446&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
</div>

## LFS

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

[^1]: [How to use Visual Studio Code as the default editor for Git MergeTool including for 3-way merge - Stack Overflow](https://stackoverflow.com/questions/44549733/how-to-use-visual-studio-code-as-the-default-editor-for-git-mergetool-including)
[^2]: [version control - Git mergetool generates unwanted .orig files - Stack Overflow](https://stackoverflow.com/questions/1251681/git-mergetool-generates-unwanted-orig-files)
