# RabbitMQ based application. Just consume messages from the specified queue 
# and publishes results into the specified exchange with specified routing key.

import pika
import sys

virtual_host = 'iavhost'
credentials = pika.PlainCredentials('ia', 'ia')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.128.1', credentials=credentials, virtual_host=virtual_host))
channel = connection.channel()

queue = 'facekeeper'

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    print("Routing key: " + method.routing_key)
    message = "Routing key: " + method.routing_key + ", photo memorized successfully"
    channel.basic_publish(exchange='iaexchange', routing_key='center.memorized', body=message)
    channel.basic_publish(exchange='iaexchange', routing_key='center.recognized', body=message)

channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

channel.start_consuming()