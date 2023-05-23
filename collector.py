import psutil
from datetime import datetime


class Collector:
    def __init__(self, update_delay=30):
        """
        Constructor for Collector.

        :param update_delay: the frequency of how often data will be
        collected (seconds). In other words, how often the collect function
        will be called.
        :param old_bytes_sent: used for measuring throughput. Will be compared
        with a value of bytes sent after the update delay to get average upload
        speed per second.
        :param old_bytes_rec: used for measuring throughput. Will be compared
        with a value of bytes received after the update delay to get average
        download speed per second.
        """
        self.update_delay = update_delay
        self.old_bytes_sent = 0
        self.old_bytes_rec = 0

    def collect(self):
        """
        This function collects data about the system and returns it as a dictionary
        to be sent to elasticsearch.
        :return: Dictionary of labeled system data
        """
        # An array of information about the RAM of the device.
        ram = psutil.virtual_memory()
        # An array of information about the main memory of the device.
        # The module's function takes a path as input, keep '/' for root
        # directory memory information.
        mainmem = psutil.disk_usage('/')
        # Cpu utilization as percentage over time since last call of this function.
        cpu = psutil.cpu_percent()
        # Network usage parameters
        io = psutil.net_io_counters()
        sent, rec = io.bytes_sent, io.bytes_recv

        # Dictionary containing all wanted data
        data = {'RAM.total': ram[0],                    # B(ytes)
                'RAM.available': ram[1],                # B
                'RAM.used.perc': ram[2],                # %
                'RAM.used.bytes': ram[3],               # B
                'RAM.free': ram[4],                     # B
                'storage.total': mainmem[0],            # B
                'storage.used.bytes': mainmem[1],       # B
                'storage.free': mainmem[2],             # B
                'storage.used.perc': mainmem[3],        # %
                'CPU': cpu,                             # %
                'upload.size': sent,                    # B
                'download.size': rec,                   # B
                'upload.speed': (sent-self.old_bytes_sent)/self.update_delay,   # B/s
                'download.speed': (rec-self.old_bytes_rec)/self.update_delay,   # B/s
                '@timestamp': datetime.now()}           # datetime.datetime

        # Reset old values of network input/output for later computations of throughput.
        self.old_bytes_sent = sent
        self.old_bytes_rec = rec

        return data
