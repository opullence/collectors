from opulence.common.job import Job, StatusCode
from opulence.common.patterns import Composite
from opulence.common.plugins import BasePlugin
from opulence.common.plugins.exceptions import PluginFormatError
from opulence.common.utils import is_list
from opulence.facts import BaseFact


class BaseCollector(BasePlugin):
    _allowed_input_ = ()
    _active_scanning_ = False

    def __init__(self, *args, **kwargs):
        if not self._allowed_input_:
            raise PluginFormatError(
                f"<{type(self).__name__}> needs at least one allowed_input"
            )
        super().__init__()

    @property
    def plugin_category(self):
        return BaseCollector.__name__

    @property
    def allowed_input(self):
        return self._allowed_input_

    def run(self, job):
        if not isinstance(job, Job):
            raise TypeError(f"Expected Job argument to run(), got {type(job)}")
        if not job.input:
            job.status = StatusCode.empty
            return job
        try:
            job.executionClock.start()
            job.status = StatusCode.started

            job.output = self._sanitize_output(self.launch(job.input))
            job.executionClock.stop()

            job.status = StatusCode.finished
        except Exception as err:
            job.status = StatusCode.error
            job.error = str(err)
            print("!!!!!!!!!!!!")
            print("Error in run():", err)
            print("!!!!!!!!!!!!")
        return job

    @staticmethod
    def _sanitize_output(output):
        if not is_list(output):
            output = [output]
        return [o for o in output if isinstance(o, BaseFact) and o.is_valid()]

    def launch(self, fact):
        raise NotImplementedError(
            f"Method launch() should be defined for Plugin <{type(self).__name__}>"
        )

    def get_allowed_input_as_list(self):
        ret = []
        for input in self.allowed_input:
            if isinstance(input, Composite):
                ret.append([i.__name__ for i in input.elements])
            else:
                ret.append([input.__name__])
        return ret

    def get_info(self):
        data = {
            "active_scanning": self._active_scanning_,
            "allowed_input": self.get_allowed_input_as_list(),
        }
        return {**super().get_info(), **data}
