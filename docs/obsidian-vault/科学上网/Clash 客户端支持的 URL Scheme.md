---
slug: "240610215435"
date: 2024-06-10
---

# Clash 客户端支持的 URL Scheme

在搭建自己的订阅服务器时，这些 URL Scheme 非常有用。规范参考 [Clash for Windows 的文档（Wayback Machine）](https://web.archive.org/web/20230930062020/https://docs.cfw.lbyczf.com/contents/urlscheme.html#%E4%B8%8B%E8%BD%BD%E9%85%8D%E7%BD%AE)，大多数 Clash 客户端都支持。


## 快速导入


``` txt
clash://install-config?url=<encoded URI>
```



## 响应头

指 Clash 客户端请求订阅链接后，服务器返回的 HTTP 响应头。

### 配置文件名

如果响应头中存在 `content-disposition` 字段，则使用 `filename` 对应的值作为配置文件名。

``` yaml
content-disposition: attachment; filename="abc.yaml"
```

否则使用 URL 最后一部分作为配置文件名。


### 配置文件自动更新间隔

如果响应头中存在 `profile-update-interval` 字段，则配置文件自动更新间隔设置为对应的值，以小时为单位。

``` yaml
profile-update-interval: 12
```


### 用户订阅信息

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

### 门户首页

如果响应头中存在 `profile-web-page-url` 字段，则在 profile 右键菜单中会显示 `Open web page` 选项，允许用户跳转到对应的门户首页。

``` yaml
profile-web-page-url: https://example.com
```



