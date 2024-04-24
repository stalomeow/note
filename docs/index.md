---
search:
  exclude: true
comments: true
---

# 欢迎~♪

!!! abstract ""

    <p style="font-size:1.2rem;text-align:center;font-weight:bold;">
    TECH OTAKUS<br>
    SAVE<br>
    THE WORLD
    </p>

我是西电 2022 级本科生，计科专业。本站内容分为下面几个部分：

- News：我用 RSS 订阅的博客的最新文章。
- Obsidian vault：我用 [Obsidian](https://obsidian.md/) 记录的所有笔记。

## 技术细节

网站使用 [MkDocs 框架](https://www.mkdocs.org/) + [Material 主题](https://squidfunk.github.io/mkdocs-material/) 制作，部署在 [Vercel](https://vercel.com/) 上。

按照我的习惯，对主题的样式做了一些定制。另外，我写了一些 [MkDocs Hooks](https://www.mkdocs.org/user-guide/configuration/#hooks) 实现了

1. 引入 [fancybox](https://fancyapps.com/fancybox/) 代替 [glightbox](https://biati-digital.github.io/glightbox/)，以获得更好的图片浏览体验。
2. RSS 阅读器。自动拉取已订阅博客的文章，排序后生成页面。配合 [GitHub Actions](https://docs.github.com/en/actions) 每天定时自动更新。
3. 集成 [Obsidian](https://obsidian.md/)。

    - 将 [Obsidian Flavored Markdown](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown) 转换为 MkDocs Markdown。
    - 为文章自动生成永久唯一的简短 url，例如 `/obsidian-vault/ecjd-acbd-cebf/`。

4. 在本地开发时自动关闭一些不必要的插件，减少页面生成耗时。

一些常用的命令组合写进了 Makefile 里，例如

- `make s`：启动本地服务。
- `make d`：快速提交代码到 GitHub。
- `make upgrade`：更新 `mkdocs-material` 的版本。

相关的代码可以在这个项目的 repo 里找到。

## 用 Obsidian 的原因

## 关于评论区

评论区大概只会在首页开启。

笔记经常会被移动、整理，导致它的 url 发生变化（甚至消失），这给维护评论区带来很高的成本。另一方面，我这个网站几乎没人访问，大多数人看了也不留评论，没什么必要开那么多评论区。

我更推荐直接去 [GitHub Discussions](https://github.com/stalomeow/note/discussions) 里留言。

## 勘误

如果发现错误，可以 <small>（二选一）</small>

- 去 [GitHub Discussions](https://github.com/stalomeow/note/discussions) 里留言。
- 点击笔记标题旁的铅笔图标，Fork GitHub 仓库后修改源文件，最后提交 PR。
