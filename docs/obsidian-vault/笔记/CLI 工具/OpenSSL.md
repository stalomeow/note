---
slug: "240526125629"
date: 2024-05-26
---

# OpenSSL

在计算机网络上，OpenSSL 是一个开放源代码的软件函式库包，应用程序可以使用这个包来进行安全通信，避免窃听，同时确认另一端连线者的身份。这个包广泛被应用在互联网的网页服务器上。

## 生成 RSA 私钥

文档：[/docs/man3.3/man1/genrsa.html (openssl.org)](https://www.openssl.org/docs/man3.3/man1/genrsa.html)

3.0 及以上版本的 OpenSSL 生成的 [[RSA 加密算法|RSA]] 私钥默认使用 [[PKCS|PKCS #8]] 和 [[PEM 格式]]。如果需要 [[PKCS|PKCS #1]] 的话，必须加上 `-traditional` 参数。

``` powershell
openssl genrsa -out priv1.pem 4096
openssl genrsa -traditional -out priv2.pem 4096
```

上面两条命令都会生成 4096 位的 RSA 私钥，前者使用 PKCS #8 后者使用 PKCS #1 。

## 导出 RSA 公钥

文档：[/docs/man3.3/man1/openssl-rsa.html](https://www.openssl.org/docs/man3.3/man1/openssl-rsa.html)

导出 RSA 公钥时

- 使用参数 `-pubout` 导出的 [[PEM 格式#常见的数据类型|PEM TYPE]] 是 `PUBLIC KEY`
- 使用参数 `-RSAPublicKey_out` 导出的 [[PEM 格式#常见的数据类型|PEM TYPE]] 是 `RSA PUBLIC KEY`

``` powershell
openssl rsa -in priv.pem -pubout -out pub1.pem
openssl rsa -in priv.pem -RSAPublicKey_out -out pub2.pem
```
