import os
import whisper
import time
import warnings
#import keyboard
from utils import audio_to_mp3
import torch

# Colores ANSI para terminal
colors = [
        "\033[91m",  # Rojo
        "\033[92m",  # Verde
        "\033[93m",  # Amarillo
        "\033[94m",  # Azul
        "\033[95m",  # Magenta
        "\033[96m",  # Cian
        "\033[97m",  # Blanco brillante
    ]
reset = "\033[0m"  # Resetear color
bold = "\033[1m"   # Texto en negrita

class TranscriptorIA():
    def __init__(self,modelo):
        self.modelo = modelo
        self.dispositivo = "cuda" if torch.cuda.is_available() else "cpu"

    # Función que será ejecutada al presionar el botón
    def transcribir_archivo(self):

        audio_folder = "Audio"
        audio_files = [f for f in os.listdir(audio_folder) if os.path.isfile(os.path.join(audio_folder, f))]

        if not audio_files:
            print("No audio files found in Audio folder")
            return

        # Siempre selecciona el primer archivo automáticamente
        audio_path = os.path.join(audio_folder, audio_files[0])
        print(f"{colors[1]}Archivo seleccionado automáticamente: {bold}{audio_files[0]}{reset}")

        self.transcribir(audio_path)

    def transcribir(self,path):

        audio_path_mp3 = audio_to_mp3(path)

        # Suprimir advertencias específicas
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

        # Load Whisper model
        self._print_device_info()
        model = self._load_whisper_model()

        start_time = time.time()
        model = whisper.load_model(name=self.modelo, device=self.dispositivo)

        # Transcribir el audio completo
        self._perform_transcription(model, audio_path_mp3)

        execution_time = time.time() - start_time
        print(f"Tiempo total de ejecución: {execution_time:.2f} segundos")

        # Clean up temporary files
        self._cleanup_temp_files()

        # Ask user if they want to delete the original file
        if self._ask_delete_file(path):
            self._delete_file(path)


    def _print_device_info(self):
        """Print information about the device being used."""
        if self.dispositivo == "cuda":
            print("Usando la 🔝")  # Using GPU
        else:
            print("Usando la cpu😒")  # Using CPU

    def _load_whisper_model(self):
        """Load the Whisper model."""
        return whisper.load_model(name=self.modelo, device=self.dispositivo)

    def _perform_transcription(self, model, audio_path):
        """Perform audio transcription using the loaded model."""
        result = model.transcribe(audio_path)  # Optional: add language="es" if needed
        transcripcion = result["text"]
        print(f"Transcripción final: \033[1m{transcripcion}\033[0m")
        return transcripcion

    def _cleanup_temp_files(self):
        """Clean up temporary files created during transcription."""
        import os

        temp_files = ["temp.wav", "audioTemporal.mp3"]

        for file in temp_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    # Uncomment for debugging: print(f"Archivo temporal '{file}' borrado.")
                except OSError as e:
                    print(f"Error al eliminar archivo temporal '{file}': {e}")

    def _ask_delete_file(self, path):
        """Ask the user if they want to delete the original file."""
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
        """Delete the specified file."""
        import os

        try:
            os.remove(path)
            print(f"Archivo '{path}' borrado exitosamente.")
        except OSError as e:
            print(f"Error al borrar el archivo: {e}")
