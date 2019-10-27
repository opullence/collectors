import multiprocessing

from opulence.common import configuration
from opulence.common.plugins import PluginManager

configuration.load_config_from_file("config.yml")
app = configuration.configure_celery(
    configuration.config["collectors_service"]["worker"]
)


manager = multiprocessing.Manager()
available_collectors = manager.dict()


@app.task
def add(x, y):
    return x + y


@app.task(name="collectors:reload_collectors")
def reload_collectors(flush=False):
    global available_collectors
    if flush:
        available_collectors.clear()
    for path in configuration.config["collectors"]["paths"]:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name not in available_collectors:
                available_collectors[plugin.plugin_name] = plugin


@app.task(name="collectors:collector_info")
def collector_info(collector_name):
    if collector_name in available_collectors:
        return available_collectors[collector_name].get_info()
    return None


@app.task(name="collectors:list_collectors")
def list_collectors():
    global available_collectors
    return [name for name, _ in available_collectors.items()]
