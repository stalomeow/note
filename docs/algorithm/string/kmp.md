# KMP

## 简介
KMP 算法是一种改进的字符串匹配算法，由 D.E.Knuth，J.H.Morris 和 V.R.Pratt 提出。

## 暴力算法
在讲 KMP 算法前，我们先来看看暴力的算法。假设 `s1` 是主串，`s2` 是要匹配的模式串。

``` cpp
int i = 0;
int j = 0;

while (i < len1)
{
    if (s1[i] == s2[j])
    {
        // 匹配则继续
        i++;
        j++;
    }
    else
    {
        // 不匹配则回溯，从头开始匹配
        i -= j - 1;
        j = 0;
    }

    if (j == len2)
    {
        // 匹配结束
        // 匹配的区间为 [i - j, i - 1]
        printf("[%d, %d]\n", i - j, i - 1);

        // 回溯，继续匹配
        i -= j - 1;
        j = 0;
    }
}
```

如果两个字符串的长度分别为 $m$ 和 $n$，那么暴力匹配的最坏时间复杂度为 $O(mn)$。

## KMP 算法
暴力算法在每次匹配失败后都会从头开始，浪费了很多时间。 ~~它没有从错误中吸取教训，就像我一样。~~ 而 KMP 算法能利用每次匹配失败后的信息，尽量减少模式串与主串的匹配次数，从而做到快速匹配。

我们来模拟一遍 KMP 的过程。首先，从头开始进行第一次匹配。

![第一次匹配](/images/kmp_01.png)

当我们匹配到第 4 个字符后，发现第 5 个字符不匹配了。这时，暴力算法会将 `i` 和 `j` 都回溯，从头开始匹配。

![暴力算法](/images/kmp_02.png)

然后，发现第 1 个字符就不匹配。。。

观察之前已经匹配成功的子串 `ABAB`。注意到主串的 `ABAB` 中后面的 `AB` 和模式串的 `ABAB` 中前面的 `AB` 是匹配的，所以我们完全可以从下面这个位置开始第二次匹配，而不是像暴力算法那样从头再来。

!!! note

    匹配时，检查的是&nbsp;`i + 1`&nbsp;和&nbsp;`j + 1`&nbsp;位置的字符。

![第二次匹配](/images/kmp_03.png)

可以发现，采用这种方式进行第二次匹配时，我们只回溯了 `j`，而 `i` 还保持在原来的位置。

我们可以定义一个数组 `next[]`，保存每次下一个字符匹配失败后 `j` 回溯的位置。特别地，如果 j 回溯到 0 就不需要再回溯了（想想为什么？）。

KMP 的核心代码如下：

``` cpp
// 从下标 1 开始储存
char s1[MAX_N]; // 主串
char s2[MAX_N]; // 模式串
int len1, len2, next[MAX_N];

void kmp()
{
    int j = 0; // 模式串下标

    for (int i = 0; i < len1; i++)
    {
        while (j > 0 && s2[j + 1] != s1[i + 1])
            j = next[j]; // 匹配失败则不断回溯 j

        if (s2[j + 1] == s1[i + 1])
            j++; // 匹配成功则 + 1

        if (j == len2)
        {
            printf("[%d, %d]\n", i - j + 2, i + 1);

            // 后面可能还有匹配的子串
            j = next[j]; // 回溯，继续匹配
        }
    }
}
```

接下来，如何求出 `next[]` 呢？想想在之前第一次匹配失败后，我们是如何找到 `AB` 的。

考虑主串中 `ABAB`（`ABAB` 是已经匹配成功的子串）的后缀集合 `[BAB, AB, B]` 和模式串中 `ABAB` 的前缀集合 `[A, AB, ABA]`。它们的交集中最长的那个字符串就是 `AB`。又因为主串中的 `ABAB` 和模式串中的 `ABAB` 是完全一样的（都是 `ABAB`），所以 `AB` 是 `ABAB` 的最长公共前后缀。而 `j` 回溯后的位置事实上就等于 `AB` 的长度，也就是 2。

于是，我们只要不断求出模式串 `[1..j]`（包含第 `j` 个字符）子串的最长公共前后缀就能得到 `next[]`。显然，`next[1]` 等于 0，因为此时模式串的子串长度为 1，没有前后缀。

一种巧妙的方式是让模式串自己和自己错开一位进行匹配。即从下图的位置开始做一次 KMP 算法。

![实际上就是用前缀去匹配后缀，后缀为主串，前缀为模式串](/images/kmp_04.png)

代码实现如下：

``` cpp
void pre()
{
    int j = 0;

    next[1] = 0; // 子串长度为 1，没有前后缀

    // 前缀为模式串
    // 后缀为主串
    for (int i = 1; i < len2; i++)
    {
        while (j > 0 && s2[j + 1] != s2[i + 1])
            j = next[j];

        if (s2[j + 1] == s2[i + 1])
            j++;

        next[i + 1] = j;
    }
}
```

KMP 算法的时间复杂度 $O(m + n)$。

## 模板题
[洛谷 P3375 【模板】KMP字符串匹配](https://www.luogu.com.cn/problem/P3375)

??? success "AC 代码"

    ``` cpp
    #include <cstdio>
    #include <cstring>

    char s1[1000010], s2[1000010];
    int len1, len2, next[1000010];

    void pre()
    {
        int j = 0;

        next[1] = 0;

        for (int i = 1; i < len2; i++)
        {
            while (j > 0 && s2[j + 1] != s2[i + 1])
                j = next[j];

            if (s2[j + 1] == s2[i + 1])
                j++;

            next[i + 1] = j;
        }
    }

    void kmp()
    {
        int j = 0;

        for (int i = 0; i < len1; i++)
        {
            while (j > 0 && s2[j + 1] != s1[i + 1])
                j = next[j];

            if (s2[j + 1] == s1[i + 1])
                j++;

            if (j == len2)
            {
                printf("%d\n", i - j + 2);
                j = next[j];
            }
        }
    }

    int main()
    {
        scanf("%s%s", s1 + 1, s2 + 1);

        len1 = strlen(s1 + 1);
        len2 = strlen(s2 + 1);

        pre();
        kmp();

        for (int j = 1; j <= len2; j++)
        {
            printf("%d ", next[j]);
        }

        return 0;
    }
    ```

## KMP 算法的优化版