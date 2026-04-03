# Spelling Bee Bot

Spelling Bee Bot is a small Python tool that records audio from a selected microphone, transcribes it with Whisper, and types the result automatically using keyboard input. (this was intended for roblox spelling bee games)

## Features

- Start recording with `F1`
- Stop recording with `F2`
- Quit with `F12`
- Records audio from a selected input device
- Transcribes speech using Whisper
- Automatically types the transcribed result
- Lightweight console-based workflow

## How it works

1. Press `F1` to begin recording.
2. Speak into your selected microphone.
3. Press `F2` to stop recording.
4. The audio is saved temporarily.
5. Whisper transcribes the audio.
6. The bot types the result into the currently focused window.

## Requirements

- Python 3.10+
- Windows recommended
- A working microphone/input device
- FFmpeg may be required for Whisper depending on your setup

## Installation

Clone the repository:

```bash
git clone https://github.com/ForceWarrior/Spelling-Bee-Bot.git
cd Spelling-Bee-Bot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python Recorder.py
```

You should see console instructions telling you which keys to use.

## Configuration

The main settings are in `Recorder.py`:

```python
Output_Filename = "output_audio.wav"
Channels = 1
Rate = 48000
device_index = 20
Chunk = 1024
```

### Notes

- AI assistance was used
- `Channels` should usually be set to `1` unless your input device supports stereo.
- `device_index` must match your audio device.
- If you get `Invalid number of channels`, your selected device likely does not support the channel count you chose.

To list available audio devices, run this in Python:

```python
import sounddevice as sd
print(sd.query_devices())
```
