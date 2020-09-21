from facekeeper import StorageInterface, PersonEmbedding
import numpy as np
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import List


class PostgreSQLStorage(StorageInterface):
    def __init__(self, dsn: str):
        super().__init__()
        self.connection = None
        self.dsn = dsn

    def save_embedding(self, person: str, digest: str, recognizer: str, embedding: np.array) -> None:
        raise NotImplementedError("Not implemented")

    def get_embeddings(self, recognizer) -> List[PersonEmbedding]:
        raise NotImplementedError("Not implemented")

    def get_connection(self) -> MongoClient:
        if self.connection is None:
            self.connection = self.connect()

        return self.connection

    def connect(self) -> MongoClient:
        return MongoClient(host=self.host, port=self.port)
