import calendar
import feedparser
import functools
import itertools
import logging
import os
import yaml

from datetime import datetime, timedelta, timezone
from paginate import Page as Pagination
from typing import Iterable, Union

from mkdocs.config import Config
from mkdocs.config.config_options import DictOfItems, Optional, SubConfig, Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import InclusionLevel, File, Files
from mkdocs.structure.nav import Section
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext


TIME_ZONE = timezone(timedelta(hours=+8))


# region Configs

class RSSConfig(Config):
    feed = Type(str)
    url = Optional(Type(str))
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

# endregion


# region Structs

class MultiPagePostsInfo(object):
    def __init__(self, slug: str) -> None:
        self.slug: str = slug
        self.posts: list[PostInfo] = []
        self.files: list[File] = []

    @property
    def firstPageCanonicalUrl(self):
        if len(self.files) < 1:
            return None
        return self.files[0].page.canonical_url

    def _getFileDir(self, pageNum: int) -> str:
        """ 文件的相对目录 """
        raise NotImplementedError()

    def _getFileContent(self, pageNum: int) -> str:
        """ 文件的内容 """
        raise NotImplementedError()

    def _getPageFilePath(self, pageNum: int):
        """ 分页文件的路径 """
        if pageNum == 1:
            return os.path.join(self._getFileDir(pageNum), self.slug + '.md')
        return os.path.join(self._getFileDir(pageNum), self.slug, 'page', f'{pageNum}.md')

    def generateFiles(self, files: Files, config: MkDocsConfig, *, sortPosts=False):
        # 按时间倒序排序
        if sortPosts:
            self.posts.sort(key=lambda p: p.publish, reverse=True)

        i = 0
        while i < len(self.posts):
            lowInclusive = i
            highExclusive = min(lowInclusive + newsConfig.pagination_per_page, len(self.posts))
            i = highExclusive

            pageNum = lowInclusive // newsConfig.pagination_per_page + 1 # 页码，从 1 开始
            path = self._getPageFilePath(pageNum)
            file = files.get_file_from_path(path)

            # 不存在则生成文件
            if not file:
                file = File.generated(
                    config,
                    path,
                    content=self._getFileContent(pageNum),
                    inclusion=InclusionLevel.NOT_IN_NAV
                )
                files.append(file)

            self.files.append(file)
            file.parent_info__ = self
            file.posts_range__ = (lowInclusive, highExclusive)

class RSSInfo(MultiPagePostsInfo):
    def __init__(self, feed, slug, config: RSSConfig) -> None:
        super().__init__(slug)

        self.url = getattr(feed, 'link', '&lt;nil&gt;') if config.url is None else config.url
        self.title = getattr(feed, 'title', '&lt;nil&gt;') if config.title is None else config.title
        self.description = getattr(feed, 'description', '&lt;nil&gt;') if config.description is None else config.description

    def _getFileDir(self, pageNum: int):
        return 'news/rss'

    def _getFileContent(self, pageNum: int):
        return f'# {self.title}\n\n- 简介：{self.description}\n- 链接：[{self.url}]({self.url}){{ target="_blank" }}'

class PostInfo(object):
    def __init__(self, entry, srcRSS: RSSInfo, *, tags=True):
        self.srcRSS = srcRSS
        self.url = getattr(entry, 'link', srcRSS.url)
        self.meta = {} # 支持 mkdocs-glightbox

        if hasattr(entry, 'published_parsed'):
            # 从 GMT 时间计算 timestamp
            timestamp = calendar.timegm(entry.published_parsed)
            # 转换到指定的时区
            self.publish = datetime.fromtimestamp(timestamp, timezone.utc).astimezone(TIME_ZONE).date()
        else:
            self.publish = datetime.now(TIME_ZONE).date()

        if tags and hasattr(entry, 'tags'):
            self.tags = [tag.term for tag in entry.tags]
        else:
            self.tags = None

        self.content = f'<h2 id="_1"><a class="toclink" href="{entry.link}" target="_blank">{entry.title}</a></h2>'

        # 现在只留一个标题，不要内容了
        # if hasattr(entry, 'summary_detail'):
        #     if entry.summary_detail.type == 'text/plain':
        #         self.content += f'<p>{entry.summary_detail.value}</p>'
        #     else:
        #         self.content += entry.summary_detail.value

class CategoryInfo(MultiPagePostsInfo):
    def __init__(self, slug: str, title: str, description: Union[str, None]) -> None:
        super().__init__(slug)

        self.title = title
        self.description = description
        self.rssList: list[RSSInfo] = []

    def _getFileDir(self, pageNum: int):
        return 'news/cats'

    def _getFileContent(self, pageNum: int):
        content = f'# {self.title}'
        if self.description is not None:
            content += f'\n\n{self.description}'
        return content

    def generateFiles(self, files: Files, config: MkDocsConfig, *, sortPosts=False):
        self.posts.clear()
        self.posts.extend(itertools.chain(*map(lambda r: r.posts, self.rssList)))
        return super().generateFiles(files, config, sortPosts=sortPosts)

class HomeInfo(MultiPagePostsInfo):
    def __init__(self) -> None:
        super().__init__('index')

    def _getFileDir(self, pageNum: int):
        return 'news'

    def _getFileContent(self, pageNum: int):
        return ''

    def _getPageFilePath(self, pageNum: int):
        if pageNum == 1:
            return super()._getPageFilePath(pageNum)
        return os.path.join(self._getFileDir(pageNum), 'page', f'{pageNum}.md')

# endregion


newsConfig: NewsConfig = None
categoryList: list[CategoryInfo] = []
homeInfo: HomeInfo = None
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

def loadNewsConfig(config: MkDocsConfig):
    configDir = os.path.dirname(config.config_file_path)
    configPath = os.path.join(configDir, 'news.yml')

    global newsConfig
    newsConfig = NewsConfig(configPath)

    with open(configPath, 'r', encoding='utf-8') as fp:
        newsConfig.load_dict(yaml.load(fp, yaml.SafeLoader))

    errors, warnings = newsConfig.validate()
    for _, w in warnings:
        log.warning(w)

    for _, e in errors:
        raise PluginError(
            f"Error reading '{configPath}':\n"
            f"{e}"
        )

@build_only
def on_files(files: Files, config: MkDocsConfig):
    global homeInfo
    homeInfo = HomeInfo()
    categoryList.clear()

    loadNewsConfig(config)

    for catSlug, catConfig in newsConfig.categories.items():
        catInfo = CategoryInfo(catSlug, catConfig.title, catConfig.description)
        categoryList.append(catInfo)

        for rssSlug, rssConfig in catConfig.rss.items():
            data = feedparser.parse(rssConfig.feed, agent=newsConfig.user_agent)

            try:
                rssInfo = RSSInfo(data.feed, rssSlug, rssConfig)
                catInfo.rssList.append(rssInfo)
            except Exception as e:
                log.warning(f'Failed to parse {rssConfig.feed}; {e}')
                continue

            # 添加 RSS 中的文章
            for entry in data.entries:
                post = PostInfo(entry, rssInfo, tags=rssConfig.posts_tags)
                rssInfo.posts.append(post)
            rssInfo.generateFiles(files, config, sortPosts=True)

            # 添加 RSS 中的文章到首页
            if rssConfig.posts_show_in_home:
                newPostCount = 0
                for post in rssInfo.posts:
                    # 只添加两天内的文章
                    if (post.publish - datetime.now(TIME_ZONE).date()).days < -2:
                        break
                    newPostCount += 1
                    homeInfo.posts.append(post)

                # 如果没有新文章，则添加最新的一篇
                if newPostCount == 0 and len(rssInfo.posts) > 0:
                    homeInfo.posts.append(rssInfo.posts[0])

        catInfo.generateFiles(files, config, sortPosts=True)

    categoryList.sort(key=lambda c: c.title)
    homeInfo.generateFiles(files, config, sortPosts=True)

@build_only
def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    if len(newsConfig) == 0:
        return

    entry = None
    for page in nav.pages:
        if page.abs_url == '/news/':
            entry = page
    # 先把下面多余的东西删掉
    entry.parent.children.clear()
    entry.parent.children.append(entry)

    last = genPaginationFirstPages(entry, entry, nav, config, '分类', categoryList)
    genPaginationFirstPages(entry, last, nav, config, '来源', sorted(
        itertools.chain(*map(lambda c: c.rssList, categoryList)),
        key=lambda r: r.title
    ))

    for rssInfo in itertools.chain(*map(lambda c: c.rssList, categoryList)):
        genPaginationRestPages(rssInfo, nav, config)
    for catInfo in categoryList:
        genPaginationRestPages(catInfo, nav, config)
    genPaginationRestPages(homeInfo, nav, config)

def genPaginationFirstPages(
        entry: Page,
        prev: Page,
        nav: Navigation,
        config: MkDocsConfig,
        sectionName: str,
        postsInfoList: Union[Iterable[RSSInfo], Iterable[CategoryInfo]]
    ):
    section = Section(sectionName, [])
    section.parent = entry.parent
    entry.parent.children.append(section)

    end = prev.next_page

    for postsInfo in postsInfoList:
        if len(postsInfo.files) < 1:
            continue

        p = Page(postsInfo.title, postsInfo.files[0], config)
        nav.pages.append(p)

        p.parent = section
        section.children.append(p)

        # 把页面串起来
        p.previous_page = prev
        prev.next_page = p
        prev = p

        p.next_page = end

    if end is not None:
        end.previous_page = prev
    return prev

def genPaginationRestPages(postsInfo: MultiPagePostsInfo, nav: Navigation, config: MkDocsConfig):
    if len(postsInfo.files) < 2:
        return

    p = postsInfo.files[0].page
    # 把生成的分页文件的 previous_page、next_page、parent 设置成和第一页一样
    for file in postsInfo.files[1:]:
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
    page.meta.setdefault('search', { 'exclude': True })
    page.meta.setdefault('comments', False)

    if isinstance(page.file.parent_info__, HomeInfo):
        firstPage = page.file.parent_info__.files[0].page

        # 在第一页加上更新时间
        if page is firstPage:
            now = datetime.now(TIME_ZONE).strftime("%Y-%m-%d %H:%M:%S")
            return markdown + f'\n\n> 上次更新时间：{now} ({TIME_ZONE})。'

        # 后面几页直接用第一页的内容
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
