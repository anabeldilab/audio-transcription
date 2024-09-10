import os
import subprocess
import wave
import json
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from pydub import AudioSegment
import time

# Convert .m4a to .wav
def convert_format_to_wav(m4a_file, output_folder="media", format="m4a"):
    wav_file = os.path.join(output_folder, "audio.wav")
    try:
        audio = AudioSegment.from_file(m4a_file, format=format)
        audio.export(wav_file, format="wav")
        return wav_file
    except Exception as e:
        print(f"Error al convertir el archivo: {e}")
        print ("Intentando con ffmpeg...")
        #ffmpeg -err_detect ignore_err -i m4a_file -c copy output.wav
        command = [
            'ffmpeg', '-err_detect', 'ignore_err', '-i', m4a_file, '-c', 'copy', wav_file
        ]
        subprocess.run(command, check=True)
        return wav_file


# Convert sample rate and channels to mono PCM
def convert_to_mono_pcm(input_wav, output_wav, sample_rate=16000):
    command = [
        'ffmpeg', '-i', input_wav,
        '-ac', '1',  # Convert to mono
        '-ar', str(sample_rate),  # Set sample rate to 16000 Hz
        '-sample_fmt', 's16',  # Set format to PCM 16-bit
        output_wav
    ]
    subprocess.run(command, check=True)


def convert_sample_rate(input_wav, output_wav, sample_rate=16000):
    command = [
        'ffmpeg', '-i', input_wav, '-ar', str(sample_rate), output_wav
    ]
    subprocess.run(command, check=True)


#Cut the audio file to the desired length
def cut_audio(input_wav, output_wav, start_time, end_time):
    # Generar un nombre de archivo temporal para el archivo de salida
    temp_output_wav = output_wav.replace('.wav', '_cut.wav')
    
    command = [
        'ffmpeg', '-i', input_wav, '-ss', start_time, '-to', end_time, temp_output_wav
    ]
    subprocess.run(command, check=True)
    
    # Renombrar el archivo temporal al nombre de archivo original
    os.replace(temp_output_wav, output_wav)


# Transcribe audio to text using Vosk
def transcribe_audio_Vosk(file_path):
    # Load the Vosk model (ensure that you have downloaded and placed the model in the correct directory)
    model_path = "vosk-model-es-0.42"  # Update this path to where your Vosk model is located
    if not os.path.exists(model_path):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack it to this folder.")
        exit(1)

    model = Model(model_path)

    # Open the audio file
    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Transcribe audio
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result)["text"]
            results.append(text)

    # Final result
    final_result = rec.FinalResult()
    final_text = json.loads(final_result)["text"]
    results.append(final_text)

    full_text = " ".join(results)
    return full_text

def transcribe_audio_google(file_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    
    try:
        # Usar reconocimiento de voz de Google en español
        text = recognizer.recognize_google(audio, language="es-ES")
        return text
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return None
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento de voz; {e}")
        return None

# Paths
media_folder = "media"
m4a_file = os.path.join(media_folder, "audio.m4a")

# Convert to .wav
wav_file = convert_format_to_wav(m4a_file, media_folder, "m4a")

while True:
    print ("Would you like to cut the audio file? (y/n)")
    cut = input()
    if cut == "y":
        print("Enter the start time (HH:MM:SS)")
        start_time = input()
        print("Enter the end time (HH:MM:SS)")
        end_time = input()
        cut_audio(wav_file, wav_file, start_time, end_time)
        break
    elif cut == "n":
        break

while True:
    print("What service would you like to use? (Vosk or Google)")
    service = input()

    transcription = ""

    if service == "Vosk" or service == "v":
        # Convert to mono PCM with 16kHz sample rate
        wav_16k_mono_file = os.path.join(media_folder, "audio_16k_mono.wav")
        convert_to_mono_pcm(wav_file, wav_16k_mono_file)
        # Transcribe audio
        start = time.time()
        transcription = transcribe_audio_Vosk(wav_16k_mono_file)
        end = time.time()
        print(f"Transcription time: {end - start} seconds")
        break
    elif service == "Google" or service == "g":
        # Convert to 16kHz sample rate
        wav_16k_file = os.path.join(media_folder, "audio_16k.wav")
        convert_sample_rate(wav_file, wav_16k_file)
        start = time.time()
        transcription = transcribe_audio_google(wav_16k_file)
        end = time.time()
        print(f"Transcription time: {end - start} seconds")
        break
    else:
        print("Invalid service. Please enter 'Vosk' or 'Google'.")

print(transcription)

# Save transcription to a text file with accents (UTF-8 encoding) and \n every 120 characters
with open("transcription.txt", "a", encoding="utf-8") as f:
    for i in range(0, len(transcription), 120):
        f.write(transcription[i:i+120] + "\n")