---
date: 2024-03-16T22:36:06
draft: false
authors:
  - stalomeow
categories:
  - Unity
---

# 实现 `IJobParallelForAppend`

Unity 的 [Collections package](https://docs.unity3d.com/Packages/com.unity.collections@2.4/manual/index.html) 里有个 [`IJobParallelForFilter`](https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobParallelForFilter.html)。我翻了相关的源码，发现虽然它名字带个 Parallel，但根本不是并行的。它的全部逻辑都是在一个线程里做的。后来，Unity 就把它名字里的 Parallel 去掉了，改成 [`IJobFilter`](https://docs.unity3d.com/Packages/com.unity.collections@2.4/api/Unity.Jobs.IJobFilter.html)。理由是

> `IJobParallelForFilter` renamed to `IJobFilter` to better reflect functionality. [^1]

我有并行的需求，自己实现了一个超级加强版。

``` csharp
[JobProducerType(typeof(IJobParallelForAppendExtensions.ParallelForAppendProducer<,>))]
public interface IJobParallelForAppend<TValue> where TValue : unmanaged
{
    bool Execute(int index, ref TValue buf);
}
```

它可以并行 Append 任意的 unmanaged 数据，不再局限于 `index`。有点像 Compute Shader 那套东西。

<!-- more -->

- `index` 是当前 for 循环的索引。
- `buf` 是一个临时缓冲区。

如果 `Execute` 返回 `true`，`buf` 的值会被 Append 到结果里。

## 代码

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

[^1]: [https://docs.unity3d.com/Packages/com.unity.collections@2.4/changelog/CHANGELOG.html#changed-10](https://docs.unity3d.com/Packages/com.unity.collections@2.4/changelog/CHANGELOG.html#changed-10)
