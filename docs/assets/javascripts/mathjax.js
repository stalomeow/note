window.MathJax = {
  loader: {
    load: ['ui/lazy']
  },
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    enableMenu: false,
    ignoreHtmlClass: '.*|',
    processHtmlClass: 'arithmatex',
  }
};

document$.subscribe(() => {
  // MathJax.startup.document.outputJax.chtmlStyles 引用着 MathJax 创建的一个 <style> 元素
  // 当切换页面以后，chtmlStyles 还引用旧页面的那个 <style> 元素，导致调用 HTMLAdaptor.insertRules 方法报错
  // 每次切换新页面都要清除旧页面 <style> 元素的引用
  MathJax.startup.document?.outputJax.clearCache();
  MathJax.typesetPromise?.();
});
