# Stalo's Note

基于 [Obsidian](https://obsidian.md/)，使用 [MkDocs](https://github.com/mkdocs/mkdocs) 和 [Material](https://github.com/squidfunk/mkdocs-material) 主题构建的个人笔记本 & 博客。

## 本地阅读 & 编辑

``` bash
git clone https://github.com/stalomeow/note.git
```

使用 Obsidian 打开 [docs/obsidian-vault](docs/obsidian-vault) 文件夹。需要字体：

- [LXGW WenKai / 霞鹜文楷](https://github.com/lxgw/LxgwWenKai)
- [Cascadia Mono](https://github.com/microsoft/cascadia-code)
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)

## 命令行工具 (Windows)

要求有 GNU Make、Python launcher 和 Python 3.12。

|功能|命令|简写|
|:-|:-|:-|
|显示帮助信息|`make help`|`make h`|
|启动本地服务|`make serve`|`make s`|
|提交到远程仓库|`make deploy`|`make d`|
|更新 `mkdocs-material` 的版本|`make upgrade`||
|压缩图片|`make tiny`||
|打开 Visual Studio Code|`make code`||
|打开 File Explorer|`make explorer`||
|安装依赖|`make install`||

- 第一次使用时，需要用 `make install` 安装依赖。
- 使用 [TinyPNG](https://tinypng.com) 压缩图片，API Key 需要设置在环境变量 `TINYPNG_API_KEY`。
- 在 Obsidian 中，使用 `Shell commands: Execute: Make` 快捷命令即可。

## Vercel

部署前端网页。

|构建设置|值|
|:-|:-|
|Framework Preset|`Other`|
|Build Command|`sh ./scripts/vercel-build.sh`|
|Install Command|`sh ./scripts/vercel-install.sh`|

|环境变量|值|说明|
|:-|:-|:-|
|`CI`|`true`|启用一些 mkdocs 插件|
|`VERCEL_DEEP_CLONE`|`true`|RSS 插件建议使用者关闭 git shallow clone，这样能获取到更准确的信息|
