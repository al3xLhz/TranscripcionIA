from transcriptor import TranscriptorIA
import argparse
import os
# 1. Iniciar Docker
# 2. Comando 'docker ps -a' para ver los contenedores
# 3. Comando 'docker start <id-contenedor>' para iniciar el contenedor
# 4. Comando 'docker exec -it <id-contenedor> bash' para acceder al contenedor
# 5. Comando 'python app.py' para ejecutar el script
def parse_arguments():
    """Parse command line arguments for model selection."""
    parser = argparse.ArgumentParser(description="Selecciona una opción de modelo")
    parser.add_argument(
        "--model",
        help="Selecciona una opción: 'turbo' o 'large' (por defecto: 'turbo')",
        choices=["turbo", "large"],
        default="turbo"
    )
    return parser.parse_args()

def initialize_transcriptor(model_type):
    """Initialize the transcriptor with the specified model."""
    print(f"🎯 Usando modelo: \033[1m{model_type}\033[0m")
    return TranscriptorIA(model_type)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    #if torch.cuda.is_available():
    #    print(f"✅ GPU detectada: {torch.cuda.get_device_name(0)}")
    #else:
    #    print("⚠️ No se detectó GPU. El procesamiento usará CPU.")
    
    args = parse_arguments()
    transcriptor = initialize_transcriptor(args.model)
    transcriptor.transcribir_archivo()

if __name__ == "__main__":
    main()