CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS "embeddings";

CREATE TABLE "embeddings" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid() UNIQUE,
    person TEXT NOT NULL,
    digest TEXT NOT NULL,
    recognizer TEXT NOT NULL,
    embedding DOUBLE PRECISION[] NOT NULL
);

CREATE UNIQUE INDEX "unique_recognizer_digest_ids" ON "embeddings" USING BTREE (recognizer, digest);
ALTER TABLE "embeddings" ADD COLUMN tags TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[];

-- INSERT INTO embeddings(person, digest, recognizer, embedding) VALUES ('test', 'test', 'test', ARRAY[]::DOUBLE PRECISION[]);