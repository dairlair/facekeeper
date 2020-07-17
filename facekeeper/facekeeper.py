from abc import ABC, abstractmethod
import numpy as np
import hashlib
from injector import inject
from typing import List, Optional


class FaceKeeperError(Exception):
    pass


class FaceNotFoundError(FaceKeeperError):
    pass


class PersonEmbedding:
    def __init__(self, person: str, embedding: np.array) -> None:
        self.person = person
        self.embedding = embedding


class StorageInterface(ABC):
    """
        StorageInterface is used to declare dependency from the storage.

        The storage must provide functionality to:
            * add face embedding for specified persons
            * retrieve all embeddings
    """

    @abstractmethod
    def add_embedding(self, person: str, image_digest: str, recognizer: str, embedding: np.array) -> None:
        """
        :param person: The unique person identifier.
        :param image_digest: Image digest calculated with some hash function. Used to avoid duplicates
        :param recognizer: Various embedder (algorithms or trained model) produces various embeddings for
                            the same face. We need to take it into account.
        :param embedding: Face embedding (e.g.: 128-dimensional vector)
        :return:
        """
        pass

    @abstractmethod
    def get_embeddings(self, recognizer) -> List[PersonEmbedding]:
        pass


class RecognizerInterface(ABC):
    """
        EmbedderInterface declares dependency from the library which is used to calculate face embeddings (encodings)
    """

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def calc_embedding(self, image: bytes) -> np.array:
        pass

    @abstractmethod
    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        pass

    @abstractmethod
    def recognise(self, image: bytes) -> str:
        pass


def get_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MemorizeResponse:
    def __init__(self, digest: str):
        self.digest = digest


class RecognizeResponse:
    def __init__(self, person: str):
        self.person = person


class FaceKeeper:
    @inject
    def __init__(self, recognizer: RecognizerInterface, storage: StorageInterface):
        self.initialized = False
        self.recognizer = recognizer
        self.storage = storage

    def initialize(self):
        embeddings = self.storage.get_embeddings(self.recognizer.get_id())
        self.recognizer.add_embeddings(embeddings)
        self.initialized = True

    def is_initialized(self):
        return self.initialized

    def memorize(self, person: str, image: bytes) -> MemorizeResponse:
        digest = get_digest(image)
        recognizer = self.recognizer.get_id()
        embedding = self.recognizer.calc_embedding(image)

        # Save calculated embedding in the storage
        self.storage.add_embedding(person, digest, recognizer, embedding)

        # Load calculated embedding into the recognizer embeddings
        self.recognizer.add_embeddings([PersonEmbedding(person, embedding)])

        return MemorizeResponse(digest)

    def recognize(self, image: bytes) -> Optional[RecognizeResponse]:
        person = self.recognizer.recognise(image)

        return RecognizeResponse(person=person) if person else None
