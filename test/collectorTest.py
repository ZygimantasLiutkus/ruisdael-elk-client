import collector
from unittest import TestCase


class TestCollection(TestCase):
    def test_constructor(self):
        col = collector.Collector()
        assert col

    def test_construct_with_delay(self):
        col = collector.Collector(5)
        assert col.update_delay == 5

    def test_collect_func(self):
        col = collector.Collector()
        res = col.collect()
        assert res
