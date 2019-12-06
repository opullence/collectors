import re

from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts.socialProfile import SocialProfile
from opulence.facts.username import Username

from opulence.collectors.bases import ScriptCollector


class Sherlock(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Sherlock"
    _description_ = "Find usernames across social networks"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("sherlock")]

    ###############
    # Collector attributes
    ###############
    _active_scanning_ = False
    _allowed_input_ = Username

    ###############
    # Script attributes
    ###############
    _script_path_ = "sherlock"


    def launch(self, fact):
        cmd = [self._script_path_, fact.name.value, "--print-found", "--folderoutput", "/tmp"]
        yield from self.parse_result(self._exec(*cmd), fact.name.value)


    def parse_result(self, result, username):
        found_social_profiles = re.findall("\\[\\+\\] (.*): (.*)", result)
        if found_social_profiles:
            for f in found_social_profiles:
                site, url = f
                yield SocialProfile(username=username, site=site, url=url)