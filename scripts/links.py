import logging

from dataclasses import dataclass
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Link

@dataclass
class LinkData:
    name: str
    url: str
    button_icon: str
    link_icon: str

LINKS = [
    LinkData(
        name='Homepage',
        url='https://stalomeow.com',
        button_icon='fontawesome/solid/house',
        link_icon='material/home',
    ),
    LinkData(
        name='Sponsor',
        url='https://stalomeow.com/#coffee',
        button_icon='fontawesome/solid/heart',
        link_icon='material/heart',
    ),
    LinkData(
        # https://github.com/travellings-link/travellings
        # https://github.com/travellings-link/travellings/blob/master/docs/join.md
        name='Travelling',
        url='https://www.travellings.cn/go.html',
        button_icon='fontawesome/solid/train-subway',
        link_icon='material/train',
    ),
]

log = logging.getLogger('mkdocs.plugins')

def on_config(config: MkDocsConfig):
    # 底部按钮
    buttons = config.extra.setdefault('social', [])
    buttons.extend(map(lambda l: {
        'name': l.name,
        'icon': l.button_icon,
        'link': l.url,
    }, LINKS))
    return config

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    # 导航栏链接
    for l in LINKS:
        link = Link(title=l.name, url=l.url)
        link.meta = { 'icon': l.link_icon }
        nav.items.append(link)
    return nav