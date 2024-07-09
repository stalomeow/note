---
slug: "240611151543"
date: 2024-06-11
---

# OpenSSH

OpenSSH（OpenBSD Secure Shell）是使用 SSH 透过计算机网络加密通信的实现。Windows 也内置了这个工具，[OpenSSH for Windows overview | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview)。

## 连接

``` powershell
ssh username@servername
```

第一次连接时，会提示

```
The authenticity of host 'servername (10.00.00.001)' can't be established. ECDSA key fingerprint is SHA256:(<a large string>). Are you sure you want to continue connecting (yes/no)?
```

输入 `yes` 后就会把它加到 `~/.ssh/known_hosts` 文件中。

## 保持连接

长时间不操作的话，连接会自动断开。可以用心跳包来保持连接，服务端和客户端一方设置就行。

### 服务端


参考：[保持 ssh 连接 | Notes (monsoir.github.io)](https://monsoir.github.io/Notes/Linux/keep-ssh-session-alive.html)。


### 客户端

在配置文件 `~/.ssh/config` 中加上

``` txt
TCPKeepAlive yes
ServerAliveInterval 300
ServerAliveCountMax 3
```

- 客户端根据 `TCPKeepAlive` 决定是否发送心跳包保持连接
- 客户端每隔 `ServerAliveInterval` 秒向服务器发送数据包，表示要保持连接
- 若服务端没有响应，则记录下没响应的次数，当次数超过 `ServerAliveCountMax` 后，断开连接

可以用下面这行命令来完成。

``` powershell
echo "TCPKeepAlive yes" "ServerAliveInterval 300" "ServerAliveCountMax 3" >> ~/.ssh/config
```


## 断开连接

有多种方法：

1. 直接关闭命令行
2. 使用 `logout` 或 `exit` 命令
3. 快捷键 Ctrl+D


