---
date: 2025-01-01T01:05:10
---

# NeRF

Neural Radiance Fields.

## 简化体渲染公式

完整的 [[体渲染#Volume Rendering Equation|体渲染公式]] 太复杂，需要进行适当地简化。令 $\tau_a=\tau_s=\sigma, L_e+L_s=C$，并忽略 $L_0$ 一项，方程简化为

$$
L(s)=\int_0^s T(v) \sigma(v) C(v) \mathrm{d}v
$$

其中

$$
T(v)=e^{-\displaystyle\int_v^s 2\sigma(u)\mathrm{d}u}
$$

## Positional Encoding

## Hierarchical Sampling
