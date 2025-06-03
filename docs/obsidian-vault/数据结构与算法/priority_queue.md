---
date: 2024-04-27T16:12:26
publish: true
comments: true
permalink: priority-queue
aliases:
---

# priority_queue

## 第三个模板参数

- `std::less<T>`：大顶堆（默认）。
- `std::greater<T>`：小顶堆。

自定义比较的方法，除了重载 `T` 的大小于号，还有：

- 函数指针

    ``` cpp
    bool cmp(ListNode* x, ListNode* y) {
        return x->val > y->val;
    }
    
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        priority_queue<ListNode*, vector<ListNode*>, decltype(&cmp)> q(cmp);
    
        // ...
    }
    ```

- Lambda 表达式

    ``` cpp
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* x, ListNode* y) { return x->val > y->val; };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> q(cmp);
    
        // ...
    }
    ```

- 仿函数

    ``` cpp
    struct Cmp
    {
        bool operator()(ListNode* x, ListNode* y) {
            return x->val > y->val;
        }
    };
    
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        priority_queue<ListNode*, vector<ListNode*>, Cmp> q;
    
        // ...
    }
    ```
