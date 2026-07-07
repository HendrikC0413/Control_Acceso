import mysql.connector
from mysql.connector import Error

class ConexionMySQL:
    def __init__(self, host="localhost", user="root", password="admin", database="controlacceso"):
        """Inicializa la conexión a MySQL"""
        try:
            self.conexion = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.conexion = None

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta SELECT y devuelve los resultados"""
        try:
            self.cursor.execute(consulta, parametros or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def ejecutar_vista(self, nombre_vista):
        """Ejecuta una vista y devuelve los resultados"""
        return self.ejecutar_consulta(f"SELECT * FROM {nombre_vista}")

    def ejecutar_procedimiento(self, nombre_proc, parametros):
        """Ejecuta un procedimiento almacenado y devuelve los resultados"""
        try:
            self.cursor.callproc(nombre_proc, parametros)
            resultados = []
            for resultado in self.cursor.stored_results():
                resultados.append(resultado.fetchall())
            return resultados
        except mysql.connector.Error as e:
            print(f"Error al ejecutar el procedimiento: {e}")
            return None

    def ejecutar_funcion(self, nombre_funcion, parametros):
        """Ejecuta una función de MySQL y devuelve el resultado"""
        try:
            param_str = ", ".join(["%s"] * len(parametros))
            self.cursor.execute(f"SELECT {nombre_funcion}({param_str})", parametros)
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la función: {e}")
            return None

    def ejecutar_procedimiento_insert(self, nombre_proc, parametros):
        """Ejecuta un procedimiento almacenado tipo INSERT con parámetros"""
        try:
            # Llamamos al procedimiento almacenado
            self.cursor.callproc(nombre_proc, parametros)

            # Commit para asegurarse de que los cambios se guardan en la base de datos
            self.conexion.commit()

            print("¡Registro insertado correctamente!")

        except mysql.connector.Error as e:
            print(f"Error al ejecutar el procedimiento: {e}")
            self.conexion.rollback()  # Si ocurre un error, revertimos la transacción

    def ejecutar_procedimiento_update(self, nombre_proc, parametros):
        """Ejecuta un procedimiento almacenado tipo UPDATE con parámetros"""
        try:
            self.cursor.callproc(nombre_proc, parametros)
            self.conexion.commit()  # Guardamos los cambios en la base de datos
            print("Cambios realizados")
        except mysql.connector.Error as e:
            print(f"Error al ejecutar el procedimiento: {e}")
            self.conexion.rollback()  # Revertimos cambios en caso de error


    def ejecutar_procedimiento2(self, nombre_proc, parametros):
        """Ejecuta un procedimiento almacenado y devuelve los resultados"""
        try:
            self.cursor.callproc(nombre_proc, parametros)
            resultados = []
            for resultado in self.cursor.stored_results():
                resultados.extend(resultado.fetchall())  # Cambiado a extend para aplanar la lista
            return resultados
        except mysql.connector.Error as e:
            print(f"Error al ejecutar el procedimiento: {e}")
            return None
    
    def ejecutar_procedimiento_Registrar_Evento(self, nombre_proc, parametros):
        """Ejecuta un procedimiento almacenado tipo INSERT con parámetros y devuelve un valor booleano"""
        completo = 0
        try:
            # Añadimos un parámetro de salida
            parametros = list(parametros)
            #parametros.append(0)  # Añadimos un valor de marcador para el parámetro de salida
            
            # Llamamos al procedimiento almacenado
            self.cursor.callproc(nombre_proc, parametros)
            # Commit para asegurarse de que los cambios se guardan en la base de datos
            self.conexion.commit()

            completo = 1

        except Error as e:
            if e.errno == 1644:  # Error MySQL generado por el SIGNAL
                # Si el error es esperado (evento ya existe), simplemente no hacemos nada y regresamos un valor neutral
                print(f"Evento ya existe, no se insertará: {e.msg}")
                completo = 2  # Mantenemos un valor neutral sin interrumpir el flujo
            else:
                print(f"Un error ocurrió: {e}")
                completo = 0  # En caso de otros errores, puedes marcar un error general
        return completo
    
    
    def fetch_biometric_models_batch(self, batch_size, offset):
        """
        Recupera un lote de modelos biométricos junto con los nombres de la tabla 'usuario'.
        """
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT huella, run FROM usuario WHERE huella IS NOT NULL LIMIT %s OFFSET %s"
                cursor.execute(sql, (batch_size, offset))
                return cursor.fetchall()
            except Error as e:
                print(f"Error al obtener huellas: {e}")
                return []
    
    
    def insertar_evento(self, idregistro, tipo_evento, hora):
        """Inserta un nuevo evento en la tabla eventos."""
        
        try:
            query = "INSERT INTO eventos (idregistro, tipo_evento, hora) VALUES (%s, %s, %s)"
            valores = (idregistro, tipo_evento, hora)
            self.cursor.execute(query, valores)
            self.conexion.commit()  # Confirmamos la transacción
            correcto = True
        except mysql.connector.Error as e:
            print(f"Error al insertar el evento: {e}")
            correcto = False
        return correcto
    
    def modificar_evento(self, idregistro, tipo_evento, hora):
        """Modifica la hora de un evento existente donde coincidan idregistro y tipo_evento."""
        try:
            query = "UPDATE eventos SET hora = %s WHERE idregistro = %s AND tipo_evento = %s"
            valores = (hora, idregistro, tipo_evento)
            self.cursor.execute(query, valores)
            self.conexion.commit()  # Confirmamos la transacción
            if self.cursor.rowcount > 0:
                 correcto = True
            else:
               correcto = False
        except mysql.connector.Error as e:
            print(f"Error al modificar el evento: {e}")
            correcto = False

        return correcto
    
    def cerrar(self):
        """Cierra la conexión"""
        if self.conexion:
            self.cursor.close()
            self.conexion.close()
