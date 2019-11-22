import re
from subprocess import PIPE, Popen

from opulence.common.plugins.exceptions import (
    PluginFormatError, PluginRuntimeError
)
from opulence.common.utils import is_list

from .baseCollector import BaseCollector


class ScriptCollector(BaseCollector):
    _script_path_ = ""
    _script_arguments_ = []

    def __init__(self, *args, **kwargs):
        if not self._script_path_:
            raise PluginFormatError("Incorrect script_path")
        if not self._script_arguments_:
            raise PluginFormatError("Incorrect script_arguments")
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
            "Method parse_result() should be defined for Plugin \
            <{}>".format(
                type(self).__name__
            )
        )

    @staticmethod
    def _exec(*cmd):
        print("ScriptCollector: launch command {}".format(cmd))
        out = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = (x.strip().decode() for x in out.communicate())
        return (out.returncode, stdout, stderr)

    def _replace_sigil(self, facts):
        args = self.script_arguments
        if not is_list(args):
            args = [args]

        def find_sigil(arg):
            result = re.search("\\$(.*)\\$", arg)
            if result is not None:
                return result.group(1)
            return result

        def replace(arg):
            found = find_sigil(arg)
            if found is None:
                return arg
            value = found
            try:
                (class_name, attribute_name) = value.split(".")
            except ValueError:
                return None
            for fact in facts:
                if str(type(fact).__name__) == class_name and hasattr(
                    fact, attribute_name
                ):
                    replaced_value = getattr(fact, attribute_name).value
                    value_to_replace = "${}$".format(value)
                    return arg.replace(value_to_replace, replaced_value)
            return None

        res = []
        for arg in args:
            replaced = replace(arg)
            if replaced is not None:
                res.append(replaced)
        return res
