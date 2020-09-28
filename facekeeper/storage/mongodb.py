from facekeeper.core import StorageInterface, PersonEmbedding
import numpy as np
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import List


class MongoDBStorage(StorageInterface):
    def __init__(self, uri: str):
        super().__init__()
        self.connection = None
        self.uri = uri

    def save_embedding(self, person: str, digest: str, recognizer: str, embedding: np.array) -> None:
        document = {
            'person': person,
            'digest': digest,
            'recognizer': recognizer,
            'embedding': embedding.tolist(),
        }
        embeddings = self.get_embeddings_collection()
        try:
            embeddings.insert_one(document)
        except DuplicateKeyError:
            pass

    def get_embeddings(self, recognizer) -> List[PersonEmbedding]:
        result = []
        embeddings = self.get_embeddings_collection()
        for embedding in embeddings.find({'recognizer': recognizer}):
            result.append(PersonEmbedding(embedding['person'], embedding['embedding']))
        return result

    def get_embeddings_collection(self):
        client = self.get_connection()
        db = client[self.database]
        return db.embeddings

    def get_connection(self) -> MongoClient:
        if self.connection is None:
            self.connection = self.connect()

        return self.connection

    def connect(self) -> MongoClient:
        return MongoClient(self.uri)
