---
slug: "240425231313"
date: 2024-04-25
---

# Aria2

Aria2 是一个轻量级、多源、跨平台、命令行界面的下载器。支持的下载协议有 HTTP/HTTPS、FTP、SFTP、BitTorrent 和 Metalink。

- GitHub 仓库：[https://github.com/aria2/aria2](https://github.com/aria2/aria2)
- 文档：[https://aria2.github.io/manual/en/html/index.html](https://aria2.github.io/manual/en/html/index.html)

## 基本用法

如果只下一个文件，直接给 URI 就行。URI 可以是种子、磁链、HTTP 链接等。

``` bash
aria2c uri
```

多个下载任务的话，需要先把所有 URI 写进一个文件里。

``` bash
aria2c -i uris.txt
```

更多用法还是看文档吧。参数太多了。

## 配置文件

一些每次都要加的参数可以写在一个配置文件里。Aria2 默认会依次检查

1. `$HOME/.aria2/aria2.conf`
2. `$XDG_CONFIG_HOME/aria2/aria2.conf`

并读取第一个找到的文件。

可以用 `--conf-path=<PATH>` 参数来指定配置文件的路径。如果不需要读取配置文件，则使用 `--no-conf` 参数。

配置文件中每行写一个参数 `NAME=VALUE`。`#` 开头的是注释。只有两个横杠开头的长参数才可以在文件中被指定，但是在文件里写的时候要把参数名开头的两个横杠去掉。

### 配置文件模板

这是在网上找到的，用之前最好先检查一下。

``` ini
## '#'开头为注释内容, 选项都有相应的注释说明, 根据需要修改 ##
## 被注释的选项填写的是默认值, 建议在需要修改时再取消注释  ##

## 文件保存相关 ##

# 文件的保存路径(可使用绝对路径或相对路径), 默认: 当前启动位置
dir=~/downloads
# 启用磁盘缓存, 0为禁用缓存, 需1.16以上版本, 默认:16M
#disk-cache=32M
# 文件预分配方式, 能有效降低磁盘碎片, 默认:prealloc
# 预分配所需时间: none < falloc ? trunc < prealloc
# falloc和trunc则需要文件系统和内核支持
# NTFS建议使用falloc, EXT3/4建议trunc, MAC 下需要注释此项
#file-allocation=none
# 断点续传
continue=true

## 下载连接相关 ##

# 最大同时下载任务数, 运行时可修改, 默认:5
#max-concurrent-downloads=5
# 同一服务器连接数, 添加时可指定, 默认:1
max-connection-per-server=5
# 最小文件分片大小, 添加时可指定, 取值范围1M -1024M, 默认:20M
# 假定size=10M, 文件为20MiB 则使用两个来源下载; 文件为15MiB 则使用一个来源下载
min-split-size=10M
# 单个任务最大线程数, 添加时可指定, 默认:5
#split=5
# 整体下载速度限制, 运行时可修改, 默认:0
#max-overall-download-limit=0
# 单个任务下载速度限制, 默认:0
#max-download-limit=0
# 整体上传速度限制, 运行时可修改, 默认:0
#max-overall-upload-limit=0
# 单个任务上传速度限制, 默认:0
#max-upload-limit=0
# 禁用IPv6, 默认:false
#disable-ipv6=true
# 连接超时时间, 默认:60
#timeout=60
# 最大重试次数, 设置为0表示不限制重试次数, 默认:5
#max-tries=5
# 设置重试等待的秒数, 默认:0
#retry-wait=0

## 进度保存相关 ##

# 从会话文件中读取下载任务
input-file=/etc/aria2/aria2.session
# 在Aria2退出时保存`错误/未完成`的下载任务到会话文件
save-session=/etc/aria2/aria2.session
# 定时保存会话, 0为退出时才保存, 需1.16.1以上版本, 默认:0
#save-session-interval=60

## RPC相关设置 ##

# 启用RPC, 默认:false
enable-rpc=true
# 允许所有来源, 默认:false
rpc-allow-origin-all=true
# 允许非外部访问, 默认:false
rpc-listen-all=true
# 事件轮询方式, 取值:[epoll, kqueue, port, poll, select], 不同系统默认值不同
#event-poll=select
# RPC监听端口, 端口被占用时可以修改, 默认:6800
#rpc-listen-port=6800
# 设置的RPC授权令牌, v1.18.4新增功能, 取代 --rpc-user 和 --rpc-passwd 选项
#rpc-secret=<TOKEN>
# 设置的RPC访问用户名, 此选项新版已废弃, 建议改用 --rpc-secret 选项
#rpc-user=<USER>
# 设置的RPC访问密码, 此选项新版已废弃, 建议改用 --rpc-secret 选项
#rpc-passwd=<PASSWD>
# 是否启用 RPC 服务的 SSL/TLS 加密,
# 启用加密后 RPC 服务需要使用 https 或者 wss 协议连接
#rpc-secure=true
# 在 RPC 服务中启用 SSL/TLS 加密时的证书文件,
# 使用 PEM 格式时，您必须通过 --rpc-private-key 指定私钥
#rpc-certificate=/path/to/certificate.pem
# 在 RPC 服务中启用 SSL/TLS 加密时的私钥文件
#rpc-private-key=/path/to/certificate.key

## BT/PT下载相关 ##

# 当下载的是一个种子(以.torrent结尾)时, 自动开始BT任务, 默认:true
#follow-torrent=true
# BT监听端口, 当端口被屏蔽时使用, 默认:6881-6999
listen-port=51413
# 单个种子最大连接数, 默认:55
#bt-max-peers=55
# 打开DHT功能, PT需要禁用, 默认:true
enable-dht=false
# 打开IPv6 DHT功能, PT需要禁用
#enable-dht6=false
# DHT网络监听端口, 默认:6881-6999
#dht-listen-port=6881-6999
# 本地节点查找, PT需要禁用, 默认:false
#bt-enable-lpd=false
# 种子交换, PT需要禁用, 默认:true
enable-peer-exchange=false
# 每个种子限速, 对少种的PT很有用, 默认:50K
#bt-request-peer-speed-limit=50K
# 客户端伪装, PT需要
peer-id-prefix=-TR2770-
user-agent=Transmission/2.77
peer-agent=Transmission/2.77
# 当种子的分享率达到这个数时, 自动停止做种, 0为一直做种, 默认:1.0
seed-ratio=0
# 强制保存会话, 即使任务已经完成, 默认:false
# 较新的版本开启后会在任务完成后依然保留.aria2文件
#force-save=false
# BT校验相关, 默认:true
#bt-hash-check-seed=true
# 继续之前的BT任务时, 无需再次校验, 默认:false
bt-seed-unverified=true
# 保存磁力链接元数据为种子文件(.torrent文件), 默认:false
bt-save-metadata=true
```

## Web 控制台

Aria2 有一个网页控制台，网址是 [http://aria2c.com/](http://aria2c.com/)。用控制台之前需要先启动本地 Aria2 的 RPC。

``` bash
aria2c --enable-rpc=true --rpc-allow-origin-all=true --rpc-listen-all=true
```

然后就可以在网页上添加或查看下载任务。相当于有了个 GUI，还是比较方便的。

网上的不少 Aria2 的教程都是让我们写一个脚本，后台运行 Aria2 RPC，再配合某个网页控制台使用。

## 解决 BT 下载慢

不保证这些方法一定有效。

### 更新 Tracker 服务器

每天自动更新的 [[Tracker 服务器]] 列表：

- [https://github.com/ngosang/trackerslist](https://github.com/ngosang/trackerslist)
- [https://github.com/XIU2/TrackersListCollection](https://github.com/XIU2/TrackersListCollection)

复制以后，用 `--bt-tracker` 参数告诉 Aria2 就行，多个 tracker 之间用 1 个 `,` 分开。如果是写在配置文件里的话，记得要每天同步更新一下。

### 记录 DHT 网络节点

Aria2 用 `dht.dat` 来记录之前遇到过的 [[DHT 网络]] 节点。加上参数 `--enable-dht=true` 就能打开。IPv6 的话，用的文件是 `dht6.dat`，参数是 `--enable-dht6=true`。[^1] [^2]

[^1]: [解决Aria2 BT下载速度慢没速度的问题 | Senraの小窝](http://www.senra.me/solutions-to-aria2-bt-metalink-download-slowly/)
[^2]: [Aria2 无法下载磁力链接、BT种子和速度慢的解决方案 - P3TERX ZONE](https://p3terx.com/archives/solved-aria2-cant-download-magnetic-link-bt-seed-and-slow-speed.html)