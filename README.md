# Stalo's Wiki

个人笔记本

## 本地阅读

使用 [Obsidian](https://obsidian.md/) 打开 [docs/obsidian-vault](docs/obsidian-vault) 文件夹

需要字体：

- [LXGW WenKai / 霞鹜文楷](https://github.com/lxgw/LxgwWenKai)
- [Cascadia Mono](https://github.com/microsoft/cascadia-code)
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)

可选：将 [TinyPNG](https://tinypng.com) 的 API Key 设置在环境变量 `TINYPNG_API_KEY`

## 本地构建

创建 Python 虚拟环境并安装依赖

``` powershell
py -3.12 -m venv env
./env/Scripts/activate
pip install -r requirements.txt
```

使用 [MkDocs](https://github.com/mkdocs/mkdocs) 和 [Material](https://github.com/squidfunk/mkdocs-material) 构建网页，请看 [官方文档](https://www.mkdocs.org/user-guide/cli/)

## 部署

使用 [Vercel](https://vercel.com/) 部署网页

|构建设置|值|
|:-|:-|
|Framework Preset|`Other`|
|Build Command|`sh ./scripts/vercel-build.sh`|
|Install Command|`sh ./scripts/vercel-install.sh`|
