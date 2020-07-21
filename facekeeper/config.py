import os


class Config(object):

    @staticmethod
    def host() -> str:
        return os.environ.get("HOST") or '0.0.0.0'

    @staticmethod
    def port() -> int:
        return os.environ.get("PORT") or 80

    @staticmethod
    def mongodb_host() -> str:
        return os.environ.get("MONGODB_HOST") or 'localhost'

    @staticmethod
    def mongodb_port() -> int:
        return os.environ.get("MONGODB_PORT") or 27017

    @staticmethod
    def mongodb_database() -> str:
        return os.environ.get("MONGODB_DATABASE") or 'facekeeper'
