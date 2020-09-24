import json
import numpy as np
from facekeeper.core import MemorizeResponse, FaceKeeper
from facekeeper.consumer import Consumer
from unittest.mock import MagicMock, create_autospec, Mock
from pika.amqp_object import Method
from pika.adapters.blocking_connection import BlockingChannel

def test_callback_returned_non_empty_object():
    """
    Ensure when callback returns non empty Object then Consumer will publish to the 
    output queue the input payload dictionary merged with object, returned by callback
    """
    # Given
    queue_in = 'facekeeper.memorize'
    queue_out = 'facekeeper.memorized'
    callback_payload = {'url': 'https://example.com/john.jpg'}
    callback_response = MemorizeResponse('embedding_id', 'digest', 'recognizer', np.array([1, 2, 3])) #

    # Setup mocks
    callback = MagicMock(return_value=callback_response)
    channel = create_autospec(BlockingChannel)
    channel.basic_publish = MagicMock()
    consumer = Consumer(create_autospec(FaceKeeper), channel, queue_in, queue_out, callback)

    # When
    method = Mock(delivery_tag='some-delivery-tag')
    consumer.on_message(channel, method, None, json.dumps(callback_payload))

    # Then
    expected_body = json.dumps({**callback_payload, **callback_response.__dict__})
    channel.basic_publish.assert_called_once_with(exchange='', routing_key=queue_out, body=expected_body)