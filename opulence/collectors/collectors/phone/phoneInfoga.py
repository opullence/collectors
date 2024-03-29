import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Country, Phone


class PhoneInfoga(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "PhoneInfoga"
    _description_ = "Gather information from international phone numbers."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("phoneinfoga")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Phone
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "phoneinfoga"

    def launch(self, fact):
        cmd_ovh = [
            self._script_path_,
            "--no-ansi",
            "--scanner",
            "ovh",
            "--number",
            fact.number.value,
        ]
        cmd_numverify = [
            self._script_path_,
            "--no-ansi",
            "--scanner",
            "numverify",
            "--number",
            fact.number.value,
        ]

        exec_numverify = self._exec(*cmd_numverify)
        yield from self.parse_ovh_result(self._exec(*cmd_ovh), fact.number.value)
        yield from self.parse_numverify_result(exec_numverify, fact.number.value)
        yield from self.parse_local_result(exec_numverify)

    def parse_local_result(self, result):
        res = re.findall(
            "Running local scan...\\n\\[\\+\\] International format: (.*)\\n\\[\\+\\] Local format: (.*)\\n\\[\\+\\] Country found: (.*) \\((.*)\\)\\n\\[\\+\\] City\\/Area: (.*)\\n\\[\\+\\] Carrier: (.*)\\n\\[\\+\\] Timezone: (.*)\\n",
            result,
        )
        if res:
            for info in res:
                il_format, local_format, country, country_code, area, carrier, timezone = (
                    info
                )
                yield Country(name=country, timezone=timezone, area=area)
                yield Phone(
                    number=il_format,
                    localformat=local_format,
                    carrier=carrier,
                    country_code=country_code,
                )

    def parse_numverify_result(self, result, number):
        res = re.findall(
            "Running Numverify.com scan...\\n\\[\\+\\] Number: \\((.*)\\) (.*)\\n\\[\\+\\] Country: (.*) \\((.*)\\)\n\\[\\+\\] Location: (.*)\\n\\[\\+\\] Carrier: (.*)\\n\\[\\+\\] Line type: (.*)\\n",
            result,
        )
        if res:
            for info in res:
                country_code, local_number, country, country_short, location, carrier, line_type = (
                    info
                )
                yield Country(name=country, code=country_short)
                yield Phone(
                    number=number,
                    localformat=local_number,
                    carrier=carrier,
                    country_code=country_code,
                    line_type=line_type,
                )

    def parse_ovh_result(self, result, number):
        yield  # TODO
