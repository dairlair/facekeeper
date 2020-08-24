from typing import List

class Dapr():
    def __init__(self, url: str, pubsub: str):
        self.url = url
        self.pubsub = pubsub

    def get_subscriptions(self) -> List[object]:
        if not self.url:
            return []

        return [
            {'pubsubName': self.pubsub, 'topic': 'memorize', 'route': 'memorize'},
            {'pubsubName': self.pubsub, 'topic': 'recognize', 'route': 'recognize'},
        ]