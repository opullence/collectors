import re

from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, IPv4, Email, URI

from opulence.collectors.bases import ScriptCollector


class BlackWidow(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "BlackWidow"
    _description_ = "Gather URLS, dynamic parameters and email addresses from a target website."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("blackwidow")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "blackwidow"
    _script_arguments_ = ["-d", "$Domain.fqdn$"]

    @staticmethod
    def read_file_line_by_line(filepath):
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                yield line.strip()
                line = fp.readline()

    def parse_result(self, result):
        urls_file = re.search("\\[\\+\\] URL's Discovered:.*\\n(.*).txt", result)
        dynamic_urls_file = re.search("\\[\\+\\] Dynamic URL's Discovered:.*\\n(.*).txt", result)
        form_urls_file = re.search("\\[\\+\\] Form URL's Discovered:.*\\n(.*).txt", result)
        dynamic_parameters_file = re.search("\\[\\+\\] Unique Dynamic Parameters Discovered:.*\\n(.*).txt", result)
        sub_domains_file = re.search("\\[\\+\\] Sub-domains Discovered:.*\\n(.*).txt", result)
        emails_file = re.search("\\[\\+\\] Emails Discovered:.*\\n(.*).txt", result)
        phones_file = re.search("\\[\\+\\] Phones Discovered:.*\\n(.*).txt", result)
        if urls_file and urls_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(urls_file.group(1))):
                yield URI(full_uri=line)
        if dynamic_urls_file and dynamic_urls_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(dynamic_urls_file.group(1))):
                yield URI(full_uri=line)
        if form_urls_file and form_urls_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(form_urls_file.group(1))):
                yield URI(full_uri=line)
        if dynamic_parameters_file and dynamic_parameters_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(dynamic_parameters_file.group(1))):
                yield URI(full_uri=line)

        if sub_domains_file and sub_domains_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(sub_domains_file.group(1))):
                yield Domain(address=line)

        if emails_file and emails_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(emails_file.group(1))):
                yield Email(address=line)

        if phones_file and phones_file.group(1):
            for line in self.read_file_line_by_line("{}.txt".format(phones_file.group(1))):
                yield Phone(number=line)
