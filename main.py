import numpy as np
import pyaudio
from scipy.io.wavfile import write
import ctypes
import os
import wave
import subprocess

# Audio configurations
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (mono)
RATE = 16000  # Sample rate (16 kHz)
CHUNK = 3200  # Number of frames per buffer (200 ms chunks)
RAW_FILE = "raw_audio.wav"  # File path for raw audio
PROCESSED_RAW_FILE = "processed_audio.raw"  # File path for processed raw audio
PROCESSED_WAV_FILE = "processed_audio.wav"  # File path for processed WAV audio

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

# Load RNNoise library
# Ensure the path is correctly formatted and accessible
rnnoise = ctypes.cdll.LoadLibrary("/home/shreyas_03/rnnoise/.libs/librnnoise.so")
rnnoise.rnnoise_create.restype = ctypes.c_void_p
rnnoise.rnnoise_process_frame.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
rnnoise.rnnoise_destroy.argtypes = [ctypes.c_void_p]

# Class to manage RNNoise state and process audio frames
class RNNoise:
    def __init__(self):
        self.state = rnnoise.rnnoise_create()

    def process_frame(self, frame):
        in_frame = np.array(frame, dtype=np.float32)
        out_frame = np.zeros_like(in_frame)
        rnnoise.rnnoise_process_frame(self.state, out_frame.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), in_frame.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
        return out_frame

    def destroy(self):
        rnnoise.rnnoise_destroy(self.state)

# Function to perform noise reduction using RNNoise
def noise_reduction(rnnoise, audio_data):
    # Ensure the frame size is 480 samples
    frame_size = 480
    num_frames = len(audio_data) // frame_size
    denoised_data = np.zeros_like(audio_data, dtype=np.float32)

    for i in range(num_frames):
        frame = audio_data[i * frame_size:(i + 1) * frame_size]
        denoised_frame = rnnoise.process_frame(frame)
        denoised_data[i * frame_size:(i + 1) * frame_size] = denoised_frame

    # Apply gain to the denoised data
    gain = 1.5
    denoised_data = denoised_data * gain

    # Convert back to int16
    denoised_data = np.clip(denoised_data * 32768.0, -32768, 32767).astype(np.int16)
    return denoised_data

# Function to capture audio from the microphone
def capture_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    return stream

# Function to process the captured audio using RNNoise
def process_audio(stream, rnnoise):
    input_frames = []
    output_frames = []
    try:
        while True:
            data = stream.read(CHUNK)
            input_frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.int16)
            processed_data = noise_reduction(rnnoise, audio_data)
            processed_bytes = processed_data.tobytes()
            output_frames.append(processed_bytes)
    except KeyboardInterrupt:
        print("Recording stopped by user.")
    return input_frames, output_frames

# Function to output the processed audio to files
def output_audio(input_frames, output_frames):
    p = pyaudio.PyAudio()
    output_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    for data in output_frames:
        output_stream.write(data)
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
    write(RAW_FILE, RATE, np.frombuffer(b''.join(input_frames), dtype=np.int16))
    write(PROCESSED_RAW_FILE, RATE, np.frombuffer(b''.join(output_frames), dtype=np.int16))

if __name__ == "__main__":
    # Initialize RNNoise instance
    rnnoise_instance = RNNoise()
    
    # Capture audio from the microphone
    stream = capture_audio()
    
    # Process the captured audio using RNNoise
    input_frames, output_frames = process_audio(stream, rnnoise_instance)
    
    # Output the processed audio to files
    output_audio(input_frames, output_frames)
    
    # Destroy the RNNoise instance
    rnnoise_instance.destroy()
    
    # Convert the processed raw audio to WAV format
    create_wav_from_raw(PROCESSED_RAW_FILE, PROCESSED_WAV_FILE, RATE, CHANNELS)
    
    # Verify the processed audio file
    verify_wav_file(PROCESSED_WAV_FILE)
    
    # Cleanup
    stream.close()
    pyaudio.PyAudio().terminate()
    os.remove(RAW_FILE)
    os.remove(PROCESSED_RAW_FILE)
    
    print(f"Processed audio saved to {PROCESSED_WAV_FILE}.")
