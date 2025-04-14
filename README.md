# Stalo's Note

个人笔记本 / 博客。

## 本地阅读

使用 [Obsidian](https://obsidian.md/) 打开 [docs/obsidian-vault](docs/obsidian-vault) 文件夹。需要字体：

- [LXGW WenKai / 霞鹜文楷](https://github.com/lxgw/LxgwWenKai)
- [Cascadia Mono](https://github.com/microsoft/cascadia-code)
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)

## 本地构建

使用 [MkDocs](https://github.com/mkdocs/mkdocs) 和 [Material](https://github.com/squidfunk/mkdocs-material) 构建网页。

- 创建 Python 虚拟环境并安装依赖

    ``` powershell
    py -3.12 -m venv env
    ./env/Scripts/activate
    pip install -r requirements.txt
    ```

- 更新依赖

    ``` powershell
    cmd/upgrade.ps1
    ```

- 使用 [TinyPNG](https://tinypng.com) 压缩图片，API Key 需要设置在环境变量 `TINYPNG_API_KEY`

    ``` powershell
    cmd/tiny.ps1
    ```

- MkDocs 的命令请看 [官方文档](https://www.mkdocs.org/user-guide/cli/)

## 部署

使用 [Vercel](https://vercel.com/) 部署网页。

|构建设置|值|
|:-|:-|
|Framework Preset|`Other`|
|Build Command|`sh ./scripts/vercel-build.sh`|
|Install Command|`sh ./scripts/vercel-install.sh`|

|环境变量|值|说明|
|:-|:-|:-|
|`CI`|`true`|启用一些 MkDocs 插件|
|`VERCEL_DEEP_CLONE`|`true`|RSS 插件建议使用者关闭 Git Shallow Clone，这样能获取到更准确的信息|
