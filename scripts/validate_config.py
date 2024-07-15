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

def pop_plugin(plugins: PluginCollection, name: str):
    value = plugins.pop(name, None)

    if value is None:
        return

    # ! Remove all registered events
    for attrName in dir(value):
        if not attrName.startswith('on_'):
            continue

        method = getattr(value, attrName)

        if callable(method):
            plugins.events[attrName[3:]].remove(method)

isServeMode = False
log = logging.getLogger('mkdocs.plugins')

def on_startup(command: str, dirty: bool):
    global isServeMode
    isServeMode = (command == 'serve')

def on_config(config: MkDocsConfig):
    if not isServeMode:
        return

    # 禁用一些插件，提高页面生成速度
    for pluginName in PLUGIN_BLACKLIST:
        pop_plugin(config.plugins, pluginName)
        log.warning('Disable plugin \'%s\' in serve mode.', pluginName)

    # 禁用一些 javascript
    for script in SCRIPTS_BLACKLIST:
        config.extra_javascript.remove(script)
        log.warning('Disable script \'%s\' in serve mode.', script)

    return config