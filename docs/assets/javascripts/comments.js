!function() {
  // Support instant loading
  document$.subscribe(() => {
    let comments = document.querySelector("#__comments");
    if (!comments) return;

    let s = document.createElement("script");
    s.setAttribute("src", "https://giscus.app/client.js");
    s.setAttribute("data-repo", "stalomeow/note");
    s.setAttribute("data-repo-id", "R_kgDOIiy-JQ");
    s.setAttribute("data-category", "Comments");
    s.setAttribute("data-category-id", "DIC_kwDOIiy-Jc4CS79f");
    s.setAttribute("data-mapping", "pathname");
    s.setAttribute("data-strict", "0");
    s.setAttribute("data-reactions-enabled", "1");
    s.setAttribute("data-emit-metadata", "0");
    s.setAttribute("data-input-position", "top");
    s.setAttribute("data-theme", "transparent_dark");
    s.setAttribute("data-lang", "en");
    s.setAttribute("data-loading", "lazy");
    s.setAttribute("crossorigin", "anonymous");
    s.setAttribute("async", "");
    comments.insertAdjacentElement("afterend", s);
  });
}();