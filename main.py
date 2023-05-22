# This is a sample Python script.
from dotenv import load_dotenv
import threading
import time
import Collector
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import elasticSearch

def main():
    # loads the .env into the environment, so the next functions can use the variables inside the .env
    load_dotenv()
    # Connects to the elastic server
    client = elasticSearch.start_client()
    print(client.info())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# collector = Collector.Collector()
#
# res = collector.collect()
#
# while True:
#     print(collector.collect())
#     time.sleep(5)

# threading.Timer(5.0, collector.collect()).start()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/