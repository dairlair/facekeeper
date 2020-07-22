from injector import singleton
from facekeeper import FaceKeeper, RecognizerInterface, StorageInterface
from recognizer import Recognizer
from mongodb import MongoDBStorage
from config import Config


def configure(binder):
    binder.bind(FaceKeeper, to=FaceKeeper, scope=singleton)
    binder.bind(RecognizerInterface, to=Recognizer('large'), scope=singleton)
    binder.bind(StorageInterface,
                to=MongoDBStorage(Config.mongodb_host(), Config.mongodb_port(), Config.mongodb_database()),
                scope=singleton)
