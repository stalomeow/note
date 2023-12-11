# 二叉树遍历

!!! abstract

    前序、中序、后序、层序遍历。

## 深度优先

- 前序（pre-order）遍历：中左右。
- 中序（in-order）遍历：左中右。
- 后序（post-order）遍历：左右中。

例题：

- [144. 二叉树的前序遍历](https://leetcode.cn/problems/binary-tree-preorder-traversal/)
- [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)
- [145. 二叉树的后序遍历](https://leetcode.cn/problems/binary-tree-postorder-traversal/)

### 递归

递归写法按遍历顺序写就行。

=== "前序"

    ``` cpp
    class Solution {
    public:
        vector<int> preorderTraversal(TreeNode* root) {
            vector<int> ans;
            dfs(root, ans);
            return ans;
        }

        void dfs(TreeNode* curr, vector<int>& ans) {
            if (curr == nullptr) return;
            ans.push_back(curr->val);    // 中
            dfs(curr->left, ans);        // 左
            dfs(curr->right, ans);       // 右
        }
    };
    ```

=== "中序"

    ``` cpp
    class Solution {
    public:
        vector<int> inorderTraversal(TreeNode* root) {
            vector<int> ans;
            dfs(root, ans);
            return ans;
        }

        void dfs(TreeNode* curr, vector<int>& ans) {
            if (curr == nullptr) return;
            dfs(curr->left, ans);        // 左
            ans.push_back(curr->val);    // 中
            dfs(curr->right, ans);       // 右
        }
    };
    ```

=== "后序"

    ``` cpp
    class Solution {
    public:
        vector<int> postorderTraversal(TreeNode* root) {
            vector<int> ans;
            dfs(root, ans);
            return ans;
        }

        void dfs(TreeNode* curr, vector<int>& ans) {
            if (curr == nullptr) return;
            dfs(curr->left, ans);        // 左
            dfs(curr->right, ans);       // 右
            ans.push_back(curr->val);    // 中
        }
    };
    ```

时间复杂度为 $O(n)$。$n$ 是节点数。

空间复杂度平均是 $O(\log n)$。最坏是 $O(n)$，此时树是一条链。

### 迭代

迭代法写起来麻烦一点。总体的思路就是用栈来模拟递归。

时间复杂度都是 $O(n)$。$n$ 是节点数。

空间复杂度都是 $O(n)$。

#### 前序

前序是最好写的，用栈来模拟。

注意：子节点入栈时，需要先右后左。

``` cpp
class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> st;

        if (root) st.push(root);

        while (st.size())
        {
            // 中
            TreeNode* curr = st.top(); st.pop();
            ans.push_back(curr->val);

            // 注意顺序：右左
            if (curr->right) st.push(curr->right);
            if (curr->left) st.push(curr->left);
        }

        return ans;
    }
};
```

#### 中序

从根节点开始不断把左子节点入栈，到底后，再处理栈中的节点。

``` cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> st;
        TreeNode* curr = root;

        while (curr || st.size())
        {
            // 左
            while (curr)
            {
                st.push(curr);
                curr = curr->left;
            }

            // 中
            curr = st.top(); st.pop();
            ans.push_back(curr->val);

            // 右
            curr = curr->right;
        }

        return ans;
    }
};
```

#### 后序

写法类似中序，但是处理栈中的节点前，要先检查它的右子节点有没有被处理过。

``` cpp
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> st;
        TreeNode* curr = root;
        TreeNode* prev = nullptr; // 前一个处理的节点

        while (curr || st.size())
        {
            // 左
            while (curr)
            {
                st.push(curr);
                curr = curr->left;
            }

            curr = st.top(); // 不 pop，因为不一定处理

            // 如果 prev 不是右节点，说明右边还没被处理过
            if (curr->right && curr->right != prev)
            {
                // 右
                curr = curr->right;
            }
            else
            {
                // 中
                st.pop();
                ans.push_back(curr->val);
                prev = curr;
                curr = nullptr;
            }
        }

        return ans;
    }
};
```

#### 用前序实现后序

后序是左右中，前序是中左右。一个比较巧妙的方法是写一个倒过来的前序（中右左），然后把结果倒过来，这样就是后序。

``` cpp
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> st;

        if (root) st.push(root);

        while (st.size())
        {
            // 中
            TreeNode* curr = st.top(); st.pop();
            ans.push_back(curr->val);

            // 注意顺序：左右
            if (curr->left) st.push(curr->left);
            if (curr->right) st.push(curr->right);
        }

        reverse(ans.begin(), ans.end());
        return ans;
    }
};
```

### 迭代的统一写法

这种写法会在要处理的节点前插入一个空指针标记。如果栈顶是一个空指针，那么意味着需要处理下一个节点。如果不是空指针，就按遍历顺序，**反过来**把节点压入栈。

=== "前序"

    ``` cpp
    class Solution {
    public:
        vector<int> preorderTraversal(TreeNode* root) {
            vector<int> ans;
            stack<TreeNode*> st;

            if (root) st.push(root);

            while (st.size())
            {
                TreeNode* curr = st.top(); st.pop();

                if (curr)
                {
                    if (curr->right) st.push(curr->right); // 右
                    if (curr->left) st.push(curr->left);   // 左
                    st.push(curr);                         // 中
                    st.push(nullptr);                      // 标记
                }
                else
                {
                    curr = st.top(); st.pop();
                    ans.push_back(curr->val);
                }
            }

            return ans;
        }
    };
    ```

=== "中序"

    ``` cpp
    class Solution {
    public:
        vector<int> inorderTraversal(TreeNode* root) {
            vector<int> ans;
            stack<TreeNode*> st;

            if (root) st.push(root);

            while (st.size())
            {
                TreeNode* curr = st.top(); st.pop();

                if (curr)
                {
                    if (curr->right) st.push(curr->right); // 右
                    st.push(curr);                         // 中
                    st.push(nullptr);                      // 标记
                    if (curr->left) st.push(curr->left);   // 左
                }
                else
                {
                    curr = st.top(); st.pop();
                    ans.push_back(curr->val);
                }
            }

            return ans;
        }
    };
    ```

=== "后序"

    ``` cpp
    class Solution {
    public:
        vector<int> postorderTraversal(TreeNode* root) {
            vector<int> ans;
            stack<TreeNode*> st;

            if (root) st.push(root);

            while (st.size())
            {
                TreeNode* curr = st.top(); st.pop();

                if (curr)
                {
                    st.push(curr);                         // 中
                    st.push(nullptr);                      // 标记
                    if (curr->right) st.push(curr->right); // 右
                    if (curr->left) st.push(curr->left);   // 左
                }
                else
                {
                    curr = st.top(); st.pop();
                    ans.push_back(curr->val);
                }
            }

            return ans;
        }
    };
    ```

## 广度优先

- 层序（level-order）：从上往下，从左往右，一层一层遍历。

例题：

- [102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

### 迭代

用队列实现。

``` cpp
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        queue<TreeNode*> q;
        vector<vector<int>> ans;

        if (root) q.push(root);

        while (q.size())
        {
            int size = q.size();
            vector<int> vec;

            for (int i = 0;i < size;i++)
            {
                TreeNode* node = q.front(); q.pop();
                vec.push_back(node->val);

                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }

            ans.push_back(vec);
        }

        return ans;
    }
};
```

时间复杂度是 $O(n)$。$n$ 是节点数。

空间复杂度是 $O(n)$。

### 递归

和深搜差不多，但要记录当前深度。

``` cpp
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        bfs(ans, root, 0);
        return ans;
    }

    void bfs(vector<vector<int>>& ans, TreeNode* root, int depth) {
        if (!root) return;

        if (ans.size() == depth) ans.emplace_back();
        ans[depth].push_back(root->val);

        bfs(ans, root->left, depth + 1);
        bfs(ans, root->right, depth + 1);
    }
};
```

时间复杂度为 $O(n)$。$n$ 是节点数。

空间复杂度平均是 $O(\log n)$。最坏是 $O(n)$，此时树是一条链。

## Morris 遍历

这种方法由 J. H. Morris 在 1979 年的论文「Traversing Binary Trees Simply and Cheaply」中首次提出，因此被称为 Morris 遍历。用了线索二叉树的思想，利用树的空闲指针，实现空间开销的极限缩减。

时间复杂度是 $O(n)$。$n$ 是节点数。

空间复杂度是 $O(1)$。

### 中序

设当前节点为 `x`，流程大致如下：

1. `#!python if x.left is None`，处理 `x` 的值，然后 `#!python x = x.right`。
2. `#!python if x.left is not None`，令 `pre` 等于 `x` 左子树上最右边的节点。`pre` 是中序遍历时 `x` 的前驱。

    - `#!python if pre.right is None`，令 `#!python pre.right = x`（线索），然后 `#!python x = x.left`。

    - `#!python if pre.right is not None`，则必有 `#!python pre.right == x`，说明我们已经遍历完 `x` 的左子树，随着线索又回到了 `x`。令 `#!python pre.right = None`（还原），处理 `x` 的值，然后 `#!python x = x.right`。

3. 重复上述操作，直至访问完整棵树。

``` cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> ans;

        while (root)
        {
            if (root->left)
            {
                // 找左子树最右边的节点
                TreeNode* pre = root->left;
                while (pre->right && pre->right != root)
                {
                    pre = pre->right;
                }

                if (pre->right)
                {
                    // 左子树访问完了
                    pre->right = nullptr;     // 还原
                    ans.push_back(root->val); // 中
                    root = root->right;       // 右
                }
                else
                {
                    // 左子树还没访问
                    pre->right = root;        // 线索
                    root = root->left;        // 左
                }
            }
            else
            {
                ans.push_back(root->val);
                root = root->right;
            }
        }

        return ans;
    }
};
```

### 前序

和中序类似，但要在访问左子树前处理当前节点。

``` cpp
class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ans;

        while (root)
        {
            if (root->left)
            {
                // 找左子树最右边的节点
                TreeNode* pre = root->left;
                while (pre->right && pre->right != root)
                {
                    pre = pre->right;
                }

                if (pre->right)
                {
                    // 左子树访问完了
                    pre->right = nullptr;      // 还原
                    root = root->right;        // 右
                }
                else
                {
                    // 左子树还没访问
                    pre->right = root;         // 线索
                    ans.push_back(root->val);  // 中
                    root = root->left;         // 左
                }
            }
            else
            {
                ans.push_back(root->val);
                root = root->right;
            }
        }

        return ans;
    }
};
```

### 后序

大体和中序差不多。但是访问完左子树后，从下往上处理左子树右边界的节点。

![Morris 后序遍历](../../../assets/images/morris-post-order-dark.svg#only-dark)
![Morris 后序遍历](../../../assets/images/morris-post-order-light.svg#only-light)

**最后，还要手动从下往上处理整棵树右边界的节点（图中第 3 个左子树右边界）。**

按这个顺序得到的就是后序遍历。

``` cpp
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> ans;

        TreeNode* x = root;
        while (x)
        {
            if (x->left)
            {
                // 找左子树最右边的节点
                TreeNode* pre = x->left;
                while (pre->right && pre->right != x)
                {
                    pre = pre->right;
                }

                if (pre->right)
                {
                    // 左子树访问完了
                    pre->right = nullptr;              // 还原
                    addRightEdgeReverse(ans, x->left); // 左子树的右边界，从下往上
                    x = x->right;                      // 右
                }
                else
                {
                    // 左子树还没访问
                    pre->right = x;                    // 线索
                    x = x->left;                       // 左
                }
            }
            else
            {
                // x->left 是空的
                // addRightEdgeReverse(ans, x->left);
                x = x->right;
            }
        }

        // 整棵树的右边界，从下往上
        addRightEdgeReverse(ans, root);
        return ans;
    }

    void addRightEdgeReverse(vector<int>& ans, TreeNode* root) {
        int count = 0;
        while (root)
        {
            ans.push_back(root->val);
            root = root->right;
            count++;
        }
        reverse(ans.end() - count, ans.end());
    }
};
```
