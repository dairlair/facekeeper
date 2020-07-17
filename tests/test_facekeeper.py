from mock import Mock, create_autospec
from typing import List
import numpy as np

from facekeeper.facekeeper import FaceKeeper, RecognizerInterface, StorageInterface, PersonEmbedding


def test_initialization():
    # Given
    recognizer_id = 'Any Recognizer ID'
    embeddings: List[PersonEmbedding] = [PersonEmbedding('Morning Star', np.array([1, 2, 3]))]

    recognizer = create_autospec(RecognizerInterface)
    recognizer.get_id = Mock(return_value=recognizer_id)

    storage = create_autospec(StorageInterface)
    storage.get_embeddings = Mock(return_value=embeddings)
    facekeeper = FaceKeeper(recognizer, storage)

    # When
    facekeeper.initialize()

    # Then
    recognizer.get_id.assert_called_once()
    storage.get_embeddings.assert_called_once_with(recognizer_id)
    recognizer.add_embeddings.assert_called_once_with(embeddings)
    assert facekeeper.is_initialized()
