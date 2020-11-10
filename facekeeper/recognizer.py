from typing import Optional
from facekeeper.core import RecognizerInterface
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
