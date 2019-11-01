
import logging.config
import multiprocessing

from opulence.common import configuration
from opulence.common.plugins import PluginManager


logger = logging.getLogger("")

app = configuration.configure_celery(
    configuration.config["collectors_service"]["worker"]
)

manager = multiprocessing.Manager()
available_collectors = manager.dict()


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


from opulence.common.job import Result


@app.task(name="execute_collector_by_name")
def execute_collector_by_name(collector_name, fact_or_composite):
    global available_collectors

    if collector_name in available_collectors:
        return available_collectors[collector_name].run(fact_or_composite)
    return "Collector not found"


# Reload collectors at startup
reload_collectors(flush=True)
print(list_collectors())
