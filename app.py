import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import warnings


def rename_file(file_path):
    if file_path.endswith(".dat.unknown"):
        new_file_path = file_path.replace(".dat.unknown", ".opus")
        os.rename(file_path, new_file_path)
        print(f"Archivo renombrado a: {new_file_path}")
        return new_file_path
    return file_path

def get_audiofile():
    input_file = askopenfilename(
        title="Selecciona el archivo M4A",
        filetypes=[("Archivos de audio", "*.m4a *.mp3 *.opus *.dat.unknown")]
        #multiple=True devolverá una tupla con las rutas de los archivos seleccionados.
    )
    # Si no se seleccionó un archivo, salir
    if not input_file:
        print("No se seleccionó ningún archivo.")
        return
    
    audio_file = rename_file(input_file)

    return audio_file

def convertir_opus_a_mp3(input_file):

    audio = AudioSegment.from_file(input_file)
    audio.export("audioTemporal.mp3", format="mp3")
    audio_path=os.path.join(os.getcwd(),"audioTemporal.mp3")

    return audio_path

def convertir_m4a_a_mp3(input_file):

    audio = AudioSegment.from_file(input_file, format="m4a")
    audio.export("audioTemporal.mp3", format="mp3")
    audio_path=os.path.join(os.getcwd(),"audioTemporal.mp3")

    return audio_path

def audio_to_mp3(audio_path):
    if audio_path.endswith(".m4a"):
        return convertir_m4a_a_mp3(audio_path)
    elif audio_path.endswith(".opus"):
        return convertir_opus_a_mp3(audio_path)
    elif audio_path.endswith(".mp3"):
        print(audio_path)
        return audio_path
    else:
        print("No convirtio nada")
    return "ERROR"

def main():
    start_time = time.time()
    # Cargar el archivo de audio
    audio_path = get_audiofile()
    
    audio_path_mp3= audio_to_mp3(audio_path)

    audio = AudioSegment.from_file(audio_path_mp3)

    # Detectar las partes donde hay audio (en milisegundos)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)

    # Mostrar los intervalos con audio
    #print("Rangos de audio detectados:", nonsilent_ranges)

    # Suprimir advertencias específicas
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

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
    transcripcion_final = " ".join(textos_filtrados)
    print(f"Transcripción final: \033[1m{transcripcion_final}\033[0m")

    # Borrar el archivo temporal
    temp_file = "temp.wav"
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"Archivo temporal '{temp_file}' borrado.")

    # Borrar el archivo temporal
    audio_temp_file = "audioTemporal.mp3"
    if os.path.exists(audio_temp_file):
        os.remove(audio_temp_file)
        print(f"Archivo temporal '{audio_temp_file}' borrado.")
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Tiempo total de ejecución: {execution_time} segundos")

if __name__ == "__main__":
    main()