---
date: 2024-06-11T21:46:30
---

# Clash

参考 [虚空终端 Docs](https://wiki.metacubex.one/)。

## 规则集

- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)

## 托管配置文件

两种方法，推荐第二个。

1. Clash 客户端可以从 URL 导入配置文件，所以可以自己搭一个服务器。
2. 把配置文件放到 [GitHub Secret Gist](https://gist.github.com/) 里。[^1] Secret Gist 无法被搜索到，只能通过 URL 访问。URL 后面有非常长的随机字符串，几乎不可能被猜到。在 Clash 客户端导入配置文件时，给出源文件的 URL 即可。

## 客户端支持的 URL Scheme

在搭建自己的订阅服务器时，这些 URL Scheme 非常有用。规范参考 [Clash for Windows 的文档（Wayback Machine）](https://web.archive.org/web/20230930062020/https://docs.cfw.lbyczf.com/contents/urlscheme.html#%E4%B8%8B%E8%BD%BD%E9%85%8D%E7%BD%AE)，大多数 Clash 客户端都支持。

### 快速导入

``` txt
clash://install-config?url=<encoded URI>
```

### 响应头

指 Clash 客户端请求订阅链接后，服务器返回的 HTTP 响应头。

#### 配置文件名

如果响应头中存在 `content-disposition` 字段，则使用 `filename` 对应的值作为配置文件名。

``` yaml
content-disposition: attachment; filename="abc.yaml"
```

否则使用 URL 最后一部分作为配置文件名。

#### 配置文件自动更新间隔

如果响应头中存在 `profile-update-interval` 字段，则配置文件自动更新间隔设置为对应的值，以小时为单位。

``` yaml
profile-update-interval: 12
```

#### 用户订阅信息

如果响应头中存在 `subscription-userinfo` 字段，则其对应的流量及到期时间会显示在订阅信息中。

``` yaml
subscription-userinfo: upload=455727941; download=6174315083; total=1073741824000; expire=1671815872
```

| 参数         | 单位          | 描述          |
| :--------- | ----------- | ----------- |
| `upload`   | 字节          | 用户已上传的流量    |
| `download` | 字节          | 用户已下载的流量    |
| `total`    | 字节          | 用户本次订阅的总流量  |
| `expire`   | [[Unix 时间]] | 用户本次订阅的到期时间 |

所有参数都是可选的，用分号 `;` 隔开。

#### 门户首页

如果响应头中存在 `profile-web-page-url` 字段，则在 profile 右键菜单中会显示 `Open web page` 选项，允许用户跳转到对应的门户首页。

``` yaml
profile-web-page-url: https://example.com
```

[^1]: [打造自己的 Clash 配置并提供订阅 - 一只萌新 (yizhimengxin.me)](https://yizhimengxin.me/2022/10/27/%E6%89%93%E9%80%A0%E8%87%AA%E5%B7%B1%E7%9A%84Clash%E9%85%8D%E7%BD%AE%E5%B9%B6%E6%8F%90%E4%BE%9B%E8%AE%A2%E9%98%85/)
