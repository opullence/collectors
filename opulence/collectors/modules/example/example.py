from opulence.collectors.bases import BaseCollector
from opulence.common.patterns import Composite
from opulence.common.plugins.dependencies import (
    BinaryDependency, FileDependency, ModuleDependency
)
from opulence.facts.person import Person


class example(BaseCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "exampleModule"
    _description_ = "This is an example"
    _author_ = "??"
    _version_ = 0.1
    _dependencies_ = (
        BinaryDependency("python"),
        ModuleDependency("shutil"),
        FileDependency("/bin/ls"),
    )

    ###############
    # Module attributes
    ###############
    _allowed_input_ = (Person, Composite(Person, Person, Person))

    @classmethod
    def verify(cls):
        pass

    def launch(self, fact):
        pass
