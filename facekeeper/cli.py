# CLI Application for memorize and recognize functions
# To memorize
# python facekeeper/cli.py memorize "Margot Robbie" "https://img1.nickiswift.com/img/gallery/what-margot-robbie-was-like-before-the-fame/intro-1596486930.jpg" "hollywood,woman"
# To recognize
# python facekeeper/cli.py recognize "https://img1.nickiswift.com/img/gallery/what-margot-robbie-was-like-before-the-fame/intro-1596486930.jpg" "hollywood,woman"
# To locate faces on the photo just run:
# python facekeeper/cli.py locate "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846"
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
