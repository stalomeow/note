import logging
import feedparser
import copy
import time
import datetime
import paginate
import posixpath
import os

from tempfile import mkdtemp
from shutil import rmtree

from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section, Link
from mkdocs.structure.files import File, Files, InclusionLevel
from mkdocs.structure.nav import Navigation
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils.templates import TemplateContext
from mkdocs.plugins import PluginCollection

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'

RSS = [
    'https://blog.unity.com/feed',
    # 'https://sspai.com/feed',
    # 'https://blog.tonycrane.cc/atom.xml',
    'https://rsshub.app/blogread/newest',
    'https://rsshub.app/github/trending/daily/javascript/en',
    'https://rsshub.app/bangumi/moe',
]

class PostSource(object):
    def __init__(self, title, url, description) -> None:
        self.title = title
        self.url = url
        self.description = description
        self.posts: list[RSSPost] = []

class PostCategory(object):
    def __init__(self, url, title) -> None:
        self.url = url
        self.title = title

class RSSPost(object):
    def __init__(self, src: PostSource, entry):
        src.posts.append(self)

        self.src = src
        self.url = entry.link

        if hasattr(entry, 'author'):
            self.author = entry.author

        self.publish = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)).date()

        if hasattr(entry, 'tags'):
            self.categories = [PostCategory('', tag.term) for tag in entry.tags]
        else:
            self.categories = []

        self.content = f'<h2 id="_1"><a class="toclink" href="{entry.link}" target="_blank">{entry.title}</a></h2>'
        self.content += entry.description

# View
# class View(Page):
#     # Set necessary metadata
#     def read_source(self, config: MkDocsConfig):
#         super().read_source(config)

#         # Ensure template is set or use default
#         self.meta.setdefault('template', 'rss-news.html')

sources: list[PostSource] = []
posts: list[RSSPost] = []
srcFiles: list[File] = []
temp_dir = mkdtemp()

def fetch_posts():
    sources.clear()
    posts.clear()

    for rss in RSS:
        data = feedparser.parse(rss, agent=USER_AGENT)
        src = PostSource(data.feed.title, data.feed.link, data.feed.description)
        sources.append(src)

        for entry in data.entries:
            posts.append(RSSPost(src, entry))

    posts.sort(key=lambda p: p.publish, reverse=True)

# Create a file for the given path, which must point to a valid source file,
# either inside the temporary directory or the docs directory
def _path_to_file(path: str, config: MkDocsConfig, *, temp = True):
    assert path.endswith(".md")
    file = File(
        path,
        config.docs_dir if not temp else temp_dir,
        config.site_dir,
        config.use_directory_urls
    )

    # Hack: mark file as generated, so other plugins don't think it's part
    # of the file system. This is more or less a new quasi-standard that
    # still needs to be adopted by MkDocs, and was introduced by the
    # git-revision-date-localized-plugin - see https://bit.ly/3ZUmdBx
    if temp:
        file.generated_by = "material/blog"

    # Return file
    return file

# Create a file with the given content on disk
def _save_to_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, "w", encoding = "utf-8") as f:
        f.write(content)

def on_shutdown():
    rmtree(temp_dir)

def on_files(files: Files, config: MkDocsConfig):
    fetch_posts()

    srcFiles.clear()
    for src in sources:
        path = _format_path_for_src(src)

        # Create file for view, if it does not exist
        file = files.get_file_from_path(path)
        if not file or temp_dir not in file.abs_src_path:
            file = _path_to_file(path, config)
            files.append(file)

            # Create file in temporary directory and temporarily remove
            # from navigation, as we'll add it at a specific location
            _save_to_file(file.abs_src_path, f'# {src.title}\n\n- 简介：{src.description}\n- 链接：[{src.url}]({src.url}){{ target="_blank" }}')

        file.inclusion = InclusionLevel.NOT_IN_NAV
        srcFiles.append(file)

def _format_path_for_src(src: PostSource):
    # Normalize path and strip slashes at the beginning and end
    path = posixpath.normpath(src.title.strip("/"))
    return posixpath.join('news/feeds', f"{path}.md")

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    if len(srcFiles) == 0:
        return

    entry = None
    for page in nav.pages:
        if page.abs_url == '/news/':
            entry = page

    section = Section('来源', [])
    section.parent = entry.parent
    entry.parent.children.append(section)

    for i in range(len(srcFiles)):
        p = Page(sources[i].title, srcFiles[i], config)
        p.parent = section
        p.previous_page = entry
        p.next_page = entry.next_page

        siblings = section.children
        if len(siblings) > 0 and isinstance(siblings[-1], Page):
            p.previous_page = siblings[-1]
            siblings[-1].next_page = p
        siblings.append(p)

        nav.pages.append(p)

    if len(section.children) > 0:
        if entry.next_page is not None:
            entry.next_page.previous_page = section.children[-1]
        entry.next_page = section.children[0]

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    if page.abs_url != '/news/' and page.file not in srcFiles:
        return
    page.meta.setdefault('template', 'rss-news.html')

def on_page_context(context: TemplateContext, page: Page, config: MkDocsConfig, nav: Navigation):
    if page.abs_url == '/news/':
        context['posts'] = posts
        return

    try:
        idx = srcFiles.index(page.file)
        context['posts'] = sources[idx].posts
    except:
        pass
