---
date: 2024-01-26T02:03:22
draft: false
authors:
  - stalomeow
categories:
  - Game Back-end
---

# 游戏注册、登录和鉴权

很多游戏公司都会搞一个通行证，官网、旗下所有游戏都用它登录。为了泛用性，这部分用的是 https 协议。我尝试用 golang + [gin 框架](https://github.com/gin-gonic/gin) + [MongoDB](https://www.mongodb.com/zh-cn) 搞了个类似的服务，包括注册、登录和鉴权。然后，用 C# 写了一套 SDK，方便在 Unity 里用。

<!-- more -->

## 前端大致流程

``` mermaid
flowchart TD
    A[尝试自动登录] -->|Old Token| B{后端}
    B -->|成功，返回 New Token| C[登录成功]
    B -->|失败| D[登录/注册]
    D -->|账号密码| B
```

登录成功后，每次请求 API 都带上 Token，后端会做鉴权。

## 密码传输与保存

很多人都是所有账号用一个密码，如果一个地方密码明文泄露了，黑客拿去撞库的话，一大堆账号都没了。只要明文不泄露，出意外的时候，损失就能仅仅控制在当前的站点。

传输密码的时候，用的是 https 协议，一般情况下已经足够安全了。Google 在传输密码时就没额外做加密。百度是自己又做了一次 RSA。还有些网站是前端 hash 一次，把结果作为用户的密码传给后端，不使用密码明文。

我用的是类似百度的方案。服务器启动时，会生成 RSA 密钥 + 公钥。公钥是公开的，前端直接请求后端 API 就能拿到。密码用公钥加密后传给后端，后端用密钥解密。

在 Unity 里，C# 的部分 RSA 相关方法是不能用的，会报 `PlatformNotSupportedException`，原因不明。推荐用开源的 Bouncy Castle 来实现加密：

- [Bouncy Castle 官网](https://www.bouncycastle.org/csharp/)
- [Bouncy Castle GitHub 镜像](https://github.com/bcgit/bc-csharp)

保存密码时，不能用可逆加密，更不能直接存明文。[2011 年中国网站用户信息泄露事件](https://zh.wikipedia.org/wiki/2011%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%BD%91%E7%AB%99%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%E4%BA%8B%E4%BB%B6) 中 CSDN 就因此泄露了大量密码。

现在一般都是给密码加盐（salt）再 hash，然后存进数据库。加盐就是给密码加上一个**长长长长的随机字符串，每个用户都不一样**。这样相当于提高了密码强度，而且相同密码的不同用户的 hash 值是不一样的。黑客就很难再建立彩虹表（Rainbow table）逆向 hash。

golang 内置了 [bcrypt 算法](https://pkg.go.dev/golang.org/x/crypto/bcrypt)，用起来很方便。

## Token 生成与管理

每次请求需要鉴权的 API 时都带上账号密码很麻烦，一般会用 Token 代替。为了安全，Token 是有过期时间的，每次登录时会刷新时间。常用 JSON Web Token，[阮一峰的博客](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html) 里讲得很清楚。

JWT 的缺点是它只保存在前端，后端不能随意废弃某一个 JWT。如果对安全性要求很高，可以自己生成 uuid 作为 Token，然后存在数据库里。还可以把用户的登录设备、IP 和 Token 关联起来，存进数据库，实现将某设备踢下线的功能。

## gin 中间件鉴权 

TODO
