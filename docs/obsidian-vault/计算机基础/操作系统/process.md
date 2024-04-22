# 进程

## 基本状态

- 运行态（Running）：进程已经获得所需资源，并占有 CPU
- 就绪态（Ready）：进程已经获得所需资源，只等待 CPU
- 阻塞态（Blocked）：也叫等待态、挂起态、睡眠态等。进程在等待某个事件，比如等待 IO 完成，等待某个资源
- 新建态（New）
- 终止态（Exit）

``` mermaid
flowchart TD
    New(新建) -- 创建完成 --> Ready(就绪)
    Ready -- 选中 --> Running(运行)
    Blocked -- 等待结束 --> Ready
    Running -- 等待事件 --> Blocked(阻塞)
    Running -- 结束执行 --> Exit(终止)
    Running -- 时间片用完 --> Ready
```

### 七状态模型

