from injector import Injector
from dependencies import configure
from facekeeper import StorageInterface
import numpy as np

# Dependency Injection setup
injector = Injector([configure])
storage: StorageInterface = injector.get(StorageInterface)

print(type(storage))
storage.save_embedding("person", "digest", "recognizer", np.array("qweqwe"))