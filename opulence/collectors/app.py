import multiprocessing

from celery.utils.log import get_task_logger
from dynaconf import settings

from opulence.common.configuration import configure_celery
from opulence.common.plugins import PluginManager

logger = get_task_logger(__name__)


app = configure_celery(settings.CELERY_WORKER)
manager = multiprocessing.Manager()
available_collectors = manager.dict()


@app.task(name="collectors:reload_collectors")
def reload_collectors(flush=False):
    global available_collectors
    logger.info("Reload collectors")
    if flush:
        available_collectors.clear()
    for path in settings.COLLECTORS_PATHS:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name not in available_collectors:
                available_collectors[plugin.plugin_name] = plugin


@app.task(name="collectors:collector_info")
def collector_info(collector_name):
    logger.info("Collector info for {}".format(collector_name))

    if collector_name in available_collectors:
        return available_collectors[collector_name].get_info()
    return None


@app.task(name="collectors:list_collectors")
def list_collectors():
    global available_collectors
    logger.info("List collectors")
    return [name for name, _ in available_collectors.items()]


@app.task(name="collectors:execute_collector_by_name")
def execute_collector_by_name(collector_name, fact_or_composite):
    global available_collectors
    logger.info(
        "Execute collector {} with \
        {}".format(
            collector_name, type(fact_or_composite)
        )
    )
    if collector_name in available_collectors:
        return available_collectors[collector_name].run(fact_or_composite)
    return "Collector not found"


# Reload collectors at startup
reload_collectors(flush=True)
print("Loaded:", list_collectors())
