from opulence.collectors.bases import PypiCollector
from opulence.common.patterns import Composite
from opulence.common.plugins.dependencies import ModuleDependency
from opulence.facts.person import Person


class TestPypi(PypiCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "TestPypi"
    _description_ = "This is an example collector"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [ModuleDependency("requests")]

    ###############
    # Module attributes
    ###############
    _allowed_input_ = Person

    ###############
    # Pypi attributes
    ###############
    _modules_ = {"p": "opulence"}

    @classmethod
    def verify(cls):
        pass

    def launch(self, fact):
        print(self.modules["p"])
