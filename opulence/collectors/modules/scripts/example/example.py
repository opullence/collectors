from opulence.collectors.bases.scriptCollector import ScriptCollector
from opulence.common.patterns import Composite
from opulence.common.plugins.dependencies import (
    BinaryDependency, FileDependency, ModuleDependency
)
from opulence.facts.person import Person


class example(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "exampleScriptModule"
    _descriptionERROR_ = "This is an example"
    _author_ = "??"
    _version_ = 0.42
    _dependencies_ = (
        BinaryDependency("python"),
        ModuleDependency("shutil"),
        FileDependency("/bin/lsdf"),
    )

    ###############
    # Module attributes
    ###############
    _allowed_input_ = (Person, Composite(Person, Person, Person))

    ###############
    # Script attributes
    ###############
    _script_path_ = "echo"
    _script_arguments_ = ["Hello", "$Person.firstname$"]

    @classmethod
    def verify(cls):
        # raise PluginVerifyError
        return "OK"

    def parse_result(self, result):
        print(f"Parsing {result}")
        return "Nice looool"
