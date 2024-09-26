---
slug: "240422210409"
date: 2024-04-22
---

# Fog

## Depth Fog

- Linear Fog

    $$
    factor = \frac{end - z}{end - start}
    $$

- Exp Fog

    $$
    factor = e^{-density\,\cdot\,z}
    $$

- Exp Squared Fog

    $$
    factor = e^{-(density\,\cdot\,z)^2}
    $$

### Height Fog

雾很多时候会沉淀在靠近地面的地方。如果低于某一个高度，那么 Fog 的强度为最大值。当高度变高时，Fog 的强度以指数衰减。

计算时需要积分，但是可以简化后计算出解析解。

### Voxel-based Volumetric Fog

体素化视锥体，近处分割得比远处密。在分割后不均匀的 Grid 中进行各种计算。中间计算结果存在 3 D Texture 里，Texture 的宽高比要尽量和屏幕宽高比一样，效果才好看。
