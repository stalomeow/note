import datetime
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
from typing import Callable, Union

class FileLinkNode(object):
    def __init__(self, file: File):
        self.file = file
        self.prev: FileLinkNode = None
        self.next: FileLinkNode = None

    # 将自己插入到 node 后面
    def insert_after(self, node: "FileLinkNode"):
        self.prev = node
        self.next = node.next
        if node.next:
            node.next.prev = self
        node.next = self

    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev

class FileLinkList(object):
    def __init__(self, file: File):
        self.file = file

        # 自己指向其他文章的链接
        # key 是其他文章的 src_uri
        # value 是插入到其他文章的 inverseLinks 中的节点
        self.links: dict[str, FileLinkNode] = {}

        # 其他文章指向自己的链接，使用有头结点的链表保存
        self.inverse_links = FileLinkNode(None)

    def clear_links(self):
        for l in self.links.values():
            l.remove()
        self.links.clear()

FOLDER_OBSIDIAN_VAULT = 'obsidian-vault'
FOLDER_NOTE = '笔记'
FOLDER_BLOG = '博客'
FOLDER_ATTACHMENT = 'attachments'

is_serve_mode = False
wiki_link_name_map: dict[str, File] = {}         # key 是文件名，无扩展名
wiki_link_path_map: dict[str, FileLinkList] = {} # key 是 src_uri
log = logging.getLogger('mkdocs.plugins')

def on_startup(command: str, dirty: bool):
    global is_serve_mode
    is_serve_mode = (command == 'serve')

def set_file_dest_uri(f: File, value: Union[str, Callable[[str], str]]):
    f.dest_uri = value if isinstance(value, str) else value(f.dest_uri)

    def delattr_if_exists(obj, attr):
        if hasattr(obj, attr):
            delattr(obj, attr)

    # 删掉 cached_property 的缓存
    delattr_if_exists(f, 'url')
    delattr_if_exists(f, 'abs_dest_path')

def process_obsidian_attachment(f: File):
    set_file_dest_uri(f, lambda uri: uri[uri.index(FOLDER_ATTACHMENT + '/'):]) # 去掉 obsidian-vault

def process_obsidian_note(f: File) -> bool:
    _, frontmatter = meta.get_data(f.content_string)

    if 'date' not in frontmatter:
        log.error('Obsidian document \'%s\' does not have a date.', f.src_uri)
        return False

    date = frontmatter['date']

    if not isinstance(date, datetime.datetime):
        log.error('Obsidian document \'%s\' has an invalid date.', f.src_uri)
        return False

    if frontmatter.get('draft', False):
        log.info('Obsidian document \'%s\' is a draft.', f.src_uri)

        # 在正式发布时不显示草稿
        if not is_serve_mode:
            return False

    slug = date.strftime('%y%m%d%H%M%S')

    # slug 目前用的是日期数字，这里把数字转换成字母
    table = str.maketrans(digits, ''.join(ascii_letters[int(i)] for i in digits), '-')
    slug = slug.translate(table).lower()

    # 重排一下并分组，让原本相似的数字看起来不太一样
    slug = '-'.join([slug[1::3], slug[2::3], slug[0::3]])

    if not f.use_directory_urls:
        set_file_dest_uri(f, posixpath.join('n', slug + '.html'))
    else:
        set_file_dest_uri(f, posixpath.join('n', slug, 'index.html'))
    return True

def process_obsidian_blog_post(f: File):
    setattr(f, 'obsidian_blog_post', True)

def post_process_obsidian_blog_posts(config: MkDocsConfig, files: Files):
    # 我们的 on_files 在 blog 插件之前运行，blog 插件也会修改 dest_uri
    # 所以只能把修改 dest_uri 的操作放在这里，在 on_nav 时执行，避免被 blog 插件覆盖

    for f in files:
        if not getattr(f, 'obsidian_blog_post', False):
            continue

        if not f.use_directory_urls:
            set_file_dest_uri(f, posixpath.join('p', f.page.config.slug + '.html'))
        else:
            set_file_dest_uri(f, posixpath.join('p', f.page.config.slug, 'index.html'))

        # https://github.com/squidfunk/mkdocs-material/blob/51c9f9acb013836910f8e190ca5041f16f09e643/src/plugins/blog/plugin.py#L403
        f.page._set_canonical_url(config.site_url)

@event_priority(100) # 放在最前面执行，不要处理其他插件生成的文件
def on_files(files: Files, config: MkDocsConfig):
    invalid_doc_count = 0
    valid_doc_count = 0
    invalid_files: list[File] = []
    wiki_link_name_map.clear()
    wiki_link_path_map.clear()

    def mark_file_invalid(f: File):
        if f.is_documentation_page():
            nonlocal invalid_doc_count
            invalid_doc_count += 1
        invalid_files.append(f)

    for f in files:
        path_names = f.src_uri.split('/')

        # 忽略 obsidian-vault 文件夹以外的文件
        # 路径中至少有一个斜杠，所以长度至少为 2
        if len(path_names) < 2 or path_names[0] != FOLDER_OBSIDIAN_VAULT:
            continue

        # 删除特定目录之外的文件
        # 路径中至少有两个斜杠，所以长度至少为 3
        if len(path_names) < 3 or path_names[1] not in (FOLDER_NOTE, FOLDER_BLOG, FOLDER_ATTACHMENT):
            mark_file_invalid(f)
            continue

        if path_names[1] == FOLDER_ATTACHMENT:
            process_obsidian_attachment(f)
        elif f.is_documentation_page():
            if path_names[1] == FOLDER_NOTE:
                if not process_obsidian_note(f):
                    mark_file_invalid(f)
                    continue
            elif path_names[1] == FOLDER_BLOG:
                process_obsidian_blog_post(f)
            valid_doc_count += 1

        wiki_link_name_map[posixpath.basename(f.src_uri)] = f
        wiki_link_path_map[f.src_uri] = FileLinkList(f)

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

    # 将 obsidian-vault 下的笔记作为 root，其他丢弃
    for child in item.children:
        if child.title == FOLDER_NOTE:
            child.title = 'Note'
            child.parent = None
            nav.items[i] = child
            return child
    else:
        raise Exception('Obsidian notes not found in navigation.')

def move_index_page_and_obsidian_root(nav: Navigation, obsidian_root: Section):
    sections = []
    others = []

    for item in nav.items:
        if isinstance(item, Section):
            sections.append(item)
        else:
            others.append(item)

    # 将 obsidian root 移到 sections 最前面
    sections.remove(obsidian_root)
    sections.insert(0, obsidian_root)

    # 将 sections 放在后面
    nav.items.clear()
    nav.items.extend(others)
    nav.items.extend(sections)

def get_str_sort_key(s: str):
    start_with_english = s[0] in ascii_letters

    # 把中文变成拼音（无音调），不是中文的部分保留
    pinyin = pypinyin.lazy_pinyin(s, style=pypinyin.Style.NORMAL, errors='default', v_to_u=False)

    # 按照 obsidian 的风格，以英文开头的内容排在中文开头的后面，不区分大小写
    return (start_with_english, ''.join(pinyin).lower())

@event_priority(-100) # 放在最后执行
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
        return get_str_sort_key(key)

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

    post_process_obsidian_blog_posts(config, files)
    obsidian_root = find_and_update_obsidian_root(nav)
    dfs(obsidian_root) # 将下面的文章重新排序
    move_index_page_and_obsidian_root(nav, obsidian_root)
    return nav

def transform_wiki_links(markdown: str, page: Page, config: MkDocsConfig) -> str:
    link_list = wiki_link_path_map.get(page.file.src_uri)

    if link_list is not None:
        assert (link_list.file == page.file)
        link_list.clear_links() # 重新解析链接

    def recordLink(target_file: File):
        if link_list is None or target_file.src_uri in link_list.links:
            return

        node = FileLinkNode(page.file)
        link_list.links[target_file.src_uri] = node
        node.insert_after(wiki_link_path_map[target_file.src_uri].inverse_links)

    def repl(m: re.Match[str]):
        is_media = m.group(1) is not None

        # [[name#heading|alias]]
        # 在表格中使用 wiki link 时，需要用 '\\|' 代替 '|'，这里去掉 '\\'
        m2 = re.match(r'^(.+?)(#(.*?))?(\|(.*))?$', m.group(2).replace('\\', ''), flags=re.U)
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
                md_link = wiki_link_path_map[abs_path].file.src_uri
            else:
                md_link = abs_path

        # 记录反向链接
        if not is_media:
            if md_link in wiki_link_path_map:
                recordLink(wiki_link_path_map[md_link].file)
            else:
                log.warning('Failed to resolve link \'%s\' in \'%s\'.', md_link, page.file.src_uri)

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
    return re.sub(r'(!)?\[\[(.*?)\]\]', repl, markdown, flags=re.M|re.U)

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
    return re.sub(r'^[^\S\r\n]*>[^\S\r\n]*\[!(.+?)\]([+-])?(.*)$', repl, markdown, flags=re.M|re.U)

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    markdown = transform_wiki_links(markdown, page, config)
    markdown = transform_callouts(markdown, page, config)
    return markdown

# 在 minify 之前执行
@event_priority(50)
def on_post_page(output: str, page: Page, config: MkDocsConfig):
    link_list = wiki_link_path_map.get(page.file.src_uri)
    if link_list is None:
        return

    assert (link_list.file == page.file)

    # 获取并排序反向链接
    inverse_link_files: list[File] = []
    head = link_list.inverse_links # 注意有个头结点
    while head.next != None:
        inverse_link_files.append(head.next.file)
        head = head.next
    if len(inverse_link_files) <= 0:
        return
    inverse_link_files.sort(key=lambda f: get_str_sort_key(f.page.title))

    links_html = r'<details class="tip" style="margin-top:0"><summary>反向链接</summary><ul>'
    for link_file in inverse_link_files:
        href = get_relative_url(link_file.page.abs_url, page.abs_url)
        links_html += rf'<li><a href="{href}">{link_file.page.title}</a></li>'
    links_html += r'</ul></details><br>'
    return re.sub(r'<article class=".*?">', rf'\g<0>{links_html}', output, count=1)
