from dotenv import load_dotenv
import time
import collector
import elasticSearch


def main():
    # loads the .env into the environment, so the next functions
    # can use the variables inside the .env
    load_dotenv()
    # Connects to the elastic server
    client = elasticSearch.start_client()
    # client.delete(index="metric_clone",id="WRLg9CiKQoqcIMtxinW2fA")
    print(client.info())
    col = collector.Collector()

    while True:
        print(elasticSearch.send_data(client, "metric_clone2", col.collect()))
        time.sleep(5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
