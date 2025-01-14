

```markdown
# Audio Noise Reduction using RNNoise

This project captures audio from the microphone, performs noise reduction using the RNNoise library, and saves both raw and processed audio to disk in WAV format. It also provides the ability to convert processed raw audio into a WAV file. 

## Features

- Captures live audio from the microphone.
- Performs noise reduction using the RNNoise algorithm.
- Saves raw and processed audio to disk.
- Converts raw processed audio into a standard WAV file.
- Supports both Windows and Linux environments (with RNNoise library setup).
  
## Requirements

### Hardware
- Microphone to capture audio.

### Software
- Python 3.6+.
- Dependencies listed in `requirements.txt`.

## Installation

### 1. Clone the Repository
Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/SJ-1407/Noise_Cancellation.git
cd your-repository-name
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
It's a good practice to create a virtual environment for your project. To create and activate a virtual environment, follow these steps:

#### For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Use the `requirements.txt` file to install the necessary Python dependencies. Run the following command:

```bash
pip install -r requirements.txt
```

### 4. Install RNNoise Library

The RNNoise library must be installed and accessible on your system. Here are the steps to install it on different systems:

#### Linux (Ubuntu)
1. First, ensure you have the required dependencies installed:
   
```bash
sudo apt-get install build-essential pkg-config libsndfile1-dev libfftw3-dev
```

2. Clone the RNNoise repository:

```bash
git clone https://github.com/xiph/rnnoise.git
cd rnnoise
```

3. Build the RNNoise library:

```bash
./autogen.sh
./configure
make
```

4. Copy the built library to a folder:

```bash
cp .libs/librnnoise.so /path/to/your/project/rnnoise/.libs/
```

Ensure you update the path in the `rnnoise = ctypes.cdll.LoadLibrary("/path/to/your/project/rnnoise/.libs/librnnoise.so")` in the code to point to the correct location.

#### Windows

For Windows, you can use [Cygwin](https://www.cygwin.com/) or [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/) to run RNNoise, or you can build it using Visual Studio by following the instructions in the [RNNoise GitHub repository](https://github.com/xiph/rnnoise).

Once built, make sure to point the code to the correct `.dll` or `.so` file for RNNoise.

### 5. Update the File Path for RNNoise Library in Code
In the Python script, the RNNoise library is loaded using:

```python
rnnoise = ctypes.cdll.LoadLibrary("/path/to/your/project/rnnoise/.libs/librnnoise.so")
```

Ensure the path to the `librnnoise.so` (or `librnnoise.dll` for Windows) file is correct. Update the path in the code according to where you installed or built RNNoise.

## How to Use

### 1. Capture and Process Audio
Once you have set up the environment and installed the dependencies, you can capture audio from your microphone and process it by running the Python script:

```bash
python3 main.py
```

This will:
- Start recording audio from your microphone.
- Apply noise reduction using the RNNoise algorithm.
- Save the raw audio to `raw_audio.wav` and the processed audio to `processed_audio.raw`.
- Convert the processed raw audio to a WAV file and save it as `processed_audio.wav`.
- Verify that the processed audio file is valid.

### 2. Stop Recording
Press `Ctrl + C` to stop the recording. The processed audio will be saved in the same directory as the script.

### 3. Output Files
The following files will be created in the current working directory:
- `raw_audio.wav`: The raw audio captured from the microphone.
- `processed_audio.raw`: The raw processed audio data (after noise reduction).
- `processed_audio.wav`: The processed audio data in WAV format.

### 4. Verify the Processed Audio
After processing, the script will verify the validity of the `processed_audio.wav` file. If everything works correctly, you'll see a message confirming the file's validity:

```bash
File: processed_audio.wav
 - Channels: 1
 - Sample Width: 2 bytes
 - Frame Rate: 16000 Hz
 - Frames: <num_frames>
File is a valid WAV file.
```

## Troubleshooting

### 1. RNNoise Library Not Found
If the script can't find the RNNoise library, make sure the file path to `librnnoise.so` (or `librnnoise.dll` for Windows) is correctly set in the code. If you're using Windows, ensure you're using WSL or Cygwin for compatibility.


### 3. Missing Dependencies
If you encounter missing dependencies, ensure that all system dependencies are installed as outlined in the RNNoise setup section.



## Acknowledgements

- [RNNoise](https://github.com/xiph/rnnoise) for the noise reduction algorithm.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for capturing audio from the microphone.
- [NumPy](https://numpy.org/) for efficient numerical operations.






