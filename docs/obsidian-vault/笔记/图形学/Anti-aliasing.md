---
slug: "240422210516"
date: 2024-04-22
---

# Anti-aliasing

## Reason of Aliasing

高频信号 vs 受限于渲染分辨率的不充足的采样。

- Edge Sampling
- Texture Sampling
- Specular Sampling

## 方法

常规的 AA 方法：根据一定规则采样自己和周围几个点，然后加权平均得到最终像素颜色（可以产生一个平滑的边界）。

### Super-sample AA (SSAA)

最直接的方法，直接绘制一个 4 倍的图像，然后降采样。

### Multi-sample AA (MSAA)

还是 4 倍（或者更多）的超采样，但是绘制时进行了优化，会跳过一些没必要的像素。硬件完全支持。

### Fast Approximate Anti-aliasing (FXAA)

基于 1 倍大小的图形进行 AA。

1. 找到处于图形边缘的像素。

### Temporal Anti-aliasing (TAA)
