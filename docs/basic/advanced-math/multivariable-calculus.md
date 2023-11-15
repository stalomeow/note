# 多元微积分

!!! abstract

    多元微积分相关。

## Nabla 算子（Del 算子）

$\nabla$ 叫 Nabla 算子、Del 算子，是一个 n 维向量微分算子。三维直角坐标系中，可以表示为

$$
\nabla = \frac{\partial}{\partial x} \vec{i} + \frac{\partial}{\partial y} \vec{j} + \frac{\partial}{\partial z} \vec{k}
$$

它实际上不是一个向量，但是用的时候可以看成向量。

## 梯度

## 散度 Divergence

设 $\vec{F}$ 为一个向量场。

$$
\mathbf{div} \ \vec{F} = \lim_{V \to 0} \frac{1}{\left | V \right | } \oiint_{\partial V} \vec{F} \cdot \mathrm{d}\vec{S}
$$

$\partial V$ 是体积 $V$ 的表面，是一个闭曲面。

散度就是穿过闭曲面通量的体密度，是一个标量。它描述向量场里一个点是汇聚点还是发源点，形象地说，就是包含这一点的一个微小体元中的向量是 ⌈向外⌋ 居多还是 ⌈向内⌋ 居多。

在三维直角坐标系中

$$
\mathbf{div} \ \vec{F} = \nabla \cdot \vec{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}
$$

高斯散度定理（高斯公式）

$$
\oiint_{\partial V} \vec{F} \cdot \mathrm{d}\vec{S} = \iiint_V ( \nabla \cdot \vec{F} ) \mathrm{d}V
$$

穿过闭曲面的通量等于其内部体积微元的散度之和。

## 旋度 Curl/Rotor

设 $\vec{F}$ 为一个向量场。

$$
(\mathbf{curl} \ F) \cdot \vec{n} = \lim_{S \to 0} \frac{1}{\left | S \right | } \oint_{\partial S} F \cdot \mathrm{d}\vec{l}
$$

$\partial S$ 是面 $S$ 的边界，是一条闭合的曲线。$\vec{n}$ 是面的单位法向量。$\partial S$ 和 $\vec{n}$ 的方向满足右手定则。

旋度就是环量的面密度，是一个向量。它描述三维欧几里德空间中的向量场的无穷小量旋转，刻画了一个点上的旋转。它的方向是旋转的轴（右手定则确定），大小是旋转的量。它在方向 $\vec{n}$ 上的投影大小表示在这个方向上的环量面密度大小，旋度方向的环量面密度最大。

- 旋度为零的向量场叫做无旋向量场、保守场。

在三维直角坐标系中

$$
\mathbf{curl} \ \vec{F} = \nabla \times \vec{F} =
\begin{vmatrix}
  \vec{i}& \vec{j}& \vec{k} \\
  \frac{\partial}{\partial x}& \frac{\partial}{\partial y}& \frac{\partial}{\partial z} \\
  F_x& F_y& F_z \\
\end{vmatrix}
$$

展开后就是

$$
\left (\frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z}, \  \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x}, \  \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right )^T
$$

旋度定理（斯托克斯公式）

$$
\oint_{\partial S} F \cdot \mathrm{d}\vec{l} = \iint_S ( \nabla \times \vec{F} ) \cdot \mathrm{d}\vec{S}
$$

区域边界的环量等于其面积微元的旋度之和。$\partial S$ 的方向由右手定则确定。
