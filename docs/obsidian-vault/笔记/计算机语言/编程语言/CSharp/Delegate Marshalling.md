---
date: 2024-04-27T18:05:10
---

# Delegate Marshalling

向非托管代码封送委托的原理。下面这些也类似：

- 使用 xLua 在 C# 中创建一个 Lua 函数的委托。
- 使用 HybridCLR 在 AOT 代码中创建一个热更方法的委托。
- ...

反过来封送的原理也都类似。

## Unmanaged Callers Only

使这个静态方法只能被非托管代码调用。取地址以后直接拿到一个非托管函数指针。

## Unmanaged Function Pointer

- Unity AOT 下，会为被标记的委托类型生成专门的 delegatePInvokeWrapperFunction（一个托管方法，在里面调用被包装的非托管函数指针），用于 Marshal.GetDelegateForFunctionPointer。

## Mono PInvoke Callback

- AOT 模式下使用。
- 只能静态方法。
- Unity 2022.3 里，如果方法是泛型方法不会生成代码。应该是个 bug。
- 在非泛型方法上标记多次，只有最后一个会被使用，生成一次代码。
- 生成的桥接函数的 Calling Convention 依赖于 MonoPInvokeCallback 参数里的委托类型。默认是 Platform Default Calling Convention。如果要修改的话，需要在委托上加 UnmanagedFunctionPointer，然后在参数里指定。
- 生成的桥接函数的代码不依赖 MonoPInvokeCallback 参数里的委托。
- 生成的函数以 ReversePInvokeWrapper 开头。

## Get Function Pointer For Delegate

- JIT 下，生成的桥接函数的代码依赖于参数里的委托，静态方法和实例方法都支持。之后需要保证该委托不被 GC 回收。使用 `GCHandle.Alloc(object)` 创建一个该委托的 Normal GCHandle 就能防止它被 GC。
- Unity AOT 下，依赖 MonoPInvokeCallback 生成的代码。只能用于静态方法。不依赖参数里的委托。委托被 GC 了也没关系。

## Get Delegate For Function Pointer

- Unity AOT 下，委托类型上需要有 UnmanagedFunctionPointer。这样才会提前生成 delegatePInvokeWrapperFunction。
