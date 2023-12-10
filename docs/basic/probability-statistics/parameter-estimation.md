---
tags:
  - 数理统计
---

# 参数估计

!!! abstract

    点估计、置信区间。

## 点估计

设总体 $X$ 的分布函数 $F(x;\theta_1,\theta_2,\cdots,\theta_k)$ 的形式已知，其中 $\theta_1,\theta_2,\cdots,\theta_k$ 为未知的参数。$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，$x_1,x_2,\cdots,x_n$ 是样本的一组样本值。若统计量 $\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ ($i=1,2,\cdots,k$) 能对参数 $\theta_i$ ($i=1,2,\cdots,k$) 作估计，则称之为 $\theta_i$ 的点估计。

- 称 $\hat{\theta}_i(X_1,X_2,\cdots,X_n)$ 为 $\theta_i$ 的**点估计量**。它是一个随机变量。
- 称 $\hat{\theta}_i(x_1,x_2,\cdots,x_n)$ 为 $\theta_i$ 的**点估计值**。它是随机变量的取值。
- 在不致混淆的情况下，点估计量和点估计值统称为点估计。

### 矩估计法

> 受 Khintchine LLN 启发，用样本矩的连续函数作为相应的总体矩的连续函数的估计量。

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

简单讲就是：用样本的各阶原点矩作为总体的各阶原点矩的估计。有几个参数就列几个方程（矩的阶数最好从小到大依次写，别跳），然后把参数求出来。

### 最大似然估计法

设总体 $X$ 的分布形式 $p(x;\theta)$（分布律/概率密度）为已知，其中 $\theta \in \Theta$ 为未知参数。$X_1,X_2,\cdots,X_n$ 为来自总体 $X$ 的一个样本，$x_1,x_2,\cdots,x_n$ 是样本的一组样本值，

- 称 $L(\theta)=\displaystyle\prod\limits_{i=1}^{n}p(x_i;\theta)$ 为参数 $\theta$ 的**似然函数**。

    若总体是离散型随机变量，它的意义是随机点 $(X_1,X_2,\cdots,X_n)$ 落在**样本点** $(x_1,x_2,\cdots,x_n)$ 的概率。若总体是连续型随机变量，则是落在该点**附近**的概率。

- 称能使 $L(\theta)$ 取得最大值的 $\hat{\theta}(x_1,x_2,\cdots,x_n)$ 为 $\theta$ 的最大似然估计。
    - 称 $\hat{\theta}(X_1,X_2,\cdots,X_n)$ 为 $\theta$ 的**最大似然估计量**。
    - 称 $\hat{\theta}(x_1,x_2,\cdots,x_n)$ 为 $\theta$ 的**最大似然估计值**。

最大似然估计法的思想是，固定 $x_1,x_2,\cdots,x_n$，然后找到一个 $\hat{\theta}$ 使得 $L(\theta)$ 取得最大值。求解步骤：

1. 写出似然函数：$L(\theta)=\displaystyle\prod\limits_{i=1}^{n} p(x_i;\theta)$。
2. 取自然对数，方便求导：$\ln L(\theta)=\displaystyle\sum\limits_{i=1}^{n} \ln p(x_i;\theta)$。
3. 令 $\dfrac{\partial \ln L(\theta)}{\partial \theta_i}=0$ ($i=1,2,\cdots,k$)，解得 $\hat{\theta}_i=\hat{\theta}_i(x_1,x_2,\cdots,x_n)$ ($i=1,2,\cdots,k$)。
