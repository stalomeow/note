# 多元微积分

!!! abstract

    多元微积分相关。

## Nabla 算子（Del 算子）

$\nabla$ 叫 Nabla 算子、Del 算子，是一个 n 维向量微分算子。三维情况下，可以表示为

$$
\nabla = \frac{\partial}{\partial x} \mathbf{i} + \frac{\partial}{\partial y} \mathbf{j} + \frac{\partial}{\partial z} \mathbf{k}
$$

它实际上不是一个向量，但是用的时候可以看成向量。

## 散度 Divergence

$$
\mathbf{div} \ \mathbf{F}(\mathbf{x_0}) = \lim_{V \to 0} \frac{1}{\left | V \right | } \oint_{S(V)} \mathbf{F} \cdot \mathrm{d}\mathbf{S}
$$

可以记为

$$
\nabla \cdot \mathbf{F} = \mathbf{div} \ \mathbf{F}
$$
