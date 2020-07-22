from typing import List, Optional

from facekeeper import RecognizerInterface, PersonEmbedding, FaceNotFoundError
import face_recognition
from PIL import Image
import numpy as np
import io


class Recognizer(RecognizerInterface):
    def __init__(self, model: str):
        self.model = model
        self.known_persons = []
        self.known_face_embeddings = []

    def get_id(self) -> str:
        return 'github.com/ageitgey/face_recognition:' + self.model

    def calc_embedding(self, image: bytes) -> np.array:
        img = read_file_to_array(image)
        embeddings = face_recognition.face_encodings(img, None, 1, self.model)
        if len(embeddings) != 1:
            raise FaceNotFoundError()

        return embeddings[0]

    def add_embeddings(self, embeddings: List[PersonEmbedding]) -> None:
        for embedding in embeddings:
            self.known_persons.append(embedding.person)
            self.known_face_embeddings.append(embedding.embedding)

    def recognize(self, image: bytes) -> Optional[str]:
        face_embedding = self.calc_embedding(image)
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(self.known_face_embeddings, face_embedding)

        if not (True in matches):
            return None

        # The match was found in known_face_embeddings, just use the first one.
        first_match_index = matches.index(True)
        return self.known_persons[first_match_index]


def read_file_to_array(image_data: bytes, mode='RGB') -> np.array:
    """
        read_file_to_array(data bytes[, mode='RGB']) -> img
        .
        .   The function load stream data to PIL.Image and returns converted image as np.array
        .
        .   @param image_data bytes
        .   @param mode string.
    """
    image = Image.open(io.BytesIO(image_data))
    if mode:
        image = image.convert(mode)
    return np.array(image)
