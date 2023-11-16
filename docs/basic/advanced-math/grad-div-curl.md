# 梯度、散度、旋度

!!! abstract

    梯度、散度、旋度和相关定理。

## Nabla 算子

$\nabla$ 叫 Nabla 算子、Del 算子，是一个 n 维向量微分算子。三维直角坐标系中，可以表示为

$$
\nabla = \frac{\partial}{\partial x} \vec{i} + \frac{\partial}{\partial y} \vec{j} + \frac{\partial}{\partial z} \vec{k}
$$

它实际上不是一个向量，但是用的时候可以看成向量。

## 梯度 Gradient

设 $f$ 为一个标量场。

梯度 $\mathbf{grad} \ f$ 是一个向量。它的方向是该点处 $f$ 的最大增长方向。它的大小是这个方向的增长率，是该点处所有方向导数的最大值。

在三维直角坐标系中

$$
\mathbf{grad} \ f = \nabla f = \left (\frac{\partial f}{\partial x}, \  \frac{\partial f}{\partial y}, \  \frac{\partial f}{\partial z} \right)^T
$$

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

高斯散度定理（Gauss's theorem 高斯公式）

$$
\oiint_{\partial V} \vec{F} \cdot \mathrm{d}\vec{S} = \iiint_V ( \nabla \cdot \vec{F} ) \mathrm{d}V
$$

穿过闭曲面的通量等于其内部体积微元的散度之和。

## 旋度 Curl

设 $\vec{F}$ 为一个向量场。

$$
(\mathbf{curl} \ F) \cdot \vec{n} = \lim_{S \to 0} \frac{1}{\left | S \right | } \oint_{\partial S^+} F \cdot \mathrm{d}\vec{l}
$$

$\partial S^+$ 是面 $S$ 的正向边界，是一条闭合的曲线。$\vec{n}$ 是面 $S$ 的单位法向量。$\partial S^+$ 和 $\vec{n}$ 的方向满足右手定则。有时候 $\mathbf{curl} \ F$ 也写成 $\mathbf{rot} \ F$。

旋度就是环量的面密度，是一个向量。它刻画了三维向量场中一个点上的旋转。它的方向是旋转的轴（右手定则确定），大小是旋转的量。它在方向 $\vec{n}$ 上的投影大小表示在这个方向上的环量面密度大小，旋度方向的环量面密度最大。

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

旋度定理（Stokes' theorem 斯托克斯公式）

$$
\oint_{\partial \Sigma^+} F \cdot \mathrm{d}\vec{l} = \iint_\Sigma ( \nabla \times \vec{F} ) \cdot \mathrm{d}\vec{S}
$$

区域边界的环量等于区域面积微元的旋度之和。$\partial \Sigma^+$ 的方向和 $\Sigma$ 的正向满足右手定则。

二维情况下，就是格林公式（Green's theorem）

$$
\oint_{\partial \Sigma^+} P\mathrm{d}x + Q\mathrm{d}y = \iint_\Sigma \left (\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right ) \mathrm{d}x\mathrm{d}y
$$

## 梯无旋，旋无散

- 梯度场的旋度为零，$\nabla \times (\nabla f) \equiv 0$。
- 旋度场的散度为零，$\nabla \cdot (\nabla \times \vec{F}) \equiv 0$。

## 特殊的场

- 旋度为零的向量场是 无旋场/保守场/有势场，比如重力场、静电场。
- 散度为零的向量场是 无散场/无源场/管形场，比如磁场、涡旋电场。
- 无散且无旋的向量场是 调和场。

## Laplace 算子

$$
\Delta = \nabla^2 = \nabla \cdot \nabla = \frac{\partial^2}{\partial x^2} \vec{i} + \frac{\partial^2}{\partial y^2} \vec{j} + \frac{\partial^2}{\partial z^2} \vec{k}
$$

可用 Laplace 算子对梯度求散度

$$
\nabla \cdot (\nabla f) = \Delta f
$$
