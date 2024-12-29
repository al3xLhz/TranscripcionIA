from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper
import time

start_time = time.time()
# Cargar el archivo de audio
audio_path = "./audios/audio.mp3"

audio = AudioSegment.from_file(audio_path)

# Detectar las partes donde hay audio (en milisegundos)
nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)

# Mostrar los intervalos con audio
#print("Rangos de audio detectados:", nonsilent_ranges)

# Cargar el modelo de Whisper
#model = whisper.load_model("base", device="cuda")
#model = whisper.load_model("medium", device="cuda")
model = whisper.load_model("medium")

# Transcribir solo las partes con voz
transcriptions = []
total_fragments = len(nonsilent_ranges)

for i, (start, end) in enumerate(nonsilent_ranges):
    # Cortar y exportar el fragmento
    audio_chunk = audio[start:end]
    audio_chunk.export("temp.wav", format="wav")

    # Transcribir
    result = model.transcribe("temp.wav")
    transcriptions.append(result["text"])

    # Mostrar progreso manual
    progress = ((i + 1) / total_fragments) * 100
    print(f"Progreso: {progress:.2f}% ({i + 1}/{total_fragments} fragmentos procesados)")

textos_filtrados = [texto for texto in transcriptions if texto.strip()]
# Imprimir la transcripción combinada
print("Transcripción final:", " ".join(textos_filtrados))

end_time = time.time()

execution_time = end_time - start_time

print(f"Tiempo total de ejecución: {execution_time} segundos")