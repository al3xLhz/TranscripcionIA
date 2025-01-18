import os
from pydub import AudioSegment
import whisper
import time
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
        filetypes=[("Archivos de audio", "*.m4a *.mp3 *.opus *.dat.unknown *.ogg")]
        #multiple=True devolverá una tupla con las rutas de los archivos seleccionados.
    )
    # Si no se seleccionó un archivo, salir
    if not input_file:
        print("No se seleccionó ningún archivo.")
        return None

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

def convertir_ogg_a_mp3(input_file):
    audio = AudioSegment.from_file(input_file, format="ogg")
    audio.export("audioTemporal.mp3", format="mp3")
    audio_path = os.path.join(os.getcwd(), "audioTemporal.mp3")

    return audio_path

def audio_to_mp3(audio_path):
    if audio_path.endswith(".m4a"):
        return convertir_m4a_a_mp3(audio_path)
    elif audio_path.endswith(".opus"):
        return convertir_opus_a_mp3(audio_path)
    elif audio_path.endswith(".ogg"):
        return convertir_ogg_a_mp3(audio_path)
    elif audio_path.endswith(".mp3"):
        print(audio_path)
        return audio_path
    else:
        print("No convirtio nada")
    return "ERROR"

"""
#ELIMINA EL RUIDO PERO HACE QUE NO DETECTE BIEN LAS PALABRAS
def eliminar_ruido(audio_segment):
    # Exportar el segmento de audio a un archivo WAV temporal
    audio_segment.export("temp.wav", format="wav")

    # Leer el archivo WAV temporal
    rate, data = wavfile.read("temp.wav")

    # Reducir el ruido
    reduced_noise = nr.reduce_noise(y=data, sr=rate)

    # Guardar el archivo WAV con ruido reducido
    wavfile.write("temp_reduced.wav", rate, reduced_noise)

    # Cargar el archivo WAV con ruido reducido como un segmento de audio
    audio_reduced = AudioSegment.from_wav("temp_reduced.wav")

    # Eliminar archivos temporales
    os.remove("temp.wav")
    os.remove("temp_reduced.wav")

    return audio_reduced
"""


# Función que será ejecutada al presionar el botón
def transcribir():

    audio_path = get_audiofile()

    if audio_path is None:
        return

    start_time = time.time()
    audio_path_mp3= audio_to_mp3(audio_path)

    #LOS SILENCIOS POR AHORA MANUAL EN AUDACITY

    # Suprimir advertencias específicas
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

    # Cargar el modelo de Whisper
    model = whisper.load_model("turbo", device="cuda")

    # Transcribir el audio completo
    result = model.transcribe(audio_path_mp3)#, language="es")
    transcripcion_final = result["text"]
    print(f"Transcripción final: \033[1m{transcripcion_final}\033[0m")

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Tiempo total de ejecución: {execution_time} segundos")

    # Borrar el archivo temporal
    temp_file = "temp.wav"
    if os.path.exists(temp_file):
        os.remove(temp_file)
        #print(f"Archivo temporal '{temp_file}' borrado.")
    # Borrar el archivo temporal
    audio_temp_file = "audioTemporal.mp3"
    if os.path.exists(audio_temp_file):
        os.remove(audio_temp_file)
        #print(f"Archivo temporal '{audio_temp_file}' borrado.")
    end_time = time.time()


def main():

    transcribir()


if __name__ == "__main__":
    main()