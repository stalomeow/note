---
date: 2023-12-23T20:28:41
slug: patch-package-cache-problem
categories:
  - Web
draft: false
comments: true
---

# 解决 patch-package 不生效的问题

<!-- more -->

`patch-package` 是一个 npm 包，用来快速修复其他包中的 bug， 不需要等原作者更新。GitHub: [https://github.com/ds300/patch-package](https://github.com/ds300/patch-package)。

==有新的 Patch 时，记得把之前的 Cache 清除掉，否则新 Patch 可能生效不了。==

## Vercel

清 Build Cache 的方法：

- 在 Dashboard 上 Redeploy，同时不勾选 `Use existing Build Cache`。
- 加环境变量 `VERCEL_FORCE_NO_BUILD_CACHE`，并把值设为 `1`。这样的话，每次 Build 都不会用 Cache。
- 更多方法见：[Vercel 文档：Understanding Build cache](https://vercel.com/docs/deployments/troubleshoot-a-build#understanding-build-cache)。

## Next .js

把 `.next` 文件夹删掉就好。
