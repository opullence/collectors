import re

from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts.socialProfile import SocialProfile
from opulence.facts.username import Username

from ..bases.scriptCollector import ScriptCollector


class Profiler(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Profiler"
    _description_ = "OSINT HUMINT Profile Collector"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("/srv/recon-ng/recon-cli")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Username

    ###############
    # Script attributes
    ###############
    _script_path_ = "/srv/recon-ng/recon-cli"
    _script_arguments_ = [
        "-m",
        "recon/profiles-profiles/profiler",
        "-o",
        "SOURCE=$Username.name$",
        "-x",
    ]

    def parse_result(self, result):
        results = []
        found_social_profiles = re.findall(
            "(.*)\\[profile\\] (.*) - (.*) \\((.*)\\)", result
        )
        if not found_social_profiles:
            return results
        for f in found_social_profiles:
            _, username, site, url = f
            results.append(SocialProfile(username=username, url=url, site=site))
        return results
