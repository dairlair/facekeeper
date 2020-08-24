from typing import List
from requests import post, Response

class Dapr():
    memorized_topic: str = 'Memorized'
    recognized_topic: str = 'Recognized'
    def __init__(self, url: str, pubsub: str):
        self.url = url
        self.pubsub = pubsub

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
        response: Response = post(f'{self.url}/publish/{self.pubsub}/{topic}', json=json)
        return response.ok