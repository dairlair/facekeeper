from typing import List, Optional

from facekeeper.core import (
    RecognizerInterface,
    PersonEmbedding,
    EmbeddingResponse,
)
from facekeeper.matcher import EmbeddingsMatcher
import face_recognition
from PIL import Image
import numpy as np
import io


class Recognizer(RecognizerInterface):
    def __init__(self, model: str):
        self.model = model
        self.matcher = EmbeddingsMatcher()

    def get_id(self) -> str:
        return "github.com/ageitgey/face_recognition:" + self.model

    def calc_embedding(self, image: bytes) -> Optional[np.array]:
        img = read_file_to_array(image)
        embeddings = face_recognition.face_encodings(img, None, 1, self.model)
        if len(embeddings) != 1:
            return None

        return embeddings[0]

    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        self.matcher.add_embeddings(embeddings)

    def recognize(self, image: bytes, tags: List[str] = []) -> Optional[str]:
        face_embedding = self.calc_embedding(image)

        # Face not found on the image
        if face_embedding is None:
            return EmbeddingResponse(
                embedding_id=None,
                digest=None,
                recognizer=self.get_id(),
                embedding=None,
                person=None,
                tags=None
            )

        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            self.known_face_embeddings, face_embedding
        )

        # Face not foung among loaded into memory faces
        if not (True in matches):
            return EmbeddingResponse(
                recognizer=self.get_id(), embedding=face_embedding, person=None
            )

        # The match was found in known_face_embeddings, just use the first one.
        first_match_index = matches.index(True)
        person = self.known_persons[first_match_index]
        return EmbeddingResponse(
            recognizer=self.get_id(), embedding=face_embedding, person=person
        )


def read_file_to_array(image_data: bytes, mode="RGB") -> np.array:
    """
        read_file_to_array(data bytes[, mode='RGB']) -> img
        .
        .   The function load stream data to PIL.Image and returns converted
        .   image as np.array
        .
        .   @param image_data bytes
        .   @param mode string.
    """
    image = Image.open(io.BytesIO(image_data))
    if mode:
        image = image.convert(mode)
    return np.array(image)
