---
date: 2024-05-26T14:05:43
publish: true
comments: true
permalink: rsa
aliases:
---

# RSA 加密算法

RSA 加密算法是一种非对称加密算法，被广泛使用。RSA（Rivest–Shamir–Adleman）是三位设计者的姓氏首字母。

## 公钥和私钥的生成

1. 随意选择两个不相等的大质数 $p$ 和 $q$，计算 $N=pq$
2. 计算 [[欧拉函数（数论）|欧拉函数]]

    $$
    r = \varphi(N)=\varphi(p)\varphi(q)=(p-1)(q-1)
    $$

3. 选择一个小于 $r$ 且与 $r$ 互质的整数 $e$，计算 $e \bmod r$ 的 [[模逆元|逆元]] $d$
4. 销毁 $p$ 和 $q$ 的记录

公钥是 $(N,e)$，私钥是 $(N,d)$，私钥不能告诉别人。

## 加密

先把消息转换成小于 $N$ 的非负整数 $n$，如果消息太长就分段，每段单独加密。使用公钥 $(N,e)$ 将 $n$ 加密成 $c$ 的公式为

$$
c = n^e \bmod N
$$

## 解密

收到加密消息 $c$ 后，使用私钥 $(N,d)$ 将 $c$ 还原回 $n$ 的公式为

$$
n = c^d \bmod N
$$

## 签名

签名就是用私钥 $(N,d)$ 对消息的 hash 加密，再把加密后的 hash 加到消息后面。

对方收到有签名的消息后，用公钥 $(N,e)$ 解密 hash，将它和自己算的 hash 比较，如果一样就说明消息没有被篡改过。

hash 的计算方式可以自己选，常用的是 SHA-256。

## 原理

由加密公式可推得

$$
c^d \equiv n^{ed} \pmod{N}
$$

因为 $ed \equiv 1 \pmod{r}$ 所以

$$
ed = hr+1 = h \varphi(N) + 1
$$

那么

$$
n^{ed} = n^{h \varphi(N) + 1} = n \left( n^{\varphi(N)} \right)^h
$$

### 互质情况

若 $n$ 与 $N$ 互质，根据 [[欧拉定理（数论）|欧拉定理]]

$$
n^{ed} \equiv n \left( n^{\varphi(N)} \right)^h \equiv n \times 1^h \equiv n \pmod{N}
$$

### 不互质情况

若 $n$ 与 $N$ 不互质，注意到 $n < N = pq$，不失一般性，可以假设 $n=kp$，则

$$
n^{ed} \equiv (kp)^{ed} \equiv 0 \equiv n \pmod{p}
$$

即

$$
p \mid (n^{ed} - n) \tag{1}
$$

另一方面

$$
n^{ed} = n^{h\varphi(N)+1} = n^{h(p-1)(q-1)+1} = n \times \left( n^{(q-1)} \right)^{h(p-1)}
$$

因为 $n$ 与 $q$ 互质，所以根据 [[费马小定理]]

$$
n^{ed} \equiv n \times 1^{h(p-1)} \equiv n \pmod{q}
$$

即

$$
q \mid (n^{ed} - n) \tag{2}
$$

因为 $p,q$ 互质，再结合 $(1)(2)$ 和 [[整除]] 的性质得

$$
pq \mid (n^{ed} - n)
$$

即

$$
n^{ed} \equiv n \pmod{N}
$$

### 总结

综上所述，无论 $n$ 与 $N$ 是否互质，都有

$$
c^d \equiv n^{ed} \equiv n \pmod{N}
$$

所以解密公式可以把加密消息 $c$ 还原回 $n$。

## 安全性

假设黑客得到了加密消息 $c$ 和公钥 $(N,e)$，他必须再知道 $d$ 才能将 $c$ 还原回 $n$。最简单的方法是将 $N$ 分解回 $p$ 和 $q$，然后得到 [[同余]] 方程

$$
de \equiv 1 \pmod{(p-1)(q-1)}
$$

进而算出 $d$，再带入解密公式

$$
n = c^d \bmod N
$$

进行破解。

但以现在人类的水平，如果 $N$ 足够大的话，将它分解回 $p$ 和 $q$ 是极其困难的，可以暂时认为是不可能的。目前，$N$ 的长度至少为 2048 位才是安全的。

假如有人能够找到一种有效的分解大整数的算法的话，或者假如量子计算机可行的话，那么在解密和制造更长的钥匙之间就会展开一场竞争。但从原理上来说 RSA 在这种情况下是不可靠的。[^1]

## 速度

RSA 的速度比对称加密算法要慢得多。实际应用中，常常先用 RSA 等非对称加密算法交换对称加密的密钥，之后再改用对称加密。

[^1]: [RSA加密算法 - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95)
