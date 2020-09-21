import os


class Config(object):
    # General application settings
    @staticmethod
    def host() -> str:
        return os.environ.get("HOST") or "0.0.0.0"

    @staticmethod
    def port() -> int:
        return os.environ.get("PORT") or 80

    # Storage settings
    @staticmethod
    def storage_dsn() -> int:
        return os.environ.get("STORAGE_DSN") or "postgresql://facekeeper:facekeeper@localhost:5432/facekeeper"

    # MongoDB settings
    @staticmethod
    def mongodb_host() -> str:
        return os.environ.get("MONGODB_HOST") or "host.docker.internal"

    @staticmethod
    def mongodb_port() -> int:
        return os.environ.get("MONGODB_PORT") or 27017

    @staticmethod
    def mongodb_database() -> str:
        return os.environ.get("MONGODB_DATABASE") or "facekeeper"

    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://guest:guest@localhost:5672/%2F'
