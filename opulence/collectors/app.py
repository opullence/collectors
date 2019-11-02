import multiprocessing

from celery.utils.log import get_task_logger

from opulence.common import configuration
from opulence.common.plugins import PluginManager

logger = get_task_logger(__name__)
app = configuration.configure_celery(
    configuration.config["collectors_service"]["worker"]
)
manager = multiprocessing.Manager()
available_collectors = manager.dict()


@app.task(name="collectors:reload_collectors")
def reload_collectors(flush=False):
    global available_collectors
    logger.info("Reload collectors")
    if flush:
        available_collectors.clear()
    for path in configuration.config["collectors"]["paths"]:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name not in available_collectors:
                available_collectors[plugin.plugin_name] = plugin


@app.task(name="collectors:collector_info")
def collector_info(collector_name):
    logger.info("Collector info for {collector_name}")
    if collector_name in available_collectors:
        return available_collectors[collector_name].get_info()
    return None


@app.task(name="collectors:list_collectors")
def list_collectors():
    global available_collectors
    logger.info("List collectors")
    return [name for name, _ in available_collectors.items()]


@app.task(name="execute_collector_by_name")
def execute_collector_by_name(collector_name, fact_or_composite):
    global available_collectors
    logger.info(f"Execute collector {collector_name} with {type(fact_or_composite)}")
    if collector_name in available_collectors:
        return available_collectors[collector_name].run(fact_or_composite)
    return "Collector not found"


# Reload collectors at startup
reload_collectors(flush=True)
print(list_collectors())
