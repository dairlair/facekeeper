from facekeeper.core import DownloaderInterface
import requests


class RequestsDownloader(DownloaderInterface):
    def download(self, url: str) -> bytes:
        response = requests.get(url)
        return response.content
