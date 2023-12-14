---
tags:
  - 概率论
---

# 随机变量及其概率分布

!!! abstract

    随机变量及其概率分布。

## 随机变量

设 $\Omega = \{ \omega \}$ 是随机试验的样本空间，称定义在样本空间 $\Omega$ 上的单值实值函数 $X = X \left(\omega \right)$ 为随机变量。

$\forall L \subset \mathbb{R}$，则 $\{ X \in L \}$ 表示事件 $\{ \omega \mid X \left(\omega \right) \in L \}$，即样本空间中满足 $X \left(\omega \right) \in L$ 的所有样本点 $\omega$ 组成的事件。

## 随机变量的分布函数

设 $X$ 是一个随机变量，称函数

$$
F \left(x \right) = P \left(X \le x \right),\ x \in \mathbb{R}
$$

为随机变量 $X$ 的分布函数 (distribution function) 或者累积分布函数 (cumulative distribution function、CDF)。

- $0 \le F \left(x \right) \le 1 \ (x \in \mathbb{R})$，且 $F \left(-\infty \right) = 0$，$F \left(+\infty \right) = 1$。

- $F \left(x \right)$ 是 **单调不减** 的 **右连续** 函数。

满足这两条性质的 $F \left(x \right)$，也一定是某个随机变量的分布函数。

---

$\forall x_1 < x_2$，有

$$
P \left(x_1 < X \le x_2 \right) = F \left(x_2 \right) - F \left(x_1 \right)
$$

## 离散型随机变量

设 $X$ 是随机变量，如果其可能的取值为有限个或可列无限多个，则称 $X$ 为离散型随机变量 (discrete random variable)。

### 分布律

设 $X$ 是离散型随机变量，其可能的取值为 $x_1, x_2, \cdots, x_i, \cdots$ 称

$$
P \left(X=x_i \right) = p_i \ , \  i=1,2, \cdots
$$

为 $X$ 的分布律 (probability mass function)，或表示为

|$X$|$x_1$|$x_2$|$\cdots$|$x_i$|$\cdots$|
|:-:|:-:|:-:|:-:|:-:|:-:|
|$P$|$p_1$|$p_2$|$\cdots$|$p_i$|$\cdots$|

- $p_i \ge 0 \left(i=1,2,\cdots \right)$。

- $\displaystyle\sum\limits_{i} p_i = 1$。

满足这两条性质的一列数，也一定是某个离散型随机变量的分布律。

### 分布函数

设离散型随机变量 $X$ 的分布律为

$$
P \left(X=x_i \right) = p_i \ , \  i=1,2, \cdots
$$

则 $X$ 的分布函数为

$$
F \left(x \right) = \sum\limits_{x_i \le x} p_i \ , \  x \in \mathbb{R}
$$

---

可从 $F \left(x \right)$ 的间断点（函数值发生跳跃的地方）逆推出 $X$ 的分布律。

若 $x_i \left(i=1,2,\cdots \right)$ 为 $F \left(x \right)$ 的间断点，则 $X$ 的分布律为

$$
\begin{align}
p_i &= P \left(X=x_i \right) \\\\
&= F \left(x_i + 0 \right) - F \left(x_i - 0 \right) \\\\
&= F \left(x_i \right) - F \left(x_i - 0 \right)
\end{align}
$$

### 两点分布

若离散型随机变量 $X$ 只可能取 $0$ 和 $1$ 两个值，它的分布律为

$$
P \left(X=k \right) = p^k \left(1-p \right)^{1-k} \ , \ 0<p<1 \ , \ k=0,1
$$

则称 $X$ 服从参数为 $p$ 的 $0-1$ 分布、两点分布 (two-point distribution) 或伯努利分布 (Bernoulli distribution)，记为 $X \sim Bernoulli \left(p \right)$ 或 $X \sim B \left(1, p \right)$。

分布律也可以写成

|$X$|$0$|$1$|
|:-:|:-:|:-:|
|$P$|$1-p$|$p$|

!!! question "国内外的说法似乎不统一"

    英文维基百科上说，这种分布叫伯努利分布，是两点分布的特例。两点分布不要求 $X$ 只取 $0$ 和 $1$ 两个值。

### 二项分布

- $n$ 次独立重复试验：$n$ 次重复试验，每次试验条件相同，结果互不影响。
- $n$ 重 Bernoulli 试验：$n$ 次独立重复试验中，每次试验的结果只有 $A$ 和 $\overline{A}$ 两个。

若离散型随机变量 $X$ 表示 $n$ 重 Bernoulli 试验中 $A$ 发生的次数（每次试验中 $A$ 发生的概率都为 $p$），其分布律为

$$
P \left(X=k \right) = C_{n}^{k} p^k \left(1-p \right)^{n-k} \ , \ k=0,1,2, \cdots, n
$$

则称 $X$ 服从参数为 $n$、$p$ 的二项分布 (binomial distribution)，记为 $X \sim B \left(n, p \right)$。

#### Poisson 定理

设 $\lambda > 0$ 是一个常数，$n$ 是任意的正整数，$np=\lambda$，则对任一固定的非负整数 $k$，有

$$
\lim_{n \to \infty} C_{n}^{k} p^k \left(1-p \right)^{n-k}=\frac{\lambda^k}{k!} e^{-\lambda}
$$

当 $n$ 充分大、$p$ 充分小时，可以用来近似计算二项分布。一般 $n \ge 20$，$p \le 0.05$ 时，效果较好。

### Poisson 分布

若离散型随机变量 $X$ 的分布律为

$$
P\left(X=k \right)=\frac{\lambda^k}{k!} e^{-\lambda} \ , \ \lambda>0 \ , \ k=0,1,2,\cdots
$$

则称 $X$ 服从参数为 $\lambda$ 的泊松分布 (Poisson distribution)，记为 $X \sim P \left(\lambda \right)$。

!!! example

    适合描述一定时间内随机事件发生的次数 $X$。

    如某一服务设施在一定时间内受到的服务请求的次数。

### 几何分布

若离散型随机变量 $X$ 的分布律为

$$
P\left(X=k \right)=\left(1-p \right)^{k-1}p \ , \ k=0,1,2,\cdots \ , \ 0<p<1
$$

则称 $X$ 服从参数为 $p$ 的几何分布 (geometric distribution)。

!!! example

    Bernoulli 试验中，得到一次成功所需要的试验次数 $X$。

    如某射手对一目标连续进行独立射击，命中率为 $p$，射击直到命中目标为止。射击次数 $X$ 就服从参数为 $p$ 的几何分布。

### 超几何分布

设有 $N$ 件产品，其中有 $M$ 件次品，从中任取 $n$ 件，则取出的次品数 $X$ 的分布律为

$$
P\left(X=k \right)=\frac{C_M^k C_{N-M}^{n-k}}{C_N^n} \ , \ k=0,1,2,\cdots, \min\{M, n\}
$$

称 $X$ 服从参数为 $N$、$M$、$n$ 的超几何分布 (hypergeometric distribution)。

---

对于固定的 $n$，当 $N \to \infty$ 时，$\dfrac{M}{N} \to p$，则

$$
\lim_{N \to \infty} P\left(X=k \right) = C_{n}^{k} p^k \left(1-p \right)^{n-k}
$$

- 当 $n$ 相对 $N$ 较小，如 $\dfrac{n}{N}$ 不超过 $5\%$ 时，超几何分布可用二项分布近似计算。

- 超几何分布的背景是不放回抽样。二项分布的背景是放回抽样。当 $N$ 很大时，不放回抽样近似于放回抽样。

## 连续型随机变量

设 $X$ 是随机变量，其分布函数为 $F\left(x \right)$，如果存在非负可积函数 $f\left(x \right)$，使得

$$
F\left(x \right)=\int_{-\infty}^{x} f\left(t \right) \mathrm{d}t \ , \ -\infty<x<+\infty
$$

则称 $X$ 为连续型随机变量 (continuous random variable)，称 $f\left(x \right)$ 为 $X$ 的概率密度函数 (probability density function)，简称概率密度。

- $f\left(x \right) \ge 0 \ \left(-\infty<x<+\infty \right)$。

- $\displaystyle\int_{-\infty}^{+\infty} f\left(x \right) \mathrm{d}x = 1$。

满足这两条性质的 $f \left(x \right)$，也一定是某个连续型随机变量的概率密度。

---

- $P\left(a < X \le b \right) = \displaystyle\int_{a}^{b} f\left(x \right) \mathrm{d}x$。

- 在 $f\left(x \right)$ 的连续点 $x$ 处，有 $F'\left(x \right)=f\left(x \right)$。

- $F\left(x \right)$ 在 $\left(-\infty, +\infty \right)$ 上连续。

- $P\left(X=a \right)=0$，但 $\{ X=a \}$ **不是** 不可能事件。（不可能事件的概率是零，但概率是零的事件未必是不可能事件。）

---

$$
P\left(a < X \le b \right)=P\left(a \le X < b \right)=P\left(a < X < b \right)=P\left(a \le X \le b \right)
$$

$$
F\left(x \right) = P\left(X \le x \right) = P\left(X < x \right) = \int_{-\infty}^{x} f\left(t \right) \mathrm{d}t
$$

$$
P\left(X \ge x \right) = P\left(X > x \right) = \int_{x}^{+\infty} f\left(t \right) \mathrm{d}t
$$

### 均匀分布

若连续型随机变量 $X$ 的概率密度为

$$
f\left(x \right)=\begin{cases}
    \dfrac{1}{b-a} &,\ a<x<b \\\\
    0 &,\ \text{其他}
\end{cases}
$$

则称 $X$ 在区间 $\left(a,b \right)$ 上服从均匀分布 (continuous uniform distribution)，记为 $X \sim U \left(a,b \right)$。

分布函数为

$$
F\left(x \right)=\begin{cases}
    0 &,\ x<a \\\\
    \dfrac{x-a}{b-a} &,\ a \le x < b \\\\
    1 &,\ x \ge b
\end{cases}
$$

---

设 $X \sim U[a,b]$，则 $X$ 在 $[a,b]$ 的任一子区间上取值的概率等价于以 $a$、$b$ 为端点的直线线段上的几何概率。

### 正态分布

若连续型随机变量 $X$ 的概率密度为

$$
f\left(x \right)=\frac{1}{\sqrt{2\pi}\sigma} e^{-\tfrac{\left(x-\mu \right)^2}{2\sigma^2}} \ , \ -\infty<x<+\infty
$$

其中 $\mu$、$\sigma \ \left(\sigma > 0 \right)$ 为常数，则称 $X$ 服从参数为 $\mu$、$\sigma^2$ 的正态分布 (normal distribution) 或高斯分布 (Gaussian distribution)，记为 $X \sim N(\mu, \sigma^2)$。

- $f\left(x \right)$ 关于 $x=\mu$ 对称，在  $x=\mu$ 处取得最大值 $f\left(\mu \right)=\dfrac{1}{\sqrt{2\pi}\sigma}$。
- $\mu$ 为位置参数。改变 $\mu$，函数图像将沿 $x$ 轴平移。
- $\sigma$ 越大，图形越扁。$\sigma$ 越小，图形越尖，$X$ 落在 $\mu$ 附近的概率越大。

分布函数为

$$
F\left(x \right) = \int_{-\infty}^{x} \frac{1}{\sqrt{2\pi}\sigma} e^{-\tfrac{\left(t-\mu \right)^2}{2\sigma^2}} \mathrm{d}t \ , \ -\infty<x<+\infty
$$

- $F\left(\mu \right) = \dfrac{1}{2}$。
- $P\left(X \le \mu \right)=P\left(X > \mu \right)=\dfrac{1}{2}$。

#### 标准正态分布

设 $X \sim N(\mu, \sigma^2)$，若 $\mu=0$，$\sigma^2=1$，则称 $X$ 服从标准正态分布 (standard normal distribution)，记为 $X \sim N(0, 1)$。

概率密度为

$$
\varphi\left(x \right)=\frac{1}{\sqrt{2\pi}} e^{-\tfrac{x^2}{2}} \ , \ -\infty<x<+\infty
$$

分布函数为

$$
\Phi\left(x \right) = \int_{-\infty}^{x} \frac{1}{\sqrt{2\pi}} e^{-\tfrac{t^2}{2}} \mathrm{d}t \ , \ -\infty<x<+\infty
$$

- $\Phi\left(0 \right) = \dfrac{1}{2}$。
- $P\left(X \le 0 \right)=P\left(X > 0 \right)=\dfrac{1}{2}$。
- $\Phi\left(-x \right) = 1 - \Phi\left(x \right)$。

---

设 $X \sim N(\mu, \sigma^2)$，

- $Z=\dfrac{X-\mu}{\sigma} \sim N(0,1)$。$Z$ 为 $X$ 的标准化。

- $Y=aX+b \sim N(a\mu+b, (a\sigma)^2)$，$\left(a \ne 0\right)$。线性变换后正态性不变。

- $F\left(x \right) = \Phi\left(\dfrac{x-\mu}{\sigma} \right)$。

$$
P\left(x_1 < X \le x_2 \right) = \Phi\left(\dfrac{x_2-\mu}{\sigma} \right) - \Phi\left(\dfrac{x_1-\mu}{\sigma} \right)$$

!!! note "$3\sigma$ 规则"

    正态分布的随机变量的取值在 $\mu$ 的 $3\sigma$ 邻域内的概率为 $0.9972$，所以该事件的发生几乎是肯定的。

    - 当 $x > 4$ 时，$\Phi\left(x \right) \approx 1$。
    - 当 $x < -4$ 时，$\Phi\left(x \right) \approx 0$。

### 指数分布

若连续型随机变量 $X$ 的概率密度为

$$
f\left(x \right)=\begin{cases}
    \lambda e^{-\lambda x} &,\ x > 0 \\\\
    0 &,\ x \le 0
\end{cases}
$$

其中 $\lambda>0$ 为常数，则称 $X$ 服从参数为 $\lambda$ 的指数分布 (exponential distribution)，记为 $X \sim E(\lambda)$。

分布函数为

$$
F\left(x \right)=\begin{cases}
    1-e^{-\lambda x} &,\ x > 0 \\\\
    0 &,\ x \le 0
\end{cases}
$$

指数分布具有无记忆性，$\forall s,t>0$，有

$$
P\left(X>s+t \mid X>s \right)=P(X>t)
$$

!!! example

    可以用来表示独立随机事件发生的时间间隔 $X$。

    如旅客进入机场的时间间隔。

## 随机变量函数

设 $X$ 是随机变量，$y=g \left(x \right)$ 是已知的连续函数，则称 $Y=g \left(X \right)$ 为随机变量 $X$ 的函数，简称随机变量函数。$Y$ 也是一个随机变量。

### 离散型随机变量函数的分布

设离散型随机变量 $X$ 的分布律为

$$
P \left(X=x_i \right) = p_i \ , \  i=1,2, \cdots
$$

则 $Y=g \left(X \right)$ 也是离散型随机变量，其分布律为

$$
P\left(Y=y_j \right)=P\left(g \left(X \right)=y_j \right)=\sum_{g \left(x_i \right)=y_j} p_i
$$

### 连续型随机变量函数的分布

设连续型随机变量 $X$ 的概率密度函数为 $f_X \left(x \right)$。

#### 分布函数法

$Y=g\left(X \right)$ 的分布函数为

$$
F_Y \left(y \right) = P \left(Y \le y \right) = P \left(g \left(X \right) \le y \right)=\int_{g\left(x \right) \le y} f_X \left(t \right) \mathrm{d}t
$$

> 上式表示，在使得 $g\left(x \right) \le y$ 的 $x$ 的区间上积分。

从而 $Y$ 的概率密度为

$$
f_Y \left(y \right)=F_Y' \left(y \right)
$$

#### 公式法

设 $y=g\left(x \right)$ 严格单调可微，则 $Y=g\left(X \right)$ 的概率密度为

$$
f_Y\left(y \right)=\begin{cases}
    f_X\left(h\left(y \right) \right) \left | h'\left(y \right) \right |  &,\ y \in I \\\\
    0 &,\ \text{其他}
\end{cases}
$$

其中，$x=h\left(y \right)$ 是 $y=g\left(x \right)$ 的反函数。$I$ 是使得 $f_X\left(h\left(y \right) \right)>0$，$h\left(y \right)$ 和 $h'\left(y \right)$ 有意义的 $y$ 的集合。
