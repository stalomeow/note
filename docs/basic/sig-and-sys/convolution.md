# 卷积

## 定义

$$
(f_1 * f_2)(t) \coloneq \int_{-\infty}^{+\infty} f_1(\tau)f_2(t-\tau) \mathrm{d}\tau
$$

## 性质

- 交换律 $f_1 * f_2 = f_2 * f_1$
- 分配率 $f_1 * (f_2 + f_3) = (f_1 * f_2) + (f_1 * f_3)$
- 结合律 $f_1 * (f_2 * f_3) = (f_1 * f_2) * f_3$
- $f * \delta = f$

### 时移

### 微积分

$$
f^{(-1)}(t) \coloneq \int_{-\infty}^{t} f(\tau) \mathrm{d}\tau
$$

若 $f = f_1 * f_2$ 则

$$
f' = f_1' * f_2 = f_1 * f_2'
$$

## 杜阿密尔积分

在 LTI 系统中，若激励为 $f(t)$ 则零状态响应

$$
y_{zs}(t)=f(t)*h(t)=f'(t)*g(t)
$$

## 图解法计算卷积

## 常用卷积

|$f_1$|$f_2$|$f_1*f_2$|
|:-:|:-:|:-:|
|$f(t)$|$\varepsilon(t)$|$\displaystyle\int_{-\infty}^{t} f(\tau) \mathrm{d}\tau$|
|$\varepsilon(t)$|$\varepsilon(t)$|$t\varepsilon(t)$|
|$t\varepsilon(t)$|$\varepsilon(t)$|$\dfrac{1}{2}t^2\varepsilon(t)$|
|$e^{-\alpha t}\varepsilon(t)$|$\varepsilon(t)$|$\dfrac{1}{\alpha}(1-e^{-\alpha t})\varepsilon(t)$|
|$e^{-\alpha t}\varepsilon(t)$|$e^{-\alpha t}\varepsilon(t)$|$te^{-\alpha t}\varepsilon(t)$|
|$te^{-\alpha t}\varepsilon(t)$|$e^{-\alpha t}\varepsilon(t)$|$\dfrac{1}{2}t^2e^{-\alpha t}\varepsilon(t)$|
