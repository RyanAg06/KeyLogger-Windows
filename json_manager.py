
# imports
from json import load

# Clase LeerJSON
class LeerJSON:

    # Constructor
    def __init__(self, ruta_json: str):
        self.__ruta_json = ruta_json

    # Obtener Valor
    def get_valor(self, clave: str) -> str:

        # Abrir JSON en Modo Lectura
        with open(self.__ruta_json, "r") as archivo_json:
            diccionario_config = load(archivo_json) # Convertir JSON a Diccionario
            return (diccionario_config["configuracion"][clave]) # Devolver Valor
    
    #     \____/\
    #     /\  /\
    #    -byRyanAg...