from typing import Optional, List
from facekeeper.core import RecognizerInterface
from facekeeper.matcher import EmbeddingsMatcher
import face_recognition
from PIL import Image
import numpy as np
import io
import base64


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

    def locate_faces(self, image: bytes) -> List[dict]:
        img = read_file_to_array(image)
        locations = face_recognition.face_locations(img, 1, "fog")
        result = []
        for i, location in enumerate(locations):
            top, right, bottom, left = location
            face = img[top:bottom, left:right]
            buffer = io.BytesIO()
            pil_image = Image.fromarray(face)
            pil_image.save(buffer, "JPEG")
            buffer = base64.b64encode(buffer.getvalue())
            result.append({"top": top, "right": right, "bottom": bottom, "left": left, "contentBase64": buffer})
        return result


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
