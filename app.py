
from transcriptor import TranscriptorIA
import time
import os
#from utils import limpiar_consola
import argparse
import torch


def menu(transcriptor, opcion: str):
    if opcion == "1":
        transcriptor.transcribir_archivo()
    elif opcion == "2":
        transcriptor.record_audio2transc()
    elif opcion == "3":
        print("Saliendo...", end="\r")
        time.sleep(2)
        print("           b a i ")
    else:
        print("No seleccionaste ninguna opción correcta.")


def main():

    if torch.cuda.is_available():
        print(f"✅ GPU detectada: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ No se detectó GPU. El procesamiento usará CPU.")

    transcriptor = TranscriptorIA()

    parser = argparse.ArgumentParser()
    parser.add_argument("--opcion", help="Selecciona una opción: 1-subir archivo, 2-grabar audio, 3-salir", required=True)
    args = parser.parse_args()

    menu(transcriptor, args.opcion)

if __name__ == "__main__":
    main()