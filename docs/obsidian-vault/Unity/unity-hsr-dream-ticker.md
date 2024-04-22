---
date: 2024-02-18T21:55:20
draft: false
authors:
  - stalomeow
categories:
  - Unity
---

# Unity 复刻星穹铁道 2.0 梦境迷钟

简单复刻，重点在图的构建和寻路上。只做了一种视角，两个关卡。

<iframe src="https://player.bilibili.com/player.html?aid=1250735475&bvid=BV1kJ4m1W76K&cid=1440682002&p=2&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

GitHub: [https://github.com/stalomeow/DreamTicker](https://github.com/stalomeow/DreamTicker)。



## 渲染

重点：

- 相机用正交投影，不要透视投影的近大远小的效果。
- 相机朝向必须和正方体的某个体对角线平行，否则做不到游戏里的效果。我用的相机欧拉角是 $(\arcsin\dfrac{1}{\sqrt{3}},-\dfrac{\pi}{4},0)$。
- 方块被分成镜子前、镜子内、镜子后三部分，提前放在场景里。

渲染流程：  

1. 镜子写入模板值 `1`（不输出颜色）
2. 绘制方块

    - 镜子前的：模板测试 `Always`
    - 镜子内的：模板测试 `Equal 1`
    - 镜子外的：模板测试 `NotEqual 1`

3. 绘制角色（深度测试 `Always`，避免被方块挡住）
4. 绘制半透明的镜子

## 建图

这是一个视错觉游戏，在三维空间中不可能的路径，只要从玩家的视角看上去没问题就能行走，所以，很容易想到把方块变换到 viewport space 或者 screen space 再建图。

实际试下来，发现这两个 space 存在一些缺点：

- 坐标依赖玩家的屏幕分辨率。不同分辨率下，算出来结果存在一些差异。
- 方块坐标和边长都不是整数。由于浮点数计算存在误差，计算相邻方块的坐标时经常算不准，没法在 `Dictionary<Vector2, Block>` 里访问到相应的方块。

考虑到相机用的是正交投影，其矩阵为

$$
\begin{bmatrix}
  \dfrac{2}{r-l} &0 &0 &-\dfrac{r+l}{r-l} \\
  0 &\dfrac{2}{t-b}  &0  &-\dfrac{t+b}{t-b} \\
  0 &0  &-\dfrac{2}{f-n}  &-\dfrac{f+n}{f-n} \\
  0 &0  &0  &1
\end{bmatrix}
$$

其中，$r,l,t,b,f,n$ 分别为视锥体的 right, left, top, bottom, far, near。Unity 的视锥体是对称的，即满足

$$
\left\{\begin{matrix}
  r+l&=0 \\
  t+b&=0
\end{matrix}\right.
$$

所以，正交投影矩阵化简为

$$
\begin{bmatrix}
  \dfrac{2}{r-l} &0 &0 &0 \\
  0 &\dfrac{2}{t-b}  &0  &0 \\
  0 &0  &-\dfrac{2}{f-n}  &-\dfrac{f+n}{f-n} \\
  0 &0  &0  &1
\end{bmatrix}
$$

对于 view space 的点 $(x,y,z)$ 用上面的矩阵变换到 NDC 后是

$$
(\dfrac{2}{r-l}x,\dfrac{2}{t-b}y,-\dfrac{2}{f-n}z-\dfrac{f+n}{f-n})
$$

发现 $x$ 和 $y$ 只是被缩放了常数倍。从 NDC 到 viewport space 或者 screen space 都是对 $x$ 和 $y$ 分别进行两种相同的线性变换。所以，从 view space 到 viewport space 或者 screen space 就是对 $x$ 和 $y$ 做了一些线性变换，完全可以省略。可以这样理解：一张照片在家里看和在学校里看没有差别，放大 10 倍和原大小整体上也没差别。

考虑到一个方块只有朝上的面才能行走，并且这个面从屏幕上看是一个平行四边形，不难构造出下面这个二维斜坐标系。任意选一个方块，将它朝上的那个面的中心作为原点。

![坐标系](../../../assets/images/unity_hsr_dream_ticker_explain.png)

若以平行四边形格子的中心点表示该格，则 $(x,y)$ 右边一格为 $(x+1,y)$，前面一格为 $(x,y+1)$，且 $x,y$ 均为整数。只要能把原来的三维地图转化成这个平行四边形网格，剩下的就很简单了。

### 计算方块对应格子的坐标

将一个方块朝上的那个面的中心点称为 `UpperCenter`。

设某方块的 `UpperCenter` 在 view space 的坐标为 $(x,y,z)^T$，变换到斜坐标系后是 $(x',y')^T$。作为斜坐标系原点的 `UpperCenter` 在 view space 的坐标为 $(O_x,O_y,O_z)^T$。

将 world space 的两个**方向** $(1,0,0)^T$ 和 $(0,0,1)^T$ 变换到 view space，只取 x 和 y 分量，不要归一化，记为 $\vec{a}$ 和 $\vec{b}$。这就是斜坐标系的两个基向量在 view space 的表示。

可求得

$$
\begin{bmatrix}
 x'\\
 y'
\end{bmatrix} = \begin{bmatrix}
 \vec{a} & \vec{b}
\end{bmatrix}^{-1} \left (\begin{bmatrix}
 x\\
 y
\end{bmatrix}-\begin{bmatrix}
 O_x\\
 O_y
\end{bmatrix} \right )
$$

### 根据镜子做剔除

镜子前的方块不用管，全部保留即可。镜子内的方块只有玩家能看到的部分才算入网格地图中，镜子后的方块同理。镜子会把方块裁成不同形状，如下图。

![镜子](../../../assets/images/unity_hsr_dream_ticker_explain2.png)

一个方块在当前视角下看是一个正六边形，根据对角线可以分成 6 个三角形。镜子只能横向移动，对移动后的坐标进行限制，可以保证这些三角形不被分割。

镜子在斜坐标系里是一个平行四边形，四条边的直线方程很容易算。上图中，红线的斜率是 $0$，黄线的斜率是 $-1$。只要知道镜子某个角的坐标，还有长和宽，就能算出四条直线方程。

如果一个三角形的重心在平行四边形内，这个三角形就是在镜子里，否则就在镜子外。

- 对镜子内的方块，把不在镜子里的三角形删掉。
- 对镜子后的方块，把在镜子里的三角形删掉。

### 根据遮挡关系做剔除

方块之间存在遮挡关系，比如下面红色的面就被挡住了，它就不能算入网格地图中。

![遮挡关系](../../../assets/images/unity_hsr_dream_ticker_explain3.png)

这部分的剔除还是以之前提到的三角形为单位。

这里其实有参考一点 Hi-Z 的思路。先把之前剔除下来的三角形的 view space z 都写入到一张 `zMap` 里，写入时只保留最大值。换句话说 `zMap` 存的是各点处离相机最近的三角形的 z 值。

``` c#
private static void SetZMap(Dictionary<Vector2Int, float> zMap, Vector2Int key, float z)
{
    if (!zMap.TryGetValue(key, out float depth))
    {
        zMap[key] = z;
    }
    else
    {
        zMap[key] = Mathf.Max(depth, z);
    }
}
```

三角形的 z 值不需要很准确，够用就行。我直接把 `UpperCenter` 变换到 view space 后的 z 值作为该方块（投影的正六边形）里所有三角形的 z。

把每个格子拆分成下图中的 Lower Triangle 和 Upper Triangle。`zMap` 分成 `zMapLower` 和 `zMapUpper`，分别记录 Lower Triangle 和 Upper Triangle。

![上下三角的定义](../../../assets/images/unity_hsr_dream_ticker_explain4.png)

正六边形则分成下面的六个三角形。

![正六边形的分割](../../../assets/images/unity_hsr_dream_ticker_explain5.png)

遍历正六边形里的三角形，写入 z 值，然后再把被挡住的三角形删掉。

``` c#
private void CullBlocksByViewSpaceZ(Dictionary<Vector2Int, BlockGroup> bMap)
{
    Dictionary<Vector2Int, float> zMapLower = new();
    Dictionary<Vector2Int, float> zMapUpper = new();

    foreach (var block in bMap.Values.SelectMany(g => g))
    {
        if ((block.ProjectedShapes & BlockProjectedShapes.LeftUpperTriangle) != 0)
        {
            SetZMap(zMapLower, block.ProjectedXY, block.ViewSpaceUpperCenterZ);
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.MiddleUpperTriangle) != 0)
        {
            SetZMap(zMapUpper, block.ProjectedXY, block.ViewSpaceUpperCenterZ);
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.RightUpperTriangle) != 0)
        {
            SetZMap(zMapLower, block.ProjectedXY + new Vector2Int(1, 0), block.ViewSpaceUpperCenterZ);
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.LeftLowerTriangle) != 0)
        {
            SetZMap(zMapUpper, block.ProjectedXY + new Vector2Int(0, -1), block.ViewSpaceUpperCenterZ);
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.MiddleLowerTriangle) != 0)
        {
            SetZMap(zMapLower, block.ProjectedXY + new Vector2Int(1, -1), block.ViewSpaceUpperCenterZ);
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.RightLowerTriangle) != 0)
        {
            SetZMap(zMapUpper, block.ProjectedXY + new Vector2Int(1, -1), block.ViewSpaceUpperCenterZ);
        }
    }

    foreach (var block in bMap.Values.SelectMany(g => g))
    {
        if ((block.ProjectedShapes & BlockProjectedShapes.LeftUpperTriangle) != 0 && block.ViewSpaceUpperCenterZ < zMapLower[block.ProjectedXY])
        {
            block.ProjectedShapes &= ~BlockProjectedShapes.LeftUpperTriangle;
        }

        if ((block.ProjectedShapes & BlockProjectedShapes.MiddleUpperTriangle) != 0 && block.ViewSpaceUpperCenterZ < zMapUpper[block.ProjectedXY])
        {
            block.ProjectedShapes &= ~BlockProjectedShapes.MiddleUpperTriangle;
        }
    }
}
```

最后删三角形时，只要考虑 Left Upper Triangle 和 Middle Upper Triangle，因为其他三角形与方块是否可以行走是无关的。

### 构建无向图

判断一个平行四边形格子是否可以行走的方法：遍历此处所有的方块，看看能不能凑出 Left Upper Triangle 和 Middle Upper Triangle。

``` c#
public bool IsWalkable
{
    get
    {
        BlockProjectedShapes shapes = BlockProjectedShapes.None;

        foreach (var b in _blocks)
        {
            shapes |= b.ProjectedShapes;

            // Walkable = LeftUpperTriangle | MiddleUpperTriangle
            if ((shapes & BlockProjectedShapes.Walkable) == BlockProjectedShapes.Walkable)
            {
                return true;
            }
        }

        return false;
    }
}
```

剩下的很简单，和普通的二维网格一样。

## 寻路

寻路一定要找最短路，否则角色可能会在地图上绕来绕去。这个 Demo 里用 bfs 就行。

## 找到正确的路径提示

小人行走前，会有个带拖尾的特效提前把路径展示出来。拖尾用 `TrailRenderer` 实现。

这里有个坑。直接给 `TrailRenderer` 应用小人移动的逻辑的话，因为地图部分地方有高度差，从相机看过去拖尾会断掉。

![拖尾的 artifact](../../../assets/images/unity_hsr_dream_ticker_explain6.png)

把移动时的 y 固定即可解决这个问题。

---

设某个方块的 `UpperCenter` 在 view space 为 $(x, y, z)^T$。给定一个 world space 里的 $y'$，需要找到 $x'$ 和 $z'$ 使得 $(x', y', z')^T$ 变换到 view space 后 x 和 y 分量分别等于 $x$ 和 $y$。

令 `worldToCameraMatrix` 等于

$$
\begin{bmatrix}
 x_1 &x_2 &x_3 &x_4 \\
 y_1 &y_2 &y_3 &y_4 \\
 z_1 &z_2 &z_3 &z_4 \\
 0 &0 &0 &1 \\
\end{bmatrix}
$$

可以列出方程

$$
\begin{bmatrix}
 x_1 &x_2 &x_3 &x_4 \\
 y_1 &y_2 &y_3 &y_4 \\
 z_1 &z_2 &z_3 &z_4 \\
 0 &0 &0 &1 \\
\end{bmatrix} \begin{bmatrix}
 x' \\
 y' \\
 z' \\
 1
\end{bmatrix} = \begin{bmatrix}
 x \\
 y \\
 t \\
 1
\end{bmatrix}
$$

有三个变量 $x',z',t$。解得

$$
\begin{bmatrix}
 x' \\
 z' \\
 t
\end{bmatrix} = \begin{bmatrix}
 x_1 &x_3 &0 \\
 y_1 &y_3 &0 \\
 z_1 &z_3 &-1 \\
\end{bmatrix}^{-1} \left ( \begin{bmatrix}
 x \\
 y \\
 0
\end{bmatrix} - y'\begin{bmatrix}
 x_2 \\
 y_2 \\
 z_2
\end{bmatrix} - \begin{bmatrix}
 x_4 \\
 y_4 \\
 z_4
\end{bmatrix} \right )
$$

把拖尾移动到 $(x', y', z')^T$（$y'$ 是可配置的定值），就能避免断裂。

## 这套算法的问题

1. 视角必须锁死
2. 处理不了纪念碑谷中的 T-Junction。参考下面视频：

<iframe width="560" height="315" src="https://www.youtube.com/embed/mCCC9hQm6MM?si=Df2R9I6B4kqWFM-C" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## 更简单更泛用的方法

人工记录每种情况下的路径，程序根据不同情况选择路径，然后是正确答案就放个动画。

缺点是配置麻烦。
