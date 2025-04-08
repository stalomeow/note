document$.subscribe(() => {
  // 让第一层的外部链接在新窗口打开
  const selectors = '.md-nav[data-md-level="0"]>.md-nav__list>.md-nav__item>a.md-nav__link';
  for (const link of document.querySelectorAll(selectors)) {
    const url = new URL(link.href);
    if (url.host !== window.location.host) {
      link.setAttribute('target', '_blank');
    }
  }
});
