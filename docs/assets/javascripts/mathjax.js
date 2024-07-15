window.MathJax = {
  loader: {
    load: ['[tex]/boldsymbol', 'ui/lazy']
  },
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    packages: {
      '[+]': ['boldsymbol']
    },
    macros: {
      abs: [String.raw`\left | #1 \right |`, 1],
      coloneq: String.raw`\mathrel{\vcenter{:}}=`,
      ddx: [String.raw`\frac{\mathrm{d}#2}{\mathrm{d}#1}`, 2, 'x'],
      dddx: [String.raw`\dfrac{\mathrm{d}#2}{\mathrm{d}#1}`, 2, 'x']
    }
  },
  options: {
    enableMenu: false,
    ignoreHtmlClass: '.*|',
    processHtmlClass: 'arithmatex',

    // assistive-mml 通常是隐藏的，但它的大小比显示的 math 块大
    enableAssistiveMml: false,
    renderActions: {
      assistiveMml: []
    }
  }
};

document$.subscribe(() => {
  // MathJax.startup.document.outputJax.chtmlStyles 引用着 MathJax 创建的一个 <style> 元素
  // 当切换页面以后，chtmlStyles 还引用旧页面的那个 <style> 元素，导致调用 HTMLAdaptor.insertRules 方法报错
  // 每次切换新页面都要清除旧页面 <style> 元素的引用
  MathJax.startup.document?.outputJax.clearCache();
  MathJax.typesetPromise?.();
});
