---
slug: "240427201955"
date: 2024-04-27
---

# 让 SRP Batch 支持 Multipass Shader


强行让 SRP Batch 支持 Multipass Shader，但不一定适用于所有情况。


``` csharp
private void DrawBatchedPasses(ScriptableRenderContext context, ref RenderingData renderingData, CommandBuffer cmd)
{
    SortingCriteria sortFlags = m_IsOpaque
        ? renderingData.cameraData.defaultOpaqueSortFlags
        : SortingCriteria.CommonTransparent;

    DrawingSettings drawSettings = CreateDrawingSettings(ShaderTagId.none, ref renderingData, sortFlags);
    FilteringSettings filterSettings = m_FilterSettings;
    RenderStateBlock stateBlock = m_RenderStateBlock;

    for (int i = 0; i < s_ShaderTagIdList.Count; i++)
    {
        (ShaderTagId shaderTagId, ProfilingSampler sampler) = s_ShaderTagIdList[i];
        drawSettings.SetShaderPassName(0, shaderTagId);

        using (new ProfilingScope(cmd, sampler))
        {
            // Begin Profiling Label
            context.ExecuteCommandBuffer(cmd);
            cmd.Clear();

            // Draw
            context.DrawRenderers(renderingData.cullResults, ref drawSettings, ref filterSettings, ref stateBlock);
        }

        // Close Profiling Label
        context.ExecuteCommandBuffer(cmd);
        cmd.Clear();
    }
}
```

重写 `ScriptableRenderPass.Execute(ScriptableRenderContext context, ref RenderingData renderingData)`，调用就行。
