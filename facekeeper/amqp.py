# RabbitMQ based application
import pika
import requests
import json
from injector import Injector
from facekeeper import FaceKeeper
from dependencies import configure
from config import Config

# Dependency Injection setup
injector = Injector([configure])

def download_image(url: str) -> bytes:
    response = requests.get(url)
    return response.content

def decode_payload(body) -> dict:
    return json.loads(body)


def memorize(channel, method, properties, body):   
    service: FaceKeeper = injector.get(FaceKeeper)
    payload = decode_payload(body)
    image = download_image(payload['url'])
    response = service.memorize(person=payload['person'], image=image)
    payload['memorization'] = {'success': True, 'data': response.__dict__ if response else None}
    channel.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_publish(exchange="", routing_key='facekeeper.memorized', body=json.dumps(payload))


def recognize(channel, method, properties, body):
    service: FaceKeeper = injector.get(FaceKeeper)
    payload = decode_payload(body)
    image = download_image(payload['url'])
    response = service.recognize(image=image)
    payload['recognition'] = {'success': True, 'data': response.__dict__ if response else None}
    channel.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_publish(exchange="", routing_key='facekeeper.recognized', body=json.dumps(payload))

connection: pika.BlockingConnection = injector.get(pika.BlockingConnection)
channel = connection.channel()
channel.basic_consume('facekeeper.memorize', memorize)
channel.basic_consume('facekeeper.recognize', recognize)

if __name__ == "__main__":
    service: FaceKeeper = injector.get(FaceKeeper)
    service.initialize()
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()