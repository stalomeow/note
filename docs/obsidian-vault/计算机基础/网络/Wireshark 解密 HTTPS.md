---
slug: "240617164714"
date: 2024-06-17
---

# Wireshark 解密 HTTPS


HTTPS 用了 TLS 做加密，需要解密后才能看到原始的 HTTP 报文。

Chrome 和 Firefox 浏览器提供了记录 TLS 密钥的功能。添加环境变量 `SSLKEYLOGFILE`，值为一个文件路径。彻底重启浏览器（任务管理器里检查），TLS 密钥相关的信息就会被保存到这个文件中。

在 Wireshark 中，点击编辑 > 首选项，找到 Protocols > TLS 中的 (Pre)-Master-Secret log filename 填入之前的文件路径就能解密 HTTPS 了。


