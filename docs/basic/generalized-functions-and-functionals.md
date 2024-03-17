# 广义函数和泛函

!!! abstract

    学信号与系统时涉及了这些内容。我没有系统地学过相关内容，只是简单记录一下基本的常识。

## 函数空间（Function Space）

如果把某一类函数集（连续函数集、可微函数集等）中的每个函数看成是空间中的一个点，这类函数的全体就构成一个函数空间（连续函数空间、可微函数空间等）。

## 泛函（Functional）

泛函是将函数映射到一个数的映射，通常在函数空间中定义。泛函可以看作是一类函数的函数，它将一个函数映射到一个数值，或者更一般地，将函数映射到另一个函数。例如，函数积分就是一个泛函，它将一个函数映射到其在某个区间上的积分值。

## 广义函数（Generalized Function）

广义函数是对普通函数的推广，通常是指在分布理论中使用的对象，也称为分布（Distribution）。它们被用来表示某些非典型函数或者非常规的对象，如 Dirac Delta 函数等。

广义函数是通过它们作用于其他函数的积分来定义的，并不是传统意义上的函数。

大概就是，选择一类性能良好的函数 $\varphi(t)$ 称为检验函数（Test Function），它们构成了一个检验函数空间 $\varPhi$，一个广义函数 $g(t)$ 赋予每个 $\varphi(t) \in \varPhi$ 一个数值 $N$，该数与广义函数 $g(t)$ 和检验函数 $\varphi(t)$ 有关，记作 $N[g(t),\varphi(t)]$。一般可以写为

$$
N[g(t),\varphi(t)]=\int_{-\infty}^{+\infty} g(t)\varphi(t)\mathrm{d}t
$$

也可以写成泛函的形式

$$
J_g[\varphi]=\int_{-\infty}^{+\infty} g(t)\varphi(t)\mathrm{d}t
$$

泛函 $J_g[\varphi]$ 把每个 $\varphi(t) \in \varPhi$ 映射到一个数。

## 广义函数相等

$\forall \varphi(t) \in \varPhi$，如果两个广义函数 $f(t),g(t)$ 满足

$$
\int_{-\infty}^{+\infty} f(t)\varphi(t)\mathrm{d}t=\int_{-\infty}^{+\infty} g(t)\varphi(t)\mathrm{d}t
$$

则 $f(t)=g(t)$。

$f(t)$ 和 $g(t)$ 可能有有限个点是不一样的。
