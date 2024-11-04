---
date: 2024-03-16T22:36:06
slug: unity-job-parallel-for-append
draft: false
comments: true
---

# 实现 IJobParallelForAppend

Unity 的 [Collections package](https://docs.unity3d.com/Packages/com.unity.collections@2.4/manual/index.html) 里有个 [`IJobParallelForFilter`](https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobParallelForFilter.html)。我翻了相关的源码，发现虽然它名字带个 Parallel，但根本不是并行的。它的全部逻辑都是在一个线程里做的。后来，Unity 就把它名字里的 Parallel 去掉了，改成 [`IJobFilter`](https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobFilter.html)。理由是

> `IJobParallelForFilter` renamed to `IJobFilter` to better reflect functionality. [^1]

我有并行的需求，自己实现了一个超级加强版。

<!-- more -->

``` csharp
[JobProducerType(typeof(IJobParallelForAppendExtensions.ParallelForAppendProducer<,>))]
public interface IJobParallelForAppend<TValue> where TValue : unmanaged
{
    bool Execute(int index, ref TValue buf);
}
```

它可以并行 Append 任意的 unmanaged 数据，不再局限于 `index`。有点像 Compute Shader 那套东西。

- `index` 是 for 循环当前的索引。
- `buf` 是一个临时缓冲区。

如果 `Execute` 返回 `true`，`buf` 的值会被 Append 到结果里。

## 样例

``` csharp
[BurstCompile]
public struct TestJob : IJobParallelForAppend<int>
{
    public bool Execute(int index, ref int buf)
    {
        if (index % 2 == 0)
        {
            buf = index * 2;
            return true;
        }

        return false;
    }
}

public class JobTest : MonoBehaviour
{
    private void Start()
    {
        using var buffer = new NativeList<int>(Allocator.TempJob);
        TestJob job = new TestJob();
        job.Schedule(buffer, 12, 2).Complete();

        for (int i = 0; i < buffer.Length; i++)
        {
            print(buffer[i]);
        }
    }
}
```

输出是 0，4，8，12，16，20，但顺序不固定。

## 核心代码

`ParallelForAppendProducer<TJob, TValue>.Execute` 是核心的方法。在 Schedule 前分配好 `NativeList<TValue>` 的空间，每次有数据要 Append 时，用 `Interlocked.Increment` 增加 List 的元素数量，把值存进去就好。

``` csharp
public static class IJobParallelForAppendExtensions
{
    internal struct ParallelForAppendProducer<TJob, TValue> where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        public unsafe struct JobWrapper
        {
            [NativeDisableUnsafePtrRestriction]
            public UnsafeList<TValue>* AppendBuffer;
            public TJob JobData;
        }

        internal static readonly SharedStatic<IntPtr> jobReflectionData = SharedStatic<IntPtr>.GetOrCreate<ParallelForAppendProducer<TJob, TValue>>();

        [BurstDiscard]
        public static unsafe void Initialize()
        {
            if (jobReflectionData.Data == IntPtr.Zero)
                jobReflectionData.Data = JobsUtility.CreateJobReflectionData(typeof(JobWrapper), typeof(TJob), (ExecuteJobFunction)Execute);
        }

        public delegate void ExecuteJobFunction(ref JobWrapper jobWrapper, IntPtr additionalPtr, IntPtr bufferRangePatchData, ref JobRanges ranges, int jobIndex);

        public static unsafe void Execute(ref JobWrapper jobWrapper, IntPtr additionalPtr, IntPtr bufferRangePatchData, ref JobRanges ranges, int jobIndex)
        {
            TValue buf = default;

            while (true)
            {
                int begin;
                int end;
                if (!JobsUtility.GetWorkStealingRange(ref ranges, jobIndex, out begin, out end))
                    break;

                JobsUtility.PatchBufferMinMaxRanges(bufferRangePatchData, UnsafeUtility.AddressOf(ref jobWrapper), begin, end - begin);

                var endThatCompilerCanSeeWillNeverChange = end;
                for (var i = begin; i < endThatCompilerCanSeeWillNeverChange; ++i)
                {
                    if (jobWrapper.JobData.Execute(i, ref buf))
                    {
                        int idx = Interlocked.Increment(ref jobWrapper.AppendBuffer->m_length) - 1;
                        jobWrapper.AppendBuffer->Ptr[idx] = buf;
                    }
                }
            }
        }
    }

    public static void EarlyJobInit<TJob>() where TJob : struct
    {
        foreach (Type iType in typeof(TJob).GetInterfaces())
        {
            if (iType.IsGenericType && iType.GetGenericTypeDefinition() == typeof(IJobParallelForAppend<>))
            {
                Type[] genericArgs = iType.GetGenericArguments();
                Type[] typeArgs = new Type[1 + genericArgs.Length];
                typeArgs[0] = typeof(TJob);
                Array.Copy(genericArgs, 0, typeArgs, 1, genericArgs.Length);

                Type producerType = typeof(ParallelForAppendProducer<,>).MakeGenericType(typeArgs);
                producerType.GetMethod("Initialize").Invoke(null, null);
                break;
            }
        }
    }

    private static IntPtr GetReflectionData<TJob, TValue>() where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        ParallelForAppendProducer<TJob, TValue>.Initialize();
        var reflectionData = ParallelForAppendProducer<TJob, TValue>.jobReflectionData.Data;
        // JobValidationInternal.CheckReflectionDataCorrect<T>(reflectionData);
        return reflectionData;
    }

    public static unsafe JobHandle Schedule<TJob, TValue>(this TJob jobData, NativeList<TValue> buffer, int arrayLength, int innerloopBatchCount, JobHandle dependsOn = new JobHandle()) where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        if (buffer.Capacity < buffer.Length + arrayLength)
        {
            buffer.SetCapacity(buffer.Length + arrayLength);
        }

        var jobWrapper = new ParallelForAppendProducer<TJob, TValue>.JobWrapper
        {
            AppendBuffer = buffer.GetUnsafeList(),
            JobData = jobData
        };

        var scheduleParams = new JobsUtility.JobScheduleParameters(UnsafeUtility.AddressOf(ref jobWrapper), GetReflectionData<TJob, TValue>(), dependsOn, ScheduleMode.Parallel);
        return JobsUtility.ScheduleParallelFor(ref scheduleParams, arrayLength, innerloopBatchCount);
    }

    public static unsafe void Run<TJob, TValue>(this TJob jobData, NativeList<TValue> buffer, int arrayLength) where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        if (buffer.Capacity < buffer.Length + arrayLength)
        {
            buffer.SetCapacity(buffer.Length + arrayLength);
        }

        var jobWrapper = new ParallelForAppendProducer<TJob, TValue>.JobWrapper
        {
            AppendBuffer = buffer.GetUnsafeList(),
            JobData = jobData
        };

        var scheduleParams = new JobsUtility.JobScheduleParameters(UnsafeUtility.AddressOf(ref jobWrapper), GetReflectionData<TJob, TValue>(), new JobHandle(), ScheduleMode.Run);
        JobsUtility.ScheduleParallelFor(ref scheduleParams, arrayLength, arrayLength);
    }

    public static unsafe JobHandle ScheduleByRef<TJob, TValue>(ref this TJob jobData, NativeList<TValue> buffer, int arrayLength, int innerloopBatchCount, JobHandle dependsOn = new JobHandle()) where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        if (buffer.Capacity < buffer.Length + arrayLength)
        {
            buffer.SetCapacity(buffer.Length + arrayLength);
        }

        var jobWrapper = new ParallelForAppendProducer<TJob, TValue>.JobWrapper
        {
            AppendBuffer = buffer.GetUnsafeList(),
            JobData = jobData
        };

        var scheduleParams = new JobsUtility.JobScheduleParameters(UnsafeUtility.AddressOf(ref jobWrapper), GetReflectionData<TJob, TValue>(), dependsOn, ScheduleMode.Parallel);
        return JobsUtility.ScheduleParallelFor(ref scheduleParams, arrayLength, innerloopBatchCount);
    }

    public static unsafe void RunByRef<TJob, TValue>(ref this TJob jobData, NativeList<TValue> buffer, int arrayLength) where TValue : unmanaged where TJob : struct, IJobParallelForAppend<TValue>
    {
        if (buffer.Capacity < buffer.Length + arrayLength)
        {
            buffer.SetCapacity(buffer.Length + arrayLength);
        }

        var jobWrapper = new ParallelForAppendProducer<TJob, TValue>.JobWrapper
        {
            AppendBuffer = buffer.GetUnsafeList(),
            JobData = jobData
        };

        var scheduleParams = new JobsUtility.JobScheduleParameters(UnsafeUtility.AddressOf(ref jobWrapper), GetReflectionData<TJob, TValue>(), new JobHandle(), ScheduleMode.Run);
        JobsUtility.ScheduleParallelFor(ref scheduleParams, arrayLength, arrayLength);
    }
}
```

## 避坑指南

写泛型 Job 接口有不少坑。

### JobProducer 类型参数顺序

泛型 Job 接口，对应的 JobProducer 的类型参数顺序必须是

1. `TJob`：具体的 Job 类型。
2. `...T`：`TJob` 实现的 Job 接口的类型参数。

否则不兼容 Burst Compiler。这个在 Burst 源码 `Runtime/Editor/BurstReflection.cs` 里的 `ScanJobType` 方法里写死了。

比如 `IJobParallelForAppend<TValue>` 对应 `ParallelForAppendProducer<TJob, TValue>`。

### EarlyJobInit 类型参数数量

这个太坑了。

> When the Collections package is included in the project, Unity generates code to call EarlyJobInit at startup. This allows Burst compiled code to schedule jobs because the reflection part of initialization, which is not compatible with burst compiler constraints, has already happened in EarlyJobInit. [^2]

生成的代码：

``` csharp
[Unity.Jobs.DOTSCompilerGenerated]
internal class __JobReflectionRegistrationOutput__2275960884
{
    public static void CreateJobReflectionData()
    {
        try
        {
            IJobParallelForAppendExtensions.EarlyJobInit<TestJob>();
        }
        catch (Exception ex)
        {
            EarlyInitHelpers.JobReflectionDataCreationFailed(ex);
        }
    }

    [InitializeOnLoadMethod]
    public static void EarlyInit()
    {
        CreateJobReflectionData();
    }
}
```

它调用 `EarlyJobInit` 时只给了一个 `TJob` 类型参数。如果我们声明的是 `EarlyJobInit<TJob, TValue>` 就会报错。这个在 Collections 源码 `Unity.Collections.CodeGen/JobReflectionDataPostProcessor.cs` 的 `GenerateCalls` 方法里写死了。。。

[^1]: [https://docs.unity3d.com/Packages/com.unity.collections@2.4/changelog/CHANGELOG.html#changed-10](https://docs.unity3d.com/Packages/com.unity.collections@2.4/changelog/CHANGELOG.html#changed-10)
[^2]: [https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobFilterExtensions.html](https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobFilterExtensions.html)
