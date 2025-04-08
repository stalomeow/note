import json
import logging
import posixpath
import re

from mkdocs.plugins import event_priority

CONFIG = {
    "Toolbar": {
        "display": {
            "left": [],
            "middle": [
                "rotateCCW",
                "rotateCW",
                "flipX",
                "flipY",
                "reset",
            ],
            "right": ["close"],
        },
    },
    "Images": {
        "Panzoom": {
            "maxScale": 2,
        },
    },
}

log = logging.getLogger('mkdocs.plugins')

def add_fancybox_css(output, head_regex: re.Pattern):
    css_link = "".join([f'<link href="{css}" rel="stylesheet"/>' for css in [
        "https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css"
    ]])
    output = head_regex.sub(f"<head>\\1 {css_link}</head>", output)

    css_code = \
        ".fancybox__caption { font-size: 0.7rem; }" \
        "[data-fancybox] { cursor: pointer; }" \
        "[data-md-color-scheme=default] figure[fancybox-only-dark] { display: none; }" \
        "[data-md-color-scheme=slate] figure[fancybox-only-light] { display: none; }"
    output = head_regex.sub(f"<head>\\1<style>{css_code}</style></head>", output)
    return output

def add_fancybox_js(output, config, head_regex: re.Pattern, body_regex: re.Pattern):
    js_script = "".join([f'<script src="{js}"></script>' for js in [
        "https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js",
        "https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/l10n/zh_CN.umd.js"
    ]])
    output = head_regex.sub(f"<head>\\1 {js_script}</head>", output)

    js_code = f"Fancybox.bind('[data-fancybox]',Object.assign({{l10n:Fancybox.l10n.zh_CN}},JSON.parse('{json.dumps(CONFIG, separators=(',', ':'))}')));"

    # support compatible with mkdocs-material Instant loading feature
    if "navigation.instant" in config["theme"].get("features", []):
        js_code = f'document$.subscribe(() => {{ {js_code} }})'

    output = body_regex.sub(f"<body\\1<script>{js_code}</script></body>", output)
    return output

# 在 minify 之前执行
@event_priority(50)
def on_post_page(output, page, config, **kwargs):
    # Define regular expressions for matching the relevant sections of the HTML code
    head_regex = re.compile(r"<head>(.*?)<\/head>", flags=re.DOTALL)
    body_regex = re.compile(r"<body(.*?)<\/body>", flags=re.DOTALL)

    output = add_fancybox_css(output, head_regex)
    output = add_fancybox_js(output, config, head_regex, body_regex)
    return output

def wrap_img(match: re.Match, skip_class, meta):
    try:
        img_tag = match.group(0)
        img_attr = match.group("attr")
        classes = re.findall(r'class="([^"]+)"', img_attr)
        classes = [c for match in classes for c in match.split()]

        # 强制懒加载
        if img_attr.find('loading="lazy"') == -1:
            img_tag = img_tag[:-1] + ' loading="lazy">'

        if set(skip_class) & set(classes):
            return img_tag

        src = re.search(r"src=[\"\']([^\"\']+)", img_attr).group(1)
        caption = re.search(r"alt=[\"]([^\"]+)", img_attr)
        caption = caption.group(1) if caption else ""

        if "fancybox-thumbnail" in classes:
            filename, ext = posixpath.splitext(src)
            filename = filename.removesuffix("-thumbnail")
            href = filename + ext
        else:
            href = src

        if src.endswith(("#only-dark", "#gh-dark-mode-only")):
            theme = "fancybox-only-dark"
        elif src.endswith(("#only-light", "#gh-light-mode-only")):
            theme = "fancybox-only-light"
        else:
            theme = ""

        a_tag = f'<a href="{href}" data-fancybox data-caption="{caption}">{img_tag}</a>'
        return f'<figure {theme}>{a_tag}<figcaption>{caption}</figcaption></figure>'
    except Exception as e:
        log.warning(f"Error in wrapping img tag with fancybox: {e} {match.group(0)}")
        return match.group(0)

def on_page_content(html, page, config, **kwargs):
    # skip emoji img with index as class name from pymdownx.emoji https://facelessuser.github.io/pymdown-extensions/extensions/emoji/
    skip_class = ["emojione", "twemoji", "gemoji", "no-fancybox"]
    return re.compile(r"<img(?P<attr>.*?)>").sub(lambda match: wrap_img(match, skip_class, page.meta), html)

# 放在 blog 之后执行，更新首页 excerpt 的内容
# https://github.com/squidfunk/mkdocs-material/blob/2f1b2e950040a89e70a5f193de762388206fb8fa/src/plugins/blog/plugin.py#L331
@event_priority(-200)
def on_page_context(context, page, config, nav):
    for post in context.get('posts', []):
        post.content = on_page_content(post.content, post, config)
