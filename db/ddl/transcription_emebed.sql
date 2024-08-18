CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE transcription_embed (
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    speaker TEXT NOT NULL,
    embedding vector,
    transcript TEXT
);