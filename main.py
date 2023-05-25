from dotenv import load_dotenv
import time
import collector
import elasticSearch
import os


def main():
    # loads the .env into the environment, so the next functions
    # can use the variables inside the .env
    load_dotenv()
    # Connects to the elastic server
    client = elasticSearch.start_client()
    # client.delete(index="metric_clone",id="WRLg9CiKQoqcIMtxinW2fA")
    print(client.info())
    col = collector.Collector()
    index = "metric_clone_" + os.uname()[1]

    # Uncomment line bellow to delete contents of the index and recreate
    # the index with selected name before sending data to it.
    # client.options(ignore_status=[400, 404]).indices.delete(index=index)

    if not client.indices.exists(index=index):
        mappings = {
            "mappings": {
                "properties": {
                    "location": {
                        "type": "geo_point"
                    }
                }
            }
        }

        print(elasticSearch.create_index(client, index, mappings))

    while True:
        print(elasticSearch.send_data(client, index, col.collect()))
        time.sleep(5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
