# RabbitMQ based application for FaceKeeper
import pika
import requests
import json
import logging
from injector import Injector
from facekeeper import FaceKeeper
from dependencies import configure
from config import Config

class GenericConsumer(object):
    def __init__(self, channel, queue_in: str, queue_out: str, callback):
        self.channel = channel
        self.callback = callback
        self.channel.queue_declare(queue=queue_in, durable=True)
        self.channel.basic_consume(queue=queue_in, on_message_callback=self.on_message)
        self.queue_out = queue_out

    def on_message(self, ch: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
        try:
            payload = json.loads(body)
            response = self.callback(injector.get(FaceKeeper), payload)
            payload['facekeeper'] = {'success': True, 'data': response.__dict__ if response else None}
            self.channel.basic_publish(exchange="", routing_key=self.queue_out, body=json.dumps(payload))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            # We can not process this message and should log the error
            # @TODO Improve the error handling for any cases: wrong messages format, internal issues, etc...
            logging.error(e)

def download_image(url: str) -> bytes:
    response = requests.get(url)
    return response.content

def memorize(service: FaceKeeper, payload: dict) ->  dict:
    image = download_image(payload['url'])
    return service.memorize(person=payload['person'], image=image)

def recognize(service: FaceKeeper, payload: dict) ->  dict:
    image = download_image(payload['url'])
    return service.recognize(image=image)



if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])

    # Just get a pika channel
    connection: pika.BlockingConnection = injector.get(pika.BlockingConnection)
    channel = connection.channel()

    # Service initialization, we can not consume messages until it's done
    service: FaceKeeper = injector.get(FaceKeeper)
    service.initialize()

    # Create two consumers for memorize and recognize queues
    GenericConsumer(channel, 'facekeeper.memorize', 'facekeeper.memorized', memorize)
    GenericConsumer(channel, 'facekeeper.recognize', 'facekeeper.recognized', recognize)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()