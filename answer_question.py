import ollama
from psycopg2 import connect

# CREATE TABLE transcription_embed (
#     start_time FLOAT NOT NULL,
#     end_time FLOAT NOT NULL,
#     speaker TEXT NOT NULL,
#     embedding vector,
#     transcript TEXT
# );


def _get_database_connection():
    return connect(
        host="localhost",
        database="vectordb",
        user="testuser",
        password="testpwd",
        port="5432"
    )


def answer_question(question: str, context: list) -> str:
    prompt = f"""
Você é um assistente que deve responder à perguntas com base em um conjunto de textos forncecidos.
Você deve entender a pergunta, analisar os textos do conjunto fornecido e montar a pergunta mais completa para a pergunta.

A resposta da pergunta deve conter apenas informações contidas no conjunto de textos fornecidos. Nenhuma informação adicional deve ser fornecida.
Caso não seja possível responder a pergunta com as informações fornecidas, a resposta deve ser "Não sei responder a pergunta".

Pergunta: `'{question}'`

Conjunto de Textos:

```
- '{'\n-'.join(context)}'
```

Resposta:
"""
    print(prompt)
    llm_response = ollama.generate('llama3:8b', prompt)
    return llm_response["response"]


def main():
    try:
        question = "Qual a utilidade da luz azul na medicina?"
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
            LIMIT 10""")
        result = sql_cursor.fetchall()
        context = [f"{row[3]}" for row in result]
        answer = answer_question(question, context)
        print(f"Pergunta: {question}")
        print(f"Resposta: {answer}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
