from typing import List
from requests import post, Response
from os import getenv
from flask import Request
import json

class Dapr():
    def __init__(self):
        port = getenv('DAPR_HTTP_PORT')
        if port:
            self.url = f'http://localhost:{port}/v1.0'
            self.pubsub = getenv('DAPR_PUBSUB') or 'pubsub'


    def publish(self, topic: str, json: str) -> bool:
        if not self.url:
            return False

        response: Response = post(f'{self.url}/publish/{self.pubsub}/{topic}', json=json)
        if response.ok:
            print('Dapr event pubslihed successfully', flush=True)
        else:
            print('Dapr event not published', flush=True)

        return response.ok

    @staticmethod
    def get_data(request: Request) -> dict:
        """
        parse data from the Flask request
        """
        payload = json.loads(request.data)
        return payload['data']
