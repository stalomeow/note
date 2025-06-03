---
date: 2025-01-01T23:02:21
publish: true
comments: true
permalink: index-min-pq
aliases:
---

# IndexMinPQ

IndexMinPQ 是一种特殊的优先队列（Priority Queue），它支持通过**索引**来**访问和修改**队列中的元素，并且保持最小堆的性质。这种数据结构在很多算法中非常有用，特别是在需要频繁更新优先级的情况下。

## 实现

``` cpp
#include <iostream>
#include <vector>
#include <climits>
#include <stdexcept>

using namespace std;

template <typename T>
class IndexMinPQ {
private:
    vector<int> pq;        // 存储堆的索引
    vector<int> qp;        // 存储元素索引在堆中的位置
    vector<T> keys;        // 存储元素的优先级
    int N;                 // 当前堆中元素的个数
    int maxN;              // 堆的最大容量

    // 判断堆顶元素是否小于某个元素
    bool less(int i, int j) const {
        return keys[pq[i]] < keys[pq[j]];
    }

    // 交换堆中的两个元素
    void exch(int i, int j) {
        swap(pq[i], pq[j]);
        qp[pq[i]] = i;
        qp[pq[j]] = j;
    }

    // 堆化上浮操作
    void swim(int k) {
        while (k > 1 && less(k, k / 2)) {
            exch(k, k / 2);
            k = k / 2;
        }
    }

    // 堆化下沉操作
    void sink(int k) {
        while (2 * k <= N) {
            int j = 2 * k;
            if (j < N && less(j + 1, j)) j++;
            if (!less(j, k)) break;
            exch(k, j);
            k = j;
        }
    }

public:
    // 构造函数
    IndexMinPQ(int maxN) : maxN(maxN), N(0), pq(maxN + 1), qp(maxN + 1, -1), keys(maxN + 1) {}

    // 检查队列是否为空
    bool isEmpty() const {
        return N == 0;
    }

    // 检查队列是否已满
    bool isFull() const {
        return N == maxN;
    }

    // 返回队列中元素的数量
    int size() const {
        return N;
    }

    // 插入元素到队列
    void insert(int index, const T& key) {
        if (index < 0 || index >= maxN) throw out_of_range("Index out of range");
        if (contains(index)) throw invalid_argument("Index already exists in the priority queue");

        N++;
        qp[index] = N;
        pq[N] = index;
        keys[index] = key;
        swim(N);
    }

    // 删除并返回堆顶元素
    int delMin() {
        if (isEmpty()) throw underflow_error("Priority queue underflow");

        int minIndex = pq[1];
        exch(1, N--);
        sink(1);
        qp[minIndex] = -1;
        keys[minIndex] = T();  // 防止重复删除，置为默认值
        pq[N + 1] = -1;        // 防止重复删除
        return minIndex;
    }

    // 返回堆顶元素
    int minIndex() const {
        if (isEmpty()) throw underflow_error("Priority queue underflow");
        return pq[1];
    }

    // 返回堆顶元素的优先级
    T minKey() const {
        if (isEmpty()) throw underflow_error("Priority queue underflow");
        return keys[pq[1]];
    }

    // 修改某个元素的优先级
    void changeKey(int index, const T& key) {
        if (!contains(index)) throw invalid_argument("Index does not exist in the priority queue");

        keys[index] = key;
        swim(qp[index]);
        sink(qp[index]);
    }

    // 检查索引是否存在
    bool contains(int index) const {
        return qp[index] != -1;
    }

    // 删除指定索引的元素
    void deleteIndex(int index) {
        if (!contains(index)) throw invalid_argument("Index does not exist in the priority queue");

        int i = qp[index];
        exch(i, N--);
        swim(i);
        sink(i);
        qp[index] = -1;
        keys[index] = T();
    }
};
```

## 示例

``` cpp
int main() {
    // 使用 IndexMinPQ 存储整数类型的优先队列
    IndexMinPQ<int> pq(10);

    // 插入一些元素
    pq.insert(0, 30);
    pq.insert(1, 40);
    pq.insert(2, 20);
    pq.insert(3, 10);
    
    // 获取最小元素并删除
    cout << "Min element index: " << pq.minIndex() << ", key: " << pq.minKey() << endl;
    pq.delMin();

    // 修改元素的优先级
    pq.changeKey(1, 5);

    // 删除指定索引的元素
    pq.deleteIndex(2);

    // 输出当前队列中的元素
    while (!pq.isEmpty()) {
        int minIndex = pq.delMin();
        cout << "Min element index: " << minIndex << ", key: " << pq.minKey() << endl;
    }

    // 使用 IndexMinPQ 存储浮点数类型的优先队列
    IndexMinPQ<double> pqDouble(10);

    pqDouble.insert(0, 30.5);
    pqDouble.insert(1, 20.2);
    pqDouble.insert(2, 40.8);

    cout << "Min element index: " << pqDouble.minIndex() << ", key: " << pqDouble.minKey() << endl;
    pqDouble.delMin();

    cout << "Min element index: " << pqDouble.minIndex() << ", key: " << pqDouble.minKey() << endl;
    
    return 0;
}
```
