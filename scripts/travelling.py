import logging

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Link

# https://github.com/travellings-link/travellings
# https://github.com/travellings-link/travellings/blob/master/docs/join.md

TITLE = 'Travelling'
URL = 'https://www.travellings.cn/go.html'

log = logging.getLogger('mkdocs.plugins')

def on_config(config: MkDocsConfig):
    # 底部按钮
    config.extra['social'].append({
        'name': TITLE,
        'icon': 'fontawesome/solid/train-subway',
        'link': URL
    })
    return config

def on_nav(nav: Navigation, config: MkDocsConfig, files: Files):
    nav.items.append(Link(title=TITLE, url=URL))
    return nav
