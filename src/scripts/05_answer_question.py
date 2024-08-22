import ollama
from psycopg2 import connect

# QUESTION = "Qual a utilidade da luz azul na medicina?"
QUESTION = "O que é o césio 137?"


def _get_database_connection():
    return connect(
        host="localhost",
        database="vectordb",
        user="testuser",
        password="testpwd",
        port="5432"
    )


def answer_question(question: str, context: list) -> str:
    with open("prompts/question_anwser.txt", "r") as file:
        template = file.read()
    prompt = template.replace("<QUESTION>", question).replace(
        "<CONTEXT>", "\n\n- ".join(context))

    print(prompt)
    llm_response = ollama.generate('llama3:8b', prompt)
    return llm_response["response"]


def main():
    try:
        question = QUESTION
        conn = _get_database_connection()
        sql_cursor = conn.cursor()
        embed_response = ollama.embed(
            "bge-m3",
            question
        )
        question_embeddings = embed_response["embeddings"][0]
        sql_cursor.execute(
            f"""select start_time, end_time, speaker, transcript,
            1 - (embedding <=> '{question_embeddings}') AS cosine_similarity
            from transcription_embed
            ORDER BY cosine_similarity desc
            LIMIT 5""")
        result = sql_cursor.fetchall()
        context = [f"{row[3]}" for row in result]
        answer = answer_question(question, context)
        print(f"Pergunta: {question}")
        print(f"Resposta: {answer}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
