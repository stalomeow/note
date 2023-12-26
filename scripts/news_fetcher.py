import logging
import feedparser
import time
import os
import itertools
import yaml
import functools

from tempfile import mkdtemp
from shutil import rmtree
from datetime import datetime
from paginate import Page as Pagination
from typing import Union

from mkdocs.config import Config
from mkdocs.config.config_options import DictOfItems, Optional, SubConfig, Type
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section
from mkdocs.structure.files import File, Files, InclusionLevel
from mkdocs.structure.nav import Navigation
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils.templates import TemplateContext

# ------------------------------------------------
# Configs
# ------------------------------------------------

class RSSConfig(Config):
    url = Type(str)
    title = Optional(Type(str))
    description = Optional(Type(str))
    posts_tags = Type(bool, default=True)
    posts_show_in_home = Type(bool, default=True)

class CategoryConfig(Config):
    title = Type(str)
    description = Optional(Type(str))
    rss = DictOfItems(SubConfig(RSSConfig), default={})

class NewsConfig(Config):
    user_agent = Type(str)
    pagination_per_page = Type(int, default=10)
    categories = DictOfItems(SubConfig(CategoryConfig), default={})

# ------------------------------------------------
# Structs
# ------------------------------------------------

class MultiPagePostsInfo(object):
    def __init__(self, slug: str, posts: list["PostInfo"]) -> None:
        self.slug = slug
        self.posts = posts
        self.files: list[File] = []

    @property
    def firstPageCanonicalUrl(self):
        return self.files[0].page.canonical_url

    def _getFileDir(self):
        pass

    def _getFileContent(self):
        pass

    def _getPageFilePath(self, pageNum):
        if pageNum == 1:
            return os.path.join(self._getFileDir(), self.slug + '.md')
        return os.path.join(self._getFileDir(), self.slug, 'page', f'{pageNum}.md')

    def generateFiles(self, srcDir: str, files: Files, config: MkDocsConfig):
        i = 0

        while i < len(self.posts):
            lowInclusive = i
            highExclusive = min(lowInclusive + newsConfig.pagination_per_page, len(self.posts))
            i = highExclusive

            path = self._getPageFilePath(lowInclusive // newsConfig.pagination_per_page + 1)
            file = files.get_file_from_path(path)
            if not file:
                file = File(
                    path,
                    srcDir,
                    config.site_dir,
                    config.use_directory_urls
                )
                file.inclusion = InclusionLevel.NOT_IN_NAV
                files.append(file)

                # Hack: mark file as generated, so other plugins don't think it's part
                # of the file system. This is more or less a new quasi-standard that
                # still needs to be adopted by MkDocs, and was introduced by the
                # git-revision-date-localized-plugin - see https://bit.ly/3ZUmdBx
                file.generated_by = 'stalomeow/news'

                # Create file in temporary directory and temporarily remove
                # from navigation, as we'll add it at a specific location
                self._saveFile(file.abs_src_path, self._getFileContent())

            self.files.append(file)
            file.parent_info__ = self
            file.posts_range__ = (lowInclusive, highExclusive)

    # Create a file with the given content on disk
    def _saveFile(self, path: str, content: str):
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, "w", encoding = "utf-8") as f:
            f.write(content)

    def deleteFiles(self, srcDir: str):
        for file in self.files:
            if srcDir not in file.abs_src_path:
                continue
            os.remove(file.abs_src_path)
        self.files.clear()

class RSSInfo(MultiPagePostsInfo):
    def __init__(self, feed, slug, config: RSSConfig) -> None:
        super().__init__(slug, [])

        self.url = feed.link
        self.title = feed.title
        self.description = feed.description

        if config.title is not None:
            self.title = config.title
        if config.description is not None:
            self.description = config.description

    def _getFileDir(self):
        return 'news/rss'

    def _getFileContent(self):
        return f'# {self.title}\n\n- 简介：{self.description}\n- 链接：[{self.url}]({self.url}){{ target="_blank" }}'

class PostInfo(object):
    def __init__(self, entry, srcRSS: RSSInfo, *, tags=True):
        self.srcRSS = srcRSS
        self.url = getattr(entry, 'link', srcRSS.url)

        if hasattr(entry, 'published_parsed'):
            timestamp = time.mktime(entry.published_parsed)
            self.publish = datetime.fromtimestamp(timestamp).date()
        else:
            self.publish = datetime.today().date()

        if tags and hasattr(entry, 'tags'):
            self.tags = [tag.term for tag in entry.tags]
        else:
            self.tags = None

        self.content = f'<h2 id="_1"><a class="toclink" href="{entry.link}" target="_blank">{entry.title}</a></h2>'

        if hasattr(entry, 'summary_detail'):
            if entry.summary_detail.type == 'text/plain':
                self.content += f'<p>{entry.summary_detail.value}</p>'
            else:
                self.content += entry.summary_detail.value

class CategoryInfo(MultiPagePostsInfo):
    def __init__(self, slug: str, title: str, description: Union[str, None], rssList: list[RSSInfo]) -> None:
        posts = itertools.chain(*map(lambda r: r.posts, rssList))
        super().__init__(slug, sorted(posts, key=lambda p: p.publish, reverse=True))

        self.title = title
        self.description = description
        self.rssList = rssList

    def _getFileDir(self):
        return 'news/cats'

    def _getFileContent(self):
        content = f'# {self.title}'
        if self.description is not None:
            content += f'\n\n{self.description}'
        return content

class HomeInfo(MultiPagePostsInfo):
    def __init__(self) -> None:
        super().__init__('index', [])

    def _getFileDir(self):
        return 'news'

    def _getFileContent(self):
        return ''

    def _getPageFilePath(self, pageNum):
        if pageNum == 1:
            return super()._getPageFilePath(pageNum)
        return os.path.join(self._getFileDir(), 'page', f'{pageNum}.md')

# ------------------------------------------------
# Logics
# ------------------------------------------------

temp_dir = None
newsConfig: NewsConfig = None
categoryList: list[CategoryInfo] = []
homeInfo = HomeInfo()
isServeMode = False
log = logging.getLogger('mkdocs.plugins')

def build_only(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        if not isServeMode:
            return func(*args, **kwargs)
    return f

def on_startup(command: str, dirty: bool):
    global isServeMode
    isServeMode = (command == 'serve')
    _on_startup_impl(command, dirty)

@build_only
def _on_startup_impl(command: str, dirty: bool):
    global temp_dir
    temp_dir = mkdtemp()

@build_only
def on_shutdown():
    rmtree(temp_dir)

def loadNewsConfig(config: MkDocsConfig):
    configDir = os.path.dirname(config.config_file_path)
    configPath = os.path.join(configDir, '.news.yaml')

    global newsConfig
    newsConfig = NewsConfig(configPath)

    with open(configPath, 'r', encoding='utf-8') as fp:
        newsConfig.load_dict(yaml.load(fp, yaml.SafeLoader))

    errors, warnings = newsConfig.validate()
    for _, w in warnings:
        print(w)
    for _, e in errors:
        # raise PluginError(
        #     f"Error reading authors file '{path}' in '{docs}':\n"
        #     f"{e}"
        # )
        print(e)

@build_only
def on_files(files: Files, config: MkDocsConfig):
    for cat in categoryList:
        cat.deleteFiles(temp_dir)
        for rss in cat.rssList:
            rss.deleteFiles(temp_dir)
    categoryList.clear()
    homeInfo.posts.clear()
    homeInfo.deleteFiles(temp_dir)

    loadNewsConfig(config)

    for catSlug, catConfig in newsConfig.categories.items():
        rssList = []
        for rssSlug, rssConfig in catConfig.rss.items():
            data = feedparser.parse(rssConfig.url, agent=newsConfig.user_agent)

            try:
                rssInfo = RSSInfo(data.feed, rssSlug, rssConfig)
                rssList.append(rssInfo)
            except Exception as e:
                log.warning(f'Failed to parse {rssConfig.url}; {e}')
                continue

            for entry in data.entries:
                post = PostInfo(entry, rssInfo, tags=rssConfig.posts_tags)
                rssInfo.posts.append(post)

            rssInfo.posts.sort(key=lambda p: p.publish, reverse=True)
            rssInfo.generateFiles(temp_dir, files, config)

            if rssConfig.posts_show_in_home:
                newPostCount = 0
                for post in rssInfo.posts:
                    if (post.publish - datetime.today().date()).days < -2:
                        break
                    newPostCount += 1
                    homeInfo.posts.append(post)

                if newPostCount == 0 and len(rssInfo.posts) > 0:
                    homeInfo.posts.append(rssInfo.posts[0])

        catInfo = CategoryInfo(catSlug, catConfig.title, catConfig.description, rssList)
        catInfo.generateFiles(temp_dir, files, config)
        categoryList.append(catInfo)

    categoryList.sort(key=lambda c: c.title)
    homeInfo.posts.sort(key=lambda p: p.publish, reverse=True)
    homeInfo.generateFiles(temp_dir, files, config)

@build_only
def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    if len(newsConfig) == 0:
        return

    entry = None
    for page in nav.pages:
        if page.abs_url == '/news/':
            entry = page

    last = genCatPages(entry, entry, nav, config, files)
    genRSSPages(entry, last, nav, config, files)

    genRSSPaginationPages(entry, entry, nav, config, files)
    genCatPaginationPages(entry, entry, nav, config, files)
    genHomePaginationPages(entry, entry, nav, config, files)

def genRSSPages(entry: Page, prev: Page, nav: Navigation, config: MkDocsConfig, files: Files):
    section = Section('来源', [])
    section.parent = entry.parent
    entry.parent.children.append(section)

    end = prev.next_page

    for rssInfo in sorted(itertools.chain(*map(lambda c: c.rssList, categoryList)), key=lambda r: r.title):
        p = Page(rssInfo.title, rssInfo.files[0], config)
        nav.pages.append(p)

        p.parent = section
        section.children.append(p)

        p.previous_page = prev
        prev.next_page = p
        prev = p

        p.next_page = end

    if end is not None:
        end.previous_page = prev
    return prev

def genRSSPaginationPages(entry: Page, prev: Page, nav: Navigation, config: MkDocsConfig, files: Files):
    for rssInfo in itertools.chain(*map(lambda c: c.rssList, categoryList)):
        for file in rssInfo.files[1:]:
            p = rssInfo.files[0].page
            subPage = Page(rssInfo.title, file, config)
            subPage.previous_page = p.previous_page
            subPage.next_page = p.next_page
            subPage.parent = p.parent

            nav.pages.append(subPage)

def genCatPages(entry: Page, prev: Page, nav: Navigation, config: MkDocsConfig, files: Files):
    section = Section('分类', [])
    section.parent = entry.parent
    entry.parent.children.append(section)

    end = prev.next_page

    for cat in categoryList:
        p = Page(cat.title, cat.files[0], config)
        nav.pages.append(p)

        p.parent = section
        section.children.append(p)

        p.previous_page = prev
        prev.next_page = p
        prev = p

        p.next_page = end

    if end is not None:
        end.previous_page = prev
    return prev

def genCatPaginationPages(entry: Page, prev: Page, nav: Navigation, config: MkDocsConfig, files: Files):
    for cat in categoryList:
        for file in cat.files[1:]:
            p = cat.files[0].page
            subPage = Page(cat.title, file, config)
            subPage.previous_page = p.previous_page
            subPage.next_page = p.next_page
            subPage.parent = p.parent

            nav.pages.append(subPage)

def genHomePaginationPages(entry: Page, prev: Page, nav: Navigation, config: MkDocsConfig, files: Files):
    for file in homeInfo.files[1:]:
        p = homeInfo.files[0].page
        subPage = Page(p.title, file, config)
        subPage.previous_page = p.previous_page
        subPage.next_page = p.next_page
        subPage.parent = p.parent

        nav.pages.append(subPage)

@build_only
def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files):
    if not hasattr(page.file, 'parent_info__'):
        return

    page.meta.setdefault('template', 'rss-news.html')

    if isinstance(page.file.parent_info__, HomeInfo):
        firstPage = page.file.parent_info__.files[0].page
        return firstPage.markdown

@build_only
def on_page_context(context: TemplateContext, page: Page, config: MkDocsConfig, nav: Navigation):
    if not hasattr(page.file, 'parent_info__'):
        return

    if hasattr(page.file, 'posts_range__'):
        postsRange = page.file.posts_range__
        posts = page.file.parent_info__.posts

        pagination = Pagination(
            posts,
            page=(postsRange[0] // newsConfig.pagination_per_page + 1),
            items_per_page=newsConfig.pagination_per_page,
            item_count=len(posts),
            url_maker=lambda n: page.file.parent_info__.files[n-1].page.canonical_url
        )

        context['posts'] = posts[postsRange[0]:postsRange[1]]
        context["pagination"] = lambda args: pagination.pager(
            format = '~2~',
            show_if_single_page = True,
            **args
        )
    else:
        context['posts'] = page.file.parent_info__.posts
