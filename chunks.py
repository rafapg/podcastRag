import json
import tiktoken

SAVE_FILE = True
TRANSCRIPTION_FILE = "data/transcription/naruhodo-424-transcript.json"
enc = tiktoken.encoding_for_model("gpt-4o")


def sec_to_time_str(sec: float) -> str:
    hours = int(sec // 3600)
    minutes = int(sec // 60 % 60)
    seconds = int(sec // 1 % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def getSpeakerName(speakerId: int) -> str:

    speaker_list_position = ["Ken Fujioka", "Altay de Souza"]
    speaker = ""
    if speakerId < len(speaker_list_position):
        speaker = speaker_list_position[speakerId]
    else:
        speaker = "Speaker" + str(speakerId)

    return speaker


def token_count(text: str) -> int:
    return len(enc.encode(text))


def create_chunk_object(speaker, text, start, end) -> object:
    return {
        "start": start,
        "end": end,
        "speaker": speaker,
        "text": text
    }


def split_paragraph_in_chunks(paragraph: object) -> list:
    transcription_chunks = []
    speaker = getSpeakerName(paragraph["speaker"])

    chunk_text = ""
    chunk_start = None
    for sentence in paragraph["sentences"]:
        if not chunk_start:
            chunk_start = sentence["start"]
        if chunk_text and token_count(chunk_text + sentence["text"]) > 512:
            chunk_object = create_chunk_object(
                speaker,
                chunk_text,
                chunk_start,
                sentence["end"]
            )
            transcription_chunks.append(chunk_object)
            chunk_text = ""
            chunk_start = None

        chunk_text += " " + sentence["text"]

    if chunk_text:
        paragraft_left_sentences = create_chunk_object(
            speaker,
            chunk_text,
            chunk_start,
            sentence["end"]
        )
        transcription_chunks.append(paragraft_left_sentences)

    return transcription_chunks


def group_paragraphs_by_speaker(paragraphs: list) -> list:
    agg_paragraph_list = []
    spekaer_sentences_agg = None
    for paragraph in paragraphs:
        if not spekaer_sentences_agg:
            spekaer_sentences_agg = paragraph
            current_speaker = paragraph["speaker"]
            continue

        if paragraph["speaker"] == current_speaker:
            spekaer_sentences_agg["sentences"] += paragraph["sentences"]
            spekaer_sentences_agg["end"] = paragraph["end"]
        else:
            current_speaker = paragraph["speaker"]
            agg_paragraph_list.append(spekaer_sentences_agg)
            spekaer_sentences_agg = paragraph
    if spekaer_sentences_agg:
        agg_paragraph_list.append(spekaer_sentences_agg)

    return agg_paragraph_list


def main():
    try:
        # Load the JSON file
        with open(TRANSCRIPTION_FILE) as file:
            data = json.load(file)

        paragraphs = data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
        grouped_paragraphs = group_paragraphs_by_speaker(paragraphs)

        transcription_chunks = []
        for sentence_agg in grouped_paragraphs:
            transcription_chunks += split_paragraph_in_chunks(sentence_agg)

        if SAVE_FILE:
            chunks_file = "data/transcription/naruhodo-424-chunks.json"
            with open(chunks_file, "w") as file:
                file.write(json.dumps(transcription_chunks, indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
