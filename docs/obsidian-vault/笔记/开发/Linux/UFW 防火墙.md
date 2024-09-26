---
slug: "240612002527"
date: 2024-06-12
---

# UFW 防火墙

Ubuntu 默认安装了 UFW (Uncomplicated Firewall) 防火墙。

## 基本使用

``` bash
sudo ufw status          # 查看状态
sudo ufw enable          # 启用防火墙
sudo ufw default deny    # 默认全部拒绝
sudo ufw allow 22        # 放行 22 端口
sudo ufw delete allow 22 # 关闭 22 端口
sudo ufw reload          # 重启防火墙
```
