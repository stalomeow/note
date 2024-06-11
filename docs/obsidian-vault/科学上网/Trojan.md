---
slug: "240609201625"
date: 2024-06-09
---

# Trojan

Trojan 是将通信流量伪装成 HTTPS 流量来避开 GFW 的协议。

- C++ 实现：[trojan-gfw/trojan](https://github.com/trojan-gfw/trojan)
- Go 实现：[p4gefau1t/trojan-go](https://github.com/p4gefau1t/trojan-go)

## 原理

trojan-go 的文档里写得很详细：[Trojan基本原理 - Trojan-Go Docs (p4gefau1t.github.io)](https://p4gefau1t.github.io/trojan-go/basic/trojan/)。

## 部署

用我 fork 的 [stalomeow/trojan](https://github.com/stalomeow/trojan) 一键部署，支持 C++ 和 Go 两种 trojan。原版有一些小 bug，我给修了。

先[[VPS 与机场选购指南|买 VPS]] 和域名，解析域名，然后用 [[OpenSSH]] 连接，执行下面的命令

``` bash
source <(curl -sL https://raw.githubusercontent.com/stalomeow/trojan/master/install.sh)
```

根据提示就能完成安装。之后，可以使用 `trojan` 命令进行管理。

浏览器访问域名，可以看到 web 管理后台，能一键导入 Clash 客户端。这个后台的密码是在第一次访问时设置的，所以部署完成后，一定要访问一次！

如果用户名中存在分号，之后生成订阅配置文件时，分号前的内容作为文件名，分号后的内容作为代理名。没有分号的话，文件名就是用户名，代理名是 `域名:端口号`。

## BBR 加速

把 TCP 拥塞控制算法[[TCP 拥塞控制#BBR 算法|改成 BBR]] 来加速。

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

