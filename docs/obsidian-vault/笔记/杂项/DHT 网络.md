---
date: 2024-04-25T22:59:17
---

# DHT 网络

[[分布式哈希表|DHT]] 网络是一种去中心化的网络。

一个 BT 客户端连入网络以后，会充当一个节点，记录一部分文件的下载方式（不需要把它真的下载下来，就是记录一下文件的位置）。每个 BT 客户端只要知道 DHT 网络中的任意一个节点就可以加入到这个网络中。多个节点可以分摊压力，所以 DHT 网络的稳定性会比基于 [[Tracker 服务器]] 的中心化网络好。

## 相关文章

- [入门DHT协议理论篇 | 生活的自留地](https://l1905.github.io/p2p/dht/2021/04/23/dht01/)
- [BT网络中DHT和UPnp的解释（转） - EasonJim - 博客园](https://www.cnblogs.com/EasonJim/p/6607869.html)
- [聊聊分布式散列表（DHT）的原理 — — 以 Kademlia（Kad） 和 Chord 为例 | by 编程随想 | Medium](https://program-think.medium.com/%E8%81%8A%E8%81%8A%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%A3%E5%88%97%E8%A1%A8-dht-%E7%9A%84%E5%8E%9F%E7%90%86-%E4%BB%A5-kademlia-kad-%E5%92%8C-chord-%E4%B8%BA%E4%BE%8B-8e648d853288)
