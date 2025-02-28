---
date: 2025-02-28T23:48:48
---

# Clustered Shading

Clustered Shading 就是将视锥体划分成很多小块（Cluster），然后计算每个小块的有效光源列表。Shading 时，先找到当前点所属的 Cluster，再遍历对应的光源列表进行计算。

这个方案同时适用于 Deferred 和 Forward 渲染路径，但是储存的代价比较大，剔除光源时计算量也相对较多。

## 视锥体划分

划分是在 View Space 进行的，这样只需要算一次，后面可以复用。XY 方向都是均匀划分，Z 方向常用的是均匀划分和指数划分。

![[Pasted image 20250301000051.png|均匀划分（Z方向）]]

![[Pasted image 20250301000106.png|指数划分（Z方向）]]

指数划分在近处 Cluster 的数量较多，远处数量较少，计算公式为

$$
Z=\text{Near}_Z \left(\frac{\text{Far}_Z}{\text{Near}_Z} \right)^{\dfrac{\text{slice}}{\text{num slices}}}
$$

其中，$\text{num slices}$ 是 Z 方向的划分数量。

[DOOM 2016](https://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf) 将视锥体划分为 $16 \times 8 \times 24$ 块，可以参考。

## 光源剔除

### 点光源剔除

### 聚光灯剔除

## 参考

- [DaveH355/clustered-shading: An OpenGL tutorial on clustered shading. A technique for efficiently rendering thousands of dyanmic lights in games.](https://github.com/DaveH355/clustered-shading)
