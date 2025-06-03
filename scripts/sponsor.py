import logging

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Link

TITLE = 'Sponsor'
URL = 'https://stalomeow.com/#coffee'

log = logging.getLogger('mkdocs.plugins')

def on_config(config: MkDocsConfig):
    # 底部按钮
    config.extra['social'].append({
        'name': TITLE,
        'icon': 'fontawesome/solid/heart',
        'link': URL,
    })
    return config

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    link = Link(title=TITLE, url=URL)
    link.meta = {
        'icon': 'material/heart',
    }
    nav.items.append(link)
    return nav
