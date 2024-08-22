
from psycopg2 import connect
import json
from dotenv import load_dotenv
load_dotenv()

# EPISODE_NAME = "naruhodo-424"
EPISODE_NAME = "h30-cesio137"

EMBED_FILE = f"data/transcription/{EPISODE_NAME}-embed.json"
INSERT_EMBEDDING = """
INSERT INTO transcription_embed (start_time, end_time, speaker, embedding, transcript)
VALUES (%s, %s, %s, %s, %s)
"""


def _get_database_connection():
    return connect(
        host="localhost",
        database="vectordb",
        user="testuser",
        password="testpwd",
        port="5432"
    )


def main():
    try:
        conn = _get_database_connection()
        sql_cursor = conn.cursor()

        with open(EMBED_FILE) as file:
            embeddings = json.load(file)

        for embedding in embeddings:
            sql_cursor.execute(INSERT_EMBEDDING, [
                embedding["start"],
                embedding["end"],
                embedding["speaker"],
                embedding["embedding"],
                embedding["text"]
            ])
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Exception: {e}")
        conn.rollback()
        conn.close()


if __name__ == "__main__":
    main()
