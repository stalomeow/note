# 大数定律和中心极限定理

!!! abstract

    Chebyshev 不等式、大数定律、中心极限定理。

## Chebyshev（切比雪夫）不等式

设 $X$ 是随机变量，如果 $EX$、$DX$ 存在，则 $\forall \varepsilon > 0$，有

$$
P \left ( \left | X-EX \right | \ge \varepsilon \right ) \le \frac{DX}{\varepsilon^2}
$$

也可以写成

$$
P \left ( \left | X-EX \right | < \varepsilon \right ) \ge 1 - \frac{DX}{\varepsilon^2}
$$

## Law of large numbers（LLN、大数定律）

随机变量的前若干项的算术平均值，在某种条件下，收敛到这些项的均值的算术平均值。

### 定义 1

设 $X_1$，$X_2$，$\cdots$，$X_n$，$\cdots$ 是随机变量序列，如果存在数列 $a_1$，$a_2$，$\cdots$，$a_n$，$\cdots$，使得 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - a_n \right | \ge \varepsilon \right ) = 0
$$

则称随机变量序列 $\{ X_n \}$ 服从大数定律。

### 定义 2

设 $X_1$，$X_2$，$\cdots$，$X_n$，$\cdots$ 是随机变量序列，$X$ 是随机变量，如果 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | X_n - X \right | \ge \varepsilon \right ) = 0
$$

则称随机变量序列 $\{ X_n \}$ 依概率收敛于 $X$，记为

$$
X_n \overset{P}{\longrightarrow} X, \  n \to \infty
$$

### Chebyshev 大数定律

若

- $\{ X_n \}$ 是随机变量序列
- $X_i$ 相互独立，具有相同的数学期望和方差（$EX_i=\mu$，$DX_i=\sigma^2$）

则 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - \mu \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \mu, \  n \to \infty
$$

---

更一般地，若

- $\{ X_n \}$ 是随机变量序列
- $X_i$ 相互独立，具有相同的数学期望（$EX_i=\mu$）
- 存在常数 $C > 0$，使得 $DX_i \le C$

则 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - \mu \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \mu, \  n \to \infty
$$

### Markov（马尔可夫）大数定律

若

- $\{ X_n \}$ 是随机变量序列
- $\lim\limits_{n \to \infty} \dfrac{1}{n^2} D \left [ \displaystyle\sum\limits_{i=1}^{n} X_i \right ] = 0$

则 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - \frac{1}{n} \sum_{i=1}^{n} EX_i \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \sum_{i=1}^{n} EX_i, \  n \to \infty
$$

### Khintchine（辛钦）大数定律

若

- $\{ X_n \}$ 是随机变量序列
- $X_i$ 相互独立，同分布，具有有限的数学期望（$EX_i=\mu$）

则 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{1}{n} \sum_{i=1}^{n} X_i - \mu \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{1}{n} \sum_{i=1}^{n} X_i \overset{P}{\longrightarrow} \mu, \  n \to \infty
$$

### Bernoulli 大数定律

若

- $n_A$ 表示 $n$ 重 Bernoulli 试验中事件 $A$ 发生的次数
- $P(A)=p$

则 $\forall \varepsilon > 0$，有

$$
\lim_{n \to \infty} P \left ( \left | \frac{n_A}{n} - p \right | \ge \varepsilon \right ) = 0
$$

即

$$
\frac{n_A}{n} \overset{P}{\longrightarrow} p, \  n \to \infty
$$

!!! note "频率的稳定性"

    Bernoulli 大数定律说明：对于给定的任意小的正数 $\varepsilon$，当 $n$ 充分大时，随机事件 $\left\{ \left | \dfrac{n_A}{n} - p \right | < \varepsilon \right\}$ 几乎是必然要发生的。

    频率不是概率。频率的极限可能不存在，所以更不是概率。但频率的稳定值是概率。

    在实际应用中，当试验次数很大时，可以用事件的频率 $\dfrac{n_A}{n}$ 来代替事件的概率 $p$。


## Central limit theorem（CLT、中心极限定理）

很多实际问题中，有些随机变量是由大量相互独立的随机因素的综合影响而形成的，但其中每个个别因素在总的影响中起的作用是微小的，这种随机变量往往近似服从正态分布。

### Lindeberg-Lévy（林德伯格 - 勒维）中心极限定理

若

- $\{ X_n \}$ 是随机变量序列
- $X_i$ 相互独立，同分布，$EX_i=\mu$，$DX_i=\sigma^2$

则 $\forall x \in \mathbb{R}$，随机变量

$$
Y_n = \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - E \left [ \displaystyle\sum\limits_{i=1}^{n} X_i \right ]}{\sqrt{D \left [ \displaystyle\sum\limits_{i=1}^{n} X_i \right ]}} = \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - n\mu}{\sqrt{n}\sigma}
$$

的分布函数 $F_n(x)$ 满足

$$
\lim_{n \to \infty} F_n(x) = \lim_{n \to \infty} P \left ( \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - n\mu}{\sqrt{n}\sigma} \le x \right ) = \int_{-\infty }^{x} \frac{1}{\sqrt{2\pi}} e^{-\frac{t^2}{2}} \mathrm{d}t = \Phi(x)
$$

所以，当 $n$ 充分大时，可以近似认为 $\displaystyle\sum\limits_{i=1}^{n} X_i \sim N(n\mu, n\sigma^2)$。对任意实数 $x$ 以及 $a<b$，有

$$
P \left ( \sum_{i=1}^{n} X_i \le x \right ) \approx \Phi \left ( \frac{x-n\mu}{\sqrt{n}\sigma} \right )
$$

$$
P \left ( a < \sum_{i=1}^{n} X_i \le b \right ) \approx \Phi \left ( \frac{b-n\mu}{\sqrt{n}\sigma} \right ) - \Phi \left ( \frac{a-n\mu}{\sqrt{n}\sigma} \right )
$$

### Lyapunov（李雅普诺夫）中心极限定理

设

- $\{ X_n \}$ 是随机变量序列
- $X_i$ 相互独立，$EX_i=\mu_i$，$DX_i=\sigma_i^2$

记

$$
B_n^2 = \sum_{i=1}^{n} \sigma_i^2
$$

若 $\exists \delta > 0$，使得当 $n \to \infty$ 时

$$
\frac{1}{B_n^{2+\delta}} \sum_{i=1}^{n} E \left [ \left | X_i - \mu_i \right |^{2+\delta} \right ] \to 0
$$

则 $\forall x \in \mathbb{R}$，随机变量

$$
Y_n = \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - E \left [ \displaystyle\sum\limits_{i=1}^{n} X_i \right ]}{\sqrt{D \left [ \displaystyle\sum\limits_{i=1}^{n} X_i \right ]}} = \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - \displaystyle\sum\limits_{i=1}^{n} \mu_i}{B_n}
$$

的分布函数 $F_n(x)$ 满足

$$
\lim_{n \to \infty} F_n(x) = \lim_{n \to \infty} P \left ( \frac{\displaystyle\sum\limits_{i=1}^{n} X_i - \displaystyle\sum\limits_{i=1}^{n} \mu_i}{B_n} \le x \right ) = \int_{-\infty }^{x} \frac{1}{\sqrt{2\pi}} e^{-\frac{t^2}{2}} \mathrm{d}t = \Phi(x)
$$

所以，当 $n$ 充分大时，可以近似认为 $\displaystyle\sum\limits_{i=1}^{n} X_i \sim N \left ( \displaystyle\sum\limits_{i=1}^{n} \mu_i, \displaystyle\sum\limits_{i=1}^{n} \sigma_i^2 \right )$。对任意实数 $x$ 以及 $a<b$，有

$$
P \left ( \sum_{i=1}^{n} X_i \le x \right ) \approx \Phi \left ( \frac{x- \displaystyle\sum\limits_{i=1}^{n} \mu_i}{\sqrt{\displaystyle\sum\limits_{i=1}^{n} \sigma_i^2}} \right )
$$

$$
P \left ( a < \sum_{i=1}^{n} X_i \le b \right ) \approx \Phi \left ( \frac{b- \displaystyle\sum\limits_{i=1}^{n} \mu_i}{\sqrt{\displaystyle\sum\limits_{i=1}^{n} \sigma_i^2}} \right ) - \Phi \left ( \frac{a- \displaystyle\sum\limits_{i=1}^{n} \mu_i}{\sqrt{\displaystyle\sum\limits_{i=1}^{n} \sigma_i^2}} \right )
$$

### De Moivre-Laplace（棣莫弗 - 拉普拉斯）中心极限定理

由前面的 Lindeberg-Lévy CLT 可以推出，若

- $n_A$ 表示 $n$ 重 Bernoulli 试验中事件 $A$ 发生的次数
- $P(A)=p$

则 $\forall x \in \mathbb{R}$，随机变量

$$
Y_n=\frac{n_A-np}{\sqrt{np(1-p)}}
$$

的分布函数 $F_n(x)$ 满足

$$
\lim_{n \to \infty} F_n(x) = \lim_{n \to \infty} P \left ( \frac{n_A-np}{\sqrt{np(1-p)}} \le x \right ) = \int_{-\infty }^{x} \frac{1}{\sqrt{2\pi}} e^{-\frac{t^2}{2}} \mathrm{d}t = \Phi(x)
$$

所以，若 $X \sim B(n,p)$，当 $n$ 充分大时，可以近似认为 $X \sim N(np, np(1-p))$。对任意实数 $x$ 以及 $a<b$，有

$$
P \left ( X \le x \right ) \approx \Phi \left ( \frac{x-np}{\sqrt{np(1-p)}} \right )
$$

$$
P \left ( a < X \le b \right ) \approx \Phi \left ( \frac{b-np}{\sqrt{np(1-p)}} \right ) - \Phi \left ( \frac{a-np}{\sqrt{np(1-p)}} \right )
$$
