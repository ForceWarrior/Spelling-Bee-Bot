import sounddevice as sd
import soundfile as sf
import Transcriber
import typeout
import keyboard
import numpy as np
import queue
import time
import threading

# ---------- SETTINGS ----------
Output_Filename = "output_audio.wav" # Output filename for the recorded audio (WAV format)
Channels = 2 # Number of audio channels (1 for mono, 2 for stereo)
Rate = 48000 # Sample rate (Hz)
device_index = 38 # put your device index here (use sd.query_devices() to find it)
Chunk = 1024 # Number of frames per read
# -------------------------------

def record_manual():
    print("Press [F1] to START recording, [F2] to STOP recording.")

    frames_q = queue.Queue()
    recording_event = threading.Event()

    def callback(indata, status):
        if status:
            print("Stream status:", status)
        if recording_event.is_set():
            # copy to avoid referencing the same buffer
            frames_q.put(indata.copy())

    try:
        with sd.InputStream(samplerate=Rate,
                            channels=Channels,
                            dtype='int16',
                            device=device_index,
                            blocksize=Chunk,
                            callback=callback):

            print("Stream opened. Waiting for keypresses...")
            while True:
                if keyboard.is_pressed('F1') and not recording_event.is_set():
                    recording_event.set()
                    print("Recording started...")
                # Stop recording
                if keyboard.is_pressed('F2') and recording_event.is_set():
                    recording_event.clear()
                    print("Recording stopped.")
                    break

                # Global quit requested
                if keyboard.is_pressed('F12'):
                    # ensure recording flag cleared and exit immediately
                    recording_event.clear()
                    print("Exit requested (F12) during recording/wait).")
                    return None
                time.sleep(0.05)

    except Exception as e:
        print("Error during recording (stream):", e)
        return False

    # Drain queue into list
    recording = []
    while not frames_q.empty():
        recording.append(frames_q.get())

    if not recording:
        print("No audio frames were recorded.")
        return False

    # Combine all chunks and save
    try:
        audio_data = np.concatenate(recording, axis=0)
        sf.write(Output_Filename, audio_data, Rate)
        print(f"Recording saved to {Output_Filename}")
        return True
    except Exception as e:
        print("Error saving recording:", e)
        return False


def transcribe_and_type():
    try:
        # Use the dynamic model selector from Transcriber.py
        transcription = Transcriber.transcribe_with_dynamic_model(audio_file=Output_Filename, show_debug=True)
        if transcription:
            words = transcription.strip().split()
            if words:
                last_word = words[-1]
                try:
                    typeout.typeout(last_word)
                except Exception as e:
                    print("Typing failed, last word:", last_word)
                    print("typeout error:", e)
            else:
                print("Transcription empty after splitting.")
        else:
            print("No transcription available (speech not recognized).")
    except Exception as e:
        print("Error during transcription:", e)


if __name__ == "__main__":
    print("Ready. Press [F1] to start recording. After stopping (F2), transcription will be typed.")
    print("Press [F12] at any time to quit.")
    try:
        while True:
            # Run one recording session (record_manual waits for F1/F2)
            result = record_manual()
            # If record_manual returned None it means user requested global quit (F12)
            if result is None:
                print("Exiting.")
                break
            if result:
                transcribe_and_type()

            # small pause to debounce keys before next loop
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
