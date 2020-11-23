from injector import singleton, Binder
from facekeeper.core import (
    FaceKeeper,
    RecognizerInterface,
    StorageInterface,
    DownloaderInterface,
    MatcherInterface,
)
from facekeeper.recognizer import Recognizer
from facekeeper.storage.postgresql import PostgreSQLStorage
from facekeeper.config import Config
from facekeeper.downloader import RequestsDownloader
from facekeeper.matcher import EmbeddingsMatcher
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from urllib.parse import urlparse, ParseResult
import sys
import logging


def configure(binder: Binder) -> None:
    binder.bind(FaceKeeper, to=FaceKeeper, scope=singleton)
    binder.bind(DownloaderInterface, to=downloader, scope=singleton)
    binder.bind(MatcherInterface, to=matcher, scope=singleton)
    binder.bind(RecognizerInterface, to=Recognizer("large"), scope=singleton)
    binder.bind(StorageInterface, storage, scope=singleton)
    binder.bind(BlockingConnection, amqp, scope=singleton)


def amqp() -> BlockingConnection:
    try:
        dsn: str = Config.amqp_url()
        return BlockingConnection(parameters=URLParameters(dsn))
    except AMQPConnectionError:
        logging.error("Couldn't connect to the AMQP broker at: [%s]" % dsn)
        sys.exit(2)


def storage() -> StorageInterface:
    dsn: str = Config.storage_dsn()
    parts: ParseResult = urlparse(dsn)

    if parts.scheme == "postgresql":
        return PostgreSQLStorage(dsn)

    raise EnvironmentError(
        """
        Wrong storage DSN provided.
        Must be in the following format:
        postgresql://username:password@hostname:port/database
        """
    )


def matcher() -> MatcherInterface:
    return EmbeddingsMatcher()


def downloader() -> DownloaderInterface:
    return RequestsDownloader()
