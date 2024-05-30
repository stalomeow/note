---
slug: "240425235307"
date: 2024-04-25
---

# KMP 算法

KMP 算法是一种改进的字符串匹配算法，由 D.E.Knuth，J.H.Morris 和 V.R.Pratt 提出。

## 暴力算法

暴力算法就是一个一个一个枚举，时间复杂度为 $O(m \times n)$，空间复杂度为 $O(1)$。

``` cpp
// 在 s 中找 p，返回 index
int find(string& s, string& p)
{
    for (int i = 0; i < s.size() - p.size() + 1; i++)
    {
        bool matched = true;

        for (int j = 0; j < p.size(); j++)
        {
            if (s[i + j] != p[j])
            {
                matched = false;
                break;
            }
        }

        if (matched)
            return i;
    }

    return -1;
}
```

## KMP 实现

> 推荐一个很好的回答：[如何更好地理解和掌握 KMP 算法? - 海纳的回答 - 知乎](https://www.zhihu.com/question/21923021/answer/281346746)。

KMP 的核心是一个叫部分匹配表（Partial Match Table）的数组。以 `p = "ababca"` 为例，它的 PMT 就是

|Char|a|b|a|b|c|a|
|:-|:-|:-|:-|:-|:-|:-|
|Index|0|1|2|3|4|5|
|Value|0|0|1|2|0|1|

`PMT[i]` 表示 `p[:i+1]` 的最长相同前后缀的长度。由[[字符串的前后缀|前后缀的定义]]，容易知道 `PMT[0]` 是 `0`。

KMP 算法用了双指针。假设是在字符串 `s` 中匹配字符串 `p`，

- `i` 指向 `s` 中正在匹配的字符。
- `j` 指向 `p` 中正在匹配的字符。

当 `s[i] != p[j]` 时，KMP 算法不会对 `i` 进行回溯。因为 `p[:j] == s[i-j:i]`，所以只要让 `j = PMT[j-1]` 然后继续匹配就行。

通常会把 PMT 向右偏移一格保存，记作 `next` 数组。

|Char|a|b|a|b|c|a|
|:-|:-|:-|:-|:-|:-|:-|
|Index|0|1|2|3|4|5|
|Value|0|0|1|2|0|1|
|Next|#|0|0|1|2|0|

然后 `j = PMT[j-1]` 改成 `j = next[j]`。

> `next[0]` 是永远不会用到的，所以不需要管它的值。可以认为 `next` 的下标从 `1` 开始。

### 基础实现

假设 `next` 数组已经构建好了。

``` cpp
// 在 s 中找 p，返回 index
int kmp(string& s, string& p)
{
    int j = 0;

    for (int i = 0; i < s.size(); i++)
    {
        // 不匹配就不断回溯 j，除非 j 已经跑到开头了
        while (j > 0 && p[j] != s[i]) j = next[j];

        if (p[j] == s[i]) j++;

        // 这时候 j 表示已经匹配的字符串的长度
        if (j == p.size())
        {
            return i - j + 1;
        }
    }

    return -1;
}
```

### 构建 next 数组

代码和上面的类似，也是双指针。其实就是在 `p` 最长的后缀 `p[1:]` 里匹配 `p` 最长的前缀 `p[:-1]`，然后记录每次匹配的字符的个数。

- `i` 指向 `p` 后缀 `p[1:]` 中正在匹配的字符。
- `j` 指向 `p` 前缀 `p[:-1]` 中正在匹配的字符。

``` cpp
vector<int> getNext(string& p)
{
    // * next 长度比 p 大 1
    // * 保证 next[1] 是 0，next[0] 随便
    vector<int> next(p.size() + 1, 0);

    int j = 0;

    // i 从 1 开始
    for (int i = 1; i < p.size(); i++)
    {
        while (j > 0 && p[j] != p[i]) j = next[j];

        if (p[j] == p[i]) j++;

        // 向右偏移一格保存
        next[i + 1] = j;
    }

    return next;
}
```

### 完整代码

总体时间复杂度为 $O(m + n)$，空间复杂度为 $O(n)$。

``` cpp
vector<int> getNext(string& p)
{
    // * next 长度比 p 大 1
    // * 保证 next[1] 是 0，next[0] 随便
    vector<int> next(p.size() + 1, 0);

    int j = 0;

    // i 从 1 开始
    for (int i = 1; i < p.size(); i++)
    {
        while (j > 0 && p[j] != p[i]) j = next[j];

        if (p[j] == p[i]) j++;

        // 向右偏移一格保存
        next[i + 1] = j;
    }

    return next;
}

// 在 s 中找 p，返回 index
int kmp(string& s, string& p)
{
    vector<int> next = getNext(p);
    int j = 0;

    for (int i = 0; i < s.size(); i++)
    {
        // 不匹配就不断回溯 j，除非 j 已经跑到开头了
        while (j > 0 && p[j] != s[i]) j = next[j];

        if (p[j] == s[i]) j++;

        // 这时候 j 表示已经匹配的字符串的长度
        if (j == p.size())
        {
            return i - j + 1;
        }
    }

    return -1;
}
```

## 优化 next 数组

## 找重复子字符串

### 暴力

### KMP

### KMP 优化版
