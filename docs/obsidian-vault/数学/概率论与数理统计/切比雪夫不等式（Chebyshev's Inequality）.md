---
slug: "20240421212800"
date: "2024-04-21"
---

# 切比雪夫不等式（Chebyshev's Inequality）


设 $X$ 是随机变量，如果 $EX$、$DX$ 存在，则 $\forall \varepsilon > 0$，有

$$
P \left ( \left | X-EX \right | \ge \varepsilon \right ) \le \frac{DX}{\varepsilon^2}
$$

也可以写成

$$
P \left ( \left | X-EX \right | < \varepsilon \right ) \ge 1 - \frac{DX}{\varepsilon^2}
$$

注意：

- 如果 $X$ 是离散型随机变量，注意 $P$ 括号里的不等号，必须是 $\ge$ 或 $<$。
- 这个估计比较粗糙。在估计一些值的上下界时，尽量用 [[中心极限定理（Central limit theorem）]]。
