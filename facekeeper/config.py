import os

class Config(object):
    # Storage settings
    @staticmethod
    def storage_dsn() -> int:
        return os.environ.get('STORAGE_DSN') or 'postgresql://facekeeper:facekeeper@172.28.128.1:5432/facekeeper'

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://ia:ia@172.28.128.1:5672/iavhost'
