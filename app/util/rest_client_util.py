import requests


class RestClientUtil:

    @staticmethod
    def get_sync(url: str) -> requests.Response:
        response = requests.get(url=url, headers={'Content-Type': 'application/json'})
        return response

    @staticmethod
    def post_sync(url: str, req_dto: dict) -> requests.Response:
        response = requests.post(url=url, data=req_dto)
        return response
