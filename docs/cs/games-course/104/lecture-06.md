# The Challenges and Fun of Rendering the Beautiful Mother Nature

## Terrain Rendering

### Heightfield（高程图）
* 最简单的方法
* 如果用得好，表现力很强

渲染方法：每隔一定距离做一个均匀的网格（Mesh Grids），把每个顶点根据高程图进行位移，再应用纹理等信息。

问题：当世界很大的时候，三角形太多！

优化方法：LOD（Level Of Detail），根据距离设置不同的精度，远处用低模。

地形是一直连续的，所以 LOD 需要用心设计。

#### Adaptive Mesh Tessellation
细分 FOV 内的 Mesh 三角形，FOV 越小，对 Mesh 的细分也需要更细密。（简单地说就是：视口不变，视角（FOV）变小，所以需要把地形放大才能填满视口，那地形就需要更多的三角形来做更清晰的渲染。具体的例子：PUBG 中的 8 倍镜就是靠缩小 FOV 实现的。）

!!! success "Two Golden Rules of Optimization"

    1. 近处密集一些，远处稀疏一些。FOV 越小越密集，FOV 越大越稀疏。
    2. 采样点变少后，地形高度的误差不要超过一个给定的阈值。相机离得越远，误差就越难从屏幕上观察出来，所以允许的误差范围也越大。~~Anyway，看上去 OK 就行！~~

##### Triangle-Based Subdivision
正方形格子斜着切一刀，切成两个等腰直角三角形。如果密度不够，就始终在等腰直角三角形的斜边中点处切一刀，再切成两个更小的等腰直角三角形。

特点：

* 效率不错。
* 二叉树的结构。
* 对地形数据的管理、保存算法不符合直觉，实际在游戏行业用得不多。
* T-Junctions：两个网格，其中一个网格切分比另一个更密，那么两个网格接缝处就可能会有裂缝。

    解决方法：继续切分那个较疏的网格，使得两个网格的切分程度相同。（简单粗暴）

##### QuadTree-Based Subdivision
主流方案