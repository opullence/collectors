# from opulence.common.facts import BaseFact
from opulence.common.job import Result, StatusCode
from opulence.common.patterns import is_composite
from opulence.common.plugins import BasePlugin
from opulence.common.plugins.exceptions import PluginFormatError
from opulence.common.utils import is_list


class BaseCollector(BasePlugin):
    _allowed_input_ = ()
    _active_scanning_ = False

    def __init__(self, *args, **kwargs):
        if not self._allowed_input_:
            raise PluginFormatError(
                "<{}> needs at least one allowed_input".format(type(self).__name__)
            )
        super().__init__()

    @property
    def plugin_category(self):
        return BaseCollector.__name__

    @property
    def allowed_input(self):
        return (
            self._allowed_input_
            if is_list(self._allowed_input_)
            else [self._allowed_input_]
        )

    def run(self, facts):
        result = Result(input=facts, status=StatusCode.ready)

        inp = result.input.get(force_array=True)
        if not inp:
            result.status = StatusCode.empty, "No input provided"
            return result
        for i in inp:
            if not i.is_valid():
                result.status = (
                    StatusCode.invalid_input,
                    "Invalid input provided: " + str(i.get_info()),
                )
                return result
        try:
            result.clock.start()
            result.status = StatusCode.started

            result.output = self.launch(result.input.get(force_array=True))

            result.clock.stop()
            result.status = StatusCode.finished

        except Exception as err:
            print("Error in run():", err)
            result.status = StatusCode.error, str(err)
        finally:
            return result

    # @staticmethod
    # def _sanitize_output(output):
    #     if not output:
    #         return []
    #     if not is_list(output):
    #         output = [output]
    #     return [o for o in output if isinstance(o, BaseFact)]  # and o.is_valid()]

    def launch(self, fact):
        raise NotImplementedError(
            "Method launch() should be defined for Plugin \
            <{}>".format(
                type(self).__name__
            )
        )

    def get_allowed_input_as_list(self):
        ret = []
        for input in self.allowed_input:
            if is_composite(input):
                ret.append([i.__name__ for i in input.elements])
            else:
                ret.append(input.__name__)
        return ret

    def get_info(self):
        data = {
            "active_scanning": self._active_scanning_,
            "allowed_input": self.get_allowed_input_as_list(),
        }
        return {**super().get_info(), **data}
