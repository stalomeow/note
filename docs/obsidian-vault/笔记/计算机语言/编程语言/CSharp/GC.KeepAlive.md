---
slug: "240427180601"
date: 2024-04-27
---

# `GC.KeepAlive`

这个方法容易望文生义，然后用错。它实际上**什么都不做**，就是单纯持有一个对象的引用，保证**在此之前**该对象不满足 GC 回收的条件。

方法实现：

``` csharp
[MethodImpl(MethodImplOptions.NoInlining)] // disable optimizations
[Intrinsic]
public static void KeepAlive(object? obj)
{
}
```

## 适用场景 1

## 适用场景 2

This method DOES NOT DO ANYTHING in and of itself. It's used to prevent a finalizable object from losing any outstanding references a touch too early. The JIT is very aggressive about keeping an object's lifetime to as small a window as possible, to the point where a 'this' pointer isn't considered live in an instance method unless you read a value from the instance. So for finalizable objects that store a handle or pointer and provide a finalizer that cleans them up, this can cause subtle race conditions with the finalizer thread. This isn't just about handles - it can happen with just about any finalizable resource.

Users should insert a call to this method right after the last line of their code where their code still needs the object to be kept alive. The object which reference is passed into this method will not be eligible for collection until the call to this method happens. Once the call to this method has happened the object may immediately become eligible for collection. Here is an example:

...all you really need is one object with a Finalize method, and a second object with a Close/Dispose/Done method. Such as the following contrived example:

``` csharp
class Foo {
    Stream stream = ...;
    protected void Finalize() { stream.Close(); }
    void Problem() { stream.MethodThatSpansGCs(); }
    static void Main() { new Foo().Problem(); }
}
```

In this code, Foo will be finalized in the middle of stream.MethodThatSpansGCs, thus closing a stream still in use.

If we insert a call to GC.KeepAlive(this) at the end of Problem(), then Foo doesn't get finalized and the stream stays open.

## 参考

- [GC.KeepAlive(Object) Method - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.gc.keepalive)
- [GC - .NET Source Browser](https://source.dot.net/#System.Private.CoreLib/src/System/GC.CoreCLR.cs,245)
