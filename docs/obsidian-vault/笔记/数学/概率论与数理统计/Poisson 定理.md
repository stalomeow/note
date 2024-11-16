---
date: 2024-04-25T13:31:35
---

# Poisson 定理

设 $\lambda > 0$ 是一个常数，$n$ 是任意的正整数，$np=\lambda$，则对任一固定的非负整数 $k$，有

$$
\lim_{n \to \infty} C_{n}^{k} p^k \left(1-p \right)^{n-k}=\frac{\lambda^k}{k!} e^{-\lambda}
$$

当 $n$ 充分大、$p$ 充分小时，可以用来近似计算 [[二项分布]]。一般 $n \ge 20$，$p \le 0.05$ 时，效果较好。
