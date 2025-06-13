import datetime
import inspect
import logging

from mkdocs.config.defaults import MkDocsConfig

log = logging.getLogger('mkdocs.plugins')

def get_copyright() -> str:
    tz = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz)
    return inspect.cleandoc(f'''
        Copyright &copy; 2022-{now.strftime('%Y')} Stalo. All rights reserved. Built on {now.strftime('%Y-%m-%d (UTC+8)')}.<br>
        Contents are licensed under the <u><a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener">CC BY-NC 4.0</a></u> license, except when otherwise noted.
        ''')

def on_config(config: MkDocsConfig):
    config.copyright = get_copyright()
    return config
