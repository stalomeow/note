# 模式匹配

!!! abstract
    揭露模式匹配语法糖的本质。

在 C# 中，以下表达式和语句支持模式匹配：

* is 表达式
* switch 语句
* switch 表达式

下面，将从这三方面深入解析各种模式。

## 声明模式
> 用于检查表达式的运行时类型，如果匹配成功，则将表达式结果分配给声明的变量。

### is 表达式
``` c#
object o1 = "10"; 
object o2 = 10;

if (o1 is string s1)
{
    print(s1);
}

if (o2 is int i1)
{
    print(i1);
}
```

等价 C# 代码如下：

``` c#
object o2 = 10;
string s1 = "10" as string;

if (s1 != null)
{
    MonoBehaviour.print((object)s1);
}

if (o2 is int)
{
    int i1 = (int)o2;
    MonoBehaviour.print((object)i1);
}
```

容易发现处理 `string` 和 `int` 的代码存在差异。这涉及到 `as` 运算符的用法，下面我将根据编译后的 IL 代码给出解释。

``` c# hl_lines="14 26 27"
.maxstack 2
.locals init (
    [0] object o2,
    [1] string s1,
    [2] int32 i1
)

// if ("10" is string s1)
IL_0000: ldstr "10"
// object o2 = 10;
IL_0005: ldc.i4.s 10
IL_0007: box [netstandard]System.Int32
IL_000c: stloc.0
IL_000d: isinst [netstandard]System.String
IL_0012: stloc.1

// MonoBehaviour.print((object)s1);
IL_0013: ldloc.1
IL_0014: brfalse.s IL_001c

IL_0016: ldloc.1
IL_0017: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)

// if (o2 is int)
IL_001c: ldloc.0
IL_001d: isinst [netstandard]System.Int32
IL_0022: brfalse.s IL_0036

// int i1 = (int)o2;
IL_0024: ldloc.0
IL_0025: unbox.any [netstandard]System.Int32
IL_002a: stloc.2

// MonoBehaviour.print((object)i1);
IL_002b: ldloc.2
IL_002c: box [netstandard]System.Int32
IL_0031: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)

IL_0036: ret
```

其中的 `isinst` 指令是 `as` 运算符实现的关键，它做了下面两件事：

1. 弹出栈顶的**对象引用**（这个引用在调用该指令前就被压入栈了）。
2. 检查引用的对象是否可以被转换为指定类型（不支持代码中自定义的转换）。如果是，则将这个对象的引用压入栈，否则将 `null` 压入栈。

由此我们得出两个结论：

1. 该指令**只能用于引用类型对象**。
2. 该指令的结果可能是一个**对象引用**也可能是 `null`。

因为 `string` 是引用类型且是可空的，所以可以直接将指令的结果赋值给 `s1`。而 `int` 是值类型，显然需要将对象引用拆箱以后才能赋值。但是 `int` 又是一个不可为空的类型，所以在拆箱前还需要做一个额外的判断，保证对象引用非空。

值得一提的是：

``` c#
object o = 10;
int a = o as int; // 编译错误，原因在上面说过了
int? b = o as int?; // 编译通过
```

第三行代码对应的部分 IL 如下：

``` c#
IL_0037: isinst valuetype [netstandard]System.Nullable`1<int32>
IL_003c: unbox.any valuetype [netstandard]System.Nullable`1<int32>
```

可以发现，`isinst` 指令的结果可以直接被拆箱为 `int?`。这是因为 CLR 底层对 `Nullable<T>` 做了特殊支持。

!!! Quote "Boxing and Unboxing of nullable type"
    When a nullable type is boxed, the common language runtime automatically boxes the underlying value of the `Nullable<T>` object, not the `Nullable<T>` object itself. That is, if the `HasValue` property is `true`, the contents of the `Value` property is boxed. When the underlying value of a nullable type is unboxed, the common language runtime creates a new `Nullable<T>` structure initialized to the underlying value.

    If the `HasValue` property of a nullable type is `false`, the result of a boxing operation is `null`. Consequently, if a boxed nullable type is passed to a method that expects an object argument, that method must be prepared to handle the case where the argument is `null`. When `null` is unboxed into a nullable type, the common language runtime creates a new `Nullable<T>` structure and initializes its `HasValue` property to `false`.

!!! Note
    事实上，`as` 运算符的左侧也可以为值类型变量/常量，但这时编译器会给出编译警告。例如：

    ``` c#
    int a = 0;
    int? b = a as int?; // 编译警告：转换是多余的。
    char? c = a as char?; // 编译警告：表达式的结果总是"char?"类型的"null"。
    ```

    这些代码都会被编译器优化为等价形式，不会执行任何运行时检查。

!!! Failure "这些代码不能通过编译"
    1. 在声明模式下，`is` 右边不能使用 nullable 的值类型。
    ``` c#
    if (a is int? b) { } // 编译错误
    ```

    2. 表达式永远不可能成立。
    ``` c#
    class A { }
    class B { }

    A a = default;
    int i = 0;

    if (a is B b) { } // 编译错误
    if (i is char c) { } // 编译错误
    ```

### switch 语句 & 表达式
switch 语句和表达式最终都将被转为等价的多个 is 表达式。

!!! Example
    ``` c#
    object o = "10";

    print(o switch
    {
        string s => s,
        int i => i,
        // int? i1 => i1, // 编译错误。想想为什么？
        _ => null
    });
    ```

    等价 C# 代码如下：

    ``` c#
    object o = "10";
    string s = o as string;
    object obj;

    if (s == null)
    {
        if (o is int)
        {
            int i = (int)o;
            obj = i;
        }
        else
        {
            obj = null;
        }
    }
    else
    {
        obj = s;
    }

    MonoBehaviour.print(obj);
    ```

## 类型模式
> 用于检查表达式的运行时类型。 在 C# 9.0 中引入。

switch 语句和 switch 表达式最后都会变成 is 表达式。类型模式的 is 表达式实际上是 C# 的基础语法，此处不再赘述。

唯一值得注意的是 `Nullable<T>` 在类型模式下只能用在 is 表达式中。

``` c#
object o = null;

if (o is int?) // 编译通过
{
    print(10);
}

print(o switch
{
    int => "1",
    // int? => "2", // 编译错误
    string => "3",
    _ => "4"
});

switch (o)
{
    case int: print("1"); break;
    // case int?: print("2"); break; // 编译错误
    case string: print("3"); break;
    default: print("4"); break;
}
```

## 常量模式
> 用于测试表达式结果是否等于指定常量。

### 布尔常量
显然，全部变成 if-else。

### null 常量
``` c# hl_lines="3 8"
UnityEngine.Object o = null;

if (o is null)
{
    print(o);
}

if (o == null)
{
    print(o);
}
```

上面代码中第 3 行和第 8 行的判断实际上并不等价。从对应的 IL 代码中可以看出差异。

``` c# hl_lines="12 21"
.maxstack 2 
.locals init (
    [0] class [UnityEngine.CoreModule]UnityEngine.Object o
)

// Object o = null;
IL_0000: ldnull
IL_0001: stloc.0

// if (o is null)
IL_0002: ldloc.0
IL_0003: brtrue.s IL_000b

// MonoBehaviour.print((object)o);
IL_0005: ldloc.0
IL_0006: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)

// if (o == null)
IL_000b: ldloc.0
IL_000c: ldnull
IL_000d: call bool [UnityEngine.CoreModule]UnityEngine.Object::op_Equality(class [UnityEngine.CoreModule]UnityEngine.Object, class [UnityEngine.CoreModule]UnityEngine.Object)
IL_0012: brfalse.s IL_001a

// MonoBehaviour.print((object)o);
IL_0014: ldloc.0
IL_0015: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)

IL_001a: ret
```

!!! Quote
    The compiler guarantees that no user-overloaded equality operator `==` is invoked when expression `x is null` is evaluated.

这在 Unity 中的某些情况下可能非常有用。因为 `UnityEngine.Object` 重载了 `==` 运算符，当关联的 Native 对象失效时，C# 端的对象就**被 Unity 认为是 null**了。例如：

``` c#
GameObject go = new GameObject("tmp");

DestroyImmediate(go); // 不能用 Destroy，因为它不会立刻销毁对象

print(go is null); // False
print(go == null); // True
```

### 整数/字符/枚举常量
无论是 is 表达式、switch 语句 还是 switch 表达式，编译器都会尽可能生成最优代码：

* 如果只有一个 default-case，那么只生成 default-case 中的代码。
* 如果只有一个常量，则生成 if-else。
* 其余情况将尽可能生成传统的 switch-case 代码。如果失败，则生成 if-else(if) 代码。

!!! Note
    其实，就算不用模式匹配，编译器也会尽可能为你生成最优代码。例如下面的代码在编译后就会变成 switch-case。

    ``` c#
    int i = 0;

    if (i == 0)
    {
        print(i);
    }
    else if (i == 1)
    {
        print(i);
    }
    else if (i == 2)
    {
        print(i);
    }
    else if (i == 3)
    {
        print(i);
    }
    else if (i == 4)
    {
        print(i);
    }
    else if (i == 5)
    {
        print(i);
    }
    ```

### 浮点数常量
无论是 is 表达式、switch 语句 还是 switch 表达式，编译器都会生成大量 if-else(if) 代码。只不过，在常量较多时会做一些优化。例如：

``` c#
float f = 10.3f;
print(f switch
{
    0.1f => "0.1f",
    10.0f => "10.0f",
    15.7f => "15.7f",
    20.1f => "20.1f",
    30.1f => "30.1f",
    40.1f => "40.1f",
    50.1f => "50.1f",
    _ => string.Empty
});
```

编译以后会变成下面这样：

``` c#
float f = 10.3f;
string text;

if (f <= 15.7f)
{
    if (f != 0.1f)
    {
        if (f != 10f)
        {
            if (f != 15.7f)
            {
                goto IL_008c;
            }
            text = "15.7f";
        }
        else
        {
            text = "10.0f";
        }
    }
    else
    {
        text = "0.1f";
    }
}
else if (f <= 30.1f)
{
    if (f != 20.1f)
    {
        if (f != 30.1f)
        {
            goto IL_008c;
        }
        text = "30.1f";
    }
    else
    {
        text = "20.1f";
    }
}
else if (f != 40.1f)
{
    if (f != 50.1f)
    {
        goto IL_008c;
    }
    text = "50.1f";
}
else
{
    text = "40.1f";
}

goto IL_0092;

IL_0092:
    MonoBehaviour.print((object)text);
    return;

IL_008c:
    text = string.Empty;
    goto IL_0092;
```

### 字符串常量
无论是 is 表达式、switch 语句 还是 switch 表达式，编译器都会生成 switch-case 代码。但字符串的 switch-case 不是通过 Jump Table 实现的（Jump Table 对应 IL 中的 `switch` 指令)。

#### 字符串常量较少
首先考虑字符串常量较少的情况：

``` c#
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

``` c#
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

这 TM 就是一堆 `if` 和 `else if` 啊！所以，字符串常量的数量较少时，switch-case 和直接写一堆 `if` 和 `else if` 是完全一样的。

#### 字符串常量较多
再来考虑一下字符串常量较多的情况：

``` c#
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

``` c#
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

!!! Tip "你可能会问：到底多少个字符串常量算多呢？"
    我大概测试了一下，当 case 的数量*大于等于 7 时*，switch-case 就会采用后一种实现方式。

## 关系模式
> 用于将表达式结果与指定常量进行比较。 在 C# 9.0 中引入。

通常都会生成 if-else 代码，除非编译器发现代码可以被优化。

<del>此处不举例了，偷个懒~</del>

## 逻辑模式
> 用于测试表达式是否与模式的逻辑组合匹配。 在 C# 9.0 中引入。

通常都会生成 if-else 代码，除非编译器发现代码可以被优化。

!!! Example

    ``` c#
    char c = 'a';
    print(c switch
    {
        (>= 'a' and <= 'z') or (>= 'A' and <= 'Z') => "1",
        (>= '0' and <= '9') => "2",
        _ => '3'
    });
    ```

    生成的 IL 代码如下（就是 if-else）：

    ``` c#
    .maxstack 2
	.locals init (
		[0] char c,
		[1] object
	)

	IL_0000: ldc.i4.s 97
	IL_0002: stloc.0

	IL_0003: ldloc.0
	IL_0004: ldc.i4.s 65
	IL_0006: blt.s IL_001b

	IL_0008: ldloc.0
	IL_0009: ldc.i4.s 97
	IL_000b: blt.s IL_0014

	IL_000d: ldloc.0
	IL_000e: ldc.i4.s 122
	IL_0010: ble.s IL_0027

	IL_0012: br.s IL_0037

	IL_0014: ldloc.0
	IL_0015: ldc.i4.s 90
	IL_0017: ble.s IL_0027

	IL_0019: br.s IL_0037

	IL_001b: ldloc.0
	IL_001c: ldc.i4.s 48
	IL_001e: blt.s IL_0037

	IL_0020: ldloc.0
	IL_0021: ldc.i4.s 57
	IL_0023: ble.s IL_002f

	IL_0025: br.s IL_0037

	IL_0027: ldstr "1"
	IL_002c: stloc.1

	IL_002d: br.s IL_003f

	IL_002f: ldstr "2"
	IL_0034: stloc.1

	IL_0035: br.s IL_003f

	IL_0037: ldc.i4.s 51
	IL_0039: box [netstandard]System.Char
	IL_003e: stloc.1

	IL_003f: ldloc.1
	IL_0040: call void [UnityEngine.CoreModule]UnityEngine.MonoBehaviour::print(object)

	IL_0045: ret
    ```

## 属性模式
> 用于测试表达式的属性或字段是否与嵌套模式匹配。

通常都会生成 if-else 代码，除非编译器发现代码可以被优化。

!!! Example

    ``` c#
    Vector3 v = new Vector3(15, 1, 2);
    print(v switch
    {
        { x: 15, y: > 0, z: not 7, magnitude: 9 } => "1",
        { x: 10, y: > 0 and < 100, z: not (7 or 8) } => "2",
        _ => "3"
    });
    ```

    编译后的代码：

    ``` c#
    Vector3 v = new Vector3(15, 1, 2);

	float x = v.x;
	string text;

	if (x != 10f)
	{
		if (x == 15f)
		{
			float y = v.y;

			if (y > 0f)
			{
				float z = v.z;

				if (z != 7f && v.magnitude == 9f)
				{
					text = "1";
					goto IL_00a6;
				}
			}
		}
	}
	else
	{
		float y = v.y;

		if (y > 0f && y < 100f)
		{
			float z = v.z;

			if (z != 7f && z != 8f)
			{
				text = "2";
				goto IL_00a6;
			}
		}
	}

	text = "3";
	goto IL_00a6;

	IL_00a6:
	    MonoBehaviour.print((object)text);
    ```

## 位置模式
> 用于解构表达式结果并测试结果值是否与嵌套模式匹配。

通常都会生成 if-else 代码，除非编译器发现代码可以被优化。

!!! Example

    ``` c#
    public readonly struct Point
    {
        public int X { get; }
        public int Y { get; }

        public Point(int x, int y) => (X, Y) = (x, y);

        public void Deconstruct(out int x, out int y) => (x, y) = (X, Y);
    }

    static string Classify(Point point) => point switch
    {
        (0, 0) => "Origin",
        (1, 0) => "positive X basis end",
        (0, 1) => "positive Y basis end",
        _ => "Just a point",
    };
    ```

    编译后的代码：

    ``` c#
    private static string Classify(Point point)
    {
        point.Deconstruct(out var x, out var y);

        if (x == 0)
        {
            if (y == 0)
            {
                return "Origin";
            }
            else if (y == 1)
            {
                return "positive Y basis end";
            }
        }
        else if (x == 1)
        {
            if (y == 0)
            {
                return "positive X basis end";
            }
        }

        return "Just a point";
    }
    ```

值得一提的是，`ValueTuple` 之间的 `==` 运算基本（或者说全部？）都会被编译器内联。有时候看上去好像创建了一个 `ValueTuple`，但实际上根本没有。

!!! Example

    ``` c#
    object a = "123";
    object b = 10;

    print((a, b) switch
    {
        (int, float and > 0.1f) => "1",
        (_, string { Length: > 7 }) => "2",
        _ => "3",
    });
    ```

    编译后的代码：

    ``` c#
    object b = 10;
	string text;

	if ("123" is int && b is float)
	{
		if (!((float)b > 0.1f))
		{
			goto IL_0050;
		}

		text = "1";
	}
	else
	{
		string text2 = b as string;

		if (text2 == null || text2.Length <= 7)
		{
			goto IL_0050;
		}

		text = "2";
	}

	goto IL_0056;

	IL_0056:
	    MonoBehaviour.print((object)text);
	    return;

	IL_0050:
	    text = "3";
	    goto IL_0056;
    ```

    我的 `ValueTuple` 呢？？？

## var 模式
> 用于**匹配任何表达式**并将其结果分配给声明的变量。

其实就是让你能够拿到一些中间变量。（有点像 Linq 里的 `let`）

!!! Example

    ``` c#
    static bool IsAcceptable(int id, int absLimit) =>
        SimulateDataFetch(id) is var results
        && results.Min() >= -absLimit 
        && results.Max() <= absLimit;

    static int[] SimulateDataFetch(int id)
    {
        var rand = new Random();
        return Enumerable
                .Range(start: 0, count: 5)
                .Select(s => rand.Next(minValue: -10, maxValue: 11))
                .ToArray();
    }
    ```

    编译后的代码：

    ``` c#
    private static bool IsAcceptable(int id, int absLimit)
    {
        int[] results = SimulateDataFetch(id);
        if (Enumerable.Min(results) >= -absLimit)
        {
            return Enumerable.Max(results) <= absLimit;
        }
        return false;
    }
    ```

## 弃元模式
> 用于匹配任何表达式（包括 null）。

在 switch 表达式中可以直接使用。但是在 is 表达式中需要写成 `x is var _`。在 switch 语句中需要写成 `case var _:`（和 `default` 等价）。

因为能匹配任何表达式，并且匹配以后还什么都不干，所以一般不会生成额外代码。

## 列表模式
> 测试序列元素是否与相应的嵌套模式匹配。 在 C# 11 中引入。

还不是正式版 Feature，开摆！

似乎是要求这个序列必须有 `Length` 或 `Count` 属性/字段，并且可以通过索引访问（实现了索引器）。
