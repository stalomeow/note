---
slug: "240427173740"
date: 2024-04-27
---

# Python 时间操作

## 毫秒级时间戳

[[Unix 时间]]

``` python
import time

# 当前时间的毫秒级时间戳
print(int(time.time() * 1000))
```

## 时间差

``` python
from datetime import datetime

time1 = datetime.now()
time2 = datetime.now()

# 打印时间差（毫秒）
print((time2 - time1).total_seconds() * 1000)
```
