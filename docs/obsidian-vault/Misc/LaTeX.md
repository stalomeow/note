---
date: 2024-11-21T18:01:39
publish: true
comments: true
permalink: latex
aliases:
---

# LaTeX

## 标序号和引用

> [MathJax: How to number and reference multiline equations? - Mathematics Meta Stack Exchange](https://math.meta.stackexchange.com/questions/13342/mathjax-how-to-number-and-reference-multiline-equations)

使用 `\tag` 标序号，`\label` 来命名。

``` latex
\int_{-\infty}^\infty e^{-\pi x^2}\,\mathrm{d}x=1\label{a}\tag{1}
```

$$
\int_{-\infty}^\infty e^{-\pi x^2}\,\mathrm{d}x=1\tag{1}
$$

使用 `\ref` 来引用之前 `\label` 中的名称。

``` latex
\ref{a}
```

然而 Obsidian 目前不支持 `\label`[^1] ，所以 `\ref` 也没法用，只能自己手动写序号引用 $(1)$。

[^1]: [“\label” in the math block and "\ref" in the content at the same time cause error - Bug graveyard - Obsidian Forum](https://forum.obsidian.md/t/label-in-the-math-block-and-ref-in-the-content-at-the-same-time-cause-error/3189/2)
