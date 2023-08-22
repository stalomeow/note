# Aria2

!!! abstract

    Aria2 是一个轻量级、多源、跨平台、命令行界面的下载器。支持的下载协议有 HTTP/HTTPS、FTP、SFTP、BitTorrent 和 Metalink。

    - GitHub 仓库：[https://github.com/aria2/aria2](https://github.com/aria2/aria2){ target="_blank" }
    - 文档：[https://aria2.github.io/manual/en/html/index.html](https://aria2.github.io/manual/en/html/index.html){ target="_blank" }

    ---

    我这里就简单记一下 Aria2 相关的东西。内存不吃紧的话，还是用 [Motrix](https://github.com/agalwood/Motrix){ target="_blank" } 吧。Motrix 是基于 Aria2、Electron 和 Vue 开发的，用起来方便一点。

    下面有些内容对 Motrix 或者其他下载器也是适用的。

## 基本用法

如果只下一个文件，直接给 URI 就行。URI 可以是种子、磁链、HTTP 链接等。

``` bash
aria2c uri
```

多个下载任务的话，需要先把所有 URI 写进一个文件里。

``` bash
aria2c -i uris.txt
```

更多用法还是去看文档吧。参数太多了。

## 配置文件

一些每次都要加的参数可以写在一个配置文件里。Aria2 默认会依次检查

1. `$HOME/.aria2/aria2.conf`
2. `$XDG_CONFIG_HOME/aria2/aria2.conf`

并读取第一个找到的文件。

可以用 `--conf-path=<PATH>` 参数来指定配置文件的路径。如果不需要读取配置文件，则使用 `--no-conf` 参数。

配置文件中每行写一个参数 `NAME=VALUE`。`#` 开头的是注释。只有两个横杠开头的长参数才可以在文件中被指定，但是在文件里写的时候要把参数名开头的两个横杠去掉。

??? example "配置文件模板"

    这是在网上找到的，用之前最好自己先检查一下。

    ``` ini title="aria2.conf"
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

Aria2 有一个网页控制台，网址是 [http://aria2c.com/](http://aria2c.com/){ target="_blank" }。用控制台之前需要先启动本地 Aria2 的 RPC。

``` bash
aria2c --enable-rpc=true --rpc-allow-origin-all=true --rpc-listen-all=true
```

然后就可以在网页上添加或查看下载任务。相当于有了个 GUI，还是比较方便的。

网上的不少 Aria2 的教程都是让我们写一个脚本，后台运行 Aria2 RPC，再配合某个网页控制台使用。

## 解决 BT 下载慢

不保证这些方法一定有效。

### Tracker 服务器

> Tracker 服务器是帮助 BitTorrent 协议在节点与节点之间做连接的服务器。
> 
> BitTorrent 客户端下载一开始就要连接到 Tracker，从 Tracker 获得其他客户端 IP 地址后，才能连接到其他客户端下载。在传输过程中，也会一直与 Tracker 通信，上传自己的信息，获取其它客户端的信息。[^1]

每天自动更新的 Tracker 列表：

- [https://github.com/ngosang/trackerslist](https://github.com/ngosang/trackerslist){ target="_blank" }
- [https://github.com/XIU2/TrackersListCollection](https://github.com/XIU2/TrackersListCollection){ target="_blank" }

复制以后，用 `--bt-tracker` 参数告诉 Aria2 就行，多个 tracker 之间用 1 个 `,` 分开。如果是写在配置文件里的话，记得要每天同步更新一下。

### DHT 网络

DHT 的全称是 [Distributed Hash Table](https://en.wikipedia.org/wiki/Distributed_hash_table)，分布式哈希表。这种哈希表使用了 [Consistent hashing（一致性哈希）](https://en.wikipedia.org/wiki/Consistent_hashing) 技术。这个技术在分布式系统中很常用，通过将「存储节点」和「数据」都映射到一个首尾相连的哈希环上，减少结点数量变化时的数据迁移量。而普通的 Hash Table 在容量变化时需要 rehash，然后移动所有数据。

DHT 网络是一种去中心化的网络。每一个 BT 客户端连入网络以后，会充当一个节点，记录一部分文件的下载方式（不需要把它真的下载下来，就是记录一下文件的位置）。多个结点可以分摊压力，所以 DHT 网络的稳定性会比基于 Tracker 服务器的中心化网络好。

一些讲 DHT 网络的文章：

- [入门DHT协议理论篇 | 生活的自留地](https://l1905.github.io/p2p/dht/2021/04/23/dht01/){ target="_blank" }
- [BT网络中DHT和UPnp的解释（转） - EasonJim - 博客园](https://www.cnblogs.com/EasonJim/p/6607869.html){ target="_blank" }
- [聊聊分布式散列表（DHT）的原理 — — 以 Kademlia（Kad） 和 Chord 为例 | by 编程随想 | Medium](https://program-think.medium.com/%E8%81%8A%E8%81%8A%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%A3%E5%88%97%E8%A1%A8-dht-%E7%9A%84%E5%8E%9F%E7%90%86-%E4%BB%A5-kademlia-kad-%E5%92%8C-chord-%E4%B8%BA%E4%BE%8B-8e648d853288){ target="_blank" }

BT 客户端只要知道 DHT 网络中的任意一个结点就可以加入到这个网络中。Aria2 用 `dht.dat` 来记录之前遇到过的结点。加上参数 `--enable-dht=true` 就能打开。IPv6 的话，用的文件是 `dht6.dat`，参数是 `--enable-dht6=true`。[^2] [^3]

## 百度网盘直链下载

安装 [油猴脚本](https://github.com/syhyz1990/baiduyun){ target="_blank" } 或者 [这里也可以装](https://www.youxiaohou.com/zh-cn/){ target="_blank" }。油猴也叫篡改猴 Tampermonkey，是一个浏览器插件。目前最好用红色的油猴，也就是 Beta 版。

推荐用 Motrix + RPC 下载。记得要修改 RPC 参数！默认是下载以后保存到 D 盘根目录，如果没有 D 盘就会一直报错。

[^1]: [BitTorrent tracker - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/BitTorrent_tracker)
[^2]: [解决Aria2 BT下载速度慢没速度的问题 | Senraの小窝](http://www.senra.me/solutions-to-aria2-bt-metalink-download-slowly/)
[^3]: [Aria2 无法下载磁力链接、BT种子和速度慢的解决方案 - P3TERX ZONE](https://p3terx.com/archives/solved-aria2-cant-download-magnetic-link-bt-seed-and-slow-speed.html)