import json
import numpy as np
from typing import Optional
from facekeeper.core import FaceKeeper
from facekeeper.consumer import Consumer
from unittest.mock import MagicMock, create_autospec, Mock
from pika.adapters.blocking_connection import BlockingChannel


def callback_input_output_helper(
    callback_input, callback_output: Optional[object], expected_body: str
):
    assert isinstance(expected_body, str)
    """
    Ensure when callback returns non empty Object callback_output then
    Consumer will publish to the output queue the callback_input
    dictionary merged with callback_output
    """
    # Given
    queue_in = "queue.in"
    queue_out = "queue.out"

    # Setup mocks
    callback = MagicMock(return_value=callback_output)
    channel = create_autospec(BlockingChannel)
    channel.basic_publish = MagicMock()
    consumer = Consumer(
        create_autospec(FaceKeeper), channel, queue_in, queue_out, callback
    )

    # When
    method = Mock(delivery_tag="some-delivery-tag")
    consumer.on_message(channel, method, None, json.dumps(callback_input))

    # Then
    channel.basic_publish.assert_called_once_with("", queue_out, body=expected_body, mandatory=True)


def test_callback_success():
    input = {"url": "https://example.com/john.jpg"}
    person = "john"
    tags = []
    output = {
        "embedding_id": "embedding_id",
        "digest": "digest",
        "recognizer": "recognizer",
        "embedding": np.array([1, 2, 3]).tolist(),
        "person": person,
        "tags": tags,
        "success": True
    }
    body = json.dumps({**input, **output})
    callback_input_output_helper(input, output, body)


def test_callback_empty_result():
    """
    Ensure when person is not found on the picture
    the app will push proper message to the queue
    """
    # When the person is not found the FaceKeeper Core returns None
    input = {"url": "https://google.com"}
    output = {"success": False}
    body = json.dumps({"url": "https://google.com", "success": False})
    callback_input_output_helper(input, output, body)
