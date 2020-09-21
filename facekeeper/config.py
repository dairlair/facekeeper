import os

class Config(object):
    # Storage settings
    @staticmethod
    def storage_dsn() -> int:
        return os.environ.get("STORAGE_DSN") or "postgresql://facekeeper:facekeeper@localhost:5432/facekeeper"

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://guest:guest@localhost:5672/%2F'
