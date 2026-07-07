from  Modelo.DatabaseConnection import ConexionMySQL
from Modelo.reg_individual import R_individual
from Modelo.user import User
from Modelo.registro import Registro
import base64
import hashlib
import re

class C_user:
    """
    Clase encargada de gestionar las operaciones relacionadas con los usuarios.
    Permite ingresar, modificar, eliminar, buscar usuarios y manejar su autenticación y tarjetas asociadas.
    """
    def __init__(self):
        self.id = None
    
    def Ingresar_Usuario(self,RUN,NOMBRE,APELLIDO_1,APELLIDO_2,TIPO_USER,CLAVE,HUELLA=None):
        """
        Ingresa un nuevo usuario en la base de datos con los datos proporcionados.
        
        Parámetros:
        RUN (str): El RUN del usuario a ingresar.
        NOMBRE (str): El nombre del usuario.
        APELLIDO_1 (str): El primer apellido del usuario.
        APELLIDO_2 (str): El segundo apellido del usuario.
        TIPO_USER (str): El tipo de usuario (por ejemplo, administrador, empleado).
        CLAVE (str): La contraseña del usuario.
        HUELLA (str, opcional): La huella del usuario, si aplica.
        """
        db = ConexionMySQL()
        print(HUELLA)
        print(RUN)
        resultado_proc = db.ejecutar_procedimiento_insert("insertar_empleados",(RUN,NOMBRE,APELLIDO_1,APELLIDO_2,TIPO_USER,CLAVE,HUELLA))
        print(resultado_proc)
        db.cerrar()
    def Ingresar_Tarjeta(self,RUN,RBD,COD_TARJETA):
        """
        Ingresa una tarjeta asociada a un usuario y escuela en la base de datos.
        
        Parámetros:
        RUN (str): El RUN del usuario.
        RBD (int): El RBD de la escuela.
        COD_TARJETA (str): El código de la tarjeta.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento_insert("insertar_tarjeta",(COD_TARJETA,RBD,RUN))
        print(resultado_proc)
        db.cerrar()

    def Ver_Usuario(self,run):
        """
        Busca un usuario en la base de datos utilizando su RUN.
        
        Parámetros:
        run (str): El RUN del usuario a buscar.
        
        Retorna:
        usuario (User): Un objeto User con los datos del usuario encontrado, o None si no se encuentra.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("VerUsuario",(run,))
        
        # Mostramos los datos obtenidos
        if resultado_proc:   
            fila = resultado_proc[0]
            usuario = User(run,fila[0]["nombre"], fila[0]["apellido_1"], fila[0]["apellido_2"], fila[0]["id_tipo_usuario"], fila[0]["clave"])      
        else:
            print("No se encontró el usuario.")
            usuario = None

        db.cerrar()
        return usuario

    def Modificar_Usuario(self,RUN,NOMBRE,APELLIDO_1,APELLIDO_2,TIPO_USER,CLAVE):
        """
        Modifica los datos de un usuario en la base de datos con los nuevos valores proporcionados.
        
        Parámetros:
        RUN (str): El RUN del usuario a modificar.
        NOMBRE (str): El nuevo nombre del usuario.
        APELLIDO_1 (str): El nuevo primer apellido del usuario.
        APELLIDO_2 (str): El nuevo segundo apellido del usuario.
        TIPO_USER (str): El nuevo tipo de usuario.
        CLAVE (str): La nueva contraseña del usuario.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento_update("ModificarUsuario",(RUN,NOMBRE,APELLIDO_1,APELLIDO_2,TIPO_USER,CLAVE))
        print(resultado_proc)
        db.cerrar()
    
    def Eliminar_Usuario(self,RUN):
        """
        Elimina un usuario de la base de datos utilizando su RUN.
        
        Parámetros:
        RUN (str): El RUN del usuario a eliminar.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento_update("EliminarUsuario",(RUN,))
        print(resultado_proc)
        db.cerrar()

    def text_mayuscula(self, Texto):
        """
        Convierte el texto proporcionado a mayúsculas.
        
        Parámetros:
        Texto (str): El texto que se desea convertir a mayúsculas.
        
        Retorna:
        str: El texto en mayúsculas.
        """
        return Texto.upper()

    def verificar_formato_run(self,run):
        """
        Verifica si el RUN proporcionado está en el formato XX.XXX.XXX-X o X.XXX.XXX-X.
        
        Parámetros:
        run (str): El RUN a verificar.
        
        Retorna:
        bool: True si el formato es válido, False en caso contrario.
        """
        # Verifica si el RUN está en el formato XX.XXX.XXX-X o X.XXX.XXX-X
        patron = re.compile(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$')
        return bool(patron.match(run))

    def formatear_run(self,run):
        """
        Formatea el RUN proporcionado eliminando puntos y guiones, y devolviendo el formato XX.XXX.XXX-X o X.XXX.XXX-X.
        
        Parámetros:
        run (str): El RUN a formatear.
        
        Retorna:
        str: El RUN formateado o None si el formato no es válido.
        """
        # Elimina cualquier punto o guión del RUN
        run = run.replace('.', '').replace('-', '').upper()
        if len(run) == 9:
            # Formato XX.XXX.XXX-X
            return f'{run[0:2]}.{run[2:5]}.{run[5:8]}-{run[8]}'
        elif len(run) == 8:
            # Formato X.XXX.XXX-X
            return f'{run[0]}.{run[1:4]}.{run[4:7]}-{run[7]}'
        else:
            return None

    def validar_run(self,run):
        """
        Valida si el RUN proporcionado es correcto según el algoritmo del dígito verificador.
        
        Parámetros:
        run (str): El RUN a validar.
        
        Retorna:
        bool: True si el RUN es válido, False en caso contrario.
        """
        # Elimina cualquier punto o guión del RUN
        run = run.replace('.', '').replace('-', '').upper()
        if len(run) not in [8, 9]:  # Un RUN válido debe tener 8 o 9 caracteres
            return False

        # Separa el cuerpo del RUN y el dígito verificador
        cuerpo, dv = run[:-1], run[-1]

        # Aplica el algoritmo de cálculo del dígito verificador
        suma, factor = 0, 2
        for c in reversed(cuerpo):  # Se recorre el cuerpo del RUN al revés
            suma += int(c) * factor
            factor = 2 if factor == 7 else factor + 1  # Ciclo de factores 2-7

        # Cálculo del dígito verificador esperado
        resto = suma % 11
        dv_calculado = '0' if resto == 0 else 'K' if resto == 1 else str(11 - resto)

        return dv == dv_calculado
    
    def Obtener_tarjeta(self,run,rbd):
        """
        Obtiene el ID de la tarjeta asociada a un usuario y una escuela.
        
        Parámetros:
        run (str): El RUN del usuario.
        rbd (int): El RBD de la escuela.
        
        Retorna:
        str: El ID de la tarjeta asociada, o una cadena vacía si no se encuentra.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("obtener_id_tarjeta",(run,rbd))
        idtarjeta =""
        # Mostramos los datos obtenidos
        if resultado_proc:   
            fila = resultado_proc[0]
            idtarjeta = fila[0]["idtarjeta"] 
        else:
            print("No se encontró el usuario.")

        db.cerrar()
        return idtarjeta
    
    def Ver_Eventos_Individual(self,fecha,idtarjeta,tipo_evento):
        """
        Obtiene los eventos individuales asociados a una tarjeta, en una fecha y tipo de evento específicos.
        
        Parámetros:
        fecha (str): La fecha de los eventos a consultar.
        idtarjeta (str): El ID de la tarjeta asociada.
        tipo_evento (str): El tipo de evento a buscar.
        
        Retorna:
        tuple: El ID del registro y la hora del evento, o cadenas vacías si no se encuentra.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("obtener_eventos",(idtarjeta,fecha,tipo_evento))
        # Mostramos los datos obtenidos
        
        if resultado_proc and len(resultado_proc) > 0 and len(resultado_proc[0]) > 0:  # Asegurar que no esté vacío
            fila = resultado_proc[0][0]  # Accedemos al diccionario dentro de la lista
            
            # Convertimos los valores de timedelta a string
            id_registro = str(fila.get("idregistro")) if fila.get("idregistro") else ""
            hora = str(fila.get("Hora")) if fila.get("Hora") else ""
            
        else:
            print("No se encontró el evento.")
            id_registro = hora = ""

        db.cerrar()
        return id_registro, hora
    
    def InsertarEvento(self,idregistro,tipo,hora):
        """
        Inserta un nuevo evento en la base de datos.
        
        Parámetros:
        idregistro (str): El ID del registro del evento.
        tipo (str): El tipo de evento.
        hora (str): La hora del evento.
        
        Retorna:
        bool: True si la inserción fue exitosa, False en caso contrario.
        """
        correcto = False
        db = ConexionMySQL()  # Crea la conexión
        if(db.insertar_evento(idregistro=idregistro, tipo_evento=tipo, hora=hora)):
            correcto = True
        else:
            correcto = False
        db.cerrar
        return correcto

    def ModificarEvento(self,idregistro,tipo,hora):
        """
        Modifica un evento existente en la base de datos.
        
        Parámetros:
        idregistro (str): El ID del registro del evento.
        tipo (str): El nuevo tipo de evento.
        hora (str): La nueva hora del evento.
        
        Retorna:
        bool: True si la modificación fue exitosa, False en caso contrario.
        """
        correcto = False
        db = ConexionMySQL()  # Crea la conexión
        if(db.modificar_evento(idregistro=idregistro, tipo_evento=tipo, hora=hora)):
            correcto = True
        else:
            correcto = False
        db.cerrar
        return correcto
    
    def verificar_usuario(self,run,clave):
        """
        Verifica las credenciales de un usuario (RUN y clave) en la base de datos.
        
        Parámetros:
        run (str): El RUN del usuario.
        clave (str): La clave del usuario.
        
        Retorna:
        str: El tipo de usuario si las credenciales son correctas, una cadena vacía si no.
        """
        dato = ""
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("verificar_usuario",(run,clave))

        if resultado_proc and len(resultado_proc) > 0 and resultado_proc[0]:   
            fila = resultado_proc[0][0]
            dato =  str(fila.get("id_tipo_usuario")) if fila.get("id_tipo_usuario") else ""
        else:
            print("No se encontró el usuario.")
            dato = ""

        db.cerrar()
        return dato

    def encode_password(password: str) -> str:
        """
        Genera un hash SHA-256 de la contraseña proporcionada y la codifica en base64.
        
        Parámetros:
        password (str): La contraseña a codificar.
        
        Retorna:
        str: La contraseña codificada en base64.
        """
        # Hash de la contraseña usando SHA-256
        hashed_password = hashlib.sha256(password.encode()).digest()
        # Codificar en base64 para mayor seguridad
        encoded_password = base64.b64encode(hashed_password).decode()
        return encoded_password