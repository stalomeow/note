import logging
import posixpath
import pypinyin
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page
from mkdocs.utils import meta, get_relative_url
from string import ascii_letters, digits

OBSIDIAN_VAULT_DIR = 'obsidian-vault'
OBSIDIAN_VAULT_BLACKLIST = ('.obsidian', 'templates')

wiki_name_map: dict[str, File] = {}
wiki_path_map: dict[str, File] = {}
log = logging.getLogger('mkdocs.plugins')

def transform_slug(slug: str) -> str:
    # slug 目前用的是日期数字，这里把数字转换成字母
    table = str.maketrans(digits, ''.join(ascii_letters[int(i)] for i in digits), '-')
    slug = slug.translate(table).lower()

    # 重排一下并分组，让原本相似的数字看起来不太一样
    return '-'.join([slug[1::3], slug[2::3], slug[0::3]])

@event_priority(100) # 放在最前面执行，不要处理其他插件生成的文件
def on_files(files: Files, config: MkDocsConfig):
    invalid_files = []
    wiki_name_map.clear()
    wiki_path_map.clear()

    for f in files:
        # 忽略 Obsidian Vault 之外的文件
        if not f.src_uri.startswith(posixpath.join(OBSIDIAN_VAULT_DIR, '')):
            continue

        # 删掉黑名单里的文件
        if f.src_uri.startswith(tuple(posixpath.join(OBSIDIAN_VAULT_DIR, b, '') for b in OBSIDIAN_VAULT_BLACKLIST)):
            invalid_files.append(f)
            continue

        if not f.is_documentation_page():
            continue

        _, frontmatter = meta.get_data(f.content_string)

        # 有 slug 的话就用 slug 作为文件名
        if "slug" in frontmatter:
            slug = transform_slug(str(frontmatter["slug"]))
            if not f.use_directory_urls:
                f.dest_uri = posixpath.join(OBSIDIAN_VAULT_DIR, slug + '.html')
            else:
                f.dest_uri = posixpath.join(OBSIDIAN_VAULT_DIR, slug, 'index.html')
        else:
            log.warning('Obsidian document \'%s\' does not have a slug.', f.src_uri)

        wiki_name_map[f.name] = f
        wiki_path_map[posixpath.splitext(f.src_uri)[0]] = f # key 无扩展名

    log.info('Obsidian documents: %s.', str(list(wiki_name_map.keys())))

    for f in invalid_files:
        log.info('Removing obsidian vault file: \'%s\'.', f.src_uri)
        files.remove(f)
    return files

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    obsidian_root = None
    for it in nav.items:
        if isinstance(it, Section) and it.title.lower().count('obsidian') > 0:
            obsidian_root = it
    if obsidian_root is None:
        return

    def get_entry_key(entry):
        # obsidian 目录下面只有 Page 和 Section
        if isinstance(entry, Page):
            # Page 对应 markdown 文件
            # 此时 markdown 还没解析，title 是 None，使用文件名代替
            key = entry.file.name
        else:
            # Section 对应文件夹，直接用 title 即可
            key = entry.title

        start_with_english = key[0] in ascii_letters

        # 把中文变成拼音（无音调），不是中文的部分保留
        pinyin = pypinyin.lazy_pinyin(key, style=pypinyin.Style.NORMAL, errors='default', v_to_u=False)

        # 按照 obsidian 的风格，以英文开头的内容排在中文开头的后面，不区分大小写
        return (start_with_english, ''.join(pinyin).lower())

    def dfs(entry):
        children = getattr(entry, 'children', None)
        if children is None:
            return

        files = []
        folders = []

        for child in entry.children:
            dfs(child)

            if isinstance(child, Page):
                files.append(child)
            else:
                folders.append(child)

        files.sort(key=get_entry_key)
        folders.sort(key=get_entry_key)
        entry.children = folders + files # 文件夹放在文件前面

    # 重新排序
    dfs(obsidian_root)
    return nav

def transform_wiki_links(markdown: str, page: Page, config: MkDocsConfig) -> str:
    def repl(m: re.Match[str]):
        # [[title#heading|alias]]
        m2 = re.match(r'^(.+?)(#(.*?))?(\|(.*))?$', m.group(1), flags=re.U)
        title = m2.group(1).strip()
        heading = m2.group(3)
        alias = m2.group(5)

        if heading:
            heading = heading.strip()
        if alias:
            alias = alias.strip()

        if title.count('/') == 0 and title.count('\\') == 0 and title in wiki_name_map:
            # title 是一个文件名（无扩展名）
            md_link = wiki_name_map[title].src_uri
        else:
            # title 是一个文件路径（无扩展名），先展开为绝对路径
            abs_path = posixpath.normpath(posixpath.join(posixpath.dirname(page.file.src_uri), title))
            title = posixpath.splitext(posixpath.basename(abs_path))[0] # 改成文件名（无扩展名）

            if abs_path in wiki_path_map:
                md_link = wiki_path_map[abs_path].src_uri
            else:
                md_link = abs_path

        # 改成 .md 文件的相对路径，这样要是链接找不到了 MkDocs 会在控制台警告
        md_link = get_relative_url(md_link, page.file.src_uri)

        if heading:
            # 根据 toc 配置，生成 heading 的 id
            # https://python-markdown.github.io/extensions/toc/
            toc_config = config.mdx_configs['toc']
            heading_id = toc_config['slugify'](heading, toc_config.get('separator', '-'))
            md_link += f'#{heading_id}'

        if alias:
            display_name = alias
        elif heading:
            display_name = f'{title} > {heading}'
        else:
            display_name = title

        return f'[{display_name}]({md_link})'

    # [[]] 和 ![[]] 可以统一处理
    # 把 [[]] 转换成 []()，那么 ![[]] 自然就变成了 ![]()
    # 匹配链接内容时必须用惰性匹配，否则会把多个链接内容合并在一起
    return re.sub(r'\[\[(.*?)\]\]', repl, markdown, flags=re.M | re.U)

def transform_callouts(markdown: str, page: Page, config: MkDocsConfig) -> str:
    # 把 Obsidian 的 Callouts 转换为 Python Markdown Callouts 拓展的格式
    # https://help.obsidian.md/Editing+and+formatting/Callouts
    # https://oprypin.github.io/markdown-callouts/index.html

    def repl(m: re.Match[str]):
        callout_type = m.group(1)
        fold = (m.group(2) or '').translate(str.maketrans('+-', '!?'))
        title = m.group(3).strip()

        ans = f'>{fold} {callout_type.upper()}:'
        if len(title) > 0:
            ans += f' **{title}**'
        return ans

    # \s 会匹配换行符，所以改用 [^\S\r\n]
    return re.sub(r'^[^\S\r\n]*>[^\S\r\n]*\[!(.+?)\]([+-])?(.*)$', repl, markdown, flags=re.M | re.U)

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    markdown = transform_wiki_links(markdown, page, config)
    markdown = transform_callouts(markdown, page, config)
    return markdown
