# 最小生成树

!!! abstract

    Kruskal 和 Prim 算法。

最小生成树（Minimum spanning tree，MST）是最小权重生成树（Minimum weight spanning tree）的简称，是一副连通加权无向图中一棵权值最小的生成树。

## Kruskal

这是个贪心算法。根据权值从小到大加入边，如果加入这条边会产生环，则丢弃这条边。

可以用优先队列来存边，用并查集来维护两节点的连通关系。如果某条边的两节点之前就已经连通，那么加入这条边就会产生环，需要丢弃这条边。

时间复杂度 $O(n \log n)$。

## Prim


