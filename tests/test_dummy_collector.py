import unittest

from opulence.collectors.collectors.dummy import Dummy
from opulence.common.plugins import PluginStatus
from opulence.facts.person import Person


class TestDummy(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dummy_info(self):
        collector = Dummy()
        collector.verify()
        should_be = {
            "plugin_data": {
                "name": "dummy collector",
                "version": "1",
                "author": "Louis",
                "category": "BaseCollector",
                "description": "This is an example collector",
                "status": PluginStatus.READY,
                "error": "",
                "canonical_name": "opulence.collectors.collectors.dummy.Dummy",
            },
            "active_scanning": False,
            "allowed_input": [Person],
        }
        self.assertEqual(collector.get_info(), should_be)

    def test_dummy_collector_exec(self):
        john = Person(firstname="john", lastname="snow")
        collector = Dummy()
        res = collector.launch([john])
        self.assertEqual(res.firstname.value, "johnDUMMY")
        self.assertEqual(res.lastname.value, "snowDUMMY")


if __name__ == "__main__":
    unittest.main()
