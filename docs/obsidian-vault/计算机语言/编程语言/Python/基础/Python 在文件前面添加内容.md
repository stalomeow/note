---
slug: "240427173926"
date: 2024-04-27
---

# Python 在文件前面添加内容


``` python
with open(file, 'r+', encoding='utf8') as fp:
    text = fp.read()
    fp.seek(0)
    fp.write('foo\n' + text)
```

## 常见错误

``` python
with open(file, 'r+', encoding='utf8') as fp:
    fp.seek(0)
    fp.write('foo\n') # 会把文件开头的部分覆盖掉！
```

