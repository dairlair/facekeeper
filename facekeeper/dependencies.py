from injector import singleton, Binder
from facekeeper import FaceKeeper, RecognizerInterface, StorageInterface
from recognizer import Recognizer
from storage.mongodb import MongoDBStorage
from storage.postgresql import PostgreSQLStorage
from config import Config
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from urllib.parse import urlparse, ParseResult
import psycopg2
import sys
import logging


def configure(binder: Binder) -> None:
    binder.bind(FaceKeeper, to=FaceKeeper, scope=singleton)
    binder.bind(RecognizerInterface, to=Recognizer('large'), scope=singleton)
    binder.bind(StorageInterface, create_storage, scope=singleton)
    binder.bind(BlockingConnection, create_blocking_connection, scope=singleton)

def create_blocking_connection() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))    
    except AMQPConnectionError as e:
        logging.error("Couldn't connect to the AMQP broker. Please, check the AMQP is available with the specified URL: [%s]" % dsn)
        sys.exit(2)

def create_storage() -> StorageInterface:
    dsn: str = Config.storage_dsn()
    parts: ParseResult = urlparse(dsn)   

    if parts.scheme == 'postgresql':
        return PostgreSQLStorage(dsn)

    if parts.scheme == 'mongodb':
        # See: https://docs.mongodb.com/manual/reference/connection-string/
        # E.g.: mongodb+srv://server.example.com/?connectTimeoutMS=300000&authSource=aDifferentAuthDB
        return MongoDBStorage(dsn)

    raise EnvironmentError('Wrong storage DSN provided. Must be in format: postgresql://username:password@hostname:port/database')
