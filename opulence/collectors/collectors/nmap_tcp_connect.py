import re

from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts.domain import Domain
from opulence.facts.ip import IPv4
from opulence.facts.port import Port

from ..bases.scriptCollector import ScriptCollector


class NmapStealth(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Nmap TCP connect"
    _description_ = "Performs nmap TCP connect scan (-sT)"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("nmap")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (Domain, IPv4)
    _active_scanning_ = True

    ###############
    # Script attributes
    ###############
    _script_path_ = "nmap"
    _script_arguments_ = [
        "-sT",
        "-oX",
        "-",
        "$Domain.fqdn$",
        "$IPv4.address$",
    ]

    def parse_result(self, result):

        found_ports = re.findall(
            'protocol="(.+?)" portid="(.+?)"><state state="(.+?)"', result
        )
        if not found_ports:
            return
        res = []
        for port in found_ports:
            proto, port_number, state = port
            res.append(Port(number=port_number, state=state, proto=proto))
        return res
