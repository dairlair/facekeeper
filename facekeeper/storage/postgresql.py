from facekeeper.core import StorageInterface, PersonEmbedding
import numpy as np
import psycopg2
from typing import List, Optional
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.extras import RealDictCursor


def addapt_numpy_array(numpy_array):
    return AsIs(list(numpy_array))


class PostgreSQLStorage(StorageInterface):
    def __init__(self, dsn: str):
        super().__init__()
        register_adapter(np.ndarray, addapt_numpy_array)
        self.dsn = dsn
        self.conn = None

    def save_embedding(self, person: str, digest: str, recognizer: str, embedding: np.array, tags: List[str],) -> str:
        try:
            cur = self.get_connection().cursor()
            sql = "INSERT INTO embeddings (person, digest, recognizer, embedding, tags) VALUES (%s, %s, %s, ARRAY%s, %s) RETURNING id"
            cur.execute(sql, (person, digest, recognizer, embedding, tags))
            row = cur.fetchone()
            self.get_connection().commit()
            return row['id']
        except psycopg2.errors.UniqueViolation:
            self.get_connection().rollback()
            # We anyway will return the ID of already saved embedding
            return self.get_embedding_id(recognizer, digest)
        finally:
            cur.close()

    def get_embeddings(self, recognizer) -> List[PersonEmbedding]:
        cur = self.get_connection().cursor()
        sql = "SELECT id, person, embedding, tags FROM embeddings WHERE recognizer = %s"
        cur.execute(sql, (recognizer,))

        return [PersonEmbedding(r['id'], r['person'], np.array(r['embedding']), r['tags']) for r in cur.fetchall()]

    def get_embedding(self, embedding_id: str) -> dict:
        cur = self.get_connection().cursor()
        sql = "SELECT * FROM embeddings WHERE id = %s"
        cur.execute(sql, (embedding_id,))
        return cur.fetchone()

    def get_embedding_id(self, recognizer, digest) -> Optional[str]:
        cur = self.get_connection().cursor()
        cur.execute(
            "SELECT id FROM embeddings WHERE recognizer = %s AND digest = %s", (recognizer, digest),
        )
        row = cur.fetchone()
        return str(row['id']) if row else None

    def get_connection(self) -> psycopg2.extensions.connection:
        if self.conn is None:
            self.conn = self.connect()

        return self.conn

    def connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
