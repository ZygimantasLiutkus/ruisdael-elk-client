import collector


def test_constructor():
    col = collector.Collector()
    assert col


def test_construct_with_delay():
    col = collector.Collector(5)
    assert col.update_delay == 5


def test_collect_func():
    col = collector.Collector()
    res = col.collect()
    assert res
