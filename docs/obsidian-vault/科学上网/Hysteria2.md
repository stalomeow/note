---
slug: "240609201630"
date: 2024-06-09
---

# Hysteria2

Hysteria2 基于魔改的 QUIC 协议，旨在伪装成标准的 HTTP/3 流量，速度很快。如果 VPS 不是很好的话，建议用这个，延迟低很多。

文档：[Home - Hysteria 2](https://v2.hysteria.network/zh/)。

## 部署

先[[VPS 与机场选购指南|买 VPS]] 和域名，解析域名，然后用 [[OpenSSH]] 连接，使用官方的安装脚本

``` bash
bash <(curl -fsSL https://get.hy2.sh/)
```

修改配置文件

``` bash
nano /etc/hysteria/config.yaml
```

配置里指定用 acme 自动申请 HTTPS 证书。另外，建议把 HTTP/HTTPS 伪装都打开，即在配置文件里加上

``` yaml
masquerade:
  # ...
  listenHTTP: :80 
  listenHTTPS: :443 
  forceHTTPS: true
```

设置开机自启， 并立即启动服务

``` bash
systemctl enable --now hysteria-server.service
```

查询服务端日志

``` bash
journalctl --no-pager -e -u hysteria-server.service
```

如果看到 `server up and running` 的日志消息，并且没有错误，那就部署成功了。以后，修改配置文件后，需要用下面的命令重启服务

``` bash
systemctl restart hysteria-server.service
```


## 流量统计

个人使用的话，我认为没必要开这个功能。功能开太多，可能反而容易被 GFW 怀疑。

流量信息可以去 VPS 面板看。

## 防火墙

以 Ubuntu 为例，[[UFW 防火墙|UFW]] 只放行 22，80，443 端口，分别对应 SSH，HTTP 和 HTTPS 服务。

``` bash
sudo ufw enable
sudo ufw default deny
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw reload
```

## 客户端

客户端可以用 Clash。根据 Clash 文档里 Hysteria2 的部分写 [[Clash 订阅配置]]。


