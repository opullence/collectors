from opulence.common.plugins.exceptions import PluginFormatError

from .baseCollector import BaseCollector


class HttpCollector(BaseCollector):
    @property
    def plugin_category(self):
        return HttpCollector.__name__
