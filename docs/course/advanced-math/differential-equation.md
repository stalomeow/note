# 微分方程

!!! abstract

    记录微分方程的相关概念和常见的解法。

- **微分方程：**表示未知函数、未知函数的导数与自变量之间的关系的方程。
- **微分方程的阶：**微分方程中出现的未知函数的最高阶导数的阶数。
    - **高阶：**二阶及以上。
- **微分方程的解：**带入微分方程后能使该方程成为恒等式的函数。
    - **隐式解：**函数为隐函数。
- **微分方程的通解：**含有任意常数，且任意常数的个数等于微分方程的阶的解。
    - **隐式通解：**解为隐式解。
- **微分方程的特解：**确定了任意常数的通解。
- **微分方程的积分曲线：**微分方程的解的图形（这个图形是一条曲线）。
- **初值条件：**用来确定通解中的任意常数的条件。
- **初值问题：**求微分方程满足一定初值条件的特解的问题。

## 分离变量

如果一阶微分方程可以写成

$$
g(y)\,\mathrm{d}y = f(x)\,\mathrm{d}x
$$

的形式，那么它称为<ins>可分离变量的微分方程</ins>，两边积分就能求解。

$$
\int g(y)\,\mathrm{d}y = \int f(x)\,\mathrm{d}x
$$

## 齐次方程

如果一阶微分方程可以写成

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} = \varphi(\dfrac{y}{x})
$$

的形式，那么它称为<ins>齐次方程</ins>。令

$$
u = \dfrac{y}{x}
$$

则有

$$
y = ux,\ \dfrac{\mathrm{d}y}{\mathrm{d}x} = u + x\dfrac{\mathrm{d}u}{\mathrm{d}x}
$$

代入原方程可得

$$
u + x\dfrac{\mathrm{d}u}{\mathrm{d}x} = \varphi(u)
$$

分离变量即可求解。

## 转化为齐次

方程

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} = f(\dfrac{ax + by + c}{a_1x + b_1y + c_1})
$$

当 $c = c_1 = 0$ 时是齐次方程

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} = \varphi(\dfrac{y}{x})
$$

其中

$$
\varphi(x) = f(\dfrac{a + bx}{a_1 + b_1x})
$$

---

当它非齐次时，如果

$$
\dfrac{a_1}{a} = \dfrac{b_1}{b} = \lambda
$$

那么原方程可以写成

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} = f(\dfrac{ax + by + c}{\lambda(ax + by) + c_1})
$$

的形式。此时，令

$$
v = ax + by
$$

带入原方程得

$$
\dfrac{1}{b}(\dfrac{\mathrm{d}v}{\mathrm{d}x} - a) = f(\dfrac{v + c}{\lambda v + c_1})
$$

分离变量即可求解。

---

如果

$$
\dfrac{a_1}{a} \ne \dfrac{b_1}{b}
$$

可以令

$$
x = X + h,\ y = Y + k
$$

其中 $h$ 和 $k$ 是待定的常数。于是

$$
\mathrm{d}x = \mathrm{d}X,\ \mathrm{d}y = \mathrm{d}Y
$$

方程变为

$$
\dfrac{\mathrm{d}Y}{\mathrm{d}X} = f(\dfrac{aX + bY + ah + bk + c}{a_1X + b_1Y + a_1h + b_1k + c_1})
$$

解方程组

$$
\left\{\begin{matrix}
  ah + bk + c = 0 \\
  a_1h + b_1k + c_1 = 0
\end{matrix}\right.
$$

解得 $h$ 和 $k$ 的值后代入可得齐次方程

$$
\dfrac{\mathrm{d}Y}{\mathrm{d}X} = f(\dfrac{aX + bY}{a_1X + b_1Y})
$$


## 降阶

对于微分方程

$$
y^{(n)} = f(x)
$$ 

只需要两边连续积分 $n$ 次就能求出通解。

---

对于微分方程

$$
y'' = f(x, y')
$$

设

$$
y' = p
$$

原方程就变为一个一阶微分方程

$$
p' = f(x, p)
$$

---

对于微分方程

$$
y'' = f(y, y')
$$

设

$$
y' = p
$$

那么

$$
y'' = \dfrac{\mathrm{d}p}{\mathrm{d}x} = \dfrac{\mathrm{d}p}{\mathrm{d}y} \cdot \dfrac{\mathrm{d}y}{\mathrm{d}x} = p \dfrac{\mathrm{d}p}{\mathrm{d}y}
$$

原方程就变为一个关于 $y, p$ 的一阶微分方程

$$
p \dfrac{\mathrm{d}p}{\mathrm{d}y} = f(y, p)
$$

## 线性微分方程

$$
y^{(n)} + a_1(x)y^{(n - 1)} + \cdots + a_{n - 1}(x)y' + a_n(x)y = f(x)
$$

- **线性：**方程对于未知函数 $y$ 及其导数是一次方程。
- **齐次：** $f(x) \equiv 0$ 。

### 解的结构

**定理：**如果函数 $y_1(x)$ 与 $y_2(x)$ 是二阶齐次线性方程

$$
y'' + P(x)\,y' + Q(x)\,y = 0
$$

的两个解，那么

$$
y = C_1\,y_1(x) + C_2\,y_2(x)
$$

也是方程的解，其中 $C_1, C_2$ 是任意常数。当且仅当 $y_1(x)$ 与 $y_2(x)$ 线性无关时，上式为方程的通解。

!!! info "函数组的线性相关/无关"

    设 $y_1(x), y_2(x), \cdots, y_n(x)$ 为定义在区间 $I$ 上的 $n$ 个函数，如果存在 $n$ 个不全为零的常数 $k_1, k_2, \cdots, k_n$ ，使得当 $x \in I$ 时有恒等式

    $$
    k_1\,y_1 + k_2\,y_2 + \cdots + k_n\,y_n \equiv 0
    $$

    成立，那么称这 $n$ 个函数在区间 $I$ 上**线性相关**；否则称为**线性无关**。

---

**推论：**如果 $y_1(x), y_2(x), \cdots, y_n(x)$ 是 $n$ 阶齐次线性方程

$$
y^{(n)} + a_1\,y^{(n-1)} + \cdots + a_{n-1}\,y' + a_n\,y = 0
$$

的 $n$ 个线性无关的解，那么，此方程的通解为

$$
y = C_1\,y_1(x) + C_2\,y_2(x) + \cdots + C_n\,y_n(x)
$$

其中 $C_1, C_2, \cdots, C_n$ 为任意常数。

---

**定理（可推广到 $n$ 阶）：**设 $y^*(x)$ 是二阶非齐次线性方程

$$
y'' + P(x)\,y' + Q(x)\,y = f(x)
$$

的一个特解。 $Y(x)$ 是对应齐次方程的通解，则

$$
y = Y(x) + y^*(x)
$$

是原方程的通解。

---

**定理（叠加原理，可推广到 $n$ 阶）：**对于二阶非齐次线性方程

$$
y'' + P(x)\,y' + Q(x)\,y = f_1(x) + f_2(x)
$$

如果 $y_1^*(x)$ 与 $y_2^*(x)$ 分别是方程

$$
y'' + P(x)\,y' + Q(x)\,y = f_1(x)
$$

与

$$
y'' + P(x)\,y' + Q(x)\,y = f_2(x)
$$

的特解，则 $y_1^*(x) + y_2^*(x)$ 就是原方程的特解。

### 特征方程法

这个方法可以用来求 $n$ 阶常系数齐次线性微分方程的通解。

!!! note "基本思想"

    由于 $y=e^{rx}$ 和它的各阶导数都只相差一个常数因子，所以希望找到合适的常数 $r$ 使该函数满足方程。找到 $n$ 个线性无关的特解后就能构造出通解。

对于二阶常系数齐次线性微分方程

$$
y'' + p\,y'+q\,y = 0
$$

其中 $p, q$ 为常数。可以按如下步骤求出通解：

1. 写出特征方程。

    $$
    r^2 + p\,r + q = 0
    $$

2. 求出特征方程的两个根 $r_1, r_2$。

3. 按下表写出通解。

|特征方程的根 $r_1, r_2$           |通解                                                       |
|:-------------------------------|:---------------------------------------------------------|
|两个不相等的实根                  |$y = C_1\,e^{r_1\,x} + C_2\,e^{r_2\,x}$                    |
|两个相等的实根                    |$y = (C_1 + C_2\,x)\,e^{r_1\,x}$                           |
|一对共轭复根 $\alpha\pm\beta\,i$ |$y = e^{\alpha\,x}\,(C_1\,\cos\beta\,x + C_2\,\sin\beta\,x)$|

---

**（推广）**对于 $n$ 阶常系数齐次线性微分方程

$$
y^{(n)} + p_1y^{(n - 1)} + \cdots + p_{n - 1}y' + p_ny = 0
$$

其中 $p_1, \cdots, p_{n - 1}, p_n$ 都为常数。可以按如下步骤求出通解：

1. 写出特征方程。

    $$
    r^n + p_1r^{n - 1} + \cdots + p_{n - 1}r + p_n = 0
    $$

2. 求出特征方程的 $n$ 个根 $r_1, \cdots, r_{n - 1}, r_n$。

3. 按下表写出通解。

|特征方程的根                                    |微分方程通解中的对应项                                                |
|:---------------------------------------------|:-----------------------------------------------------------------|
|单实根 $r$                                     |给出一项： $Ce^{rx}$                                                |
|一对单复根 $r_{1, 2} = \alpha\pm\beta\,i$       |给出两项： $e^{\alpha\,x}\,(C_1\,\cos\beta\,x + C_2\,\sin\beta\,x)$ |
| $k$ 重实根 $r$                                |给出 $k$ 项： $e^{rx}(C_1 + C_2x + \cdots + C_kx^{k - 1})$          |
|一对 $k$ 重复根 $r_{1, 2} = \alpha\pm\beta\,i$  |给出 $2k$ 项： $e^{\alpha\,x}\,\left[(C_1 + C_2x + \cdots + C_kx^{k - 1})\,\cos\beta\,x + (D_1 + D_2x + \cdots + D_kx^{k - 1})\,\sin\beta\,x\right]$|

### 常数变易法

这个方法可以用来求 $n$ 阶非齐次线性微分方程的通解。

!!! note "基本思想"

    将原方程对应的齐次方程的通解中的任意常数替换为新的未知函数，再回带到原方程确定未知函数，最终得到原方程的通解。

对于一阶非齐次线性微分方程

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = Q(x)
$$

对应的齐次方程

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = 0
$$

的通解为

$$
y = Ce^{-\int P(x)\,\mathrm{d}x}
$$

那么，可以令原方程的通解为

$$
y = u(x)e^{-\int P(x)\,\mathrm{d}x}
$$

于是

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} = u'e^{-\int P(x)\,\mathrm{d}x} - uP(x)e^{-\int P(x)\,\mathrm{d}x}
$$

带入原方程可得

$$
u' = Q(x)e^{\int P(x)\,\mathrm{d}x}
$$

两端积分后可得 $u(x)$ 。所以原方程通解为

$$
y = e^{-\int P(x)\,\mathrm{d}x}\left(\int Q(x)e^{\int P(x)\,\mathrm{d}x}\,\mathrm{d}x + C\right)
$$

其中 $C$ 为任意常数。

---

对于二阶非齐次线性微分方程

$$
y'' + P(x)y' + Q(x)y = f(x)
$$

如果已知对应的齐次方程

$$
y'' + P(x)y' + Q(x)y = 0
$$

的通解为

$$
Y(x) = C_1\,y_1(x) + C_2\,y_2(x)
$$

那么，可以令

$$
y = v_1(x)\,y_1(x) + v_2(x)\,y_2(x)
$$

接下来，需要解一个关于 $v_1', v_2'$ 的二元线性方程组

$$
\left\{\begin{matrix}
  y_1\,v_1' + y_2\,v_2' = 0 \\
  y_1'\,v_1' + y_2'\,v_2' = f
\end{matrix}\right.
$$

??? note "关于这个方程组"

    因为两个未知函数 $v_1$ 和 $v_2$ 只需使 $y$ 满足一个关系式（原方程），所以可以规定它们再满足一个关系式。由于

    $$
    y' = y_1v_1' + y_2v_2' + y_1'v_1 + y_2'v_2
    $$

    为了使 $y''$ 的表示中不含 $v_1''$ 和 $v_2''$ ，可以设

    $$
    y_1\,v_1' + y_2\,v_2' = 0
    $$

    在这个条件下，将 $y, y', y''$ 带入原方程可得

    $$
    y_1'\,v_1' + y_2'\,v_2' = f
    $$

如果系数行列式

$$
W =
\begin{vmatrix}
  y_1& y_2\\
  y_1'& y_2'
\end{vmatrix}
= y_1\,y_2' - y_1'\,y_2 \ne 0
$$

那么可以解得

$$
v_1' = -\dfrac{y_2\,f}{W}, v_2' = \dfrac{y_1\,f}{W}
$$

假设 $f(x)$ 连续，对上面两式积分可得 $v_1, v_2$。于是，原方程通解为

$$
y = C_1\,y_1 + C_2\,y_2 - y_1 \int \dfrac{y_2\,f}{W}\,\mathrm{d}x + y_2 \int \dfrac{y_1\,f}{W}\,\mathrm{d}x
$$

其中 $C_1, C_2$ 是任意常数。

### 待定系数法

这个方法可以用来求 $n$ 阶常系数非齐次线性微分方程的通解。

!!! note "基本思想"

    原方程对应的齐次方程的通解可以用特征方程求得，所以只需要猜出原方程的一个特解就能构造出通解。

对于二阶常系数非齐次线性微分方程

$$
y'' + py' + qy = f(x)
$$

其中 $p, q$ 是常数。设它的一个特解为 $y^*$。

如果

$$
f(x) = e^{\lambda\,x} \, P_m(x)
$$

其中 $\lambda$ 是常数， $P_m(x)$ 是 $x$ 的一个 $m$ 次多项式：

$$
P_m(x) = a_0x^m + a_1x^{m - 1} + \cdots + a_{m - 1}x + a_m
$$

那么可以设

$$
y^* = x^kR_m(x)e^{\lambda x}
$$

其中 $R_m(x)$ 是 $x$ 的一个 $m$ 次多项式，而 $k$ 的取值如下：

* $\lambda$ 不是特征方程的根， $k = 0$ 。
* $\lambda$ 是特征方程的单根， $k = 1$ 。
* $\lambda$ 是特征方程的重根， $k = 2$ 。

将 $y^*$ 带回原方程，对比系数就能求出该特解。

??? tip "推广"

    推广到 $n$ 阶后， $k$ 是特征方程含根 $\lambda$ 的重复次数。

    * 若 $\lambda$ 不是特征方程的根， $k = 0$ 。
    * 若 $\lambda$ 是特征方程的 $s$ 重根， $k = s$ 。

---

如果

$$
f(x) = e^{\lambda\,x} \, \left [P_l(x)\cos\omega\,x + Q_n(x)\sin\omega\,x \right ]
$$

其中

* $\lambda, \omega$ 是常数， $\omega \ne 0$ 。
* $P_l(x)$ 和 $Q_n(x)$ 分别是 $x$ 的 $l$ 次和 $n$ 次多项式。
* $P_l(x)$ 和 $Q_n(x)$ 中仅有一个可为零。 

那么可以设

$$
y^* = x^ke^{\lambda x}[R_m^{(1)}(x)\cos\omega\,x + R_m^{(2)}(x) \sin\omega\,x]
$$

其中 $R_m^{(1)}(x)$ 和 $R_m^{(2)}(x)$ 是 $x$ 的 $m$ 次多项式， $m = \max\{l, n\}$，而 $k$ 的取值如下：

* $\lambda + \omega\,i$ （或 $\lambda - \omega\,i$ ）不是特征方程的根， $k = 0$ 。
* $\lambda + \omega\,i$ （或 $\lambda - \omega\,i$ ）是特征方程的单根， $k = 1$ 。

将 $y^*$ 带回原方程，对比系数就能求出该特解。

??? tip "推广"

    推广到 $n$ 阶后， $k$ 是特征方程含根 $\lambda + \omega\,i$ （或 $\lambda - \omega\,i$ ）的重复次数。

## 伯努利方程

伯努利（Bernoulli）方程的形式如下

$$
\dfrac{\mathrm{d}y}{\mathrm{d}x} + P(x)y = Q(x)y^n \ \ (n \ne 0, 1)
$$

两边同时除以 $y^n$ 得

$$
y^{-n}\dfrac{\mathrm{d}y}{\mathrm{d}x} + P(x)y^{1 - n} = Q(x)
$$

引入新的因变量

$$
z = y^{1 - n}
$$

那么

$$
\dfrac{\mathrm{d}z}{\mathrm{d}x} = (1 - n)y^{-n}\dfrac{\mathrm{d}y}{\mathrm{d}x}
$$

带入原方程后可以得到一阶非齐次线性微分方程

$$
\dfrac{\mathrm{d}z}{\mathrm{d}x} + (1 - n)P(x)z = (1 - n)Q(x)
$$

## 欧拉方程

欧拉方程的形式如下

$$
x^ny^{(n)} + p_1x^{n - 1}y^{(n - 1)} + \cdots + p_{n - 1}xy' + p_ny = f(x)
$$

其中 $p_1, p_2, \cdots, p_n$ 为常数。

作变换 $x = e^t$ 或 $t = \ln x$ ，将 $x$ 换成 $t$ 。如果将 $\dfrac{\mathrm{d}}{\mathrm{d}t}$ 记为 $\mathrm{D}$，那么有

$$
x^ky^{(k)} = \mathrm{D}(\mathrm{D} - 1) \cdots (\mathrm{D} - k + 1)y
$$

带入欧拉方程就能得到一个以 $t$ 为自变量的常系数线性微分方程。

??? example

    $$
    x^3y''' + x^2y'' - 4xy' = 3x^2
    $$

    作变换 $x = e^t$ 或 $t = \ln x$ ，原方程化为

    $$
    \mathrm{D}(\mathrm{D} - 1)(\mathrm{D} - 2)y + \mathrm{D}(\mathrm{D} - 1)y - 4\mathrm{D}y = 3e^{2t}
    $$

    化简得

    $$
    \mathrm{D}^3y - 2\mathrm{D}^2y - 3\mathrm{D}y = 3e^{2t}
    $$

    即

    $$
    y''' - 2y'' - 3y' = 3e^{2t}
    $$

    这是一个关于 $t$ 的三阶常系数非齐次线性微分方程。