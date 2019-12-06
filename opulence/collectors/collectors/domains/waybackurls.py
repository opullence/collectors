from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, URI

from opulence.collectors.bases import ScriptCollector


class Waybackurls(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "waybackurls"
    _description_ = "Enumerate URLS using the Wayback machine"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("waybackurls")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "waybackurls"
    _script_arguments_ = ["$Domain.fqdn$"]

    def parse_result(self, result):
        uris = result.split("\n")
        if uris:
            for uri in uris:
                yield URI(full_uri=uri)
