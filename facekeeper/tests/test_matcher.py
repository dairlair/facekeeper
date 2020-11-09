# Ensures that EmbeddingsMatcher works as expected.
from typing import List
from facekeeper.core import PersonEmbedding
from facekeeper.matcher import EmbeddingsMatcher
from facekeeper.tests.embeddings import get_main_embeddings, get_test_embeddings


def test_matching():
    # Given - the matcher with embeddings
    embeddings: List[PersonEmbedding] = get_main_embeddings()
    matcher = EmbeddingsMatcher()
    matcher.add_embeddings(embeddings)

    tags = []
    for embedding in embeddings:
        for tag in embedding.tags:
            if tag not in tags:
                tags.append(tag)

    assert tags == ['hollywood', 'british', 'australian']

    test_embeddings = get_test_embeddings()
    for embedding in test_embeddings:
        # Each test embeddings must be found with
        # all his tags and with empty specified tags.
        # And must be not found with omited tags.
        for tag in embedding.tags:
            match = matcher.match(embedding.embedding)