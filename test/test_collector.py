from collections import namedtuple

import collector
from unittest import TestCase, mock

mock_vm = namedtuple("mock_vm", ["a", "b", "c", "d", "e"])
mock_du = namedtuple("mock_du", ["a", "b", "c", "d"])
mock_nioc = namedtuple("mock_nioc", ["bytes_sent", "bytes_recv"])
mock_time = "Current time"
mock_details = {'instrument_name': "mock_name",
                'latitude': 2,
                'longitude': 1,
                'elevation': "2 m",
                'location': "mock_location",
                'instrument_type': "mock_type"}


class TestCollection(TestCase):
    def setUp(self):
        self.patcher = mock.patch('collector.open', mock.mock_open(read_data=mock_details.__str__()))
        self.mock_foo = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_constructor(self):
        col = collector.Collector()
        assert col

    def test_construct_with_delay(self):
        col = collector.Collector(5)
        assert col.update_delay == 5

    @mock.patch("collector.psutil")
    def test_mock_psutil_no_throughput(self, lib_mock):
        lib_mock.virtual_memory = mock.MagicMock(return_value=mock_vm(0, 1, 2, 3, 4))
        lib_mock.disk_usage = mock.MagicMock(return_value=mock_du(5, 6, 7, 8))
        lib_mock.cpu_percent = mock.MagicMock(return_value=9)

        col = collector.Collector()

        res = col.collect()

        lib_mock.virtual_memory.assert_called_once()
        lib_mock.disk_usage.assert_called_once()
        lib_mock.cpu_percent.assert_called_once()

        subres = [res[k] for k in ('RAM.total', 'RAM.available', 'RAM.used.perc', 'RAM.used.bytes', 'RAM.free',
                                   'storage.total', 'storage.used.bytes', 'storage.free', 'storage.used.perc',
                                   'CPU')]
        assert subres == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    @mock.patch("collector.psutil.net_io_counters")
    def test_mock_throughput_psutil(self, lib_mock):
        lib_mock.return_value = mock_nioc(1, 2)

        col = collector.Collector(2)

        res = col.collect()

        lib_mock.assert_called_once()
        assert col.old_bytes_sent == 1
        assert col.old_bytes_rec == 2

        subres = [res[k] for k in ('upload.size', 'download.size', 'upload.speed', 'download.speed')]

        assert subres == [1, 2, 0.5, 1.0]

    @mock.patch("collector.datetime")
    def test_mock_datetime(self, lib_mock):
        lib_mock.utcnow().strftime = mock.MagicMock(return_value=mock_time)

        col = collector.Collector()

        res = col.collect()

        lib_mock.utcnow.assert_called()

        assert res['@timestamp'] == mock_time

    @mock.patch("collector.yaml")
    def test_mock_location(self, lib_mock):
        lib_mock.safe_load.return_value = mock_details

        col = collector.Collector()

        res = col.collect()

        lib_mock.safe_load.assert_called_once()

        subres = [res[k] for k in ('location.coordinates', 'location.elevation', 'instrument.name',
                                   'location.name', 'instrument.type')]

        assert subres == [[1, 2], "2 m", "mock_name", "mock_location", "mock_type"]
