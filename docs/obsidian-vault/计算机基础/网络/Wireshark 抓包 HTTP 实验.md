---
slug: "240617163636"
date: 2024-06-17
---

# Wireshark 抓包 HTTP 实验

计网作业。

## 过滤

现在网站基本都用 HTTPS，先[[Wireshark 解密 HTTPS|配置 Wireshark 解密 HTTPS]]，再设置过滤表达式 `http || http2 || http3 || tcp`，然后去浏览器打开 https://www.baidu.com 过一会再关闭。

回到 Wireshark，找到协议为 TLSv1.2 的 `Client Hello (SNI=www.baidu.com)`，得知目标的 ip 地址为 110.242.68.3。

更新过滤表达式为 `(http || http2 || http3 || tcp) && (ip.src == 110.242.68.3 || ip.dst == 110.242.68.3)`。


## 数据包分析


### 应用层


![[wireshark-exp-http-data.png|应用层]]

应用层使用 HTTP。

- 请求行，方法为 `GET`，URL 为 `/`，版本为 `HTTP/1.1`

    ``` txt
    GET / HTTP/1.1 
    ```

- 请求头

    ``` yaml
    Host: www.baidu.com 
    Connection: keep-alive 
    sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24" 
    sec-ch-ua-mobile: ?0 
    sec-ch-ua-platform: "Windows" 
    Upgrade-Insecure-Requests: 1 
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0 
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7 
    Sec-Fetch-Site: none 
    Sec-Fetch-Mode: navigate 
    Sec-Fetch-User: ?1 
    Sec-Fetch-Dest: document 
    Accept-Encoding: gzip, deflate, br, zstd 
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    Cookie: ...
    ```

- 空行
- 主体（这里没有）


### 传输层


![[wireshark-exp-tcp-data.png|传输层]]

传输层使用 TCP。

- 源始端口：`e9 88`（59784 端口）
- 目的端口：`01 bb`（443 端口）
- 序列号：`85 ad cd ce`（2242760142）
- 确认号：`df cc 85 0f`（3754722575）
- 偏移：`5`（头部长度为 5*4=20 字节）
- 保留：`0`
- 标志：`18`（ACK 和 PSH）
- 窗口大小：`02 03`（515）
- 校验和：`01 6d`
- 紧急指针：`00 00`


### 网络层


![[wireshark-exp-ip-data.png|网络层]]

网络层使用 IP。

- 版本：`4`（表示 IPv4）
- 头长：`5`（头部长度为 5*4=20 字节）
- 服务类型：`00`（默认）
- 包裹总长：`0000`（IP 数据包总长 0 字节，可能是 TSO 的原因）
- 重组标识：`cacf`（51919，发送主机赋予的标识，以便接收方进行分片重组）
- 标志（3 位）段偏移量（13 位）：`4000`（标志：不分片，段偏移量：0）
- 生存时间：`80`（128，每经过一个路由器，该值就减一，到零丢弃）
- 协议代码：`06`（表示 TCP 协议）
- 头校验和：`0000`（没开启校验）
- 源始地址：`0ac643ab`（10.198.67.171）
- 目的地址：`6ef24403`（110.242.68.3）


### 数据链路层


![[wireshark-exp-ethernet-data.png|数据链路层]]

数据链路层使用 Ethernet II。

- 目的 MAC 地址：`b0 76 1b 21 30 ab`（b0:76:1b:21:30:ab）
- 源始 MAC 地址：`54 6c eb b3 0b 05`（54:6c:eb:b3:0b:05）
- 类型：`08 00`（表示 IPv4）


## TCP 连接建立


![[wireshark-exp-tcp-conn.png|TCP 连接建立]]


1. 客户端（10.198.67.171）向百度（110.242.68.3）发送第一个段，SYN 被置位，序列号为 2242758111（相对值 0）。
2. 百度（110.242.68.3）向客户端（10.198.67.171）发送第二个段，SYN 和 ACK 被置位，序列号为 3754722416（相对值 0），确认号为 2242758112（相对值 1）。
3. 客户端（10.198.67.171）向百度（110.242.68.3）发送第三个段，ACK 被置位，序列号为 2242758112（相对值 1），确认号为 3754722417（相对值 1）。

经过三次握手，TCP 连接建立。


## TCP 连接终止


![[wireshark-exp-tcp-close.png|TCP 连接终止]]


1. 客户端（10.198.67.171）向百度（110.242.68.3）发送第一个段，FIN 和 ACK 被置位，序列号为 2242765910（相对值 7799），确认号为 3754841098（相对值 118682）。
2. 百度（110.242.68.3）向客户端（10.198.67.171）发送第二个段，ACK 被置位，序列号为 3754841098（相对值 118682），确认号为 2242765911（相对值 7800）。
3. 百度（110.242.68.3）向客户端（10.198.67.171）发送剩余的数据，图中为 TLS 的关闭通知。
4. 百度（110.242.68.3）向客户端（10.198.67.171）发送第三个段，FIN 和 ACK 被置位，序列号为 3754841129（相对值 118713），确认号为 2242765911（相对值 7800）。
5. 客户端（10.198.67.171）向百度（110.242.68.3）发送第四个段，ACK 被置位，序列号为 2242765911（相对值 7800），确认号为 3754841130（相对值 118714）。

经过四次握手，TCP 连接终止。


