!function() {
  function getTheme() {
    let palette = __md_get("__palette");
    if (palette && typeof palette.color === "object") {
      return palette.color.scheme === "slate" ? "transparent_dark" : "light";
    }
    return "light";
  }

  // TODO giscus 每次初始化都会注册 message 事件，导致重复打印同一个 warning，但不影响功能

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
    s.setAttribute("data-theme", getTheme());
    s.setAttribute("data-lang", "en");
    s.setAttribute("data-loading", "lazy");
    s.setAttribute("crossorigin", "anonymous");
    s.setAttribute("async", "");
    comments.insertAdjacentElement("afterend", s);
  });

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("[data-md-component=palette]").addEventListener("change", () => {
      let giscus = document.querySelector(".giscus-frame");
      if (!giscus) return;

      // Instruct Giscus to change theme
      giscus.contentWindow.postMessage(
        { giscus: { setConfig: { theme: getTheme() } } },
        "https://giscus.app"
      );
    });
  });
}();