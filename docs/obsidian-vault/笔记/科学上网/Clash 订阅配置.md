---
slug: "240611214630"
date: 2024-06-11
---

# Clash 订阅配置

Clash Meta 的文档：[虚空终端 Docs (metacubex.one)](https://wiki.metacubex.one/)。

## 规则集

有现成的可以用：[Loyalsoldier/clash-rules (github.com)](https://github.com/Loyalsoldier/clash-rules)。根据 README 上的教程复制粘贴即可。

## 托管配置文件

在不同设备间拷贝配置文件是很麻烦的，Clash 客户端可以从 URL 导入配置文件。所以可以自己搭一个服务器，再进阶一点可以顺便实现 [[Clash 客户端支持的 URL Scheme]]。

还有一个懒人方法，就是把配置文件放到 [GitHub Secret Gist](https://gist.github.com/) 里。[^1] Secret Gist 无法被搜索到，只能通过 URL 访问。URL 后面有非常长的随机字符串，几乎不可能被猜到。在 Clash 客户端导入配置文件时，给出源文件的 URL 即可。

[^1]: [打造自己的 Clash 配置并提供订阅 - 一只萌新 (yizhimengxin.me)](https://yizhimengxin.me/2022/10/27/%E6%89%93%E9%80%A0%E8%87%AA%E5%B7%B1%E7%9A%84Clash%E9%85%8D%E7%BD%AE%E5%B9%B6%E6%8F%90%E4%BE%9B%E8%AE%A2%E9%98%85/)
