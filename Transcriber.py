import whisper
import string

def transcribe_audio(audio_file: str = "output_audio.wav", show_debug: bool = False) -> str | None:
    try:
        # Load the base Whisper model change if needed (fast & accurate)
        model = whisper.load_model("base")

        if show_debug:
            print(f"Whisper: Transcribing {audio_file} ...")

        # Transcribe audio
        result = model.transcribe(audio_file)
        text = result.get("text", "").strip()

        # Remove punctuation at the end
        text = text.rstrip(string.punctuation).strip()

        #if show_debug:
            #print(f"Whisper transcription (cleaned): {text}")

        if text:
            return text
        else:
            if show_debug:
                print("transcribe_audio: No speech detected.")
            return None

    except Exception as e:
        print("transcribe_audio: Error during transcription:", e)
        return None
