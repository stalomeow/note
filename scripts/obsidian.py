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

wiki_link_name_map: dict[str, File] = {}
wiki_link_path_map: dict[str, File] = {}
log = logging.getLogger('mkdocs.plugins')

def transform_slug(slug: str) -> str:
    # slug 目前用的是日期数字，这里把数字转换成字母
    table = str.maketrans(digits, ''.join(ascii_letters[int(i)] for i in digits), '-')
    slug = slug.translate(table).lower()

    # 重排一下并分组，让原本相似的数字看起来不太一样
    return '-'.join([slug[1::3], slug[2::3], slug[0::3]])

def should_ignore_obsidian_file(f: File) -> bool:
    top_folder = f.src_uri.split('/')[1] # [0] 是 obsidian vault

    # 配置文件和模板文件
    if top_folder in ('.obsidian', 'templates'):
        return True

    # Excalidraw 原始文件
    if f.src_uri.endswith('.excalidraw.md'):
        return True

    return False

def is_obsidian_note_file(f: File) -> bool:
    if not f.is_documentation_page():
        return False
    return f.src_uri.startswith(posixpath.join(OBSIDIAN_VAULT_DIR, 'notes'))

@event_priority(100) # 放在最前面执行，不要处理其他插件生成的文件
def on_files(files: Files, config: MkDocsConfig):
    invalid_doc_count = 0
    valid_doc_count = 0
    invalid_files: list[File] = []
    wiki_link_name_map.clear()
    wiki_link_path_map.clear()

    for f in files:
        # 忽略 Obsidian Vault 之外的文件
        if not f.src_uri.startswith(posixpath.join(OBSIDIAN_VAULT_DIR, '')):
            continue

        if should_ignore_obsidian_file(f):
            if f.is_documentation_page():
                invalid_doc_count += 1
            invalid_files.append(f)
            continue

        if f.is_documentation_page():
            valid_doc_count += 1

            # notes 里的文档需要处理 slug
            if is_obsidian_note_file(f):
                _, frontmatter = meta.get_data(f.content_string)

                # 有 slug 的话就用 slug 作为文件名
                if 'slug' in frontmatter:
                    slug = transform_slug(str(frontmatter['slug']))
                    if not f.use_directory_urls:
                        f.dest_uri = posixpath.join('', slug + '.html')
                    else:
                        f.dest_uri = posixpath.join('', slug, 'index.html')
                else:
                    log.warning('Obsidian document \'%s\' does not have a slug.', f.src_uri)

        wiki_link_name_map[posixpath.basename(f.src_uri)] = f
        wiki_link_path_map[f.src_uri] = f

    total_doc_count = invalid_doc_count + valid_doc_count
    log.info('Found %d obsidian documents (%d ignored).', total_doc_count, invalid_doc_count)

    for f in invalid_files:
        files.remove(f)
    return files

def find_and_update_obsidian_root(nav: Navigation) -> Section:
    # 找到 obsidian-vault
    for i, item in enumerate(nav.items):
        if isinstance(item, Section) and item.title.lower().count('obsidian') > 0:
            break
    else:
        raise Exception('Obsidian vault not found in navigation.')

    # 将 obsidian-vault 下的 notes 作为 root，其他丢弃
    for child in item.children:
        if child.title.lower() == 'notes':
            child.parent = None
            nav.items[i] = child
            return child
    else:
        raise Exception('Obsidian notes not found in navigation.')

def move_index_page_and_obsidian_root(nav: Navigation, obsidian_root: Section):
    # 找到网站的 index
    for i, item in enumerate(nav.items):
        if isinstance(item, Page) and item.is_index:
            break
    else:
        raise Exception('Index page not found in navigation.')

    # 将网站的 index 放到 obsidian root 下的最前面
    nav.items.pop(i)
    item.parent = obsidian_root
    obsidian_root.children.insert(0, item)

    # 将 obsidian root 移到最前面
    nav.items.remove(obsidian_root)
    nav.items.insert(0, obsidian_root)

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
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

    obsidian_root = find_and_update_obsidian_root(nav)
    dfs(obsidian_root) # 将下面的文章重新排序
    move_index_page_and_obsidian_root(nav, obsidian_root)
    return nav

def transform_wiki_links(markdown: str, page: Page, config: MkDocsConfig) -> str:
    def repl(m: re.Match[str]):
        is_media = m.group(1) is not None

        # [[name#heading|alias]]
        m2 = re.match(r'^(.+?)(#(.*?))?(\|(.*))?$', m.group(2), flags=re.U)
        name = m2.group(1).strip()
        heading = m2.group(3)
        alias = m2.group(5)

        # 自动给文档加 .md 后缀名
        if not is_media and (name + '.md') in wiki_link_name_map:
            name += '.md'

        if heading:
            heading = heading.strip()
        if alias:
            alias = alias.strip()

        if name.count('/') == 0 and name in wiki_link_name_map:
            # name 是一个文件名
            md_link = wiki_link_name_map[name].src_uri
        else:
            # name 是一个文件路径，先展开为绝对路径
            abs_path = posixpath.normpath(posixpath.join(posixpath.dirname(page.file.src_uri), name))

            if abs_path in wiki_link_path_map:
                md_link = wiki_link_path_map[abs_path].src_uri
            else:
                md_link = abs_path

        # 改成文件的相对路径，这样要是链接找不到了 MkDocs 会在控制台警告
        md_link = get_relative_url(md_link, page.file.src_uri)
        title = posixpath.splitext(posixpath.basename(name))[0] # 标题不要后缀名

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

        return ('!' if is_media else '') + f'[{display_name}]({md_link})'

    # 匹配链接内容时必须用惰性匹配，否则会把多个链接内容合并在一起
    return re.sub(r'(!)?\[\[(.*?)\]\]', repl, markdown, flags=re.M | re.U)

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
