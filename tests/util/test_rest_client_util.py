from unittest import TestCase
from unittest.mock import patch

from app.util.rest_client_util import RestClientUtil


def mock_req_get(url, headers):
    return "get response returned"


def mock_req_post(url, json):
    return "post response returned"


class TestRestClientUtil(TestCase):
    @patch("requests.get", mock_req_get)
    def test_rest_client_util_get_sync(self):
        response = RestClientUtil.get_sync("some/path")
        assert response == "get response returned"

    @patch("requests.post", mock_req_post)
    def test_rest_client_util_post_sync(self):
        response = RestClientUtil.post_sync("some url", {"dto": "req dto"})
        assert response == "post response returned"
