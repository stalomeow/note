---
slug: "240427183017"
date: 2024-04-27
---

# CSharp 字符串 switch-case 原理

无论是 is 表达式、switch 语句还是 switch 表达式，编译器都会生成 switch-case 代码。但字符串的 switch-case 不是通过 Jump Table 实现的（Jump Table 对应 IL 中的 `switch` 指令)。

## 字符串常量较少

``` csharp
string text;

switch (name)
{
    case "1":
        text = "1";
        break;
    case "12":
        text = "12";
        break;
    case "123":
        text = "123";
        break;
    default:
        text = string.Empty;
        break;
}

print(text);
```

这段代码对应的 IL 如下：

``` csharp
.maxstack 2
.locals init (
    [0] string,
    [1] string
)

IL_0000: ldarg.0
IL_0001: call instance string [UnityEngine.CoreModule]UnityEngine.Object::get_name()
IL_0006: stloc.1

IL_0007: ldloc.1
IL_0008: ldstr "1"
IL_000d: call bool [netstandard]System.String::op_Equality(string, string)
IL_0012: brtrue.s IL_0030

IL_0014: ldloc.1
IL_0015: ldstr "12"
IL_001a: call bool [netstandard]System.String::op_Equality(string, string)
IL_001f: brtrue.s IL_0038

IL_0021: ldloc.1
IL_0022: ldstr "123"
IL_0027: call bool [netstandard]System.String::op_Equality(string, string)
IL_002c: brtrue.s IL_0040

IL_002e: br.s IL_0048

IL_0030: ldstr "1"
IL_0035: stloc.0
IL_0036: br.s IL_004e

IL_0038: ldstr "12"
IL_003d: stloc.0
IL_003e: br.s IL_004e

IL_0040: ldstr "123"
IL_0045: stloc.0
IL_0046: br.s IL_004e

IL_0048: ldsfld string [netstandard]System.String::Empty
IL_004d: stloc.0

IL_004e: ldloc.0

IL_004f: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)
IL_0054: ret
```

就是一堆 `if` 和 `else if`。

## 字符串常量较多

``` csharp
string text;

switch (name)
{
    case "1":
        text = "1";
        break;
    case "12":
        text = "12";
        break;
    case "123":
        text = "123";
        break;
    case "1234":
        text = "1234";
        break;
    case "12345":
        text = "12345";
        break;
    case "123456":
        text = "123456";
        break;
    case "1234567":
        text = "1234567";
        break;
    default:
        text = string.Empty;
        break;
}

print(text);
```

这段代码对应的 IL 如下：

``` csharp
.maxstack 2
.locals init (
    [0] string text,
    [1] string,
    [2] uint32
)

IL_0000: ldarg.0
IL_0001: call instance string [UnityEngine.CoreModule]UnityEngine.Object::get_name()
IL_0006: stloc.1

IL_0007: ldloc.1
IL_0008: call uint32 '<PrivateImplementationDetails>'::ComputeStringHash(string)
IL_000d: stloc.2
IL_000e: ldloc.2
IL_000f: ldc.i4 1136836824
IL_0014: bgt.un.s IL_0033

IL_0016: ldloc.2
IL_0017: ldc.i4 501951850
IL_001c: beq.s IL_007a

IL_001e: ldloc.2
IL_001f: ldc.i4 873244444
IL_0024: beq.s IL_0068

IL_0026: ldloc.2
IL_0027: ldc.i4 1136836824
IL_002c: beq.s IL_00aa

IL_002e: br IL_010f

IL_0033: ldloc.2
IL_0034: ldc.i4 1916298011
IL_0039: bgt.un.s IL_0053

IL_003b: ldloc.2
IL_003c: ldc.i4 1672378663
IL_0041: beq IL_00c8

IL_0046: ldloc.2
IL_0047: ldc.i4 1916298011
IL_004c: beq.s IL_008c

IL_004e: br IL_010f

IL_0053: ldloc.2
IL_0054: ldc.i4 -1718241622
IL_0059: beq.s IL_00b9

IL_005b: ldloc.2
IL_005c: ldc.i4 -37477635
IL_0061: beq.s IL_009b

IL_0063: br IL_010f

IL_0068: ldloc.1
IL_0069: ldstr "1"
IL_006e: call bool [netstandard]System.String::op_Equality(string, string)
IL_0073: brtrue.s IL_00d7

IL_0075: br IL_010f

IL_007a: ldloc.1
IL_007b: ldstr "12"
IL_0080: call bool [netstandard]System.String::op_Equality(string, string)
IL_0085: brtrue.s IL_00df

IL_0087: br IL_010f

IL_008c: ldloc.1
IL_008d: ldstr "123"
IL_0092: call bool [netstandard]System.String::op_Equality(string, string)
IL_0097: brtrue.s IL_00e7

IL_0099: br.s IL_010f

IL_009b: ldloc.1
IL_009c: ldstr "1234"
IL_00a1: call bool [netstandard]System.String::op_Equality(string, string)
IL_00a6: brtrue.s IL_00ef

IL_00a8: br.s IL_010f

IL_00aa: ldloc.1
IL_00ab: ldstr "12345"
IL_00b0: call bool [netstandard]System.String::op_Equality(string, string)
IL_00b5: brtrue.s IL_00f7

IL_00b7: br.s IL_010f

IL_00b9: ldloc.1
IL_00ba: ldstr "123456"
IL_00bf: call bool [netstandard]System.String::op_Equality(string, string)
IL_00c4: brtrue.s IL_00ff

IL_00c6: br.s IL_010f

IL_00c8: ldloc.1
IL_00c9: ldstr "1234567"
IL_00ce: call bool [netstandard]System.String::op_Equality(string, string)
IL_00d3: brtrue.s IL_0107

IL_00d5: br.s IL_010f

IL_00d7: ldstr "1"
IL_00dc: stloc.0
IL_00dd: br.s IL_0115

IL_00df: ldstr "12"
IL_00e4: stloc.0
IL_00e5: br.s IL_0115

IL_00e7: ldstr "123"
IL_00ec: stloc.0
IL_00ed: br.s IL_0115

IL_00ef: ldstr "1234"
IL_00f4: stloc.0
IL_00f5: br.s IL_0115

IL_00f7: ldstr "12345"
IL_00fc: stloc.0
IL_00fd: br.s IL_0115

IL_00ff: ldstr "123456"
IL_0104: stloc.0
IL_0105: br.s IL_0115

IL_0107: ldstr "1234567"
IL_010c: stloc.0
IL_010d: br.s IL_0115

IL_010f: ldsfld string [netstandard]System.String::Empty
IL_0114: stloc.0

IL_0115: ldloc.0

IL_0116: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)
IL_011b: ret
```

简单阅读一下，发现编译器生成了一个类 `<PrivateImplementationDetails>`，其中有一个静态方法 `uint ComputeStringHash(string s)`。我在 Python 中实现了这个方法：

``` python
import numpy as np

def ComputeStringHash(s: str) -> np.uint32:
    num = np.uint32(2166136261)
    for c in s:
        unicodeCharValue = np.uint32(ord(c))
        num = (unicodeCharValue ^ num) * np.uint32(16777619)
    return num
```

在上面的 IL 代码中，还有许多 Magic Number，比如第 16 行处的 1136836824。受 `ComputeStringHash` 启发，我猜测这些数字是 switch-case 中字符串常量的 Hash。

我写了一个简单的 Python 程序来验证猜想：

``` python
values = [
    '1',
    '12',
    '123',
    '1234',
    '12345',
    '123456',
    '1234567'
]

ans = [ComputeStringHash(v) for v in values]
ans.sort()

# IL 指令 ldc.i4 加载的是 int32，but 我们算出的 Hash 是 uint32
# 所以，这里需要做一次强制转换
print([np.int32(v) for v in ans])
```

代码将输出如下结果（我手动做了格式化）：

``` json
[
    501951850,
    873244444,
    1136836824,
    1672378663,
    1916298011,
    -1718241622,
    -37477635
]
```

分析到这里，之前的 IL 代码就相当好懂了：

1. 编译器预计算了所有字符串常量的 Hash，然后硬编码进了 IL 代码中。
2. 在运行时，用相同的 Hash 算法计算需要匹配的字符串的 Hash。
3. 用二分法查找出所有具有相同 Hash 的字符串常量。
4. 逐一判断这些字符串常量的值是否和待匹配字符串完全相同（解决 Hash 碰撞问题）。
5. 如果没找到匹配的字符串常量，那么就走 `default case`。

所以，字符串常量的数量较多时，switch-case 的实现方式就是二分搜索 + 链表，只不过所有操作都被编译器内联了。

我大概测试了一下，当 case 的数量大于等于 7 时，switch-case 就会采用后一种实现方式。
