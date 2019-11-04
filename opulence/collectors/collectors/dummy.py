from opulence.common.plugins.dependencies import (
    BinaryDependency, FileDependency, ModuleDependency
)
from opulence.facts.person import Person

from ..bases import BaseCollector


class Dummy(BaseCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "dummy collector"
    _description_ = "This is an example collector"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = (
        BinaryDependency("ls"),
        ModuleDependency("pip"),
        FileDependency("/bin/ls"),
    )

    ###############
    # Module attributes
    ###############
    _allowed_input_ = Person

    @classmethod
    def verify(cls):
        pass

    def launch(self, fact):
        return Person(
            firstname=fact.firstname.value + "DUMMY",
            lastname=fact.lastname.value + "DUMMY",
        )
