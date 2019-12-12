import multiprocessing

from celery.utils.log import get_task_logger
from dynaconf import settings

from opulence.common.configuration import configure_celery
from opulence.common.plugins import PluginManager
from opulence.common.job import StatusCode

from opulence.collectors import services

logger = get_task_logger(__name__)


app = configure_celery(settings.CELERY_WORKER)
manager = multiprocessing.Manager()
available_collectors = manager.dict()


@app.task(name="collectors:reload_collectors", ignore_result=True)
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


@app.task(name="collectors:list_collectors")
def list_collectors():
    global available_collectors
    logger.info("List collectors")
    return [ c.get_info() for _, c in available_collectors.items() ]


@app.task(name="collectors:execute_collector_by_name")
def execute_collector_by_name(collector_name, fact_or_composite):
    global available_collectors
    logger.info(
        "Execute collector {} with {}".format(
            collector_name, type(fact_or_composite)
        )
    )
    result = services.create_result(input=fact_or_composite)
    if collector_name in available_collectors:
        return available_collectors[collector_name].run(result)
    result.status = StatusCode.error, "Could not find collector {}".format(collector_name)
    return result

# Reload collectors at startup
reload_collectors(flush=True)
print("Loaded:", list_collectors())
