# KMP

!!! abstract

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

KMP 的核心是一个叫部分匹配表（Partial Match Table）的数组。以 `#!python p = "ababca"` 为例，它的 PMT 就是

|Char|a|b|a|b|c|a|
|:-|:-|:-|:-|:-|:-|:-|
|Index|0|1|2|3|4|5|
|Value|0|0|1|2|0|1|

`#!python PMT[i]` 表示 `#!python p[:i+1]` 的最长相同前后缀的长度。`#!python PMT[0]` 一定是 `#!python 0`。

!!! note "字符串的前缀和后缀"

    假设 `A`、`B`、`S` 均为字符串，且 `S` 非空。

    - 若 `A = BS`，则 `B` 是 `A` 的前缀。
    - 若 `A = SB`，则 `B` 是 `A` 的后缀。
    - `A` 既不是自己的前缀，也不是自己的后缀。

    最长相同前后缀：前缀集合和后缀集合的交集中，长度最长的元素。

    以字符串 `#!python "abab"` 为例。

    - 前缀集合 `#!python { "a", "ab", "aba" }`。
    - 后缀集合 `#!python { "bab", "ab", "b" }`。
    - 最长相同前后缀 `#!python "ab"`。

KMP 算法用了双指针。假设是在字符串 `s` 中匹配字符串 `p`，

- `i` 指向 `s` 中正在匹配的字符。
- `j` 指向 `p` 中正在匹配的字符。

当 `#!python s[i] != p[j]` 时，KMP 算法不会对 `i` 进行回溯。因为 `#!python p[:j] == s[i-j:i]`，所以只要让 `#!python j = PMT[j-1]` 然后继续匹配就行。

通常会把 PMT 向右偏移一格保存，记作 `next` 数组。

|Char|a|b|a|b|c|a|
|:-|:-|:-|:-|:-|:-|:-|
|Index|0|1|2|3|4|5|
|Value|0|0|1|2|0|1|
|Next|-1|0|0|1|2|0|

然后 `#!python j = PMT[j-1]` 改成 `#!python j = next[j]`。

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

代码和上面的类似，也是双指针。其实就是在 `#!python p` 最长的后缀 `#!python p[1:]` 里匹配 `#!python p` 最长的前缀 `#!python p[:-1]`，然后记录每次匹配的字符的个数。

- `i` 指向 `#!python p` 后缀 `#!python p[1:]` 中正在匹配的字符。
- `j` 指向 `#!python p` 前缀 `#!python p[:-1]` 中正在匹配的字符。

``` cpp
vector<int> getNext(string& p)
{
    // 保证 next[1] 是 0，next[0] 随便
    // next 长度比 p 大 1
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
    // 保证 next[1] 是 0，next[0] 随便
    // next 长度比 p 大 1
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

## 模板题

??? question

    给你两个字符串 `haystack` 和 `needle`，请你在 `haystack` 字符串中找出 `needle` 字符串的第一个匹配项的下标（下标从 0 开始）。如果 `needle` 不是 `haystack` 的一部分，则返回 -1 。

    示例 1：

    > 输入：haystack = "sadbutsad", needle = "sad"
    >
    > 输出：0
    >
    > 解释："sad" 在下标 0 和 6 处匹配。
    >
    > 第一个匹配项的下标是 0 ，所以返回 0 。

    示例 2：

    > 输入：haystack = "leetcode", needle = "leeto"
    >
    > 输出：-1
    >
    > 解释："leeto" 没有在 "leetcode" 中出现，所以返回 -1 。

    提示：

    `1 <= haystack.length, needle.length <= 104`

    `haystack` 和 `needle` 仅由小写英文字符组成

直接把板子套上去就行，不写了。

## 重复的子字符串

??? question

    给定一个非空的字符串 `s`，检查是否可以通过由它的一个子串重复多次构成。

    示例 1:

    > 输入: s = "abab"
    >
    > 输出: true
    >
    > 解释: 可由子串 "ab" 重复两次构成。

    示例 2:

    > 输入: s = "aba"
    >
    > 输出: false

    示例 3:

    > 输入: s = "abcabcabcabc"
    >
    > 输出: true
    >
    > 解释: 可由子串 "abc" 重复四次构成。 (或子串 "abcabc" 重复两次构成。)

    提示：

    `1 <= s.length <= 104`

    `s 由小写英文字母组成`

### 暴力

### KMP

### KMP 优化版
