# 判断是否有环

!!! abstract

    判断无向图、有向图中是否有环的方法。

## 无向图

### DFS

### 并查集

!!! warning

    有向图不可以用并查集来判环，因为并查集没有记录边的方向。

## 有向图

### DFS

### 拓扑排序

把拓扑排序稍微简化一下即可。

``` cpp
int N;                // 结点数量
vector<int> G[MAX_N]; // 邻接表
int in[MAX_N];        // 存储每个结点的入度

bool has_cycle() {
    int cnt = 0;
    queue<int> q;

    // 零入度结点入队列
    for (int i = 0; i < N; i++)
    {
        if (!in[i]) q.push(i);
    }

    // 不断删除零入度结点，包括它的边
    while (q.size())
    {
        int v = q.front(); q.pop();
        cnt++;

        for (int adj : G[v])
        {
            // 更新相邻结点的入度，如果变成零则入队列
            if (--in[adj] == 0) q.push(adj);
        }
    }

    // 数量不相等，说明有环
    return cnt != N;
}
```

时间复杂度：$O(V+E)$。

空间复杂度：$O(V)$。考虑邻接表：$O(V+E)$。
