# RabbitMQ based application for FaceKeeper
import pika
import requests
import json
import logging
from injector import Injector
from facekeeper.core import FaceKeeper
from facekeeper.dependencies import configure
from facekeeper.config import Config
from facekeeper.consumer import Consumer

def download_image(url: str) -> bytes:
    response = requests.get(url)
    return response.content

def memorize(service: FaceKeeper, payload: dict) ->  dict:
    image = download_image(payload['url'])
    return service.memorize(person=payload['person'], image=image, tags=payload['tags'])

def recognize(service: FaceKeeper, payload: dict) ->  dict:
    image = download_image(payload['url'])
    return service.recognize(image=image)

if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])

    # Just get a pika channel
    connection: pika.BlockingConnection = injector.get(pika.BlockingConnection)
    channel = connection.channel()
    # We process a heavy tasks, don't need to prefetch more than one message
    channel.basic_qos(prefetch_count=1)

    # Service initialization, we can not consume messages until it's done
    service: FaceKeeper = injector.get(FaceKeeper)
    service.initialize()

    # Create two consumers for memorize and recognize queues
    Consumer(service, channel, 'facekeeper.memorize', 'facekeeper.memorized', memorize)
    Consumer(service, channel, 'facekeeper.recognize', 'facekeeper.recognized', recognize)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()