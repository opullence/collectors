import opulence.facts as facts
from opulence.collectors.bases import PypiCollector
from opulence.common.passwordstore import Store
from opulence.common.plugins.dependencies import ModuleDependency


class Shodan(PypiCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Shodan"
    _description_ = "Gather information aout a domain using shodan"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [
        ModuleDependency("shodan"),
        # Password dependency
    ]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (facts.IPv4, facts.IPv6)
    _active_scanning_ = False

    ###############
    # Pypi attributes
    ###############
    _modules_ = {"s": "shodan"}

    _apikey_ = Store().get_decrypted_password("opulence/shodan_api")

    def launch(self, fact):
        api = self.modules["s"].Shodan(self._apikey_)
        host = api.host(fact.address.value)

        yield facts.Country(name=host.get("country_name", None), code=host.get("country_code", None))
        yield facts.Organization(name=host.get("org", None))
        yield facts.OperatingSystem(family=host.get("os", None))

        for item in host["data"]:
            for cpe in item["cpe"]:
                yield facts.CPE(id=cpe)
            if item["os"]:
                yield facts.OperatingSystem(family=item["os"])
            if item["location"] and item["location"]["country_name"]:
                yield facts.Country(
                    name=item["location"]["country_name"],
                    code=item["location"]["country_code"],
                )
            if (
                item["location"]
                and item["location"]["longitude"]
                and item["location"]["latitude"]
            ):
                yield facts.GeoCoordinates(
                    longitude=item["location"]["longitude"],
                    latitude=item["location"]["latitude"],
                )
            if item["asn"]:
                yield facts.ASN(id=item["asn"], organization=item["org"])
            if item["data"]:
                yield facts.Banner(
                    message=item["data"], port=item["port"], product=item["product"]
                )
            if item["port"]:
                yield facts.Port(number=item["port"], transport=item["transport"])