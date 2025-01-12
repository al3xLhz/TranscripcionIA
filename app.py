import os
import threading
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import warnings
from scipy.io import wavfile
import noisereduce as nr
from tkinter import messagebox
import torch


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
    start_time = time.time()
    # Cargar el archivo de audio

    
    audio_path = get_audiofile()
    audio_path_mp3= audio_to_mp3(audio_path)
    audio = AudioSegment.from_file(audio_path_mp3)
    print(torch.cuda.is_available())  # Esto debe devolver True.
    print(torch.cuda.get_device_name(0))
    # Eliminar el ruido ambiental
    #audio = eliminar_ruido(audio)
    
    # Detectar las partes donde hay audio (en milisegundos)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)

    # Mostrar los intervalos con audio
    #print("Rangos de audio detectados:", nonsilent_ranges)

    # Suprimir advertencias específicas
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

    # Cargar el modelo de Whisper
    #model = whisper.load_model("base", device="cuda")
    model = whisper.load_model("medium", device="cuda")
    #model = whisper.load_model("medium")

    # Transcribir solo las partes con voz
    transcriptions = []
    total_fragments = len(nonsilent_ranges)

    for i, (start, end) in enumerate(nonsilent_ranges):
        # Cortar y exportar el fragmento
        audio_chunk = audio[start:end]
        audio_chunk.export("temp.wav", format="wav")

        # Transcribir
        result = model.transcribe("temp.wav", language="es")
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
        #print(f"Archivo temporal '{temp_file}' borrado.")

    # Borrar el archivo temporal
    audio_temp_file = "audioTemporal.mp3"
    if os.path.exists(audio_temp_file):
        os.remove(audio_temp_file)
        #print(f"Archivo temporal '{audio_temp_file}' borrado.")
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Tiempo total de ejecución: {execution_time} segundos")
    #messagebox.showinfo("",transcripcion_final)



def main():

    transcribir()
    return
    global label
    # Crear la ventana principal
    root = tk.Tk()

    # Configurar la ventana principal
    root.title("")  # Título de la ventana
    window_width = 300  # Ancho de la ventana
    window_height = 200  # Alto de la ventana

    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular las coordenadas x e y para centrar la ventana
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Configurar la geometría de la ventana
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Opcional: evitar redimensionar la ventana
    root.resizable(False, False)

    # Agregar widgets
    label = tk.Label(root, text="Bienvenido al transcriptor!")  # Crear una etiqueta
    label.pack(pady=20)  # Mostrar la etiqueta con un espacio de 20 píxeles

    button_transcriptor = tk.Button(root, text="Elegir audio", command=transcribir)  # Crear un botón para cerrar la ventana
    button_transcriptor.pack(pady=10)
    button = tk.Button(root, text="Cerrar", command=root.destroy)  # Crear un botón para cerrar la ventana
    button.pack(pady=10)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()
    
    return
    

if __name__ == "__main__":
    main()