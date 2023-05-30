import os
from unittest import TestCase, mock
import elasticSearch

mocked_ip = "MockIP"
mocked_password = "MockPassword"
mocked_fingerprint = "MockFingerPrint"

@mock.patch.dict(os.environ, {"ELASTIC_IP_ADDRESS": mocked_ip,
                              "ELASTIC_PASSWORD": mocked_password,
                              "CERT_FINGERPRINT": mocked_fingerprint})
class StartClientTests(TestCase):

    def test_environ_IP(self):
        self.assertEqual(os.environ["ELASTIC_IP_ADDRESS"], mocked_ip)

    def test_environ_Password(self):
        self.assertEqual(os.environ["ELASTIC_PASSWORD"], mocked_password)

    def test_environ_Cert_fingerprint(self):
        self.assertEqual(os.environ["CERT_FINGERPRINT"], mocked_fingerprint)

    @mock.patch('elasticsearch.Elasticsearch.__new__')
    def test_if_elastic_is_called(self, mock_elastic):
        mock_inst = mock.MagicMock()
        mock_elastic.return_value = mock_inst

        elasticSearch.start_client()

        # assert called once
        mock_elastic.assert_called_once()
        # assert called with right parameters
        mock_elastic.assert_called_with(elasticSearch.Elasticsearch, mocked_ip,
                                        ssl_assert_fingerprint= mocked_fingerprint,
                                        basic_auth=("elastic", mocked_password))

    def test_if_send_data_works(self):
        mock_elastic = mock.MagicMock()
        mock_return_send = mock.MagicMock()
        mock_elastic.index.return_value = mock_return_send
        index = "index"
        document = {"Document1": "content1", "Document2": "content2"}

        elasticSearch.send_data(mock_elastic, index , document)

        mock_elastic.index.assert_called_once()

        mock_elastic.index.assert_called_with(index= index, document=document)

    def test_create_new_index(self):
        mock_elastic = mock.MagicMock()
        mock_return_create = mock.MagicMock()
        mock_elastic.indices.create.return_value = mock_return_create
        index = "index"
        mappings = {
            "mappings": {
                "properties": {}
            }
        }

        elasticSearch.create_index(mock_elastic, index, mappings)

        mock_elastic.indices.create.assert_called_once()

        mock_elastic.indices.create.assert_called_with(index=index, body=mappings)
