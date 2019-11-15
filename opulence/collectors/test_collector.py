import sys

from dynaconf import settings

from opulence.common.plugins import PluginManager


def _exec_collector(cls):
    if not cls.errored:
        print("* Name: {}".format(cls.plugin_name))
        print("* Description: {}".format(cls.plugin_description))
        print("* Version: {}".format(cls.plugin_version))
        print("* Category: {}".format(cls.plugin_category))
    print(" ==================================== ")
    print("| STATUS: {}".format(cls.status))
    print("|")
    print("| INPUT: {}".format(cls.allowed_input))
    print(" ==================================== ")


def main():
    if len(sys.argv) <= 1:
        return print("Give me a plugin_name to execute")

    for path in settings.COLLECTORS_PATHS:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name == sys.argv[1]:
                _exec_collector(plugin)
                return "DONE executing {}".format(plugin.plugin_name)
            else:
                print(" - skipped {}".format(plugin.plugin_name))


if __name__ == "__main__":
    sys.exit(main())
