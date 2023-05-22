import os
import psutil
from datetime import datetime, timedelta


class Collector:
    def __init__(self):
        return

    def collect(self):
        '''
        This function collects data about the system and returns it as a dictionary
        to be sent to elasticsearch.
        :return: Dictionary of labeled system data
        '''
        # An array of information about the RAM of the device.
        # Index 0 contains the total size of memory,
        # index 1 contains the size of available memory,
        # index 2 contains % of used memory,
        # index 3 contains the size of used memory
        # index 4 contains the size of free memory left.
        ram = psutil.virtual_memory()[2]
        # An array of information about the main memory of the device.
        # The module's function takes a path as input, keep '/' for root
        # directory memory information.
        # Index 0 contains the total size of main memory,
        # index 1 contains the size of used memory,
        # index 2 contains the size of free memory,
        # index 3 contains the % of used memory.
        mainmem = psutil.disk_usage('/')[3]
        # Returns cpu utilization as percentage over time since last call of this function.
        cpu = psutil.cpu_percent()
        print(datetime.now())
        return {'RAM':ram,
                'storage':mainmem,
                'CPU': cpu,
                '@timestamp': datetime.now()}
