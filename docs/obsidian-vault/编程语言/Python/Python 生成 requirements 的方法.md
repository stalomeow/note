---
slug: "240427165117"
date: 2024-04-27
---

# Python 生成 requirements 的方法

## `pip freeze`

最简单的方法，会把当前环境里**所有的包**都列出来，需要配合 [[Python 虚拟环境|虚拟环境]] 使用。

``` bash
pip freeze > requirements.txt
```

==这个方法会把非直接依赖的包（二级依赖、三级依赖、...）也列出来。==

## `pipreqs`

通过检查代码中的 `import` 语句来生成 requirements.txt，只列出项目的直接依赖。即使没有真的安装依赖包，它也能列出来。

- [GitHub 仓库](https://github.com/bndr/pipreqs)

==在生成完以后最好检查一下。== 如果用 `importlib` 或者其他阴间方法导入包，它认不出来，就不会把包列进依赖里。

### 安装

``` bash
pip install pipreqs
```

### 使用

```
Usage:
    pipreqs [options] [<path>]

Arguments:
    <path>                The path to the directory containing the application files for which a requirements file
                          should be generated (defaults to the current working directory)

Options:
    --use-local           Use ONLY local package info instead of querying PyPI
    --pypi-server <url>   Use custom PyPi server
    --proxy <url>         Use Proxy, parameter will be passed to requests library. You can also just set the
                          environments parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories, each separated by a comma
    --no-follow-links     Do not follow symbolic links in the project
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard output
    --force               Overwrite existing requirements.txt
    --diff <file>         Compare modules in requirements.txt to project imports
    --clean <file>        Clean up requirements.txt by removing modules that are not imported in project
    --mode <scheme>       Enables dynamic versioning with <compat>, <gt> or <non-pin> schemes
                          <compat> | e.g. Flask~=1.1.2
                          <gt>     | e.g. Flask>=1.1.2
                          <no-pin> | e.g. Flask
```

### 例子

``` bash
pipreqs ./proj --encoding=utf8 --force
```

- Windows 下为了避免编码问题，加上 `--encoding=utf8` 参数。
- 加上 `--force` 参数，覆盖之前的 requirements.txt。

执行完，就会生成 `./proj/requirements.txt`。

