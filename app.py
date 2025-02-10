
from transcriptor import TranscriptorIA
import time
import os
from utils import limpiar_consola


def menu(transcriptor: TranscriptorIA):

    while True:
        print("\tQue quieres hacer?")
        print("1. Subir un archivo")
        print("2. Grabar el audio ")
        print("3. Salir ")
        opcion = input("Seleccione su opcion: ")
        if opcion in ["1","2","3"]:
            if opcion == "1":
                transcriptor.transcribir_archivo()
            elif opcion == "2":
                transcriptor.record_audio2transc()
            elif opcion == "3":
                print("Saliendo...", end="\r")  # Imprime "Cargando..." sin salto de línea
                time.sleep(2)  # Espera 2 segundos
                print("           b a i ")  # Sobrescribe la línea con espacios
            break
        else:
            limpiar_consola()
            print("No seleccionaste ninguna opcion correcta",end="\n")
            time.sleep(1)
            limpiar_consola()


def main():

    transcriptor = TranscriptorIA()
    menu(transcriptor)

if __name__ == "__main__":
    main()