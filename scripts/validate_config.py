import logging

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import PluginCollection

PLUGIN_BLACKLIST = [
    'material/search',
    'minify',
]

SCRIPTS_BLACKLIST = [
    'assets/javascripts/comments.js',
]

is_serve_mode = False
log = logging.getLogger('mkdocs.plugins')

def on_startup(command: str, dirty: bool):
    global is_serve_mode
    is_serve_mode = (command == 'serve')

def pop_plugin(plugins: PluginCollection, name: str):
    value = plugins.pop(name, None)

    if value is None:
        return

    # ! Remove all registered events
    for attr_name in dir(value):
        if not attr_name.startswith('on_'):
            continue

        method = getattr(value, attr_name)

        if callable(method):
            # 这段代码是在 on_config 里执行的，MkDocs 正在遍历 on_config 的方法列表
            # 如果在下面删除其他插件的 on_config，会导致迭代器出错，所以这里只是把方法替换成一个空方法
            method_list = plugins.events[attr_name[3:]]
            method_list[method_list.index(method)] = (lambda *args, **kwargs: None)

def on_config(config: MkDocsConfig):
    if not is_serve_mode:
        return

    # 禁用一些插件，提高页面生成速度
    for plugin_name in PLUGIN_BLACKLIST:
        pop_plugin(config.plugins, plugin_name)
        log.warning('Disable plugin \'%s\' in serve mode', plugin_name)

    # 禁用一些 javascript
    for script in SCRIPTS_BLACKLIST:
        config.extra_javascript.remove(script)
        log.warning('Disable script \'%s\' in serve mode', script)

    return config