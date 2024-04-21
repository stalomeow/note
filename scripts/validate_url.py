import os
import posixpath

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.utils import meta

def on_files(files: Files, config: MkDocsConfig):
    invalid_files = []

    for f in files:
        if not f.is_documentation_page():
            continue

        # '.' 开头的会被自动忽略，不用处理
        if f.src_uri.startswith('Obsidian Notes/_templates'):
            invalid_files.append(f)
            continue

        with open(f.abs_src_path, encoding='utf-8-sig', errors='strict') as fp:
            source = fp.read()
        _, frontmatter = meta.get_data(source)

        if "slug" in frontmatter:
            slug = str(frontmatter["slug"])
            if not config.use_directory_urls:
                f.dest_uri = slug + '.html'
            else:
                f.dest_uri = posixpath.join(slug, 'index.html')

            f.url = f._get_url(config.use_directory_urls)
            f.abs_dest_path = os.path.normpath(os.path.join(config.site_dir, f.dest_uri))

            # print(f.url)

    for f in invalid_files:
        files.remove(f)
    return files
