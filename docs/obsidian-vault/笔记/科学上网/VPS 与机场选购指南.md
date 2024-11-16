---
date: 2024-06-11T00:11:00
---

# VPS 与机场选购指南

买之前一定要根据自己的需求做好调研，别被坑。

## 资源

这些网站会提供较新的资讯，还有各个商家的促销活动。建议先去这些网站看看。

- [P3TERX ZONE](https://p3terx.com/)
- [jcnf的导航站 | 只谈实用不谈技术 (ybfl.net)](https://ybfl.net/)
- [我爱白嫖 | 52BP](https://52bp.org/index.html)

## VPS 商家

- [Mass VPS hosting on Enterprise equipment - BandwagonHost VPS (bwh89.net)](https://bwh89.net/)
- [DMIT - High Performance VM in DMIT.IO Cloud Infrastructure Services](https://www.dmit.io/)
- [SSD VPS Servers, Cloud Servers and Cloud Hosting - Vultr.com](https://www.vultr.com/)
- [RackNerd - Introducing Infrastructure Stability](https://www.racknerd.com/)
- [狗云 - 高性价比的云服务器 (dogyun.com)](https://www.dogyun.com/)

## VPN 商家

- [Gatern](https://shuttle.gt-all.com/)，这家 IP 非常干净，速度也不错
- [大哥云](https://www.dageyun.net/)

## VPS 线路选择

<div class="responsive-video-container">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/x6B5JEwXSEg?si=3RbF_rTjo1hTmvcr" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## VPS IP 选择

先检查 [[网络工具#IP 可用性|IP 可用性]]，要是已经被墙了就直接换。对速度有要求的话，做一下 [[网络工具#Ping|Ping 测试]] 和 [[网络工具#跟踪路由|路由跟踪]]。

像 ChatGPT、Netflix 这类网站审查比较严格，如果要使用他们的服务，需要干净的 IP 地址，可以按下面的方法挑选。

### IP 分类

只是为了选 VPS 方便才这样分类，实际上并不专业，有时也有歧义。

#### 原生 IP

原生 IP 简单说就是当地的 IP，是由当地互联网服务提供商（ISP）提供的本地 IP 地址，即纯本土归属地。反之就是广播 IP，IP 地址与机房所在地不一致的 IP 地址。原生 IP 价格相对较高。

因为 IPv4 数量不多，不能每个国家随便用，所以就有一个专门的机构去分配记录这些 IP。有些国家有很多分配的 IP 用不着，而有些国家早就用完了，那么就把一些已分配的闲置 IP 通过广播技术给需要的国家使用，这样的 IP 就是非原生的 IP。[^1]

#### 住宅 IP

住宅 IP 是互联网服务提供商（ISP）分配给家庭用户的 IP 地址。这些 IP 地址通常用于家庭网络中的个人设备，如计算机、智能手机、平板电脑等。

住宅 IP 看起来更像是普通用户，所以它们通常被认为更可靠和可信，但是价格贵。

#### 数据中心 IP

这些 IP 地址通常由托管在数据中心的服务器使用，不像住宅 IP 那样由家庭用户使用。

网站和服务通常可以很容易地识别出数据中心 IP，并可能将其标记为潜在的爬虫或自动化工具来源。但是它们更容易获取且数量庞大，价格也便宜。

### 选择建议

在 [Hurricane Electric BGP Toolkit (he.net)](https://bgp.he.net/) 网站中搜索需要查询的 IP，然后点击 `Whois` 选项卡，可以看到详细的 IP 分配信息。看不懂的话，可以丢给 GPT 翻译一下。

IP 初始被分配到哪个国家，就是谁的原生 IP。之后，IP 可能还会经历多次重分配。建议：

1. 重分配太多次的 IP 就算了。
2. 如果一个 IP 最后落到一个国家手里，但是却在另一个国家被使用，一般都被当成 VPN 处理，不要选。比如，我之前买过一个香港 VPS，它的 IP 是美国原生 IP，之后重分配给新加坡的一个组织，这个组织在香港机房使用这个 IP，ChatGPT 就把它当 VPN 处理。
3. 如果有钱的话，尽量选原生 IP（机房在 IP 的初始分配国家中）和住宅 IP（其他的容易跳人机验证）。
4. 检查 [[网络工具#IP 伪装度|IP 伪装度]]。

接下来就是看运气了，要是这个 IP 以前的主人干了什么坏事被拉黑，那也没办法。不过，加钱能解决一切问题，越贵用的人越少。

网上有不少流媒体检测脚本，也可以用它们检测一下。

[^1]: [具体什么是原生IP节点？我们该如何识别 原生节点 ？ - TikTok, Netflix, ChatGPT... (tiktokrobinhood.com)](https://tiktokrobinhood.com/%e5%85%b7%e4%bd%93%e4%bb%80%e4%b9%88%e6%98%af%e5%8e%9f%e7%94%9fip%e8%8a%82%e7%82%b9%ef%bc%9f%e6%88%91%e4%bb%ac%e8%af%a5%e5%a6%82%e4%bd%95%e8%af%86%e5%88%ab%ef%bc%9f/)
