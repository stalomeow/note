---
date: 2024-05-30T13:21:56
publish: true
comments: true
permalink: asn1
aliases:
---

# ASN.1

Abstract Syntax Notation One (ASN.1) 是一个标准的接口描述语言（IDL），用于定义平台无关的数据结构（类似 Protobuf）。它被广泛使用在电信、计算机网络、密码学领域中。

用 ASN.1 定义的数据结构与具体的硬件或编程语言是无关的，换句话说就是跨平台、跨语言。有需要时，ASN.1 编译器可以帮你生成具体编程语言实现的代码。

## 语法示例

下面的代码定义了一个 `FooProtocol` [^1]

``` asn1
FooProtocol DEFINITIONS ::= BEGIN

    FooQuestion ::= SEQUENCE {
        trackingNumber INTEGER,
        question       IA5String
    }

    FooAnswer ::= SEQUENCE {
        questionNumber INTEGER,
        answer         BOOLEAN
    }

END
```

## 编码

比如，要通过网络发送下面这条消息（它符合上面的 `FooProtocol`）

``` asn1
myQuestion FooQuestion ::= {
    trackingNumber     5,
    question           "Anybody there?"
}
```

必须要先把它编码成字节流。ASN.1 提供了很多种编码规则，其中标准的有：

| 名称       | 英文                                 |
| :------- | ---------------------------------- |
| 基本编码规则   | Basic Encoding Rules (BER)         |
| 规范编码规则   | Canonical Encoding Rules (CER)     |
| 唯一编码规则   | Distinguished Encoding Rules (DER) |
| 压缩编码规则   | Packed Encoding Rules (PER)        |
| XML 编码规则 | XML Encoding Rules (XER)           |

例如，上面的消息用 XER 编码后是（108 字节）

``` xml
<FooQuestion>
    <trackingNumber>5</trackingNumber>
    <question>Anybody there?</question>
</FooQuestion>
```

用 DER 编码后是（21 字节）

```
30 13 02 01 05 16 0e 41 6e 79 62 6f 64 79 20 74 68 65 72 65 3f
```

> DER 使用 `type length value` 的模式将数据编码为字节序列。

`FooProtocol` 的制定者应该提前明确好具体的编码规则，不然其他人不知道该用哪个。

[^1]: [ASN.1 - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/ASN.1)
