# CLI Application for memorize and recognize functions
# Usage example: python facekeeper/cli.py memorize "https://img1.nickiswift.com/img/gallery/what-margot-robbie-was-like-before-the-fame/intro-1596486930.jpg" "Margot Robbie" "hollywood,woman"
import fire
from injector import Injector
from facekeeper.dependencies import configure
from facekeeper.amqp import download_image
from facekeeper.core import FaceKeeper

if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])
    service: FaceKeeper = injector.get(FaceKeeper)
    service.initialize()

    def memorize(url: str, person: str, tags: tuple = []) -> dict:
        image = download_image(url)
        response = service.memorize(person, image, list(tags))
        return response.embeddingId or "Not memorized"

    def recognize(url: str, tags: tuple = []) -> dict:
        image = download_image(url)
        response = service.recognize(image, list(tags))
        return response.person or "Person not recognized"

    fire.Fire({"memorize": memorize, "recognize": recognize})
