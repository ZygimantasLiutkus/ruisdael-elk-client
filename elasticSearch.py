
from elasticsearch import Elasticsearch
import os
from datetime import datetime



def start_client():
    """Creates a connection to elastic search, collecting the fingerprint and password from the .env

    Returns
    A client connected to the elastic search
    """
    # Colons and uppercase/lowercase don't matter when using
    # the 'ssl_assert_fingerprint' parameter

    return Elasticsearch(
        os.getenv("ELASTIC_IP_ADDRESS"),
        ssl_assert_fingerprint=os.getenv('CERT_FINGERPRINT'),
        basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD'))
    )

def send_data(client, index, document):
    """
    This method adds the provided data to the given index on the given elastic search instance
    :param client: The elastic search connection
    :param index: The index to which the data needs to be appended
    :param document: The data that needs to be appended
    :return: the response of the request
    """
    return client.index(
        index= index,
        document=document,
        )

