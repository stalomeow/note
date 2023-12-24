# Half Lambert 勘误

!!! abstract

    半兰伯特光照模型的勘误。感谢 b 站 UP 主 [给你柠檬椰果养乐多你会跟我玩吗](https://space.bilibili.com/32704665)。

Half Lambert 是 Valve 在开发《半条命》时提出的，所以他们的官方文档肯定是最权威的。

> ***Implementation***

> To soften the diffuse contribution from local lights, ==the dot product from the Lambertian model is scaled by ½, add ½ and squared==. The result is that this dot product, which normally lies in the range of -1 to +1, is instead in the range of 0 to 1 and has a more pleasing falloff. [^1]

把高亮部分翻译成数学公式

$$
halfLambert = (NdotL * 0.5 + 0.5)^2
$$

网上大部分的文章里都**漏掉了平方**。《Unity Shader 入门精要》也是。

[^1]: [Half Lambert - Valve Developer Community](https://developer.valvesoftware.com/wiki/Half_Lambert)