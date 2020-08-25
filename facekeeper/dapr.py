from typing import List
from requests import post, Response
from os import getenv
from flask import Request
import json

class Dapr():
    memorized_topic: str = 'Memorized'
    recognized_topic: str = 'Recognized'
    def __init__(self):
        port = getenv('DAPR_HTTP_PORT')
        if port:
            self.url = f'http://localhost:{port}/v1.0'
            self.pubsub = getenv('DAPR_PUBSUB') or 'pubsub'

    def get_subscriptions(self) -> List[object]:
        if not self.url:
            return []

        return [
            {'pubsubName': self.pubsub, 'topic': 'Memorize', 'route': 'dapr/memorize'},
            {'pubsubName': self.pubsub, 'topic': 'Recognize', 'route': 'dapr/recognize'},
        ]

    def publish_memorized(self, json: str) -> bool:
        return self.publish(self.memorized_topic, json)

    def publish_recognized(self, json: str) -> bool:
        return self.publish(self.recognized_topic, json)

    def publish(self, topic: str, json: str) -> bool:
        if not self.url:
            return False

        response: Response = post(f'{self.url}/publish/{self.pubsub}/{topic}', json=json)
        return response.ok

    @staticmethod
    def get_data(request: Request) -> dict:
        """
        parse data from the Flask request
        """
        payload = json.loads(request.data)
        return payload['data']
