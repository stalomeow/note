---
date: 2024-12-30T22:40:15
---

# Monte Carlo 积分

基本思想

$$
\begin{align}
\int_a^b f(x) \mathrm{d}x &= \int_a^b \frac{f(x)}{pdf(x)} \cdot pdf(x)\mathrm{d}x\\
\\
&=E \left ( \frac{f(X)}{pdf(X)} \right)
\end{align}
$$

其中 $X \sim pdf(x)$。这样，就将积分转化为 [[数学期望]]，然后可以用 [[弱大数定律|大数定律]] 近似计算。

## Monte Carlo estimator

按 $X_i \sim pdf(x)$ 分布随机采样 $N$ 次后取平均值。

$$
\int_a^b f(x) \mathrm{d}x \approx \frac{1}{N} \sum_{i=1}^N \frac{f(X_i)}{pdf(X_i)}
$$

如果是 [[均匀分布|均匀采样]]，那么 $pdf(x)=\dfrac{1}{b-a}$，上式变成

$$
\int_a^b f(x) \mathrm{d}x \approx \frac{b-a}{N} \sum_{i=1}^N f(X_i)
$$

这是最基本的 Monte Carlo estimator。
