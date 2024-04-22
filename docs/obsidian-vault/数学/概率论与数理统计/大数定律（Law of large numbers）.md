---
slug: "20240421213303"
date: "2024-04-21"
---

# 大数定律（Law of large numbers）

> 下面说的都是弱大数定律（WLLN）。

随机变量的前若干项的算术平均值，在某种条件下，收敛到这些项的均值的算术平均值。

## 定义

设 $X_1$，$X_2$，$\cdots$，$X_n$，$\cdots$ 是随机变量序列，如果存在数列 $a_1$，$a_2$，$\cdots$，$a_n$，$\cdots$，使得 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - a_n \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} a_n, \  n \to \infty
$$

则称随机变量序列 $\{ X_n \}$ 服从大数定律。

## Chebyshev 大数定律

若

- $X_i$ 相互独立，具有相同的数学期望（$EX_i=\mu$）
- 存在常数 $C > 0$，使得 $DX_i \le C$

则

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \mu, \  n \to \infty
$$

## Markov（马尔可夫）大数定律

若

- $\lim\limits_{n \to \infty} D \left [ \dfrac{1}{n} \displaystyle\sum\limits_{i=1}^{n} X_i \right ] = 0$

则

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \frac{1}{n} \sum_{i=1}^{n} EX_i, \  n \to \infty
$$

## Khintchine（辛钦）大数定律

若

- $X_i$ 相互独立，同分布，具有有限的数学期望（$EX_i=\mu$）

则

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \mu, \  n \to \infty
$$

## Bernoulli 大数定律

若

- $n_A$ 表示 $n$ 重 Bernoulli 试验中事件 $A$ 发生的次数
- $P(A)=p$

则

$$
\frac{n_A}{n} \overset{P}{\longrightarrow} p, \  n \to \infty
$$

### 频率的稳定性

Bernoulli 大数定律说明：对于给定的任意小的正数 $\varepsilon$，当 $n$ 充分大时，随机事件 $\left\{ \left | \dfrac{n_A}{n} - p \right | < \varepsilon \right\}$ 几乎是必然要发生的。

频率不是概率。频率的极限可能不存在，所以更不是概率。但频率的稳定值是概率。

在实际应用中，当试验次数很大时，可以用事件的频率 $\dfrac{n_A}{n}$ 来代替事件的概率 $p$。