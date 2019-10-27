from subprocess import PIPE, Popen

from opulence.collectors.bases import BaseCollector
from opulence.common.plugins.exceptions import (
    PluginFormatError, PluginRuntimeError
)
from opulence.common.utils import is_list


class ScriptCollector(BaseCollector):
    _script_path_ = ""
    _script_arguments_ = []

    def __init__(self, *args, **kwargs):
        if not self._script_path_:
            raise PluginFormatError(f"Incorrect script_path")
        if not self._script_arguments_:
            raise PluginFormatError(f"Incorrect script_arguments")
        super().__init__()

    @property
    def plugin_category(self):
        return ScriptCollector.__name__

    @property
    def script_path(self):
        return self._script_path_

    @property
    def script_arguments(self):
        return self._script_arguments_

    def launch(self, fact):
        args = self._replace_sigil(fact)
        (return_code, stdout, stderr) = self._exec(self.script_path, *args)
        if return_code:
            raise PluginRuntimeError(stderr)
        return self.parse_result(stdout)

    def parse_result(self, result):
        raise NotImplementedError(
            f"Method parse_result() \
            should be defined for Plugin <{type(self).__name__}>"
        )

    @staticmethod
    def _exec(*cmd):
        out = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = (x.strip().decode() for x in out.communicate())
        return (out.returncode, stdout, stderr)

    def _replace_sigil(self, facts):
        facts = facts.get()
        args = self.script_arguments
        if not is_list(args):
            args = [args]

        def replace(arg):
            value = arg[1:-1]
            class_name = value.split(".")[0]
            attribute_name = value.split(".")[1]
            for fact in facts:
                if str(type(fact).__name__) == class_name and hasattr(
                    fact, attribute_name
                ):
                    return getattr(fact, attribute_name)
            print(f"WARNING: Sigil ({arg}) was not replaced. This should not happen")
            return ""

        def is_sigil(arg):
            return arg.startswith("$") and arg.endswith("$")

        return [replace(arg) if is_sigil(arg) else arg for arg in args]
