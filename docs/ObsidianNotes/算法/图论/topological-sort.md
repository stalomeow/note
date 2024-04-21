# 拓扑排序

!!! abstract

    两种实现拓扑排序的方法。

## 简介

拓扑排序 (Topological sorting) 用于将有向图的结点排成一个序列。该序列满足：

- 图中每个结点都出现，且只出现 1 次。
- 如果图中存在 A 到 B 的路径，那么 A 排在 B 前面。

这样的序列**不唯一**。另外，如果有向图中存在环，就无法排成这样的序列。

常见的应用：做课程安排、计算关键路径、有向图判环。

## BFS (Kahn 算法)

不断删除零入度结点实现。

``` cpp
int N;                // 结点数量
vector<int> G[MAX_N]; // 邻接表
int in[MAX_N];        // 存储每个结点的入度

bool topological_sort(vector<int>& ans) {
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
        ans.push_back(v);

        for (int adj : G[v])
        {
            // 更新相邻结点的入度，如果变成零则入队列
            if (--in[adj] == 0) q.push(adj);
        }
    }

    // 数量不相等，说明有环，拓扑排序失败
    if (ans.size() != N)
    {
        ans.clear();
        return false;
    }

    return true;
}
```

代码中的 `queue` 可以按需换成其他数据结构，比如 `priority_queue`、`stack` 等。这决定了「有多个零入度结点时的选择策略」，进而影响结果序列中的结点顺序：

- `queue`：先入队列的结点排在前面。
- `stack`：最后入栈的结点排在前面。
- `priority_queue`：最大/最小的结点排在前面。

时间复杂度：

- `queue`、`stack`：$O(V+E)$。
- `priority_queue`：$O(V \log V + E)$。

空间复杂度：$O(V)$。考虑邻接表：$O(V+E)$。

## DFS

逆向思维：对于每一个结点，都先把之后所有未访问过的结点加进结果中，再把自己加进结果中。最后把结果反转。

``` cpp
int N;                // 结点数量
vector<int> G[MAX_N]; // 邻接表
int vis[MAX_N];       // 0=未搜索，1=搜索中，2=已完成

bool dfs(int v, vector<int>& ans) {
    // 标记为搜索中
    vis[v] = 1;

    // 先处理之后的结点
    for (int adj : G[v])
    {
        // 遇到正在搜索中的结点，说明有环
        if (vis[adj] == 1) return false;

        // 继续搜索未访问过的结点
        if (vis[adj] == 0 && !dfs(adj, ans)) return false; 
    }

    // 标记为已完成
    vis[v] = 2;

    // 将自己放入结果中
    ans.push_back(v);
    return true;
}

bool topological_sort(vector<int>& ans) {
    for (int i = 0; i < N; i++)
    {
        if (vis[i] == 0 && !dfs(i, ans))
        {
            // 有环，拓扑排序失败
            ans.clear();
            return false;
        }
    }

    // 把结果反转
    reverse(ans.begin(), ans.end());
    return true;
}
```

时间复杂度：$O(V+E)$。

空间复杂度：$O(V)$。考虑邻接表：$O(V+E)$。
