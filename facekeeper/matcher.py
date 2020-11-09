from typing import List
from facekeeper.core import PersonEmbedding
import face_recognition
import numpy as np


DEFAULT_TAG = "all"


class EmbeddingsMatcher(object):
    def __init__(self):
        pass

    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        for embedding in embeddings:
            embedding.tags.append(DEFAULT_TAG)

            for tag in embedding.tags:
                pass
                # TODO Implement
                # self.known_persons.append(embedding.person)
                # self.known_face_embeddings.append(embedding.embedding)


    def match(self, face_embedding: np.array, tags: List[str]):
        matches = face_recognition.compare_faces(
            self.known_face_embeddings, face_embedding
        )

        return matches