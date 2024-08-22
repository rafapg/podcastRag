import json
import ollama

# EPISODE_NAME = "naruhodo-424"
EPISODE_NAME = "h30-cesio137"

TRANSCRIPT_CHUNKS_FILE = f"data/transcription/{EPISODE_NAME}-chunks.json"
TRANSCRIPT_EMBED_FILE = f"data/transcription/{EPISODE_NAME}-embed.json"


def main():
    embedding_list = []
    try:
        # Load the JSON file
        with open(TRANSCRIPT_CHUNKS_FILE) as file:
            chunks = json.load(file)

        for chunk in chunks:
            embed_response = ollama.embed("bge-m3", chunk["text"])
            chunk_embeddings = embed_response["embeddings"][0]
            chunk["embedding"] = chunk_embeddings
            embedding_list.append(chunk)

        with open(TRANSCRIPT_EMBED_FILE, "w") as file:
            file.write(json.dumps(embedding_list))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
