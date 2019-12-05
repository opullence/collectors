from opulence.facts.file import File

from ..bases import BaseCollector


class VirusTotal(BaseCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "virus total collector"
    _description_ = "return info on file from his hash"
    _author_ = "Henry"
    _version_ = 1

    ###############
    # Module attributes
    ###############
    _allowed_input_ = File

    def launch(self, facts):
        return File(filename="file name from virus total", hash="fffffffffff")
