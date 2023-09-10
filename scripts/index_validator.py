import logging
import re

from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section, Link
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig
from typing import Union

isServeMode = False
log = logging.getLogger('mkdocs.plugins')

def on_startup(command: str, dirty: bool):
    global isServeMode
    isServeMode = (command == 'serve')

def get_url(element: Union[Section, Page, Link]):
    if not isinstance(element, Section):
        return element.abs_url

    # Section 对应这种情况：
    # - 游戏开发:
    #   - gamedev/index.md
    for child in element.children:
        if isinstance(child, Page) and child.is_index:
            return child.abs_url

    return None

def get_url_and_markdown(element: Union[Section, Page, Link], indentCount: int):
    url = get_url(element)
    indent = '    ' * indentCount
    content = ''

    if isinstance(url, str):
        content = f'- [{element.title}]({url})\n'
    else:
        content = f'- {element.title}\n'

    return (url, indent + content)

def generate_toc(page: Page):
    markdowns = ['\n## Table of Contents { data-search-exclude }\n']

    if isServeMode:
        markdowns.append('- TOC is disabled in serve mode in order to improve performance.\n')
    else:
        iterStack = [iter(page.parent.children)]

        while len(iterStack) > 0:
            try:
                child = next(iterStack[-1])

                # 跳过这种：
                # - gamedev/index.md
                if getattr(child, 'is_index', False):
                    continue

                url, md = get_url_and_markdown(child, len(iterStack) - 1)
                markdowns.append(md)

                if child.children is not None:
                    # 如果这个 Section 有自己的 index，那就不往下遍历了
                    if not (isinstance(child, Section) and isinstance(url, str)):
                        iterStack.append(iter(child.children))
            except StopIteration:
                iterStack.pop()

    return ''.join(markdowns)

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    # 只处理不是首页的 index
    if (not page.is_index) or (page.abs_url == '/'):
        return markdown

    if page.meta.get('comments', True):
        log.warning('[index-validator] \'%s\' should have comments disabled.', page.file.abs_src_path)

    if re.search(r'^ *#{2,6} +Table of Contents *$', markdown, flags=re.M | re.I):
        log.warning('[index-validator] \'%s\' may have duplicated TOC.', page.file.abs_src_path)

    return markdown + generate_toc(page)