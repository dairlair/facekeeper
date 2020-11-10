# CLI Application for memorize and recognize functions
# Usage example: python facekeeper/cli.py memorize "https://img1.nickiswift.com/img/gallery/what-margot-robbie-was-like-before-the-fame/intro-1596486930.jpg" "Margot Robbie" "hollywood,woman"
# Or python facekeeper/cli.py recognize "https://img1.nickiswift.com/img/gallery/what-margot-robbie-was-like-before-the-fame/intro-1596486930.jpg" "Margot Robbie" "hollywood,woman"
import fire
from injector import Injector
from facekeeper.dependencies import configure
from facekeeper.core import FaceKeeper

if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])
    service: FaceKeeper = injector.get(FaceKeeper)
    service.initialize()
    fire.Fire(service)
