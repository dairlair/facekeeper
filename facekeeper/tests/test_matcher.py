# Ensures that EmbeddingsMatcher works as expected.
from typing import List
from facekeeper.core import PersonEmbedding
from facekeeper.matcher import EmbeddingsMatcher
from facekeeper.tests.embeddings import (
    get_main_embeddings,
    get_delevingne_embeddings,
    get_robbie_embeddings,
)


def test_matching():
    # Given - the matcher with embeddings
    embeddings: List[PersonEmbedding] = get_main_embeddings()
    matcher = EmbeddingsMatcher()
    matcher.add_embeddings(embeddings)

    test_embeddings = get_delevingne_embeddings()
    for embedding in test_embeddings:
        print("Check embedding")
        print(embedding.id + ", " + embedding.person)
        # Each test embeddings MUST be recognized with empty tags
        # or with tags "hollywood" or "british".
        # And MUST NOT be recognize with tag "australian"
        match = matcher.match(embedding.embedding, [])
        assert match

        match = matcher.match(embedding.embedding, ["british"])
        assert match

        match = matcher.match(embedding.embedding, ["australian"])
        assert match is None

    test_embeddings = get_robbie_embeddings()
    for embedding in test_embeddings:
        # Each test embeddings MUST be recognized with empty tags
        # or with tags "hollywood" or "australian".
        # And MUST NOT be recognize with tag "british"
        match = matcher.match(embedding.embedding, [])
        assert match

        match = matcher.match(embedding.embedding, ["australian"])
        assert match

        match = matcher.match(embedding.embedding, ["british"])
        assert match is None
