---
slug: "240422184035"
date: 2024-04-22
---

# 散度（Divergence）

设 $\vec{F}$ 为一个向量场。

$$
\mathbf{div} \ \vec{F} = \lim_{V \to 0} \frac{1}{\left | V \right | } \iint_{\partial V} \vec{F} \cdot \mathrm{d}\vec{S}
$$

$\partial V$ 是体积 $V$ 的表面，是一个 ==闭曲面==。

散度就是穿过闭曲面通量的体密度，是一个标量。它描述向量场里一个点是汇聚点还是发源点，形象地说，就是包含这一点的一个微小体元中的向量是 ⌈向外⌋ 居多还是 ⌈向内⌋ 居多。

在三维直角坐标系中

$$
\mathbf{div} \ \vec{F} = \nabla \cdot \vec{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}
$$

## 高斯散度定理 

即高斯公式。

$$
\iint_{\partial V} \vec{F} \cdot \mathrm{d}\vec{S} = \iiint_V ( \nabla \cdot \vec{F} ) \mathrm{d}V
$$

穿过闭曲面的通量等于其内部体积微元的散度之和。