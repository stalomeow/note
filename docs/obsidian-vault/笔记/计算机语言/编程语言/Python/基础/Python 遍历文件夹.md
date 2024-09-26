---
slug: "240427173827"
date: 2024-04-27
---

# Python 遍历文件夹

``` python
import os

for root, dirs, files in os.walk(r'.', topdown=False):
    for name in dirs:
        print(os.path.join(root, name))

    for name in files:
        print(os.path.join(root, name))
```

- `root`: 当前文件夹的路径。
- `dirs`: 当前文件夹中的子文件夹列表（不包括子文件夹的子文件夹）。
- `files`: 当前文件夹中的文件列表。
- `topdown`: 如果为 `True`，则从上往下遍历，否则从下往上遍历。默认为 `True`。
