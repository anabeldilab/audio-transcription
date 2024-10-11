import torch
import whisper
from pydub import AudioSegment
import os
import time


# Función para convertir el audio a WAV
def convert_to_wav(input_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    wav_audio_path = os.path.splitext(input_audio_path)[0] + ".wav"
    audio.export(wav_audio_path, format="wav")
    return wav_audio_path


# Función para transcribir el audio con Whisper
def transcribe_audio(audio_path):
    if torch.cuda.is_available():
        print("GPU disponible")
        device = "cuda"
    else:
        print("GPU no disponible")
        device = "cpu"
    # Cargar el modelo base de Whisper
    model = whisper.load_model(
        "large", device=device
    )  # base, tiny, small, medium, large

    # Convertir a WAV si no es WAV
    if not audio_path.endswith(".wav"):
        print(f"Convirtiendo {audio_path} a WAV...")
        audio_path = convert_to_wav(audio_path)

    # Transcribir el archivo de audio
    print("Transcribiendo el audio...")
    start = time.time()
    result = model.transcribe(audio_path)
    print(f"Tiempo de transcripción: {time.time() - start:.2f} segundos")

    # Retornar la transcripción
    return result["text"]


# Ruta del archivo de audio (por ejemplo, archivo.m4a)
input_audio_path = "media/Oct 2, 12.19_ satcomm.m4a"

# Llamar a la función de transcripción
transcription = transcribe_audio(input_audio_path)

# Mostrar la transcripción
print("Transcripción del audio:")
print(transcription)
# Save transcription to a text file with accents (UTF-8 encoding) and \n every 120 characters
with open("transcription-reunión-satcomm-2024-10-02", "a", encoding="utf-8") as f:
    for i in range(0, len(transcription), 120):
        f.write(transcription[i : i + 120] + "\n")
