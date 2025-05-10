
from transcriptor import TranscriptorIA
import argparse
#import torch

def main():

    #if torch.cuda.is_available():
    #    print(f"✅ GPU detectada: {torch.cuda.get_device_name(0)}")
    #else:
    #    print("⚠️ No se detectó GPU. El procesamiento usará CPU.")

    
    parser = argparse.ArgumentParser(description="Selecciona una opción de modelo")
    parser.add_argument(
        "--model",
        help="Selecciona una opción: 'turbo' o 'large' (por defecto: 'turbo')",
        choices=["turbo", "large"],
        default="turbo"
    )
    args = parser.parse_args()
    print(f"🎯 Usando modelo: \033[1m{args.model}\033[0m")
    transcriptor = TranscriptorIA(args.model)

    transcriptor.transcribir_archivo()


if __name__ == "__main__":
    main()