import os
from dotenv import load_dotenv
from datetime import datetime
import httpx

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    UrlSource,
)

load_dotenv()

# EPISODE_NAME = "naruhodo-423"
# AUDIO_FILE = "data/audio/naruhodo-423.mp3"

# história em 30 minutos - cesio 137
EPISODE_NAME = "h30-cesio137"
AUDIO_FILE = "https://traffic.megaphone.fm/APO7774053839.mp3"

# Teste de podcast com 5 minutos - arroz de festa
# EPISODE_NAME = "arroz-de-festa"
# AUDIO_FILE = "https://traffic.megaphone.fm/APO4411763321.mp3"

TRANSCRIPT_FILE = f"data/transcription/{EPISODE_NAME}-transcript.json"
API_KEY = os.getenv("DG_API_KEY")


def transcribe_audio_file(audioFile: str, client: DeepgramClient, options: PrerecordedOptions):
    with open(audioFile, "rb") as file:
        buffer = file.read()
    source: FileSource = {
        "buffer": buffer,
    }
    response = client.listen.rest.v("1").transcribe_file(
        source,
        options,
        timeout=httpx.Timeout(300.0, connect=10.0),
    )
    return response


def transcribe_audio_url(url: str, client: DeepgramClient, options: PrerecordedOptions):
    source: UrlSource = {
        "url": url,
    }
    response = client.listen.rest.v("1").transcribe_url(
        source,
        options,
        timeout=httpx.Timeout(1000.0, connect=10.0),
    )
    return response


def transcribe_audio(audioFile: str, client: DeepgramClient, options: PrerecordedOptions):
    before = datetime.now()
    if (audioFile.startswith("http")):
        response = transcribe_audio_url(AUDIO_FILE, client, options)
    else:
        response = transcribe_audio_file(AUDIO_FILE, client, options)
    after = datetime.now()

    difference = after - before
    print("")
    print(f"time: {difference.seconds}")
    return response


def main():
    try:
        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        # Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="whisper-large",
            language="pt-BR",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )

        transcript_response = transcribe_audio(AUDIO_FILE, deepgram, options)
        with open(TRANSCRIPT_FILE, "w") as file:
            file.write(transcript_response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
