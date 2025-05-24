---
date: 2025-05-24T17:06:21
aliases: 
slug: hysteria2-trojan-proxy
draft: false
comments: true
---

# Hysteria2 + Trojan 科学上网

Hysteria2 基于魔改的 QUIC 协议，伪装成标准的 HTTP/3 流量，速度比较快，但它本质上是 UDP 流量，容易被运营商或校园网针对。Trojan 是 TCP + TLS，伪装成普通的 HTTPS 流量，速度相对慢一点，但是更稳定。

我是自己买 VPS 搭的梯子，之前只使用 Hysteria2。最近校园网限制 UDP 流量，导致我一天只有几分钟能连上梯子，就算开端口跳跃或者换 IP 地址也没用。于是，我在原来的基础上又部署了 Trojan 作为 Fallback 方案。

<!-- more -->

## 服务端

我使用的是一台美国的 VPS，系统是 Ubuntu 22.04.1 LTS，每月 4TB 流量，一年 16.88 美元。

### 部署 Hysteria2

使用官方的安装脚本

``` bash
bash <(curl -fsSL https://get.hy2.sh/)
```

修改配置文件

``` bash
vim /etc/hysteria/config.yaml
```

重点：

- 把 443 端口留给 Trojan，让 Hysteria2 监听其他端口，我使用 27015
- 用 ACME 自动申请 TLS 证书
- 在 80 和 27015 启动 HTTP/HTTPS 服务，不要开启 `forceHTTPS`，后面 Trojan 要反向代理 80 端口的 HTTP 服务，如果开启 `forceHTTPS` 则每次都会重定向到 27015 端口

``` yaml
listen: :27015

acme:
  domains:
    - 域名
  email: 邮箱

auth:
  type: userpass
  userpass:
    用户名: 密码

masquerade:
  type: proxy
  proxy:
    url: 反向代理的网站
    rewriteHost: true
  listenHTTP: :80
  listenHTTPS: :27015
  forceHTTPS: false
```

设置开机自启，并立即启动服务

``` bash
systemctl enable --now hysteria-server
```

查询服务状态，检查是否成功启动

``` bash
systemctl status hysteria-server
```

查询服务日志

``` bash
journalctl --no-pager -e -u hysteria-server
```

修改配置文件后，需要用下面的命令重启服务

``` bash
systemctl restart hysteria-server
```

### 部署 Trojan

下载并解压最新的 Trojan-Go

``` bash
mkdir ~/trojan-go && cd ~/trojan-go
wget https://github.com/p4gefau1t/trojan-go/releases/download/v0.10.6/trojan-go-linux-amd64.zip
unzip trojan-go-linux-amd64.zip && rm trojan-go-linux-amd64.zip
```

编写配置文件

``` bash
vim server.json
```

重点：

- 监听 443 端口，HTTP 服务使用 Hysteria2 的 `127.0.0.1:80`
- TLS 证书使用 Hysteria2 申请的，一般在 `/var/lib/hysteria/acme/certificates` 目录里，或者用 `find / -type d -name "acme"` 命令找一下
- TLS 握手失败后，把请求转发到 Hysteria2 的 HTTPS 服务 `127.0.0.1:27015` 上，伪装成正常的 HTTPS 服务

``` json
{
    "run_type": "server",
    "local_addr": "0.0.0.0",
    "local_port": 443,
    "remote_addr": "127.0.0.1",
    "remote_port": 80,
    "password": [
        "密码"
    ],
    "ssl": {
        "cert": "/var/lib/hysteria/acme/certificates/acme-v02.api.letsencrypt.org-directory/域名/域名.crt",
        "key": "/var/lib/hysteria/acme/certificates/acme-v02.api.letsencrypt.org-directory/域名/域名.key",
        "fallback_addr": "127.0.0.1",
        "fallback_port": 27015
    }
}
```

制作一个 service

``` bash
vim /etc/systemd/system/trojan-go.service
```

粘贴下面的内容，需要修改 `ExecStart` 中的路径

``` ini
[Unit]
Description=Trojan-Go - An unidentifiable mechanism that helps you bypass GFW
Documentation=https://github.com/p4gefau1t/trojan-go
After=network.target nss-lookup.target
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStart=/path/to/trojan-go/trojan-go -config /path/to/trojan-go/server.json
Restart=on-failure
RestartSec=10
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
```

设置开机自启，并立即启动服务

``` bash
systemctl enable --now trojan-go
```

查询服务状态，检查是否成功启动

``` bash
systemctl status trojan-go
```

查询服务日志

``` bash
journalctl --no-pager -e -u trojan-go
```

修改配置文件后，需要用下面的命令重启服务

``` bash
systemctl restart trojan-go
```

### 使用 BBR 拥塞控制算法

检查当前的 TCP 拥塞控制算法，默认是 Cubic

``` bash
sysctl net.ipv4.tcp_congestion_control
```

Linux 4.9 及以上的内核内置了 BBR 算法，可以用下面的命令开启

``` bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```

然而我这里 BBR 不如 Cubic 快，所以要测试一下，不能无脑换。

### 防火墙

只放行 22，80，443，27015 端口，分别对应 SSH，HTTP，HTTPS（Trojan）和 HTTPS（Hysteria2）

``` bash
ufw enable
ufw default deny
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 27015
ufw reload
```

## Clash 配置

配置文件可以放到 [GitHub Secret Gist](https://gist.github.com/) 里。[^1] 它无法被搜索到，只能通过 URL 访问。URL 后面有非常长的随机字符串，几乎不可能被猜到。

在 Clash 客户端导入配置文件时，给出源文件的 URL 即可。修改 Gist 的文件后，需要在 Clash 客户端更新 URL。

### 代理组

使用 Fallback 模式，当 Hysteria2 无法使用时改用 Trojan，每隔 300 秒检查一次

``` yaml
proxies:
  - name: "US 27015"
    type: hysteria2
    server: 域名
    port: 27015
    password: "用户名:密码"
    sni: 域名
    skip-cert-verify: false
  - name: "US 443"
    type: trojan
    server: 域名
    port: 443
    password: "密码"
    udp: true
    sni: 域名
    skip-cert-verify: false

proxy-groups:
  - name: PROXY
    type: fallback
    proxies:
      - "US 27015"
      - "US 443"
    interval: 300
    lazy: true
```

### 规则集

在 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 的基础上，按需添加下面的规则

- 将 `dcg.microsoft.com` 设置为直连，避免 Windows 11 的手机连接提示「无法连接到你的 Android 设备，因为你正在尝试访问中国以外的应用程序，目前我们不支持漫游区域」[^2]

    ``` yaml
    rules:
      - DOMAIN,dcg.microsoft.com,DIRECT
    ```

- Google Analytics 的 API 必须直连

    ``` yaml
    rules:
      - DOMAIN,www.googletagmanager.com,DIRECT
      - DOMAIN,www.google-analytics.com,DIRECT
    ```

- 把梯子的 IP 也设置为直连，这样挂着梯子也能 SSH

## 参考

- [虚空终端 Docs](https://wiki.metacubex.one/)
- [Home - Hysteria 2](https://v2.hysteria.network/zh/)
- [简介 - Trojan-Go Docs](https://p4gefau1t.github.io/trojan-go/)
- [保姆級 Trojan-Go 與「誰在講幹話」入門搭建 | jkgtw's blog ](https://www.jkg.tw/p3360/)

[^1]: [打造自己的 Clash 配置并提供订阅 - 一只萌新](https://yizhimengxin.me/2022/10/27/%E6%89%93%E9%80%A0%E8%87%AA%E5%B7%B1%E7%9A%84Clash%E9%85%8D%E7%BD%AE%E5%B9%B6%E6%8F%90%E4%BE%9B%E8%AE%A2%E9%98%85/)
[^2]: [Windows的“手机连接”显示无法连接你的设备，你正尝试访问中国以外的应用，不支持漫游区域怎么解决？ - 知乎](https://www.zhihu.com/question/570222831)
