from Modelo.registro import Registro
from  Modelo.DatabaseConnection import ConexionMySQL
from PySide6.QtWidgets import QMessageBox
from datetime import datetime

class C_Registro:
    """
    Clase encargada de gestionar los registros de asistencia y reportes de usuarios.
    Proporciona métodos para generar reportes individuales y generales, verificar usuarios,
    y registrar asistencias en la base de datos.
    """
    def __init__(self):
        self.id = None

    def Reporte_Usuario(self, rbd, run, fecha_ini, fecha_fin, mes, opcion):
            """
            Genera un reporte individual de asistencia para un usuario específico.

            Parámetros:
            - rbd (str): Identificador del establecimiento.
            - run (str): RUN del usuario.
            - fecha_ini (str): Fecha de inicio del reporte.
            - fecha_fin (str): Fecha de fin del reporte.
            - mes (str): Mes del reporte.
            - opcion (int): Opción para filtrar el reporte.

            Retorna:
            - list: Lista de datos con la información de asistencia del usuario.
            """
            db = ConexionMySQL()
            idtajeta = self.Obtener_tarjeta(run, rbd)
            resultado_proc = db.ejecutar_procedimiento("obtener_reporte_individual", (opcion, fecha_ini, fecha_fin, mes, rbd, idtajeta))
            # Lista para almacenar los datos
            datos = []

            if resultado_proc:
                for fila in resultado_proc:
                    for entrada in fila:  # Asegurarnos de que estamos iterando correctamente sobre las filas
                        if isinstance(entrada, dict):
                            datos.append([
                                entrada.get("run", ""),  
                                entrada.get("rbd", ""),  
                                entrada.get("fecha").strftime("%Y-%m-%d") if entrada.get("fecha") else "",  
                                str(entrada.get("Hora_entrada", "")) if entrada.get("Hora_entrada") else "",  
                                str(entrada.get("Hora_salida", "")) if entrada.get("Hora_salida") else "",  
                                str(entrada.get("Hora_salida_colacion", "")) if entrada.get("Hora_salida_colacion") else "",  
                                str(entrada.get("Hora_entrada_colacion", "")) if entrada.get("Hora_entrada_colacion") else "",  
                                entrada.get("Completo", "")  
                            ])
                        else:
                            print(f"Error: Se esperaba un diccionario, pero se recibió: {type(entrada)}")
            else:
                print("⚠️ No se pudo generar el reporte")
                
            db.cerrar()
            return datos

    def Reporte_General(self, rbd, fecha_ini, fecha_fin, mes, year, opcion):
            """
            Genera un reporte general de asistencia para todos los usuarios de un establecimiento.

            Parámetros:
            - rbd (str): Identificador del establecimiento.
            - fecha_ini (str): Fecha de inicio del reporte.
            - fecha_fin (str): Fecha de fin del reporte.
            - mes (str): Mes del reporte.
            - year (str): Año del reporte.
            - opcion (int): Opción para filtrar el reporte.

            Retorna:
            - list: Lista de datos con la información de asistencia general.
            """
            db = ConexionMySQL()
            resultado_proc = db.ejecutar_procedimiento("obtener_asistencia_completa", (opcion, fecha_ini, fecha_fin, mes, year, rbd))
            # Lista para almacenar los datos
            datos = []

            if resultado_proc:
                #print(f"📌 Resultado del procedimiento: {resultado_proc}")  # Imprimir para depuración
                for fila in resultado_proc:
                    for entrada in fila:  # Asegurarnos de que estamos iterando correctamente sobre las filas
                        if isinstance(entrada, dict):
                            datos.append([
                                entrada.get("run", ""),  
                                entrada.get("nombre", ""),
                                entrada.get("apellido_1", ""),
                                entrada.get("Dias_Asistidos", ""),   
                                entrada.get("Dias_Completos", "")  
                            ])
                        else:
                            print(f"Error: Se esperaba un diccionario, pero se recibió: {type(entrada)}")
            else:
                print("⚠️ No se pudo generar el reporte")
                
            db.cerrar()
            return datos
    
    def Obtener_tarjeta(self,run,rbd):
        """
        Obtiene el ID de la tarjeta asociada a un usuario y establecimiento.

        Parámetros:
        - run (str): RUN del usuario.
        - rbd (str): Identificador del establecimiento.

        Retorna:
        - str: ID de la tarjeta asociada al usuario.
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
    
    def Verificar_usuario_clave(self,run,clave,rbd,tipo_E):
        """
        Verifica las credenciales de un usuario y registra su asistencia si son válidas.

        Parámetros:
        - run (str): RUN del usuario.
        - clave (str): Clave del usuario.
        - rbd (str): Identificador del establecimiento.
        - tipo_E (str): Tipo de evento a registrar.

        Retorna:
        - bool: True si la asistencia se registró correctamente, False en caso contrario.
        """
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("obtener_dato_por_run",(run,))
        Id_personal =""
        completado = False
        # Mostramos los datos obtenidos
        if resultado_proc:   
            fila = resultado_proc[0]
            Id_personal = fila[0]["clave"] 
        else:
            print("No se encontró el usuario.")
            QMessageBox.warning(None, "Error", "No se encontró el usuario.")
        db.cerrar()
      
        if Id_personal != clave:
            QMessageBox.warning(None, "Error", "Clave erronea intente nuevamente")
        else:
            idTarjeta = self.Obtener_tarjeta(run,rbd)
            if self.Registrar_Asistencia(idTarjeta,tipo_E)==1:
                msgBox = QMessageBox()
                msgBox.setText("PERFECTO, ASISTENCIA MARCADA... ¡BIENVENIDO¡")
                msgBox.exec()
                completado = True
            else:
                QMessageBox.warning(None, "Error", "No se pudo registrar su asistencia")
        return completado
    
    def Registrar_Asistencia(self, idTarjeta, tipo_E):
        """
        Registra la asistencia de un usuario en la base de datos.

        Parámetros:
        - idTarjeta (str): ID de la tarjeta del usuario.
        - tipo_E (str): Tipo de evento a registrar.

        Retorna:
        - bool: True si el registro fue exitoso, False en caso contrario.
        """
        completado = 0
        # Obtener fecha y hora actuales
        now = datetime.now()

        # Formatear la fecha y la hora
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento_Registrar_Evento("registrar_evento",(fecha, idTarjeta, tipo_E, hora))

        if resultado_proc == 1:
            print("¡Registro insertado correctamente!")
            completado = 1
        elif resultado_proc == 2:
            completado = 2
            #QMessageBox.warning(None, "Error", "El evento ya había sido registrado")
            print("El evento ya había sido registrado")
        else:
            print("Ocurrió un problema al registrar el evento")
            #QMessageBox.warning(None, "Error", "Ocurrió un problema al registrar el evento")

        db.cerrar()

        return completado