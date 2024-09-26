---
slug: "240530193957"
date: 2024-05-30
---

# PEM 格式

Privacy-Enhanced Mail (PEM) 是存储、传输密钥、公开密钥证书和其他数据的文件格式的业界标准。

很多加密标准使用 [[ASN.1]] 定义数据结构，再用 DER 进行编码，但这样产生的是二进制数据，在电子邮件等系统中传输不方便，所以有了 PEM 格式。

## 格式

PEM 的基础格式如下

``` pem
-----BEGIN TYPE-----
base64 编码的二进制数据
-----END TYPE-----
```

第一行和最后一行分别是 header 和 footer。`TYPE` 表示数据的类型，常见的有 `CERTIFICATE`、`PRIVATE KEY` 等。中间的是用 base64 编码的二进制数据。PEM 没有规定二进制数据的用途，所以想放什么进去都行。

一个 PEM 文件中可以包含多段上面那样的数据块。

## 常见的数据类型

PEM 中常见的 `TYPE` 和对应的数据类型如下

| `TYPE`                  | 数据类型                                   |
| :---------------------- | -------------------------------------- |
| `RSA PRIVATE KEY`       | [[PKCS\|PKCS #1]] [[RSA 加密算法]] 私钥      |
| `RSA PUBLIC KEY`        | [[PKCS\|PKCS #1]] [[RSA 加密算法\|RSA]] 公钥 |
| `PRIVATE KEY`           | [[PKCS\|PKCS #8]] 私钥                   |
| `ENCRYPTED PRIVATE KEY` | [[PKCS\|PKCS #8]] 私钥（被加密过）             |
| `CERTIFICATE`           | [[X.509]] 证书                           |
| `PUBLIC KEY`            | [[X.509]] 主题公钥信息                       |
