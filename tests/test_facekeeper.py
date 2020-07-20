from mock import Mock, create_autospec
from typing import List
import numpy as np

from facekeeper.facekeeper import FaceKeeper, RecognizerInterface, StorageInterface, PersonEmbedding, get_digest


def test_initialization():
    # Given
    recognizer_id = 'Any Recognizer ID'
    embeddings: List[PersonEmbedding] = [PersonEmbedding('Agent Smith', np.array([1, 2, 3]))]

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


# Ensure that when we call memorize method the FaceKeeper will:
#   1. calculate embeddings for given image
#   2. store the embeddings in the Storage and
#   3. add them into to the currently running Recognizer
def test_memorize():
    # Given
    recognizer_id: str = 'Any Recognizer ID'
    person: str = 'John Smith'
    image: bytes = bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
    digest = get_digest(image)
    embedding: np.array = np.array([1, 2, 3])

    recognizer = create_autospec(RecognizerInterface)
    recognizer.get_id = Mock(return_value=recognizer_id)
    recognizer.calc_embedding = Mock(return_value=embedding)

    storage = create_autospec(StorageInterface)

    facekeeper = FaceKeeper(recognizer, storage)

    # When
    facekeeper.memorize(person, image)

    # Then
    recognizer.get_id.assert_called_once()
    recognizer.calc_embedding.assert_called_once_with(image)
    recognizer.add_embeddings.assert_called_once()
    storage.save_embedding.assert_called_once_with(person, digest, recognizer_id, embedding)
