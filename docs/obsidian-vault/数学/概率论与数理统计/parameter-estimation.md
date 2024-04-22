# 参数估计

!!! abstract

    点估计、置信区间。

## 点估计

设总体 $X$ 的分布函数 $F(x;\theta_1,\theta_2,\cdots,\theta_k)$ 的形式已知，其中 $\theta_1,\theta_2,\cdots,\theta_k$ 为未知的参数。$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，$x_1,x_2,\cdots,x_n$ 是样本的一组样本值。若统计量 $\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ ($i=1,2,\cdots,k$) 能对参数 $\theta_i$ ($i=1,2,\cdots,k$) 作估计，则称之为 $\theta_i$ 的点估计。

- 称 $\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ 为 $\theta_i$ 的**点估计量**。它是一个随机变量。
- 称 $\hat{\theta}_i(x_1,x_2,\cdots,x_n)$ 为 $\theta_i$ 的**点估计值**。它是随机变量的取值。
- 在不致混淆的情况下，点估计量和点估计值统称为点估计。

### 矩估计法

> 思想：受 Khintchine LLN 启发，用样本的各阶原点矩作为总体的各阶原点矩的估计。有几个参数就列几个方程，然后把参数求出来。（矩的阶数最好从小到大依次写，别跳）

设总体 $X$ 的分布函数为 $F(x;\theta_1,\theta_2,\cdots,\theta_k)$，其中 $\theta_1,\theta_2,\cdots,\theta_k$ 为未知的参数。假设总体 $X$ 的 $k$ 阶原点矩 $\mu_k=EX^k$ 存在，由下面方程组

$$
\left\{\begin{matrix}
\mu_1(\theta_1,\theta_2,\cdots,\theta_k)&=\dfrac{1}{n}\displaystyle\sum\limits_{i=1}^{n}X_i \\
\mu_2(\theta_1,\theta_2,\cdots,\theta_k)&=\dfrac{1}{n}\displaystyle\sum\limits_{i=1}^{n}X_i^2\\
\vdots \\
\mu_k(\theta_1,\theta_2,\cdots,\theta_k)&=\dfrac{1}{n}\displaystyle\sum\limits_{i=1}^{n}X_i^k
\end{matrix}\right.
$$

解得 $\hat{\theta}_i=\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ ($i=1,2,\cdots,k$) 作为参数 $\theta_i$ 的估计量。

- 称 $\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ 为 $\theta_i$ 的**矩估计量**。
- 称 $\hat{\theta}_i(x_1,x_2,\cdots,x_n)$ 为 $\theta_i$ 的**矩估计值**。

### 最大似然估计法

设总体 $X$ 的分布律（或概率密度）$p(x;\theta)$ 为已知，其中 $\theta \in \Theta$ 为未知参数。$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，$x_1,x_2,\cdots,x_n$ 是样本的一组样本值，

- 称 $L(\theta)=\displaystyle\prod\limits_{i=1}^{n}p(x_i;\theta)$ 为参数 $\theta$ 的**似然函数 (Likelihood function)**。

    - 若总体是离散型随机变量，它的意义是随机点 $(X_1,X_2,\cdots,X_n)$ 落在**样本点** $(x_1,x_2,\cdots,x_n)$ 的概率。
    - 若总体是连续型随机变量，则是落在**样本点附近**的概率。

- 称能使 $L(\theta)$ 取得最大值的 $\hat{\theta}(x_1,x_2,\cdots,x_n)$ 为参数 $\theta$ 的**最大似然估计 (Maximum likelihood estimation、MLE)**。

    - 称 $\hat{\theta}(X_1,X_2,\cdots,X_n)$ 为 $\theta$ 的**最大似然估计量**。
    - 称 $\hat{\theta}(x_1,x_2,\cdots,x_n)$ 为 $\theta$ 的**最大似然估计值**。

> 思想：固定 $x_1,x_2,\cdots,x_n$，然后找到一个 $\hat{\theta} \in \Theta$ 使得 $L(\theta)$ 取得最大值。换句话说就是使随机点 $(X_1,X_2,\cdots,X_n)$ 落在**样本点** $(x_1,x_2,\cdots,x_n)$（附近）的概率最大。

求解步骤：

1. 写出似然函数：$L(\theta)=\displaystyle\prod\limits_{i=1}^{n} p(x_i;\theta)$。
2. 取自然对数，方便求导：$\ln L(\theta)=\displaystyle\sum\limits_{i=1}^{n} \ln p(x_i;\theta)$。
3. 令 $\dfrac{\partial \ln L(\theta)}{\partial \theta_i}=0$ ($i=1,2,\cdots,k$)，解得 $\hat{\theta}_i=\hat{\theta}_i(x_1,x_2,\cdots,x_n)$ ($i=1,2,\cdots,k$)。

!!! note "最大似然估计的不变性"

    设 $\theta$ 的函数 $u=u(\theta)$ ($\theta \in \Theta$) 具有单值反函数 $\theta=\theta(u)$ ($u \in U$)，$\hat{\theta}$ 是总体 $X$ 的概率分布中参数 $\theta$ 的最大似然估计，则 $\hat{u}=u(\hat{\theta})$ 是 $u(\theta)$ 的最大似然估计。

## 区间估计

对于一个未知参数 $\theta$，除了它的估计值 $\hat{\theta}$ 外，还需要估计误差。估计出一个区间范围，同时给出它包含参数 $\theta$ 真值的可信程度，这种形式的估计叫**区间估计**。

### 双侧置信区间

设总体 $X$ 的分布函数 $F(x;\theta)$ 的形式为已知，$\theta$ 为未知参数，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本。如果 $\forall 0<\alpha<1$，能由样本确定统计量 $\underline{\theta}=\underline{\theta}(X_1,X_2,\cdots,X_n)$ 与 $\overline{\theta}=\overline{\theta}(X_1,X_2,\cdots,X_n)$，使得

$$
P \left (\underline{\theta}(X_1,X_2,\cdots,X_n)<\theta<\overline{\theta}(X_1,X_2,\cdots,X_n) \right ) = 1-\alpha
$$

则称随机区间 $(\underline{\theta}, \ \overline{\theta})$ 为参数 $\theta$ 的置信水平为 $1-\alpha$ 的**（双侧）置信区间**，$\underline{\theta}$ 与 $\overline{\theta}$ 分别称为**置信下限**和**置信上限**，$1-\alpha$ 称为**置信水平、置信度**。

> 含义：若反复抽样多次（每次样本容量相等），每组样本值确定一个区间 $(\underline{\theta}, \ \overline{\theta})$，每个这样的区间要么包含 $\theta$ 的真值，要么不包含。由 Bernoulli LLN 知，这么多区间中，包含 $\theta$ 的真值的约占 $100(1-\alpha)\%$，不包含的约占 $100\alpha\%$。

- 当总体 $X$ 是离散型随机变量时，对于给定的 $\alpha$，常常找不到区间 $(\underline{\theta}, \ \overline{\theta})$ 使得 $P \left (\underline{\theta}<\theta<\overline{\theta} \right )$ 恰好为 $1-\alpha$。这时，可以找使得 $P \left (\underline{\theta}<\theta<\overline{\theta} \right )$ 不小于且最接近 $1-\alpha$ 的区间 $(\underline{\theta}, \ \overline{\theta})$。

- 置信水平为 $1-\alpha$ 的置信区间不是唯一的。区间长度越短，表示估计的精度越高，区间越优。

??? note "求参数 $\theta$ 的置信水平为 $1-\alpha$ 的双侧置信区间的步骤"

    1. 选一个样本 $X_1,X_2,\cdots,X_n$ 的函数

        $$
        Z = Z(X_1,X_2,\cdots,X_n;\theta)
        $$

        $Z$ 包含待估参数 $\theta$ 且分布已知，但不依赖其他未知参数。

    2. 选定常数 $a,b$，使得

        $$
        P \left (a<Z(X_1,X_2,\cdots,X_n;\theta)<b \right )=1-\alpha
        $$

    3. 求出 $a<Z(X_1,X_2,\cdots,X_n;\theta)<b$ 的等价不等式 $\underline{\theta}<\theta<\overline{\theta}$，其中 $\underline{\theta}=\underline{\theta}(X_1,X_2,\cdots,X_n)$ 与 $\overline{\theta}=\overline{\theta}(X_1,X_2,\cdots,X_n)$ 都是统计量，从而求出区间 $(\underline{\theta}, \ \overline{\theta})$。

### 单侧置信区间

设总体 $X$ 的分布函数 $F(x;\theta)$ 的形式为已知，$\theta$ 为未知参数，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本。

- 如果 $\forall 0<\alpha<1$，能由样本确定统计量 $\underline{\theta}=\underline{\theta}(X_1,X_2,\cdots,X_n)$，使得

    $$
    P \left (\theta > \underline{\theta}(X_1,X_2,\cdots,X_n) \right ) = 1-\alpha
    $$

    则称随机区间 $(\underline{\theta}, \ +\infty)$ 为参数 $\theta$ 的置信水平为 $1-\alpha$ 的**单侧置信区间**，$\underline{\theta}$ 称为**单侧置信下限**。

- 如果 $\forall 0<\alpha<1$，能由样本确定统计量 $\overline{\theta}=\overline{\theta}(X_1,X_2,\cdots,X_n)$，使得

    $$
    P \left (\theta<\overline{\theta}(X_1,X_2,\cdots,X_n) \right ) = 1-\alpha
    $$

    则称随机区间 $(-\infty, \ \overline{\theta})$ 为参数 $\theta$ 的置信水平为 $1-\alpha$ 的**单侧置信区间**，$\overline{\theta}$ 称为**单侧置信上限**。

其中，$1-\alpha$ 称为**置信水平、置信度**。

### 单正态总体参数

设总体 $X \sim N(\mu,\sigma^2)$，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，样本均值为 $\overline{X}$，样本方差为 $S^2$。

---

求 $\mu$ 的置信水平为 $1-\alpha$ 的置信区间：

|条件|$\sigma^2$ 已知|$\sigma^2$ 未知|
|:-|:-|:-|
|枢轴量|$\dfrac{\overline{X} -\mu}{\sigma/\sqrt{n}} \sim N(0,1)$|$\dfrac{\overline{X} -\mu}{S/\sqrt{n}} \sim t(n-1)$|
|双侧|$\left ( \overline{X} - \dfrac{\sigma}{\sqrt{n}} z_{\alpha/2},\ \overline{X} + \dfrac{\sigma}{\sqrt{n}} z_{\alpha/2} \right )$|$\left ( \overline{X} - \dfrac{S}{\sqrt{n}} t_{\alpha/2}(n-1),\ \overline{X} + \dfrac{S}{\sqrt{n}} t_{\alpha/2}(n-1) \right )$|
|单侧 1|$\left ( \overline{X} - \dfrac{\sigma}{\sqrt{n}} z_{\alpha},\ +\infty \right )$|$\left ( \overline{X} - \dfrac{S}{\sqrt{n}} t_{\alpha}(n-1),\ +\infty \right )$|
|单侧 2|$\left (-\infty ,\ \overline{X} + \dfrac{\sigma}{\sqrt{n}} z_{\alpha} \right )$|$\left (-\infty ,\ \overline{X} + \dfrac{S}{\sqrt{n}} t_{\alpha}(n-1) \right )$|

---

求 $\sigma^2$ 的置信水平为 $1-\alpha$ 的置信区间：

|条件|$\mu$ 已知|$\mu$ 未知|
|:-|:-|:-|
|枢轴量|$\dfrac{\displaystyle\sum\limits_{i=1}^n (X_i -\mu)^2}{\sigma^2} \sim \chi^2(n)$|$\dfrac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$|
|双侧|$\left ( \dfrac{\displaystyle\sum\limits_{i=1}^n (X_i -\mu)^2}{\chi^2_{\alpha/2}(n)},\ \dfrac{\displaystyle\sum\limits_{i=1}^n (X_i -\mu)^2}{\chi^2_{1-\alpha/2}(n)} \right )$|$\left ( \dfrac{(n-1)S^2}{\chi^2_{\alpha/2}(n-1)},\ \dfrac{(n-1)S^2}{\chi^2_{1-\alpha/2}(n-1)} \right )$|
|单侧 1|$\left ( \dfrac{\displaystyle\sum\limits_{i=1}^n (X_i -\mu)^2}{\chi^2_{\alpha}(n)},\ +\infty \right )$|$\left ( \dfrac{(n-1)S^2}{\chi^2_{\alpha}(n-1)},\ +\infty \right )$|
|单侧 2|$\left (0 ,\ \dfrac{\displaystyle\sum\limits_{i=1}^n (X_i -\mu)^2}{\chi^2_{1-\alpha}(n)} \right )$|$\left (0 ,\ \dfrac{(n-1)S^2}{\chi^2_{1-\alpha}(n-1)} \right )$|

### 双正态总体参数

设 $X_1,X_2,\cdots,X_{n_1}$ 为来自第一个总体 $X \sim N(\mu_1,\sigma_1^2)$ 的一个样本，样本均值为 $\overline{X}$，样本方差为 $S_1^2$。

设 $Y_1,Y_2,\cdots,Y_{n_2}$ 为来自第二个总体 $Y \sim N(\mu_2,\sigma_2^2)$ 的一个样本，样本均值为 $\overline{Y}$，样本方差为 $S_2^2$。

两个样本构成的合样本 $X_1,X_2,\cdots,X_{n_1}, Y_1,Y_2,\cdots,Y_{n_2}$ 相互独立。

---

求 $\mu_1-\mu_2$ 的置信水平为 $1-\alpha$ 的置信区间：

|条件|$\sigma_1^2,\sigma_2^2$ 已知|$\sigma_1^2=\sigma_2^2$ 但未知|
|:-|:-|:-|
|枢轴量|$\dfrac{\overline{X}-\overline{Y} - (\mu_1-\mu_2)}{\sqrt{\dfrac{\sigma_1^2}{n_1}+\dfrac{\sigma_2^2}{n_2}}} \sim N(0,1)$|$\dfrac{\overline{X}-\overline{Y} - (\mu_1-\mu_2)}{S_\omega\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}}} \sim t(n_1 + n_2 - 2) \ \left (\text{其中 } S_\omega=\sqrt{\dfrac{(n_1-1)S_1^2+(n_2-1)S_2^2}{n_1 + n_2 - 2}} \right )$|
|双侧|$\left ( \overline{X}-\overline{Y} - \sqrt{\dfrac{\sigma_1^2}{n_1}+\dfrac{\sigma_2^2}{n_2}} z_{\alpha/2},\ \overline{X}-\overline{Y} + \sqrt{\dfrac{\sigma_1^2}{n_1}+\dfrac{\sigma_2^2}{n_2}} z_{\alpha/2} \right )$|$\left ( \overline{X}-\overline{Y} - S_\omega\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}} t_{\alpha/2}(n_1 + n_2 - 2),\ \overline{X}-\overline{Y} + S_\omega\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}} t_{\alpha/2}(n_1 + n_2 - 2) \right )$|
|单侧 1|$\left ( \overline{X}-\overline{Y} - \sqrt{\dfrac{\sigma_1^2}{n_1}+\dfrac{\sigma_2^2}{n_2}} z_{\alpha},\ +\infty \right )$|$\left ( \overline{X}-\overline{Y} - S_\omega\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}} t_{\alpha}(n_1 + n_2 - 2),\ +\infty \right )$|
|单侧 2|$\left (-\infty ,\ \overline{X}-\overline{Y} + \sqrt{\dfrac{\sigma_1^2}{n_1}+\dfrac{\sigma_2^2}{n_2}} z_{\alpha} \right )$|$\left (-\infty ,\ \overline{X}-\overline{Y} + S_\omega\sqrt{\dfrac{1}{n_1}+\dfrac{1}{n_2}} t_{\alpha}(n_1 + n_2 - 2) \right )$|

---

求 $\dfrac{\sigma_1^2}{\sigma_2^2}$ 的置信水平为 $1-\alpha$ 的置信区间：

|条件|$\mu_1,\mu_2$ 已知|$\mu_1,\mu_2$ 未知|
|:-|:-|:-|
|枢轴量|$\dfrac{n_2\sigma_2^2\displaystyle\sum\limits_{i=1}^{n_1} (X_i -\mu_1)^2}{n_1\sigma_1^2\displaystyle\sum\limits_{i=1}^{n_2} (Y_i -\mu_2)^2} \sim F(n_1,n_2)$|$\dfrac{\sigma_2^2 S_1^2}{\sigma_1^2 S_2^2} \sim F(n_1-1,n_2-1)$|
|双侧|$\left ( \dfrac{n_2\displaystyle\sum\limits_{i=1}^{n_1} (X_i -\mu_1)^2}{n_1\displaystyle\sum\limits_{i=1}^{n_2} (Y_i -\mu_2)^2} \dfrac{1}{F_{\alpha/2}(n_1,n_2)},\ \dfrac{n_2\displaystyle\sum\limits_{i=1}^{n_1} (X_i -\mu_1)^2}{n_1\displaystyle\sum\limits_{i=1}^{n_2} (Y_i -\mu_2)^2} F_{\alpha/2}(n_2,n_1) \right )$|$\left ( \dfrac{S_1^2}{S_2^2} \dfrac{1}{F_{\alpha/2}(n_1-1,n_2-1)},\ \dfrac{S_1^2}{S_2^2} F_{\alpha/2}(n_2-1,n_1-1) \right )$|
|单侧 1|$\left ( \dfrac{n_2\displaystyle\sum\limits_{i=1}^{n_1} (X_i -\mu_1)^2}{n_1\displaystyle\sum\limits_{i=1}^{n_2} (Y_i -\mu_2)^2} \dfrac{1}{F_{\alpha}(n_1,n_2)},\ +\infty \right )$|$\left ( \dfrac{S_1^2}{S_2^2} \dfrac{1}{F_{\alpha}(n_1-1,n_2-1)},\ +\infty \right )$|
|单侧 2|$\left (0 ,\ \dfrac{n_2\displaystyle\sum\limits_{i=1}^{n_1} (X_i -\mu_1)^2}{n_1\displaystyle\sum\limits_{i=1}^{n_2} (Y_i -\mu_2)^2} F_{\alpha}(n_2,n_1) \right )$|$\left (0 ,\ \dfrac{S_1^2}{S_2^2} F_{\alpha}(n_2-1,n_1-1) \right )$|

### 0-1 分布总体参数

设总体 $X \sim B(1,p)$，$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本（需要满足 $n>50$，为大样本），样本均值为 $\overline{X}$。

由中心极限定理，

$$
\frac{\displaystyle\sum\limits_{i=1}^{n} X_i-np}{\sqrt{np(1-p)}} = \frac{n\overline{X}-np}{\sqrt{np(1-p)}}
$$

近似服从 $N(0,1)$，求得参数 $p$ 的置信水平为 $1-\alpha$ 的置信区间为

$$
\left ( \frac{1}{2a} \left (-b-\sqrt{b^2-4ac} \right ),\ \frac{1}{2a} \left (-b+\sqrt{b^2-4ac} \right ) \right )
$$

其中 $a=n+z_{\alpha/2}^2$，$b=-(2n\overline{X}+z_{\alpha/2}^2)$，$c=n\overline{X}^2$。

## 估计量的评选标准

设 $X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，$\theta \in \Theta$ 为包含在总体 $X$ 的分布中的未知参数。

### 无偏性

设 $\hat{\theta}=\hat{\theta}(X_1,X_2,\cdots,X_n)$ 是 $\theta$ 的估计量。如果 $\forall\theta \in \Theta$，有

$$
E\hat{\theta}=\theta
$$

则称 $\hat{\theta}$ 为 $\theta$ 的**无偏估计量**。

- 以 $\hat{\theta}$ 作为 $\theta$ 的估计的系统误差：$E(\hat{\theta}-\theta)$。
- 无偏估计：无系统误差。

### 有效性

设 $\hat{\theta}_1=\hat{\theta}_1(X_1,X_2,\cdots,X_n)$ 与 $\hat{\theta}_2=\hat{\theta}_2(X_1,X_2,\cdots,X_n)$ 都是 $\theta$ 的无偏估计量。如果 $\forall\theta \in \Theta$，有

$$
D\hat{\theta}_1<D\hat{\theta}_2
$$

则称 $\hat{\theta}_1$ 较 $\hat{\theta}_2$ **有效**。

### 一致性（相合性）

设 $\hat{\theta}_n=\hat{\theta}_n(X_1,X_2,\cdots,X_n)$ 是 $\theta$ 的估计量。如果 $\forall\theta \in \Theta$

$$
\hat{\theta}_n \overset{P}{\longrightarrow} \theta, \  n \to \infty
$$

则称 $\hat{\theta}_n$ 是 $\theta$ 的**一致（相合）估计量**。

!!! note

    - 如果估计量不具有一致性（相合性），那么不论将样本容量 $n$ 取多大，都不能将参数 $\theta$ 估计得足够准确。这样的估计量是不可取的。
    - 矩估计量都是相合估计量。
