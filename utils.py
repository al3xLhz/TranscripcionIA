from pydub import AudioSegment
#from tkinter.filedialog import askopenfilename
import os

def rename_file(file_path):
    if file_path.endswith(".dat.unknown"):
        new_file_path = file_path.replace(".dat.unknown", ".opus")
        os.rename(file_path, new_file_path)
        print(f"Archivo renombrado a: {new_file_path}")
        return new_file_path
    return file_path
"""
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
"""
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

def convertir_wav_a_mp3(input_file):
        audio = AudioSegment.from_file(input_file,format="wav")
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
        #print(audio_path)
        return audio_path
    elif audio_path.endswith(".wav"):
        return convertir_wav_a_mp3(audio_path)
    else:
        print("No convirtio nada")
    return "ERROR"
    
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' para Windows, 'clear' para Linux/macOS