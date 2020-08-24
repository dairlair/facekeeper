import os


class Config(object):
    # General application settings
    @staticmethod
    def host() -> str:
        return os.environ.get("HOST") or '0.0.0.0'

    @staticmethod
    def port() -> int:
        return os.environ.get("PORT") or 80

    # MongoDB settings
    @staticmethod
    def mongodb_host() -> str:
        return os.environ.get("MONGODB_HOST") or 'localhost'

    @staticmethod
    def mongodb_port() -> int:
        return os.environ.get("MONGODB_PORT") or 27017

    @staticmethod
    def mongodb_database() -> str:
        return os.environ.get("MONGODB_DATABASE") or 'facekeeper'

    # Dapr settings
    @staticmethod
    def dapr_url() -> str:
        return os.environ.get("DAPR_URL") or None

    @staticmethod
    def dapr_pubsub() -> str:
        return os.environ.get("DAPR_PUBSUB") or 'pubsub'