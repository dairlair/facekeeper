from abc import ABC, abstractmethod
import numpy as np
import hashlib
from injector import inject
from typing import List, Optional


class FaceKeeperError(Exception):
    """
        Just a general error for FaceKeeper
    """
    pass


class FaceNotFoundError(FaceKeeperError):
    """
        This error must be raised when the recognizer can not recognize face in the given image
    """
    pass


class PersonEmbedding:
    """
        The person embedding is structure which contains information about person
        and the vector representation of his face features
    """

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
    def save_embedding(self, person: str, image_digest: str, recognizer: str, embedding: np.array) -> None:
        """
        :param person: The unique person identifier.
        :param image_digest: Image digest calculated with some hash function. Used to avoid duplicates
        :param recognizer: The unique identifier of neural network and trained model used to embedding calculation
        :param embedding: Face embedding (e.g.: 128-dimensional vector)
        """
        pass

    @abstractmethod
    def get_embeddings(self, recognizer: str) -> List[PersonEmbedding]:
        """
        This method must retrieves from the storage all embeddings made with specified recognizer
        :param recognizer: The unique identifier of neural network and trained model used to embedding calculation
        """
        pass


class RecognizerInterface(ABC):
    """
        RecognizerInterface declares dependency from the library which is used to calculate face embeddings (encodings)
    """

    @abstractmethod
    def get_id(self) -> str:
        """
        Every new implementation of RecognizerInterface must returns unique ID. Every new trained model
        used inside must returns the new ID as well, cause we can not compare face embeddings received calculated
        with parameters.
        """
        pass

    @abstractmethod
    def calc_embedding(self, image: bytes) -> np.array:
        """
        Must returns face embedding calculated with certain trained model.
        """
        pass

    @abstractmethod
    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        """
        Must adds embeddings to the internal storage of recognizer.
        They will be used for face recognition.
        """
        pass

    @abstractmethod
    def recognize(self, image: bytes) -> str:
        """
        Must calculate face embeddings and try to find similar embedding among the known person embeddings
        to identify the person from the image.
        """
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
    initialized: bool = False

    @inject
    def __init__(self, recognizer: RecognizerInterface, storage: StorageInterface):
        self.recognizer = recognizer
        self.storage = storage

    def initialize(self):
        """
        Retrieves all known embeddings which suits current recognizer from the storage and load them
        into the recognizer.
        """
        embeddings = self.storage.get_embeddings(self.recognizer.get_id())
        self.recognizer.add_embeddings(embeddings)
        self.initialized = True

    def is_initialized(self):
        return self.initialized

    def memorize(self, person: str, image: bytes) -> MemorizeResponse:
        """
        Takes the person identifier and the picture.
        Calculates the face embeddings for face on the photo and remember this embeddings as related with person.

        Note: if the image contains zero or more than one faces this method will raise error: FaceNotFoundError.
        """
        digest = get_digest(image)
        recognizer = self.recognizer.get_id()
        embedding = self.recognizer.calc_embedding(image)

        # Save calculated embedding in the storage
        self.storage.save_embedding(person, digest, recognizer, embedding)

        # Load calculated embedding into the recognizer embeddings
        self.recognizer.add_embeddings([PersonEmbedding(person, embedding)])

        return MemorizeResponse(digest)

    def recognize(self, image: bytes) -> Optional[RecognizeResponse]:
        """
        Tries to find the similar embeddings and returns the person identifier if it is found, None otherwise.

        Note: if the image contains zero or more than one faces this method will raise error: FaceNotFoundError.
        """
        person = self.recognizer.recognize(image)

        return RecognizeResponse(person=person) if person else None
