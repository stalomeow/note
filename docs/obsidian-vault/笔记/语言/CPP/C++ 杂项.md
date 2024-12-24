---
date: 2024-12-24T19:40:55
---

# C++ 杂项

## 运算符重载

可以实现为实例方法，或者非成员函数。`()` 和 `[]` 可以实现为静态成员方法。

### 二元运算

对于二元运算，如果实现为实例方法，`this` 总是左操作符。例如

``` cpp
class complex
{
public:
    complex operator+(int);
}
```

只能是 `complex + int` 不能是 `int + complex`，如果要实现 `+` 的对称性，要用非成员版的 `+` 运算符实现另一种。

``` cpp
complex operator+(int, const complex&);
```

### 自增自减

``` cpp
// 前置 ++
T& T::operator++();
T& operator++(T& a);

// 后置 ++ 需要一个 int 参数做区分
T T::operator++(int); 
T operator++(T& a, int);
```

## 成员变量指针

``` cpp
成员类型 类名::*指针名 = &类名::成员名;
```

例如

``` cpp
Point point(0, 0);
Point* pp = &point;

float Point::*pX = &Point::X; // 成员变量指针
cout << point.*pX << endl;
cout << pp->*pX << endl;
```

`.*` 和 `->*` 叫 `pointer-to-member access operators`。

## 成员函数指针

``` cpp
成员函数返回类型 (类名::*指针名)(形参) = &类名::成员函数名; // `&`可以不要
```

例如

``` cpp
Point point(0, 0);
Point* pp = &point;

float (Point::*pGetX)() = &Point::GetX; // 成员函数指针
cout << (point.*pGetX)() << endl;
cout << (pp->*pGetX)() << endl;
```

括号不能去掉，因为 `()` 优先级比 `.*` 和 `->*` 更高。[^1]

## 初始化

基本类型要显式指定初始值，否则不会自动初始化。类类型会自动调用无参构造初始化。

### 编译器生成的默认构造

- **基本类型成员**：编译器不会自动初始化，值未定义

    ``` cpp
    class MyClass {
    public:
        int x;  // 未初始化
    };
    
    MyClass obj;  // x 未被初始化
    ```

- **有默认值的成员**：会使用默认值进行初始化

    ``` cpp
    class MyClass {
    public:
        int x = 10;  // 默认值为 10
    };
    
    MyClass obj;  // x 被初始化为 10
    ```

- **类类型成员**：会调用其类的默认构造函数进行初始化，如果没有默认构造会报错

    ``` cpp
    class MyClass {
    public:
        int x;
        MyClass() : x(10) {}  // 手动初始化
    };
    
    class MyOtherClass {
    public:
        MyClass obj;  // 会调用 MyClass 的默认构造函数
    };
    ```

- **`const` 成员**：报错，必须通过构造函数显式初始化

    ``` cpp
    class MyClass {
    public:
        const int x;          // 必须通过构造函数初始化
        MyClass() : x(10) {}  // 默认构造函数需要显式初始化 x
    };
    ```

### new

- **基本类型**：默认不会初始化，除非显式指定初始值

    ``` cpp
    int* p = new int;         // 不会初始化，包含垃圾值
    int* p1 = new int(10);    // 使用值初始化，初始化为 10
    int* arr = new int[5];    // 不会初始化，包含垃圾值
    int* arr1 = new int[5](); // 使用空括号进行值初始化，数组元素将被初始化为 0

    // int* arr = new int[5](10); // 错误，应使用 std::fill_n
    std::fill_n(arr, 5, 10);      // 填充为 10
    ```

- **类类型**：会调用无参构造来初始化

    ``` cpp
    class MyClass {
    public:
        int x;
        MyClass() : x(10) {}  // 在构造函数中初始化成员变量
    };
    
    MyClass* p = new MyClass;       // 会调用无参构造初始化
    MyClass* arr = new MyClass[5];  // 会调用无参构造初始化每个元素
    ```

## 继承

- 构造时，从最顶层父类**向下**依次执行构造，同级的父类按多继承声明顺序**从左往右**构造，成员变量按**定义的顺序从上往下**构造
- 析构时，从最底层子类**向上**依次执行析构，同级的父类按多继承声明顺序**从右往左**析构，成员变量按**定义的顺序从下往上**析构
- 构造时，子类还没初始化，析构时，子类已经销毁，所以此时虚函数相当于没有 `virtual`，不会动态绑定子类方法
- 基类的析构要声明为虚函数，否则 `delete` 基类不会调用子类析构

## 虚继承

解决菱形继承问题。

``` cpp
class A {
public:
    int x;
};

class B : public A {
public:
    int y;
};

class C : public A {
public:
    int z;
};

class D : public B, public C {
public:
    int w;
};
```

- 在 `D` 中包含两个 `x`，分别来自 `A -> B -> D` 和 `A -> C -> D` 两条路径
- 在 `D` 中直接使用 `x` 有歧义，应该使用 `B::x` 或 `C::x` 指定来源

使用虚继承可以去除冗余的基类副本，`D` 中就只有一个 `x` 了。

``` cpp
class A {
public:
    int x;
    A() : x(10) {}
};

class B : virtual public A {
public:
    int y;
    B() : y(20) {}
};

class C : virtual public A {
public:
    int z;
    C() : z(30) {}
};

class D : public B, public C {
public:
    int w;
    D() : w(40) {}
};

int main() {
    D d;
    std::cout << d.x << std::endl;  // 10, 通过虚继承，只会有一份 A
    return 0;
}
```

每个派生类（直接和间接）都要调用虚基类的构造，但是最后实际只会被调用一次，使用最底层的派生类（最终派生类）给的参数。

``` cpp
#include <iostream>

class A {
public:
    int x;
    
    // 虚基类的构造函数带有参数
    A(int val) : x(val) {
        std::cout << "A constructor called with x = " << x << std::endl;
    }
};

class B : virtual public A {
public:
    // B 的构造函数，需要调用 A 的构造函数并传递参数
    B(int val) : A(val) {
        std::cout << "B constructor called" << std::endl;
    }
};

class C : virtual public A {
public:
    // C 的构造函数，需要调用 A 的构造函数并传递参数
    C(int val) : A(val) {
        std::cout << "C constructor called" << std::endl;
    }
};

class D : public B, public C {
public:
    // D 的构造函数，需要调用 A 的构造函数并传递参数
    D(int val) : A(val), B(val), C(val) {
        std::cout << "D constructor called" << std::endl;
    }
};

int main() {
    D d(10);  // 创建 D 类型对象，并传递参数给 A 的构造函数
    return 0;
}
```

结果

``` bash
A constructor called with x = 10
B constructor called
C constructor called
D constructor called
```

调用顺序

1. 虚基类 `A` 的构造函数：在 `D` 类的构造过程中，虚基类 `A` 的构造函数首先被调用。`D` 类的构造函数显式地通过初始化列表将参数 `10` 传递给了 `A` 的构造函数，因此 `A` 会使用这个参数来初始化 `x`。
2. 派生类 `B` 和 `C` 的构造函数：因为 `B` 和 `C` 都是虚继承自 `A`，它们不会负责初始化 `A`。虚继承确保了 `A` 只有一个副本，并且 `A` 的初始化由最底层派生类 `D` 负责。因此，`B` 和 `C` 的构造函数会按照顺序依次调用。
3. 最终派生类 `D` 的构造函数：最后，`D` 类的构造函数会被调用。

[^1]: [C++ Operator Precedence - cppreference.com](https://en.cppreference.com/w/cpp/language/operator_precedence)
