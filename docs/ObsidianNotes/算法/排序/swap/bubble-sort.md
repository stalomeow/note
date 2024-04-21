# 冒泡排序

!!! abstract

    冒泡排序。

## 原理

## 分析

## 模板

``` cpp
#define MAX_N 1000000

int N;
int nums[MAX_N];

void bubbleSort()
{
    bool changed = true;

    for (int i = 0; i < N - 1 && changed; i++)
    {
        changed = false;

        for (int j = 0; j < N - 1 - i; j++)
        {
            if (nums[j] > nums[j + 1])
            {
                std::swap(nums[j], nums[j + 1]);
                changed = true;
            }
        }
    }
}
```
