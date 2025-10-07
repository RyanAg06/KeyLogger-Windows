
# Imports
import email
from fileinput import filename
from pydoc import plain
from ssl import create_default_context
from json_manager import LeerJSON
from email.message import EmailMessage
import smtplib
import socket

# Clase Enviar Correo
class Enviar_Email:

    """
        PUERTO 25: Puerto Estandar Sin Cifrar SOLO para Servidores (No Recomendado, Bloqueado Regularmente por SPAM)
        PUERTO 465: Puerto por SSL/TLS Cifrado (Descontinuado pero Algunas Aplicaciones aun lo Soportan)
        PUERTO 587: Puerto con STARTTLS Cifrado (Estandar Moderno, y mas Seguro que SSL)
    """

    # Constructor
    def __init__(self, ruta_config: str, ruta_log: str):
        self.__leerJson = LeerJSON(ruta_json=ruta_config)
        self.__ruta_log = ruta_log
        self.__remitente = self.__leerJson.get_valor("remitente")
        self.__remitente_psw = self.__leerJson.get_valor("remitente_psw")
        self.__destinatarios = self.__leerJson.get_valor("destinatarios")
        self.__asunto_correo = self.__leerJson.get_valor("asunto_correo")
        self.__cuerpo_correo = self.__leerJson.get_valor("cuerpo_correo")
        self.__nombre_log_adjunto = self.__leerJson.get_valor("nombre_log_adjunto")
        self.__puerto = self.__leerJson.get_valor("puerto")
        self.__dominio = f"smtp.{self.__leerJson.get_valor('dominio')}"

    # Enviar Correo
    def enviar_correo(self, mensaje_enviado: str) -> bool:

        # Contenido Correo
        correo = EmailMessage()
        correo["From"] = self.__remitente
        correo["To"] = self.__destinatarios
        correo["Subject"] = self.__asunto_correo
        correo.set_content(self.__cuerpo_correo)
        with open(self.__ruta_log, "rb") as log:
            correo.add_attachment(log.read(), maintype="text", subtype="plain", filename=self.__nombre_log_adjunto)

        # Prueba de Conexion
        try:

            # Cargar Certificados CA Confiables del Sistema
            contexto = create_default_context()

            # Puerto 465 (SSL)
            if self.__puerto == 465:
                print("[-] Iniciando Conexion SSL...")
                with smtplib.SMTP_SSL(host=self.__dominio, port=self.__puerto, context=contexto, timeout=10) as server:
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    print("[-] Enviando Correo...")
                    server.send_message(msg=correo)
                    print(f"{mensaje_enviado}")
                    return True

            # Puerto 587 (TLS)
            elif self.__puerto == 587:
                print("[-] Iniciando Conexion TLS...")
                with smtplib.SMTP(host=self.__dominio, port=self.__puerto, timeout=10) as server:
                    server.ehlo()
                    server.starttls(context=contexto) # Cifrar
                    server.ehlo()
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    print("[-] Enviando Correo...")
                    server.send_message(msg=correo)
                    print(f"{mensaje_enviado}")
                    return True
                
            # Puerto 25 (Sin Cifrado)
            elif self.__puerto == 25:
                print("[-] Iniciando Conexion...")
                with smtplib.SMTP(host=self.__dominio, port=self.__puerto, timeout=10) as server:
                    server.ehlo()
                    if server.has_extn('starttls'):
                        server.starttls(context=contexto)
                        server.ehlo()
                    else:
                        print("[!] El Servidor No Soporta STARTTLS; Continuando Sin Cifrado...")
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    print("[-] Enviando Correo...")
                    server.send_message(msg=correo)
                    print(f"{mensaje_enviado}")
                    return True

            else:
                print("[!] Puerto Desconocido")
                return False

        # Error por Credenciales Invalidas
        except smtplib.SMTPAuthenticationError:
            print("[!] No se Pudo Iniciar Sesion, Credenciales Invalidas")
            return False

        # Error por No lograr Conexion
        except smtplib.SMTPConnectError as e:
            print(f"[!] No se Pudo Establecer la Conexion: {e}")
            return False

        # Error por Desconexion del Servidor
        except smtplib.SMTPServerDisconnected:
            print(f"[!] Servidor SMTP Desconectado")
            return False

        # Error en HELO/EHLO o caracteristicas no soportadas
        except (smtplib.SMTPHeloError, smtplib.SMTPNotSupportedError):
            print(f"[!] Error de Protocolo SMTP")
            return False

        # Errores de Red / DNS / Timeout
        except (socket.timeout, socket.gaierror, OSError):
            print(f"[!] Error de Red")
            return False

        # Error Inesperado en SMTP
        except smtplib.SMTPException as e:
            print(f"[!] Error SMTP")
            return False

        # Alguna Exception No Controlada
        except Exception as e:
            print(f"[!] No se Pudo Enviar Correo. Error Inesperado: {e}")
            return False

    # Prueba de Conexion
    def prueba_conexion(self) -> bool:
        print("[-] Iniciando Prueba de Conexion...")
        try:

            # Cargar Certificados CA Confiables del Sistema
            contexto = create_default_context()

            # Puerto 465 (SSL)
            if self.__puerto == 465:
                with smtplib.SMTP_SSL(host=self.__dominio, port=self.__puerto, context=contexto, timeout=10) as server:
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    return True

            # Puerto 587 (TLS)
            elif self.__puerto == 587:
                with smtplib.SMTP(host=self.__dominio, port=self.__puerto, timeout=10) as server:
                    server.ehlo()
                    server.starttls(context=contexto)
                    server.ehlo()
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    return True
                
            # Puerto 25 (Sin Cifrado)
            else:
                with smtplib.SMTP(host=self.__dominio, port=self.__puerto, timeout=10) as server:
                    server.ehlo()
                    if server.has_extn('starttls'):
                        server.starttls(context=contexto)
                        server.ehlo()
                    else:
                        print("[!] El Servidor No Soporta STARTTLS; Continuando Sin Cifrado...")
                    server.login(self.__remitente, self.__remitente_psw)
                    print("[+] Conexion Establecida")
                    return True

        except Exception:
            print(f"[!] Prueba de Conexion Fallida")
            return False

    #     \____/\
    #     /\  /\
    #    -byRyanAg...