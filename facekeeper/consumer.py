import json
from pika.adapters.blocking_connection import BlockingChannel
from facekeeper.core import FaceKeeper


class Consumer(object):
    def __init__(
        self, service: FaceKeeper, channel: BlockingChannel, queue_in: str, queue_out: str, callback,
    ):
        self.service = service
        self.channel = channel
        self.callback = callback
        self.queue_out = queue_out
        self.channel.queue_declare(queue=queue_in, durable=True)
        self.channel.queue_declare(queue=queue_out, durable=True)
        self.channel.basic_consume(queue=queue_in, on_message_callback=self.on_message)

    def on_message(self, ch: BlockingChannel, method, properties, body: str):
        payload = json.loads(body)
        response = self.callback(self.service, payload)
        payload = {**payload, **response}
        self.channel.basic_publish("", self.queue_out, body=json.dumps(payload), mandatory=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
