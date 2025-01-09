import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import warnings

def convertir_opus_a_mp3(input_file):

    audio = AudioSegment.from_file(input_file)
    audio.export("audioTemporal.mp3", format="mp3")
    audio_path=os.path.join(os.getcwd(),"audioTemporal.mp3")
    
    return audio_path

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

def main():

    audio = get_audiofile()
    print(os.path.dirname(audio))
    convertir_opus_a_mp3(audio)

if __name__ == "__main__":
    main()