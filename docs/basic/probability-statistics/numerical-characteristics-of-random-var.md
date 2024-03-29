# 随机变量的数字特征

!!! abstract

    数学期望、方差、协方差。

## 数学期望

设 $X$ 是离散型随机变量，其分布律为

$$
P \left(X=x_i \right) = p_i \ , \  i=1,2, \cdots
$$

如果级数 $\displaystyle\sum\limits_{i} x_ip_i$ 绝对收敛，则称其为 $X$ 的数学期望、均值，记为 $EX$ 或 $E(X)$。

## 方差

$$
DX = EX^2 - (EX)^2
$$

## 协方差

$$
\mathrm{cov}(X,Y)=E(XY)-EX \cdot EY
$$

## 相关系数

$$
\rho_{XY}=\frac{\mathrm{cov}(X,Y)}{\sqrt{DX}\sqrt{DY}}
$$

相关系数表示两个随机变量间的**线性关系**的程度。

- 相互独立 $\Leftrightarrow$ 没有任何关系 $\Rightarrow$ 不相关。
- 相关 $\Rightarrow$ 存在线性关系 $\Rightarrow$ 不独立。
- 不相关 $\Rightarrow$ 没有线性关系，但可能有其他关系 $\Rightarrow$ 不一定独立。

## 常见分布的期望和方差

|分布|$EX$|$DX$|
|:-|:-|:-|
|0-1分布|$p$|$p(1-p)$|
|二项分布|$np$|$np(1-p)$|
|泊松分布|$\lambda$|$\lambda$|
|均匀分布|$\dfrac{a+b}{2}$|$\dfrac{(b-a)^2}{12}$|
|指数分布|$\dfrac{1}{\lambda}$|$\dfrac{1}{\lambda^2}$|
|正态分布|$\mu$|$\sigma^2$|
|卡方分布|$n$|$2n$|
|t 分布|$0$|$\dfrac{n}{n-2}$|
