from typing import List, Optional
from facekeeper.core import PersonEmbedding
import face_recognition
import numpy as np


DEFAULT_TAG = "all"


class EmbeddingsMatcher(object):
    def __init__(self):
        self.ids = {DEFAULT_TAG: []}
        self.embeddings = {DEFAULT_TAG: []}
        pass

    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        for embedding in embeddings:
            embedding.tags.append(DEFAULT_TAG)

            for tag in embedding.tags:
                if tag not in self.ids:
                    self.embeddings[tag] = []
                    self.ids[tag] = []

                self.ids[tag].append(embedding.id)
                self.embeddings[tag].append(embedding.embedding)

    def match(self, embedding: np.array, tags: List[str]) -> Optional[str]:
        if not tags:
            tags = [DEFAULT_TAG]

        for tag in tags:
            embedding_id = self.match_in_tag(embedding, tag)
            if embedding_id is not None:
                return embedding_id

        return None

    def match_in_tag(self, embedding: np.array, tag: str) -> str:
        matches = face_recognition.compare_faces(self.embeddings[tag], embedding, tolerance=0.5)

        # Face not found among loaded into memory embeddings
        if not (True in matches):
            return None

        # The match was found in known_face_embeddings, just use the first one.
        first_match_index = matches.index(True)

        return self.ids[tag][first_match_index]
