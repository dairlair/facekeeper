import os

class Config(object):
    # Storage settings
    @staticmethod
    def storage_dsn() -> int:
        return os.environ.get('STORAGE_DSN') or 'postgresql://facekeeper:facekeeper@host.docker.internal:5432/facekeeper'

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://ia:ia@host.docker.internal:5672/iavhost'
