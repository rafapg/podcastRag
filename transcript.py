import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

AUDIO_FILE = "data/audio/naruhodo-423.mp3"
API_KEY = os.getenv("DG_API_KEY")


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="enhanced",
            language="pt-BR",
            smart_format=True,
            diarize=True,
        )

        # STEP 3: Call the transcribe_file method with
        response = deepgram.listen.prerecorded.v("1").transcribe_file(
            payload,
            options,
            timeout=300,
        )

        # STEP 4: Print the response
        print(response.to_json(indent=4))

        # STEP 5: Save to output json file
        with open("data/transcription/naruhodo-424-transcript.json", "w") as file:
            file.write(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
