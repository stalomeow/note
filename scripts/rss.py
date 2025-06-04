import datetime
import email.utils
import html
import inspect
import logging
import posixpath

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files, InclusionLevel

FILE_NAME = 'rss.xml'

log = logging.getLogger('mkdocs.plugins')

def get_content(config: MkDocsConfig) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    build_datetime = html.escape(email.utils.format_datetime(now))
    return inspect.cleandoc(f'''
        <?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
        <channel>
            <title>{html.escape(config.site_name)}</title>
            <description>{html.escape(config.site_description or config.site_name)}</description>
            <link>{html.escape(config.site_url)}</link>
            <atom:link href="{posixpath.join(config.site_url, FILE_NAME)}" rel="self" type="application/rss+xml" />
            <docs>{html.escape(config.repo_url)}</docs>
            <language>zh</language>
            <pubDate>{build_datetime}</pubDate>
            <lastBuildDate>{build_datetime}</lastBuildDate>
            <ttl>1440</ttl>
            <generator>This site no longer provides RSS and the file is only for backward compatibility</generator>
        </channel>
        </rss>
        ''')

def on_files(files: Files, config: MkDocsConfig):
    files.append(File.generated(config, FILE_NAME,
        content=get_content(config),
        inclusion=InclusionLevel.INCLUDED))
