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
        }
    },
    options: {
        enableMenu: false,
        ignoreHtmlClass: '.*|',
        processHtmlClass: 'arithmatex',

        // assistive-mml 通常是隐藏的，但它的大小比显示的 math 块大，
        // 在 css 中用了 clip 进行裁剪，
        // 但是它的大小
        enableAssistiveMml: false,
        renderActions: {
            assistiveMml: []
        }
    }
};

// TODO 目前会报错
// document$.subscribe(() => {
//     MathJax.typesetPromise();
// });