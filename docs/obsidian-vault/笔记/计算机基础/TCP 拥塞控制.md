---
slug: "240612000944"
date: 2024-06-12
---

# TCP 拥塞控制

## BBR 算法

这个视频简单提到了 BBR 的原理。

<div class="responsive-video-container">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Azj8-1rdF-o?si=NvNuThLlf3UZyhJz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

Linux 中检查当前的 TCP 拥塞控制算法

``` bash
sysctl net.ipv4.tcp_congestion_control
```

Linux 4.9 及以上的内核内置了 BBR 算法。开启方法：用 root 账户执行下面的命令

``` bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```
