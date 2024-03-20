# 单调栈

始终满足单调性的栈。新元素入栈时，先把比它大（小）的元素都出栈，自己再入栈，以维持单调性。

典型的应用场景：在一维数组中，寻找每个元素左（右）边第一个满足某条件的元素。

## 每日温度

> [739. 每日温度](https://leetcode.cn/problems/daily-temperatures/description/){ target="_blank" }

> 给定一个整数数组 <code>temperatures</code> ，表示每天的温度，返回一个数组 <code>answer</code> ，其中 <code>answer[i]</code> 是指对于第 <code>i</code> 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 <code>0</code> 来代替。

> **提示：**

> *   <code>1 <= temperatures.length <= 10<sup>5</sup></code>
> *   <code>30 <= temperatures[i] <= 100</code>

??? success "解析"

    算是模板题了。单调栈中存的是当前还没处理的元素下标。

    ``` cpp
    class Solution {
    public:
        vector<int> dailyTemperatures(vector<int>& temperatures) {
            vector<int> ans(temperatures.size(), 0);
            stack<int> s;

            for (int i = 0;i < temperatures.size();i++)
            {
                while (s.size() && temperatures[i] > temperatures[s.top()])
                {
                    ans[s.top()] = i - s.top();
                    s.pop();
                }
                s.push(i);
            }

            return ans;
        }
    };
    ```

    时间复杂度：$O(n)$。每个元素下标最多入栈一次，出栈一次。

    空间复杂度：$O(n)$。

## 下一个更大元素 I

> [496. 下一个更大元素 I](https://leetcode.cn/problems/next-greater-element-i/description/){ target="_blank" }

> <code>nums1</code> 中数字 <code>x</code> 的 **下一个更大元素** 是指 <code>x</code> 在 <code>nums2</code> 中对应位置 **右侧** 的 **第一个** 比 <code>x</code> 大的元素。

> 给你两个 **没有重复元素** 的数组 <code>nums1</code> 和 <code>nums2</code> ，下标从 **0** 开始计数，其中<code>nums1</code> 是 <code>nums2</code> 的子集。

> 对于每个 <code>0 <= i < nums1.length</code> ，找出满足 <code>nums1[i] == nums2[j]</code> 的下标 <code>j</code> ，并且在 <code>nums2</code> 确定 <code>nums2[j]</code> 的 **下一个更大元素** 。如果不存在下一个更大元素，那么本次查询的答案是 <code>-1</code> 。

> 返回一个长度为 <code>nums1.length</code> 的数组 <code>ans</code> 作为答案，满足 <code>ans[i]</code> 是如上所述的 **下一个更大元素** 。

> **提示：**

> *   <code>1 <= nums1.length <= nums2.length <= 1000</code>
> *   <code>0 <= nums1[i], nums2[i] <= 10<sup>4</sup></code>
> *   <code>nums1</code>和<code>nums2</code>中所有整数 **互不相同**
> *   <code>nums1</code> 中的所有整数同样出现在 <code>nums2</code> 中

??? success "解析"

    `nums1` 中数字不是按顺序排的。不过没什么难度，加个 `map` 就行。

    ``` cpp
    class Solution {
    public:
        vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
            unordered_map<int, int> ids;
            for (int i = 0;i < nums1.size();i++)
            {
                ids[nums1[i]] = i;
            }

            vector<int> ans(nums1.size(), -1);
            stack<int> s;

            for (int i = 0;i < nums2.size();i++)
            {
                while (s.size() && nums2[i] > nums2[s.top()])
                {
                    if (ids.count(nums2[s.top()]))
                    {
                        ans[ids[nums2[s.top()]]] = nums2[i];
                    }
                    s.pop();
                }
                s.push(i);
            }

            return ans;
        }
    };
    ```

    时间复杂度：$O(m+n)$。

    空间复杂度：$O(m+n)$。

## 下一个更大元素 II

> [503. 下一个更大元素 II](https://leetcode.cn/problems/next-greater-element-ii/description/){ target="_blank" }

> 给定一个循环数组 <code>nums</code> （ <code>nums[nums.length - 1]</code> 的下一个元素是 <code>nums[0]</code> ），返回 _<code>nums</code> 中每个元素的 **下一个更大元素**_ 。

> 数字 <code>x</code> 的 **下一个更大的元素** 是按数组遍历顺序，这个数字之后的第一个比它更大的数，这意味着你应该循环地搜索它的下一个更大的数。如果不存在，则输出 <code>-1</code> 。

> **提示:**

> *   <code>1 <= nums.length <= 10<sup>4</sup></code>
> *   <code>-10<sup>9</sup> <= nums[i] <= 10<sup>9</sup></code>

??? success "解析"

    遍历两次数组就行。

    ``` cpp
    class Solution {
    public:
        vector<int> nextGreaterElements(vector<int>& nums) {
            vector<int> ans(nums.size(), -1);
            stack<int> s;

            for (int i = 0;i < 2 * nums.size();i++)
            {
                int idx = i % nums.size();
                while (s.size() && nums[idx] > nums[s.top()])
                {
                    ans[s.top()] = nums[idx];
                    s.pop();
                }
                s.push(idx);
            }

            return ans;
        }
    };
    ```

    时间复杂度：$O(n)$。

    空间复杂度：$O(n)$。

## 接雨水

> [42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/description/){ target="_blank" }

> 给定 <code>n</code> 个非负整数表示每个宽度为 <code>1</code> 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

> **提示：**

> *   <code>n == height.length</code>
> *   <code>1 <= n <= 2 * 10<sup>4</sup></code>
> *   <code>0 <= height[i] <= 10<sup>5</sup></code>

经典题，非常重要。

??? success "解析 1"

    动态规划。

    对下标 `i` 这一列，能接的雨水数量为 `max(height[:i+1])` 和 `max(height[i:])` 的最小值减去 `height[i]`。

    用 `leftMax[i]` 表示 `max(height[:i+1])`，`rightMax[i]` 表示 `max(height[i:])`。有
    
    - `leftMax[0]=height[0]`
    - `leftMax[i]=max(leftMax[i-1], height[i])`
    - `rightMax[n-1]=height[n-1]`
    - `rightMax[i]=max(rightMax[i+1], height[i])`

    ``` cpp
    class Solution {
    public:
        int trap(vector<int>& height) {
            vector<int> leftMax(height.size());
            leftMax[0] = height.front();

            for (int i = 1; i < height.size(); i++)
            {
                leftMax[i] = max(leftMax[i - 1], height[i]);
            }

            vector<int> rightMax(height.size());
            rightMax.back() = height.back();

            for (int i = height.size() - 2; i >= 0; i--)
            {
                rightMax[i] = max(rightMax[i + 1], height[i]);
            }

            int ans = 0;
            for (int i = 0; i < height.size(); i++)
            {
                ans += min(leftMax[i], rightMax[i]) - height[i];
            }
            return ans;
        }
    };
    ```

    时间复杂度：$O(n)$。

    空间复杂度：$O(n)$。

??? success "解析 2"

    双指针。

    ``` cpp
    class Solution {
    public:
        int trap(vector<int>& height) {
            int leftMax = -1;
            int rightMax = -1;
            int left = 0;
            int right = height.size() - 1;
            int ans = 0;

            // 这里条件中等号可以加也可以不加
            // 最后 left 和 right 一定会聚在最高处
            while (left < right)
            {
                leftMax = max(leftMax, height[left]);
                rightMax = max(rightMax, height[right]);

                if (height[left] < height[right])
                {
                    ans += leftMax - height[left];
                    left++;
                }
                else
                {
                    ans += rightMax - height[right];
                    right--;
                }
            }

            return ans;
        }
    };
    ```

    时间复杂度：$O(n)$。

    空间复杂度：$O(1)$。

??? success "解析 3"

    单调栈。动态规划是竖着数雨水，而单调栈是横着数雨水。

## 柱状图中最大的矩形

> [84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/description/){ target="_blank" }

> 给定 _n_ 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

> 求在该柱状图中，能够勾勒出来的矩形的最大面积。

> **提示：**

> *   <code>1 <= heights.length <=10<sup>5</sup></code>
> *   <code>0 <= heights[i] <= 10<sup>4</sup></code>
