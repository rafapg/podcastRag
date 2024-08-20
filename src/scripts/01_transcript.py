import os
from dotenv import load_dotenv
from datetime import datetime
import httpx

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

AUDIO_FILE = "data/audio/naruhodo-423.mp3"
TRANSCRIPT_FILE = "data/transcription/bkp_naruhodo-424-transcript.json"
API_KEY = os.getenv("DG_API_KEY")


def main():
    try:
        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer = file.read()

        source: FileSource = {
            "buffer": buffer,
        }

        # Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="whisper-large",
            language="pt-BR",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )

        # Call the transcribe_file method with
        before = datetime.now()
        response = deepgram.listen.rest.v("1").transcribe_file(
            source,
            options,
            timeout=httpx.Timeout(300.0, connect=10.0),
        )
        after = datetime.now()

        print("")
        difference = after - before
        print(f"time: {difference.seconds}")

        with open(TRANSCRIPT_FILE, "w") as file:
            file.write(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
