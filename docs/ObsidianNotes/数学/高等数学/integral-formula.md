# 积分公式

!!! abstract

    记录一些积分公式<del>（小寄巧）</del>。

## 区间再现公式

$$
\int_{a}^{b} f(x)\mathrm{d}x = \int_{a}^{b} f(a + b - x)\mathrm{d}x
$$

令 $x = a + b - t$ 换元，即可证明。

### 推论

$$
\int_{a}^{b} f(x)\mathrm{d}x = \frac{1}{2} \int_{a}^{b} (f(x) + f(a + b - x))\mathrm{d}x
$$

??? example "例题"

    $$
    \int_{-1}^{1} \frac{1}{(1+x^2)(1+e^x)}\mathrm{d}x
    $$

    用区间再现公式可以化简为

    $$
    \frac{1}{2} \int_{-1}^{1}\frac{1}{1+x^2}\mathrm{d}x
    $$

## 三角函数相关

### 一

$$
\int_{0}^{\tfrac{\pi}{2}} f(\sin x) \mathrm{d}x = \int_{0}^{\tfrac{\pi}{2}} f(\cos x) \mathrm{d}x
$$

用区间再现公式，即可证明。

### 二

$$
\int_{0}^{\pi} xf(\sin x) \mathrm{d}x = \frac{\pi}{2} \int_{0}^{\pi} f(\sin x) \mathrm{d}x
$$

用区间再现公式的推论，即可证明。

### 三

$$
\begin{align}
\int_{0}^{\pi} f(\sin x) \mathrm{d}x &= 2\int_{0}^{\tfrac{\pi}{2}} f(\sin x) \mathrm{d}x \\
\\
\int_{0}^{\pi} xf(\sin x) \mathrm{d}x &= \pi \int_{0}^{\tfrac{\pi}{2}} f(\sin x) \mathrm{d}x
\end{align}
$$

对称性。

### 四

$$
\int_{0}^{\tfrac{\pi}{2}} x(f(\sin x) + f(\cos x)) \mathrm{d}x = \frac{\pi}{2} \int_{0}^{\tfrac{\pi}{2}} f(\sin x) \mathrm{d}x
$$

#### 证明

$$
\begin{align}
\int_{0}^{\tfrac{\pi}{2}} xf(\sin x) \mathrm{d}x &= \int_{0}^{\tfrac{\pi}{2}} (\frac{\pi}{2} - x)f(\sin (\frac{\pi}{2} - x)) \mathrm{d}x \\
\\
&= \frac{\pi}{2} \int_{0}^{\tfrac{\pi}{2}} f(\cos x) \mathrm{d}x - \int_{0}^{\tfrac{\pi}{2}} xf(\cos x) \mathrm{d}x
\end{align}
$$

等式两边再加上

$$
\int_{0}^{\tfrac{\pi}{2}} xf(\cos x) \mathrm{d}x
$$

就得到结论了。

### 五

$$
\begin{align}
\int \sec x \mathrm{d}x &= \int \dfrac{\sec x(\sec x + \tan x)}{\sec x + \tan x} \mathrm{d}x \\
\\
&= \int \dfrac{\mathrm{d} (\sec x + \tan x)}{\sec x + \tan x} \\
\\
&= \ln \left | \sec x + \tan x \right | + C
\end{align}
$$

或者

$$
\begin{align}
\int \sec x \mathrm{d}x &= \int \dfrac{\cos x}{\cos^2 x} \mathrm{d}x \\
\\
&= \int \dfrac{\mathrm{d} \sin x}{1 - \sin^2 x} \\
\\
&= \dfrac{1}{2} \int (\dfrac{1}{1 + \sin x} + \dfrac{1}{1 - \sin x}) \mathrm{d} \sin x \\
\\
&= \dfrac{1}{2} \ln \left | \dfrac{1 + \sin x}{1 - \sin x} \right | + C
\end{align}
$$

### 六

$$
\begin{align}
\int \csc x \mathrm{d}x &= \int \dfrac{1}{\sin x} \mathrm{d}x \\
\\
&= \int \dfrac{1}{2 \sin \dfrac{x}{2} \cos \dfrac{x}{2}} \mathrm{d}x \\
\\
&= \int \dfrac{\cos \dfrac{x}{2}}{\sin \dfrac{x}{2} \cos^2 \dfrac{x}{2}} \mathrm{d} \dfrac{x}{2} \\
\\
&= \int \dfrac{\sec^2 \dfrac{x}{2}}{\tan \dfrac{x}{2}} \mathrm{d} \dfrac{x}{2} \\
\\
&= \int \dfrac{1}{\tan \dfrac{x}{2}} \mathrm{d} \tan \dfrac{x}{2} \\
\\
&= \ln \left | \tan \dfrac{x}{2} \right | + C
\end{align}
$$

由于

$$
\begin{align}
\tan \dfrac{x}{2} &= \dfrac{\sin \dfrac{x}{2}}{\cos \dfrac{x}{2}} \\
\\
&= \dfrac{2 \sin^2 \dfrac{x}{2}}{2 \sin \dfrac{x}{2} \cos \dfrac{x}{2}} \\
\\
&= \dfrac{1 - \cos x}{\sin x} \\
\\
&= \csc x - \cot x
\end{align}
$$

所以，也有

$$
\int \csc x \mathrm{d}x = \ln \left | \csc x - \cot x \right | + C
$$

## Wallis 公式

又叫华里士公式、点火公式。

$$
\int_{0}^{\tfrac{\pi}{2}} \sin^n x \mathrm{d}x = \int_{0}^{\tfrac{\pi}{2}} \cos^n x \mathrm{d}x = \frac{(n-1)!!}{n!!} \cdot H
$$

- $n$ 为偶数时，$H$ 为 $\dfrac{\pi}{2}$。
- $n$ 为奇数时，$H$ 为 $1$。

即

$$
= \left\{\begin{matrix}
 \dfrac{n-1}{n} \cdot \dfrac{n-3}{n-2} \cdots \dfrac{3}{4} \cdot \dfrac{1}{2} \cdot \dfrac{\pi}{2} &,n\text{为偶数}\\
 \\
 \dfrac{n-1}{n} \cdot \dfrac{n-3}{n-2} \cdots \dfrac{4}{5} \cdot \dfrac{2}{3} \cdot 1 &,n\text{为奇数}
\end{matrix}\right.
$$

用分部积分求出第 $n$ 和 $n-2$ 项的递推关系，然后易得。

### 推论一

$$
\int_{0}^{\tfrac{\pi}{2}} \sin^n x \cos^n x \mathrm{d}x = \frac{1}{2^n} \int_{0}^{\tfrac{\pi}{2}} \sin^n x \mathrm{d}x
$$

#### 证明

$$
\begin{align}
\int_{0}^{\tfrac{\pi}{2}} \sin^n x \cos^n x \mathrm{d}x &= \int_{0}^{\tfrac{\pi}{2}} (\sin x \cos x)^n \mathrm{d}x \\
\\
&= \int_{0}^{\tfrac{\pi}{2}} (\frac{1}{2} \sin 2x)^n \mathrm{d}x
\end{align}
$$

然后，令 $t = 2x$ 换元，即可证明。

### 推论二

$$
\lim_{n \to +\infty} \left (\frac{(2n)!!}{(2n-1)!!} \right)^2 \frac{1}{2n+1} = \frac{\pi}{2}
$$

借助双阶乘的性质

$$
\begin{align}
& (2n)!! = \prod_{k=1}^{n} (2k) = 2^nn! \\
\\
& (2n - 1)!! = \dfrac{(2n)!}{(2n)!!} = \dfrac{(2n)!}{2^nn!}
\end{align}
$$

该推论也可以表示为

$$
\lim_{n \to +\infty} \frac{(n!)^2 \cdot 2^{2n}}{(2n)!\sqrt{n}} = \sqrt{\pi}
$$

#### 证明

令

$$
I_n = \int_{0}^{\tfrac{\pi}{2}} \sin^n x \mathrm{d}x
$$

当 $x \in \left [0, \dfrac{\pi}{2} \right ]$ 时，有

$$
\sin^{2k + 1} x \le \sin^{2k} x \le \sin^{2k - 1} x
$$

从 $0$ 到 $\dfrac{\pi}{2}$ 积分得

$$
I_{2k + 1} \le I_{2k} \le I_{2k - 1}
$$

即

$$
\frac{(2k)!!}{(2k+1)!!} \le \frac{(2k - 1)!!}{(2k)!!} \cdot \frac{\pi}{2} \le \frac{(2k - 2)!!}{(2k - 1)!!}
$$

变形后得

$$
1 \le \frac{\cfrac{\pi}{2}}{\left ( \cfrac{(2k)!!}{(2k-1)!!} \right )^2 \cdot \cfrac{1}{2k+1}} \le \frac{2k+1}{2k}
$$

当 $k \to +\infty$ 时，由夹逼定理即可求得结论。

### 推论三

当 $n \to +\infty$ 时，有

$$
\dfrac{(2n)!!}{(2n-1)!!} = \dfrac{(n!)^2 \cdot 2^{2n}}{(2n)!} \sim \sqrt{\pi n}
$$
