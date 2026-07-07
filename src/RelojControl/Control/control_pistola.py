import threading
from Modelo.pistola import Lectora_codigo_barras
from PySide6.QtWidgets import QMessageBox
from Control.C_Registro import C_Registro


class ControladorLector:
    """
    Controlador encargado de gestionar la lectura de códigos de barras y el registro de asistencia.
    Conecta la lectora de códigos de barras con los procesos de registro de asistencia.
    """ 
    def __init__(self):
        """
        Inicializa el controlador, creando la instancia de la lectora de códigos de barras y 
        conectando el evento de lectura completada a la función Realizar_Registro.
        """
        self.lectora = Lectora_codigo_barras(timeout=1)
        self.lectora.lectura_completada.connect(self.Realizar_Registro)

    def iniciar_lectura(self):
        """
        Inicia la lectura de códigos de barras si no está activamente en proceso de lectura.
        
        No recibe parámetros. Inicia un hilo para ejecutar la lectura del código de barras.
        """
        if not self.lectora.leer_activo:  # Si no está leyendo, inicia la lectura
            print("Esperando código de barras...")
            
            # Ejecutar la lectura en un hilo separado
            threading.Thread(target=self.lectora.leer_codigo_barras, daemon=True).start()

    def detener_lectura(self):
        """
        Detiene la lectura de códigos de barras si está activamente leyendo.
        
        No recibe parámetros. Detiene el proceso de lectura de la lectora.
        """
        if self.lectora.leer_activo:
            self.lectora.detener_lectura()  # Detenemos el listener
            print("Lectura detenida.")
    
    def set_tipo_marcacion(self, tipo):
        """
        Actualiza el tipo de marcación desde la interfaz de usuario.

        Parámetros:
        tipo (str): El tipo de marcación que se debe establecer (por ejemplo, asistencia, salida, etc.).
        """
        self.lectora.set_tipo_marcacion(tipo)

    def Realizar_Registro(self, codigo, tipo_marcacion):
        """
        Registra la asistencia de un usuario después de haber leído un código de barras.

        Parámetros:
        codigo (str): El código de barras leído, utilizado para identificar al usuario.
        tipo_marcacion (str): El tipo de marcación de la asistencia (por ejemplo, entrada, salida).

        Muestra un mensaje indicando si el registro fue exitoso o fallido.
        """
        Registro = C_Registro()
        if Registro.Registrar_Asistencia(codigo, tipo_marcacion)==1:
            QMessageBox.information(None, "Éxito", "PERFECTO, ASISTENCIA MARCADA... ¡BIENVENIDO!")
        else:
            QMessageBox.warning(None, "Error", "No se pudo registrar su asistencia")
