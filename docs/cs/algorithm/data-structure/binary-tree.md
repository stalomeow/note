# 二叉树

!!! abstract

    二叉树相关的定义和题目。

## 完全二叉树的节点个数

> 给你一棵 **完全二叉树** 的根节点 `root` ，求出该树的节点个数。

??? quote "完全二叉树的定义"

    在完全二叉树中，除了最底层节点可能没填满外，其余每层节点数都达到最大值，并且最下面一层的节点都集中在该层最左边的若干位置。若最底层为第 `h` 层，则该层包含 `1~ 2h` 个节点。

??? example "示例"

    - 输入：`root = [1,2,3,4,5,6]`

        ``` mermaid
        graph TB;
            A((1))-->B((2))
            A-->C((3));
            B-->E((4))
            B-->F((5))
            C-->H((6))
        ```

        输出：`6`

    - 输入：`root = []`

        输出：`0`

    - 输入：`root = [1]`

        输出：`1`

??? info "Definition for a binary tree node"

    ``` cpp
    struct TreeNode {
        int val;
        TreeNode *left;
        TreeNode *right;
        TreeNode() : val(0), left(nullptr), right(nullptr) {}
        TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
        TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
    };
    ```

### 遍历

时间复杂度 $O(n)$，空间复杂度 $O(log\ n)$。

### 递归

时间复杂度 $O(log^2\ n)$，空间复杂度 $O(log\ n)$。

``` cpp
int countNodes(TreeNode* root) {
    return countNodesRecur(root);
}

int countNodesRecur(TreeNode* root) {
    if (!root) return 0;

    int leftDepth = getDepth(root, 0);
    int rightDepth = getDepth(root, 1);

    if (leftDepth == rightDepth)
    {
        return (1 << leftDepth) - 1;
    }

    return countNodesRecur(root->left) + countNodesRecur(root->right) + 1;
}

int getDepth(TreeNode* root, int right) {
    int depth = 0;
    while (root)
    {
        depth++;
        root = right ? root->right : root->left;
    }
    return depth;
}
```

### 二分查找

时间复杂度 $O(log^2\ n)$，空间复杂度 $O(1)$。

``` cpp
int countNodes(TreeNode* root) {
    return countNodesBinarySearch(root);
}

int countNodesBinarySearch(TreeNode* root) {
    int h = getDepth(root, 0) - 1;
    if (h < 0) return 0;

    int low = 0;
    int high = (1 << h) - 1;

    // [low, high]
    while (low < high)
    {
        int mid = (high - low + 1) / 2 + low;
        TreeNode* node = root;

        for (int i = h - 1;i >= 0;i--)
        {
            int cmd = (mid >> i) & 1;
            node = cmd ? node->right : node->left;
        }

        if (node) low = mid;
        else high = mid - 1;
    }

    return (low + 1) + ((1 << h) - 1);
}

int getDepth(TreeNode* root, int right) {
    int depth = 0;
    while (root)
    {
        depth++;
        root = right ? root->right : root->left;
    }
    return depth;
}
```
