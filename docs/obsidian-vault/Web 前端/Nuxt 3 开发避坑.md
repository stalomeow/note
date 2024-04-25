---
slug: "240425201035"
date: 2024-04-25
---

# Nuxt 3 开发避坑


开发个人主页时用了 Nuxt 3。虽然有些坑，但它还是很好用的。

文档：[https://nuxt.com/docs/getting-started/introduction](https://nuxt.com/docs/getting-started/introduction)。

## 解决初始化报错

执行初始化命令后

``` bash
npx nuxi@latest init <project-name>
```

显示下面的报错。

> Error: Failed to download template from registry: Failed to download [https://raw.githubusercontent.com/nuxt/starter/templates/templates/v3.json](https://raw.githubusercontent.com/nuxt/starter/templates/templates/v3.json): TypeError: fetch failed

在 GitHub 上找到了相关的 Issues：[support http proxy when using `nuxi init` with node >= 18](https://github.com/nuxt/cli/issues/159)。其中有人总结了原因：

> The main issue is native fetch API provided by newer Node.js versions (18+), does not support HTTP agents for proxy support.

简单概括就是它不走代理。目前有 3 种解决方法：

1. 改 hosts 文件。这个我不喜欢，跳过。
2. 换源。有人把相关的文件 clone 到了 gitee 上，设置环境变量

    ``` bash
    set NUXI_INIT_REGISTRY="https://gitee.com/hzgotb/nuxt-starter/raw/templates/templates"
    ```

    之后再初始化就可以了。

3. 官方目前提供了一个支持代理的版本，但是 nightly 版，还不是正式版。 

    ``` bash
    npx nuxi-nightly@latest init <project-name>
    ```

## Font Awesome

### 配置

按它的文档做就行：[https://docs.fontawesome.com/web/use-with/vue/use-with#nuxt](https://docs.fontawesome.com/web/use-with/vue/use-with#nuxt)。建议把 Integrations/Vue 里的文档全看一下。

需要先装两个核心的包。

``` bash
npm i --save @fortawesome/fontawesome-svg-core
npm i --save @fortawesome/vue-fontawesome@latest-3
```

常用的免费 Icon Packages，可以全部安装。

``` bash
npm i --save @fortawesome/free-solid-svg-icons
npm i --save @fortawesome/free-regular-svg-icons
npm i --save @fortawesome/free-brands-svg-icons
```

在写它的 plugin 文件时要注意

``` js
// For Nuxt 3
import { library, config } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'

// This is important, we are going to let Nuxt worry about the CSS
config.autoAddCss = false

// You can add your icons directly in this plugin. See other examples for how you
// can add other styles or just individual icons.
library.add(fas)

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('font-awesome-icon', FontAwesomeIcon, {})
})

// Modify the `nuxt.config.ts` file by adding to the `export default defineNuxtConfig()`
export default defineNuxtConfig({
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css'
  ]
})
```

上面一半代码是写在 `plugins/fontawesome.js` 里的。下面 `export default defineNuxtConfig({...})` 里的代码是加在 `nuxt.config.ts` 里的。

另外不建议像上面一样，直接把一个 `IconPack` 加进 `library` 里。最好是只加需要用到的 `IconDefinition`，这样能显著减小 build 以后的 js 文件大小。

### Hydration Mismatch

相关的 Issues：[Nuxt 3: Hydration mismatch when using SSR](https://github.com/FortAwesome/vue-fontawesome/issues/394)。开 SSR 时，浏览器控制台会警告 Hydration Mismatch，命令行会提示 `Could not find one or more icon(s)`。

SSR 还是建议开的，参考：[https://nuxt.com/docs/getting-started/deployment#static-hosting](https://nuxt.com/docs/getting-started/deployment#static-hosting)。

最简单粗暴的解决方式是用 `<ClientOnly>` 标签把 `<font-awesome-icon>` 包起来，这样服务端就不渲染了，自然就没有 Mismatch 了。（

另一种更好的解决方法来自 Discussions：[Using FontAwesome in Nuxt 3](https://github.com/nuxt/nuxt/discussions/16014)。虽然他们讨论的是另一个问题，但也能解决我这里的问题。根据 Answer 里的第一条回复，把引入的所有 Font Awesome 包都写进 `nuxt.config.ts` 的 `build.transpile` 中。

``` ts
export default defineNuxtConfig({
  build: {
    transpile: [
      '@fortawesome/vue-fontawesome',
      '@fortawesome/fontawesome-svg-core',
      '@fortawesome/free-brands-svg-icons',
      '@fortawesome/free-regular-svg-icons',
      '@fortawesome/free-solid-svg-icons',
    ]
  }
})
```

## 设置页面 head 信息

文档 [https://nuxt.com/docs/getting-started/seo-meta#usehead](https://nuxt.com/docs/getting-started/seo-meta#usehead) 里推荐用 `usehead` 来实现。它是 [Unhead](https://unhead.unjs.io/) 提供的，现在已经被 Nuxt 内置了，直接用就行。

## AppConfig

### `useAppConfig()` 的代码提示

文档 [https://nuxt.com/docs/guide/directory-structure/app-config#typing-app-config](https://nuxt.com/docs/guide/directory-structure/app-config#typing-app-config) 中提到 Nuxt 会自动生成 `app.config.ts` 的类型信息。

实际使用时，以 VSCode 为例，需要重启编辑器才能生效。

### AppConfig 的限制

`useAppConfig()` 返回的是配置对象的 Reactive Proxy，所以和 Vue 的 `reactive()` 有一样的限制。具体可以参考 Vue 的文档 [`reactive()` 的局限性](https://cn.vuejs.org/guide/essentials/reactivity-fundamentals.html#limitations-of-reactive)。

## 纯静态部署到 Vercel

把 Nuxt 3 项目部署到 Vercel 时，默认是部署了一个叫 `__nitro` 的 Serverless Function。用户访问时，`__nitro` 就会被调用，然后返回对应的页面。

实际用了几天后，我发现每隔一段时间访问网站时，请求的耗时会显著增加。背后的原因，大概是每过一段时间 `__nitro` 就会把 cache 给失效掉，然后重新渲染整个页面，所以耗时比较长。对于我的没什么功能的小网站来说，这些步骤完全是多余的，还给用户带来了负面的体验，所以我决定直接静态化部署网站。

[Vercel 的文档](https://vercel.com/docs/frameworks/nuxt#static-rendering) 中提到了用 `nuxt generate` 和 `nuxt build`（默认）部署时的不同做法，但是后面一种我自己试的时候失败了，所以就用了前一种。流程很简单：

1. 修改 `nuxt.config.ts`

    ``` ts
    export default defineNuxtConfig({
      nitro: {
        static: true,
      },
    });
    ```

2. 在 Vercel 上去项目 Settings 面板重写 `Build Command` 为 `npm run generate`（或 `nuxt generate`）
