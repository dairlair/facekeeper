from abc import ABC, abstractmethod
import numpy as np
import hashlib
from injector import inject
from typing import List, Optional


class PersonEmbedding(object):
    """
    The person embedding is structure which contains information
    about person and the vector representation of his face features
    """

    def __init__(self, id: str, person: str, embedding: np.array, tags: List[str]) -> None:
        self.id = id
        self.person = person
        self.embedding = embedding
        self.tags = tags


class DownloaderInterface(ABC):
    @abstractmethod
    def download(self, url: str) -> bytes:
        raise NotImplementedError


class MatcherInterface(ABC):
    @abstractmethod
    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        raise NotImplementedError

    @abstractmethod
    def match(self, embedding: np.array, tags: List[str]) -> Optional[str]:
        raise NotImplementedError


class StorageInterface(ABC):
    """
    StorageInterface is used to declare dependency from the storage.

    The storage must provide functionality to:
        * add face embedding for specified persons
        * retrieve all embeddings
    """

    @abstractmethod
    def save_embedding(
        self, person: str, image_digest: str, recognizer: str, embedding: np.array, tags: List[str],
    ) -> str:
        """
        :param person: The unique person identifier.
        :param image_digest: Image digest calculated with some hash function.
                             Used to avoid duplicates.
        :param recognizer:   The unique identifier of neural network and
                             trained model used to embedding calculation
        :param embedding:    Face embedding (e.g.: 128-dimensional vector)
        """
        raise NotImplementedError

    @abstractmethod
    def get_embeddings(self, recognizer: str) -> List[PersonEmbedding]:
        """
        This method must retrieves from the storage all embeddings made with specified recognizer
        :param recognizer: The unique identifier of neural network and trained model used to embedding calculation
        """
        raise NotImplementedError


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
        raise NotImplementedError

    @abstractmethod
    def calc_embedding(self, image: bytes) -> Optional[np.array]:
        """
        Must returns face embedding calculated with certain trained model.
        Must return None when the given image does not contains exactly one face.
        """
        raise NotImplementedError

    @abstractmethod
    def locate_faces(self, image: bytes) -> List[tuple]:
        """
        Returns an array of bounding boxes of human faces in a image

        :param img: Image content, just a bytes
        :return: A list of tuples of found face locations in css (top, right, bottom, left) order
        """
        raise NotImplementedError


def get_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FaceKeeper:
    initialized: bool = False

    @inject
    def __init__(
        self,
        downloader: DownloaderInterface,
        recognizer: RecognizerInterface,
        storage: StorageInterface,
        matcher: MatcherInterface,
    ):
        self.downloader = downloader
        self.recognizer = recognizer
        self.storage = storage
        self.matcher = matcher

    def initialize(self):
        """
        Retrieves all known embeddings which suits current recognizer
        from the storage and load them into the recognizer.
        """
        embeddings = self.storage.get_embeddings(self.recognizer.get_id())
        self.matcher.add_embeddings(embeddings)
        self.initialized = True

    def is_initialized(self):
        return self.initialized

    def memorize(self, person: str, url: str, tags: List[str] = []) -> dict:
        """
        Takes the person identifier and the picture.
        Calculates the face embeddings for face on the photo and remember
        this embeddings as related with person.

        Note: if the image contains zero or more than one faces
        this method will return None.
        """
        tags = list(tags)
        image = self.downloader.download(url)
        digest = get_digest(image)
        recognizer = self.recognizer.get_id()
        embedding = self.recognizer.calc_embedding(image)

        # Save calculated embedding in the storage
        embedding_id: str = self.storage.save_embedding(person, digest, recognizer, embedding, tags)

        # Load calculated embedding into the recognizer embeddings
        person_embedding = PersonEmbedding(embedding_id, person, embedding, tags)
        self.matcher.add_embeddings([person_embedding])

        return {"success": True, "embedding_id": embedding_id}

    def recognize(self, url: str, tags: List[str] = []) -> dict:
        """
        Tries to find the similar embeddings and returns the most similar embedding if it is found.

        """
        tags = list(tags)
        image = self.downloader.download(url)
        embedding = self.recognizer.calc_embedding(image)
        # Face not found on the image
        if embedding is None:
            return {"success": False, "resolution": "FACE_NOT_RECOGNIZED"}

        embedding_id = self.matcher.match(embedding, tags)
        # We have no similar embeddings in the matcher database
        if embedding_id is None:
            return {"success": False, "resolution": "SIMILAR_FACE_NOT_FOUND"}

        return {"success": True, "embedding_id": embedding_id}

    def locate(self, url: str) -> dict:
        image: bytes = self.downloader.download(url)
        faces = self.recognizer.locate_faces(image)
        if not faces:
            return {"success": False, "resolution": "FACES_NOT_LOCATED"}

        return {"success": True, "faces": faces}
