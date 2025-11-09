import os
import whisper
import time
import warnings
from utils import audio_to_mp3
import torch

class TranscriptorIA:
    """Clase para realizar transcripciones de audio usando Whisper."""

    # Constantes para colores ANSI
    COLORS = {
        'red': "\033[91m",
        'green': "\033[92m",
        'yellow': "\033[93m",
        'blue': "\033[94m",
        'magenta': "\033[95m",
        'cyan': "\033[96m",
        'white': "\033[97m"
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def __init__(self, modelo):
        """Inicializa el transcriptor con el modelo especificado."""
        self.modelo = modelo
        self.dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None

    def transcribir_archivo(self):
        """Transcribe el primer archivo de audio encontrado en la carpeta Audio."""
        audio_folder = "Audio"
        audio_files = [f for f in os.listdir(audio_folder)
                        if os.path.isfile(os.path.join(audio_folder, f))]

        if not audio_files:
            print("No audio files found in Audio folder")
            return

        audio_path = os.path.join(audio_folder, audio_files[0])
        print(f"{self.COLORS['green']}Archivo seleccionado automáticamente: "
                f"{self.BOLD}{audio_files[0]}{self.RESET}")

        self.transcribir(audio_path)

    def transcribir(self, path):
        """Realiza la transcripción completa de un archivo de audio."""
        audio_path_mp3 = audio_to_mp3(path)
        self._configurar_advertencias()

        start_time = time.time()
        self._inicializar_modelo()
        transcripcion = self._perform_transcription(self.model, audio_path_mp3)

        self._mostrar_tiempo_ejecucion(start_time)
        self._cleanup_temp_files()

        #!if self._ask_delete_file(path):
        #self._delete_file(path)


    def _configurar_advertencias(self):
        """Configura los filtros de advertencias."""
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

    def _inicializar_modelo(self):
        """Inicializa y carga el modelo Whisper."""
        self._print_device_info()
        self.model = whisper.load_model(name=self.modelo, device=self.dispositivo)

    def _print_device_info(self):
        """Muestra información sobre el dispositivo en uso."""
        if self.dispositivo == "cuda":
            print("Usando la 🔝")
        else:
            print("Usando la cpu😒")

    def _perform_transcription(self, model, audio_path):
        """Realiza la transcripción del audio."""
        result = model.transcribe(audio_path)
        transcripcion = result["text"]
        print(f"Transcripción final: {transcripcion}")
        return transcripcion

    def _mostrar_tiempo_ejecucion(self, start_time):
        """Muestra el tiempo total de ejecución."""
        execution_time = time.time() - start_time
        print(f"Tiempo total de ejecución: {execution_time:.2f} segundos")

    def _cleanup_temp_files(self):
        """Limpia los archivos temporales creados durante la transcripción."""
        temp_files = ["temp.wav", "audioTemporal.mp3"]

        for file in temp_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except OSError as e:
                    print(f"Error al eliminar archivo temporal '{file}': {e}")

    def _ask_delete_file(self, path):
        """Pregunta al usuario si desea eliminar el archivo original."""
        while True:
            response = input(f"¿Desea borrar el archivo '{path}'? (s/n): ").lower()
            if response == 's':
                return True
            elif response == 'n':
                print("El archivo no será borrado.")
                return False
            else:
                print("Por favor, ingrese 's' para sí o 'n' para no.")

    def _delete_file(self, path):
        """Elimina el archivo especificado."""
        try:
            os.remove(path)
            print(f"Archivo '{path}' borrado exitosamente.")
        except OSError as e:
            print(f"Error al borrar el archivo: {e}")
