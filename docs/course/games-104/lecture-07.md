# Render Pipeline, Post-processing and Everything

## Ambient Occlusion
近似计算环境光因为遮挡产生的衰减。

### Precomputed AO
在做好模型以后，用光线追踪离线预计算 AO，然后存到贴图里。

* 空间换时间。
* 只能用在静态物体上。

### Screen Space Ambient Occlusion (SSAO)
1. 在 View Space，对每一个像素 $p$ ，在它周围的球型范围中随机采样 N 个点。
2. 对于每一个采样点，将它的深度和 depth buffer 中的值比较，进而判断它是否被遮挡（判断的是对于相机的可见性）。
3. 计算平均的可见度来近似 AO，公式如下：

    $$
    A(p) = 1 - \frac{Occlusion}{N}
    $$

!!! warning

    这个方法在数学上是有问题的。

### SSAO+
改进版的 SSAO，只采样法线方向的半个球。公式如下：

$$
AO(\mathbf{p}, \mathbf{n}) = \frac{1}{\pi}\int_{\Omega}V(\mathbf{p}, \omega)\,\mathbf{n} \cdot \omega\,d\omega
$$

其中， $V(\mathbf{p}, \omega)$ 是 $\omega$ 方向的可见性， $\mathbf{n} \cdot \omega$ 是 $\omega$ 方向的权重。

!!! note

    由于屏幕空间的信息有限，所以这个方法有时也会产生一些 Artifact。~~简单算法的代价。~~

### Horizon-based Ambient Occlusion (HBAO)
引入了一个 attenuation function 来避免离得很远的物体产生太强的 AO。大体流程如下（忽略了很多细节）：

1. 利用 depth buffer 构建 heightfield。
2. 用 Ray Marching 找到一个点周围一圈每个方向上遮挡物最高点的仰角。
3. 近似计算 AO。

### Ground Truth-based Ambient Occlusion (GTAO)
* 引入了 cosine 项（类似算光照时那个 cosine）。
* 给出了一个三次多项式，可以根据 single bounce 的 AO 值直接近似计算 multi bounce 以后的最终结果。

### Ray-Tracing Ambient Occlusion
借助硬件做光线追踪，然后计算 AO。

## Fog

### Depth Fog
* Linear Fog

    $$
    factor = \frac{end - z}{end - start}
    $$

* Exp Fog

    $$
    factor = e^{-density\,\cdot\,z}
    $$

* Exp Squared Fog

    $$
    factor = e^{-(density\,\cdot\,z)^2}
    $$

### Height Fog
雾很多时候会沉淀在靠近地面的地方。如果低于某一个高度，那么 Fog 的强度为最大值。当高度变高时，Fog 的强度以指数衰减。

计算时需要积分，但是可以简化后计算出解析解。

### Voxel-based Volumetric Fog
体素化视锥体，近处分割得比远处密。在分割后不均匀的 Grid 中进行各种计算。中间计算结果存在 3D Texture 里，Texture 的宽高比要尽量和屏幕宽高比一样，效果才好看。

## Anti-aliasing

!!! note "Reason of Aliasing"

    高频信号 vs 受限于渲染分辨率的不充足的采样。

    * Edge Sampling
    * Texture Sampling
    * Specular Sampling

常规的 AA 方法：根据一定规则采样自己和周围几个点，然后加权平均得到最终像素颜色（可以产生一个平滑的边界）。

### Super-sample AA (SSAA) and Multi-sample AA (MSAA)
SSAA：最直接的方法，直接绘制一个 4 倍的图像，然后降采样。

MSAA（硬件完全支持）：还是 4 倍（或者更多）的超采样，但是绘制时进行了优化，会跳过一些没必要的像素。

### Fast Approximate Anti-aliasing (FXAA)
基于 1 倍大小的图形进行 AA。

1. 找到处于图形边缘的像素。
2. 

### Temporal Anti-aliasing (TAA)




