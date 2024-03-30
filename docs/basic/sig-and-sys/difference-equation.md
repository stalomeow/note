# 差分方程

## 移位序列

称

$$
\cdots, f(k+2), f(k+1), \cdots, f(k-1), f(k-2), \cdots
$$

为 $f(k)$ 的移位序列。

## 差分

$\Delta$ 和 $\nabla$ 称为差分算子。差分对应连续信号的微分。

- 一阶前向差分：$\Delta f(k) \coloneq f(k+1)-f(k)$
- 一阶后向差分：$\nabla f(k) \coloneq f(k)-f(k-1)$
- 关系：$\nabla f(k)=\Delta f(k-1)$

前向与后向差分的性质相同，之后都采用后向差分。

- 线性性质：$\nabla[\alpha_1 f_1(k) + \alpha_2 f_2(k)] = \alpha_1 \nabla f_1(k) + \alpha_2 \nabla f_2(k)$
- 二阶差分：$\nabla^2 f(k) = f(k) - 2f(k-1) + f(k-2)$
- $n$ 阶差分：

    $$
    \nabla^n f(k) = \sum_{j=0}^{n} (-1)^j {n \choose j} f(k-j)
    $$

## 求和

序列 $f(k)$ 的求和运算，对应连续信号的积分。

$$
\sum_{i=-\infty}^{k} f(i)
$$

## 差分方程

一般形式

$$
F[k, y(k), \nabla y(k), \cdots, \nabla^n y(k)] = 0
$$

差分的最高阶为 $n$ 阶，所以称为 $n$ 阶差分方程。各阶差分可以写成 $y(k)$ 的移位序列的线性组合，所以差分方程也可以写为

$$
G[k, y(k), y(k-1), \cdots, y(k-n)] = 0
$$

本质上是递推的代数方程，若已知初始条件和激励，可用迭代法求数值解。

---

对单输入-单输出的 LTI 系统，若激励为 $f(k)$，全响应为 $y(k)$，则其数学模型一般为 $n$ 阶常系数线性差分方程

$$
y(k) + a_{n-1} y(k-1) + \cdots + a_0 y(k-n) = b_m f(k) + b_{m-1} f(k-1) + \cdots + b_0 f(k-m)
$$

### 齐次解（自由响应）

由特征方程

$$
\lambda^n + a_{n-1} \lambda^{n-1} + \cdots + a_1 \lambda + a_0 = 0
$$

求得 $n$ 个特征根。

|特征根 $\lambda$|齐次解中的对应项|
|:-:|:-:|
|单实根|$C\lambda^k$|
|$r$ 重实根|$\lambda^k \displaystyle\sum\limits_{i=0}^{r-1} C_i k^i$|
|一对共轭复根||
|$r$ 重共轭复根||

### 特解（强迫响应）

|激励 $f(k)$|特解形式|
|:-:|:-:|
|$k^m$|$k^r \displaystyle\sum\limits_{i=0}^{m} P_i k^i$，$r$ 为特征根中等于 $1$ 的数量|
|$a^k$|$a^k \displaystyle\sum\limits_{i=0}^{r} P_i k^i$，$r$ 为特征根中等于 $a$ 的数量|
|$\cos(\beta k)$ 或 $\sin(\beta k)$|$P\cos(\beta k) + Q\sin(\beta k)$，所有特征根都不等于 $e^{\pm j\beta}$|

### 零输入响应

$$
y_{zi}(k) + a_{n-1} y_{zi}(k-1) + \cdots + a_0 y_{zi}(k-n) = 0
$$

如果激励在 $k=0$ 时接入，则初始状态

- $y_{zi}(-1)=y(-1)$
- $y_{zi}(-2)=y(-2)$
- $\cdots$
- $y_{zi}(-n)=y(-n)$

因为是*零输入*，所以可以直接把他们当初始值，没必要再算 $y_{zi}(0), y_{zi}(1)$ 等值。

最后记得乘 $\varepsilon(k)$。

### 零状态响应

$$
\left\{\begin{array}{l}
y_{zs}(k) + a_{n-1} y_{zs}(k-1) + \cdots + a_0 y_{zs}(k-n) = b_m f(k) + b_{m-1} f(k-1) + \cdots + b_0 f(k-m)\\
y_{zs}(-1)=y_{zs}(-2)=\cdots=y_{zs}(-n)=0
\end{array}\right.
$$

根据递推，可求出初始值 $y_{zs}(0),y_{zs}(1),\cdots,y_{zs}(n-1)$。

最后记得乘 $\varepsilon(k)$。

### 全响应

它有两种分解方式

- 自由响应 + 强迫响应
- 零输入响应 + 零状态响应
