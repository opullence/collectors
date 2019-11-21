import sys

from dynaconf import settings

from opulence.common.plugins import PluginManager


def print_state(cls):
    print("----------------------------------------------")
    if not cls.errored:
        print("* Name: {}".format(cls.plugin_name))
        print("* Description: {}".format(cls.plugin_description))
        print("* Version: {}".format(cls.plugin_version))
        print("* Category: {}".format(cls.plugin_category))
        print("\t-----------")

    print("\n* STATUS: {}".format(cls.status), " **")
    print("* INPUT: {}".format(cls.allowed_input), " **")
    print("----------------------------------------------")


def _exec_collector(collector):
    print_state(collector)
    allowed_input = collector.get_allowed_input_as_list()
    test_inputs = []
    for input in allowed_input:
        test_input = {}
        for i in input().get_fields():
            test_input.update({i: "test-{}".format(i)})
        test_inputs.append(input(**test_input))
    for input in test_inputs:
        print("\n+ Running collector with input: ", input)
        print("+\t -> ", input.get_fields())
        result = collector.run(input)
        print("@ Got result: ", result.status)
        for i in result.output:
            print("@-----------------\n@\t->", i)
            for f in i.get_fields():
                print("@\t\t->", f, ":", getattr(i, f).value)


def main():
    if len(sys.argv) <= 1:
        print("Give me a collector name to execute!\n")
        print("Collectors loaded:")
        for path in settings.COLLECTORS_PATHS:
            PluginManager().discover(path)
            for plugin in PluginManager().get_plugins(path):
                print("\t{}".format(plugin.plugin_name))
        return
    for path in settings.COLLECTORS_PATHS:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name == sys.argv[1]:
                _exec_collector(plugin)
                return "DONE executing {}".format(plugin.plugin_name)
            else:
                print(" - skipped {}".format(plugin.plugin_name))


if __name__ == "__main__":
    main()
