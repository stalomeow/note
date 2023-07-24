from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section, Link
from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig

import logging
import re

def get_url(element: Section | Page | Link):
    if not isinstance(element, Section):
        return element.abs_url

    for child in element.children:
        if isinstance(child, Page) and child.is_index:
            return child.abs_url

    return None

def get_markdowns(element: Section | Page | Link, indentCount: int):
    indent = '    ' * indentCount
    content = ''

    # Vercel 还不支持 match-case
    # match get_url(element):
    #     case str() as url:
    #         content = f'- [{element.title}]({url})\n'
    #     case _:
    #         content = f'- {element.title}\n'

    url = get_url(element)

    if isinstance(url, str):
        content = f'- [{element.title}]({url})\n'
    else:
        content = f'- {element.title}\n'

    return (indent, content)

def generate_toc(page: Page):
    markdowns = ['\n## Table of Contents\n']
    iterStack = [iter(page.parent.children)]

    while len(iterStack) > 0:
        try:
            child = next(iterStack[-1])

            if getattr(child, 'is_index', False):
                continue

            markdowns.extend(get_markdowns(child, len(iterStack) - 1))

            if child.children is not None:
                iterStack.append(iter(child.children))
        except StopIteration:
            iterStack.pop()

    return ''.join(markdowns)

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    # 只处理不是首页的 index
    if (not page.is_index) or (page.abs_url == '/'):
        return markdown

    log = logging.getLogger('mkdocs')

    if page.meta.get('comments', True):
        log.warning('[index-validator] \'%s\' should have comments disabled.', page.file.abs_src_path)

    if re.search(r'^ *#{2,6} +Table of Contents *$', markdown, flags=re.MULTILINE):
        log.warning('[index-validator] \'%s\' may have duplicated TOC.', page.file.abs_src_path)

    return markdown + generate_toc(page)