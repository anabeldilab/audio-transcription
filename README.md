# Audio Transcription Tool

This script converts audio files from `.m4a` format to `.wav`, processes them as needed, and transcribes the audio using two different services: [Vosk](https://alphacephei.com/vosk/) and Google Speech Recognition. The transcription is saved in a text file.

## Requirements

Before running the script, make sure you have the following Python packages installed:

- pydub
- vosk
- SpeechRecognition
- ffmpeg (you need to install ffmpeg on your operating system; it is not a Python package).

You can install the required Python packages with the following command:

```bash
pip install pydub vosk SpeechRecognition
```

To install ffmpeg, follow the instructions on [FFmpeg.org](https://ffmpeg.org/download.html).

## Usage

1. **Place your `.m4a` file in the `media` folder**. The file should be named `trimmed_repaired.m4a` or you can modify the script to point to the correct file.

2. **Run the script**:

   ```bash
   python transcribe.py
   ```

3. **Choose the transcription service** when prompted. You can select either Vosk or Google.

4. **The transcription will be saved in a file named `transcription.txt`**. The text will be UTF-8 encoded with a newline every 120 characters.

## Code Structure

- `convert_m4a_to_wav(m4a_file, output_folder="media")`: Converts a `.m4a` file to `.wav`.
- `convert_to_mono_pcm(input_wav, output_wav, sample_rate=16000)`: Converts the `.wav` file to mono PCM format with a 16kHz sample rate.
- `convert_sample_rate(input_wav, output_wav, sample_rate=16000)`: Changes the sample rate of the `.wav` file.
- `transcribe_audio_Vosk(file_path)`: Transcribes the audio file using the Vosk model.
- `transcribe_audio_google(file_path)`: Transcribes the audio file using Google Speech Recognition.

## Vosk Models

To use Vosk, you need to download a speech recognition model and place it in the correct directory. You can download models from [here](https://alphacephei.com/vosk/models).

Make sure to update the `model_path` variable in the script to point to the correct location of your model.

## Notes

- The script uses ffmpeg to convert audio formats, so ffmpeg must be properly installed and accessible in your PATH.
- The output file `transcription.txt` is saved in the directory where the script is executed.
- The script is set up to work with Spanish audio files. If you need to transcribe audio in another language, make sure to adjust the parameters in `recognize_google`.

## Example Usage

```bash
python transcribe.py
```

**Expected Output**:

```text
What service would you like to use? (Vosk or Google)
Google
Transcription time: 10.54 seconds
The resulting transcription of the audio...
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
