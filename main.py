''''Assignment: Real-Time Noise Cancellation System
Objective
The goal of this assignment is to develop a real-time noise cancellation system that
processes audio in two distinct scenarios:
1. Single Speaker Scenario: In this case, the system isolates and enhances the audio
of one primary speaker while treating all other voices and background noises as
interference to be minimized or eliminated.
2. Multiple Speaker Scenario: In this case, the system preserves multiple speaker
voices and simultaneously filters out environmental noise (e.g., white noise,
workplace background noise, or vehicle noise).
Requirements
You will implement a noise cancellation system that filters out unwanted background noise in
real-time from a live audio stream (such as a microphone input) and outputs the processed
audio in two possible scenarios (single speaker and multiple speakers). The processed
audio should retain the clarity of the target speaker(s) while significantly reducing any
interfering noise.
The system must meet the following key requirements:
● Real-time processing: The system should process audio streams in real-time, with
a latency of less than 100 milliseconds for each 200 ms audio chunk.
● Input and Output: The system will take live audio input from a microphone and
output a clean, noise-reduced audio stream.
● File Output: The processed (cleaned) audio will be saved as a .wav file.
● Write a neat and commented code in Python.'''
import pyaudio
import wave
import subprocess
import os

# Audio configurations
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 3200  # 200 ms chunks
RAW_FILE = "raw_audio.wav"
PROCESSED_RAW_FILE = "processed_audio.raw"
PROCESSED_WAV_FILE = "processed_audio.wav"

# Function to verify if a file is a valid WAV file
def verify_wav_file(file_path):
    try:
        with wave.open(file_path, "rb") as wf:
            print(f"File: {file_path}")
            print(f" - Channels: {wf.getnchannels()}")
            print(f" - Sample Width: {wf.getsampwidth()} bytes")
            print(f" - Frame Rate: {wf.getframerate()} Hz")
            print(f" - Frames: {wf.getnframes()}")
            print("File is a valid WAV file.\n")
    except wave.Error as e:
        print(f"Error: {e}")
        print(f"{file_path} is not a valid WAV file.\n")

# Function to wrap raw audio data into a valid WAV file
def create_wav_from_raw(raw_file, wav_file, sample_rate, channels):
    try:
        with wave.open(wav_file, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit audio = 2 bytes per sample
            wf.setframerate(sample_rate)
            with open(raw_file, "rb") as rf:
                wf.writeframes(rf.read())
        print(f"Converted raw audio to WAV format: {wav_file}")
    except Exception as e:
        print(f"Error creating WAV file: {e}")

# Initialize PyAudio
audio = pyaudio.PyAudio()
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording audio... Press Ctrl+C to stop.")
frames = []

try:
    while True:
        data = input_stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

except KeyboardInterrupt:
    print("\nStopping recording...")

# Save raw audio
with wave.open(RAW_FILE, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))

print(f"Raw audio saved to {RAW_FILE}")

# Verify the raw WAV file
verify_wav_file(RAW_FILE)

# Path to rnnoise_demo inside WSL
rnnoise_path = "/home/shreyas_03/rnnoise/examples/rnnoise_demo"

# Apply noise suppression using rnnoise_demo
try:
    result = subprocess.run(
        ['wsl', rnnoise_path, RAW_FILE, PROCESSED_RAW_FILE],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"Noise suppression complete: {result.stdout.decode()}")
except subprocess.CalledProcessError as e:
    print(f"Error during noise suppression: {e.stderr.decode()}")

# Convert raw output to WAV format
create_wav_from_raw(PROCESSED_RAW_FILE, PROCESSED_WAV_FILE, RATE, CHANNELS)

# Verify processed audio
verify_wav_file(PROCESSED_WAV_FILE)

# Cleanup
input_stream.close()
audio.terminate()
os.remove(RAW_FILE)
os.remove(PROCESSED_RAW_FILE)

print(f"Processed audio saved to {PROCESSED_WAV_FILE}.")
