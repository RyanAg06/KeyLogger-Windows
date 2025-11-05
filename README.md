
# KeyLogger para Windows en Python
KeyLogger Para Windows Desarrollado en Python con Parametros Personalizables Facilmente Desde **config.json**

## Caracteristicas Principales:
- Guardar Teclas Presionadas en Log (Principal de Pulsaciones)
- Guardar Portapapeles en Log (Secundario del Portapapeles)
- Enviar Correo por SMTP
- Enviar Correo por Inactividad, Hora Programada y Excedes Cantidad de Caracteres
- Obtener Datos Usuario Al Iniciar (Nombre Sesion, Hora, Fecha)
- Configurable Desde **config.json**
- Al Apagar el Equipo y Encenderlo, Verificar si Hay un Log que no se Envio, Trabajar Sobre El
- Mejorar Seguridad del Correo con Protocolos Seguros

# Funcionamiento

### Dependencias
Antes de Iniciar el Script es **OBLIGATORIO** Instalar las Dependencias para su Funcionamineto, solo Ejecuta este Comando para Instalarlas:
```python
    pip install -r requirements.txt
```
Una Vez Instaladas ya Puedes Ejecutar el Script y el Compilado

### Ejecutar Por Primera Vez
Al Ejecutar el KL por Primera Vez este se Encargara de Crear un Archivo Log (Principal) Donde se Guardaran las Pulsaciones del Usuario, el Nombre de Este Archivo Puede ser Modificado en el Parametro de `nombre_log_pulsaciones`, en Caso que Quede Vacio (Por Defecto) el Nombre del Log Sera **key-log_NOMBRE_USUARIO_ACTUAL.txt**. Tambien a se Creara Otro Log (Secundario) que Este Guardara el Portapapeles, el Nombre de este Log Tambien es Personalizable con el Parametro `nombre_log_portapapeles`, De Igual Forma por Defecto Esta Vacio, se le Pondra Como Nombre **key-log_ClipBoard.txt**

### Ejecutar Despues De La Primera Vez
Al Iniciar el KL Despues de la Primera Vez Verificara si ya hay un log Principal, Verificara si este se Encuentra Vacio (Sin Importar la Cabecera) Entonces se Eliminara y Creara uno Nuevo.

### Configuracion De La Cuenta Remitente
Esta Cuenta se Encargara de Enviar los Correos a los Destinatarios, en Este Caso se Usara una Cuenta de Google, En el Parametro de `remitente` se Colocara el Correo de la Cuenta, y en el Parametro de `remitente_psw` se Pondra un Token Especial de 16 Digitos, para eso se Necesita Tener la **Autenticacion de 2 Pasos Activada (FA2)** en la Cuenta del Remitente y Crear el Token en: [AppPasswords](https://myaccount.google.com/apppasswords)

### Funcionamiento De Logs
- **Principal (Pulsaciones)**: En Este Log se Guardaran 2 Cosas; La Cabecera que Contiene el Nombre de la Sesion Actual, La Fecha, La Hora de Inicio del KL y la Version del Sistema Actual y las Teclas que el Usuario Vaya Ingresando

- **Secundario (Portapapeles)**: Aqui se Guardaran lo que el Usuario Copie Usando **(Control + C)** o **(Control + X)** se Guardara en este Log, al Cual se le Asignara un ID para que Pueda ser Referenciado en el Principal sin Necesidad de Colocar Todo lo que Copio y Asi Evitar Muchas Lineas Inecesarias en el Log Principal

### Modo Inactividad
Este Modo Enviara un Correo Cuando El Usuario Pase Un Lapso de Tiempo sin Tocar Alguna Tecla Desde la Ultima Pulsacion, Esta Configuracion Puede Ser Modificada Desde el **config.json** Modificando las Variables de:
- **horas_inactivo**
- **minutos_inactivo**
- **segundos_inactivo**

### Modo Hora Programada
Para Activar el Modo de Hora Programada Debes de Configurar los Parametros de Esta Forma:
- **horas_inactivo:** 0
- **minutos_inactivo:** 0
- **segundos_inactivo:** 0

Al Tener el Tiempo de Inactividad a 0 el Modo de **hora_programada** se Activara
- **Ejemplo:** Enviar a las 5pm → [17,0,0] (Formato de 24 Horas).

Tambien es Posible Colocar una Hora Exacta **Combinando** Horas, Minutos y Segundos
- **Ejemplo:** Enviar a las 10am con 30 Minutos y 15 Segundos → [10,30,15]

### Modo Caracteres Maximos
Este Modo Es Independiente a los 2 Anteriores ya que en los Otros Modos solo se Puede Activar Uno, pero en Este Modo se Puede Activar o Desactivar si es que no lo Necesitas tan solo Poniendo el Parametro de `caracteres_maximos` a un Numero Negativo (-1). Cuando el Usuario Alcance la Cantidad de Caracteres Maximos Establecido se Enviara un Correo

### Compilado
Dentro del Mismo Proyecto Viene el Archivo **compilar.bat**, Este Archivo Creara un Ejecutable Exe con un Icono que Puedes Cambiar Por Alguno de tu Preferencia, Se Asignara un Nombre Predeterminado "UserProfileServices", Puedes Cambiarlo al Terminar de Compilar, para Finalizar se **Recomienda** Colocar el Ejecutable en la Ruta de Inicio de Windows para que al Iniciar el Equipo el Ejecutable se Inicie Automaticamente

### Uso de Puertos
Se Necesita Escoger el Puerto por el Cual el Correo Sera Enviado,Hay Distintos Protocolos que se Usan, Aqui se Listan lo Protocolos Compatibles con SMTP, Cualquier Otro Puerto que **NO** se Encuentre en la Lista **Fallara**:
- **Puerto 587:** Este Puerto Usa el Protocolo **TLS** que es Mas Moderno y Seguro que el SSL (Recomendado)
- **Puerto 467:** Se Usa el Protocolo **SSL**, Este Puerto esta Descontinuado, No se Tendran Problemas al Momento de Enviar Correos ya que Aun es Compatible con Muchos Servicios de Correo Pero Se Recomienda Usar el Puerto 587
- **Puerto 25:** Este Puerto **NO** Tiene Cifrado, por lo que lo Hace Menos Seguro y Hace que los Servicios de Correo lo Tomen como SPAM y Causen **Correo Fallido en la Mayoria de Casos**

```
    \____/\
    /\  /\
```