import os
import pyaudio
from pydub import AudioSegment
import whisper
import time
import warnings
import keyboard
from utils import get_audiofile, audio_to_mp3
import wave
import keyboard
from utils import limpiar_consola



class TranscriptorIA():
    def __init__(self):
        self.modelo = "turbo"
        self.dispositivo = "cuda"

    # Función que será ejecutada al presionar el botón
    def transcribir_archivo(self):

        audio_path = get_audiofile()

        self.transcribir(audio_path)


    def record_audio2transc(self):
        # Configuración de parámetros de grabación
        FORMAT = pyaudio.paInt16
        CHANNELS = 1  # Mono
        RATE = 44100  # Frecuencia de muestreo
        CHUNK = 1024  # Tamaño del buffer
        WAV_FILENAME = "grabacion.wav"
        MP3_FILENAME = "grabacion.mp3"

        # Inicializar PyAudio
        audio = pyaudio.PyAudio()

        # Configurar flujo de audio
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Presiona 'SPACE' para pausar/reanudar, 'ESC' para detener la grabación.")

        frames = []
        recording = True  # Estado de grabación
        paused = False    # Estado de pausa

        while recording:
            if keyboard.is_pressed('esc'):  # Si presiona ESC, detiene la grabación
                time.sleep(1)
                limpiar_consola()
                print("\nGrabación finalizada.")
                break
            if keyboard.is_pressed('space'):  # Si presiona SPACE, pausa o reanuda
                paused = not paused
                if paused:
                    print("\n🔴 Grabación en pausa. Presiona 'SPACE' para reanudar.")
                else:
                    print("\n🟢 Grabación reanudada.")
                time.sleep(0.3)
            
            if not paused:
                data = stream.read(CHUNK)
                frames.append(data)

        # Detener y cerrar el flujo de audio
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Guardar en formato WAV
        with wave.open(WAV_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        #print(f"Archivo guardado como {WAV_FILENAME}")

        # Convertir a MP3 usando pydub
        audio_segment = AudioSegment.from_wav(WAV_FILENAME)
        audio_segment.export(MP3_FILENAME, format="mp3")
        #print(f"Archivo convertido a {MP3_FILENAME}")

        if os.path.exists(WAV_FILENAME):
            os.remove(WAV_FILENAME)

        

        self.transcribir(MP3_FILENAME)


        if os.path.exists(MP3_FILENAME):
            os.remove(MP3_FILENAME)

    def transcribir(self,path = None):

        if path == None:
            print("No hay nada, viejo")
            return
        start_time = time.time()
        audio_path_mp3 = audio_to_mp3(path)

        # Suprimir advertencias específicas
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

        # Cargar el modelo de Whisper
        model = whisper.load_model(name=self.modelo, device=self.dispositivo)

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
