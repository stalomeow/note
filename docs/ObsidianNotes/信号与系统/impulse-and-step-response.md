# 冲激响应和阶跃响应

## 冲激响应

激励为 $\delta(t)$ 时，系统的零状态响应，记作 $h(t)$。

$$
h(t) \coloneq T[\{0\}, \delta(t)]
$$

对 LTI 系统，微分方程等号右边只有 $f(t)=\delta(t)$ 时

$$
\left\{\begin{array}{l}
  h^{(n)}(t) + a_{n-1}h^{(n-1)}(t) + \cdots + a_0h(t)=\delta(t) \\
  h^{(j)}(0_-)=0, \  j=0,1,2,\cdots,n-1
\end{array}\right.
$$

可得 $0_+$ 时的初始值

$$
\left\{\begin{array}{l}
  h^{(j)}(0_+)=0, \  j=0,1,2,\cdots,n-2 \\
  h^{(n-1)}(0_+)=1
\end{array}\right.
$$

$t>0$ 时，微分方程可以写成 

$$
h^{(n)}(t) + a_{n-1}h^{(n-1)}(t) + \cdots + a_0h(t)=0
$$

设 $H(x)$ 是齐次解，则

$$
h(t)=H(t)\varepsilon(t)
$$

## 阶跃响应

激励为 $\varepsilon(t)$ 时，系统的零状态响应，记作 $g(t)$。

$$
g(t) \coloneq T[\{0\}, \varepsilon(t)]
$$

对 LTI 系统，微分方程等号右边只有 $f(t)=\varepsilon(t)$ 时

$$
\left\{\begin{array}{l}
  g^{(n)}(t) + a_{n-1}g^{(n-1)}(t) + \cdots + a_0g(t)=\varepsilon(t) \\
  g^{(j)}(0_-)=0, \  j=0,1,2,\cdots,n-1
\end{array}\right.
$$

可得 $0_+$ 时的初始值

$$
g^{(j)}(0_+)=0, \  j=0,1,2,\cdots,n-1
$$

$t>0$ 时，微分方程可以写成 

$$
g^{(n)}(t) + a_{n-1}g^{(n-1)}(t) + \cdots + a_0g(t)=1
$$

特解是常数 $\dfrac{1}{a_0}$。设 $G(x)$ 是齐次解，则

$$
g(t)=\left (G(t) + \frac{1}{a_0} \right ) \varepsilon(t)
$$

## 两者的关系

在 LTI 系统中

$$
h(t)=\ddx[t]{g(t)}
$$

$$
g(t)=\int_{-\infty}^{t}h(\tau)\mathrm{d}\tau
$$
