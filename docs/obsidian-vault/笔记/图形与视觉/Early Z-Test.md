---
date: 2024-11-04T14:33:38
---

# Early Z-Test

由图形驱动控制，不能用 D3D API 控制。如果像素着色器会修改深度（`SV_Depth`），就不能应用 Early Z-Test。参考 DX12 龙书第 400 页。
