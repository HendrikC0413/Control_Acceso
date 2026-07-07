
import sys
from PySide6.QtCore import QTimer, Signal,QObject
from PySide6.QtWidgets import  QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from Modelo.huella import FingerprintScanner

class FingerprintManager():
    """
    Clase encargada de gestionar el escaneo y manejo de huellas dactilares.
    Controla el proceso de escaneo, captura y lectura de huellas mediante un escáner de huellas dactilares.
    Además, permite gestionar las opciones de registro y verificación de huellas.
    """
    image_captured = Signal(str)
    def __init__(self):
        """
        Inicializa el gestor de huellas, configurando el escáner de huellas, el temporizador
        y los valores predeterminados para las opciones de escaneo y el estado de la huella.
        
        También se configura la señal para verificar el escáner de huellas en intervalos regulares.
        """
        self.fingerprint_scanner = FingerprintScanner()
        self.scanning_active = False
        self.opcion = 0  # Establecemos la opción al inicializar la clase
        self.ruta = ""
        self.Huella = bytearray()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_fingerprint_scanner)

    def start_fingerprint_scanning(self):
        """
        Inicia el proceso de lectura de huellas.
        
        Si el escaneo no está activo, comienza la lectura y se activa el temporizador
        para comprobar el escáner cada 100 ms.
        """
        if not self.scanning_active:
            print("Iniciando el escaneo de huellas...")
            self.scanning_active = True
            self.timer.start(100)  # Verificar cada 100 ms

    def stop_fingerprint_scanning(self):
        """
        Detiene el proceso de lectura de huellas.
        
        Si el escaneo está activo, se detiene el temporizador y el escáner.
        """
        if self.scanning_active:
            print("Deteniendo el escaneo de huellas...")
            self.scanning_active = False
            self.timer.stop()

    def check_fingerprint_scanner(self):
        """
        Verifica si se ha capturado una huella y maneja el proceso según la opción seleccionada.
        
        Si se detecta una huella, se maneja según la opción de registro o lectura establecida.
        """
        if self.scanning_active:
            capture = self.fingerprint_scanner.zkfp2.AcquireFingerprint()
            if capture:
                # Verificar la opción seleccionada y llamar al manejador correspondiente
                if self.opcion == 1:
                    # Llamar a capture_handler si la opción es 1
                    #print("Estamos AQUI")
                    self.fingerprint_scanner.start_registration()
                    self.fingerprint_scanner.capture_handler(capture)
                    self.Huella = self.fingerprint_scanner.getHuella()
                elif self.opcion == 2:
                    # Llamar a read_handler si la opción es 2
                    self.fingerprint_scanner.read_handler(capture)

    def get_image(self):
        """
        Obtiene la imagen asociada al escaneo de huella.
        
        Actualmente, esta función retorna False ya que no se está capturando una imagen explícita.
        """
        return False
    
    def set_option(self, opcion):
        """
        Establece la opción de operación para el escaneo de huellas.
        
        Parámetros:
        opcion (int): La opción seleccionada (1 para registro, 2 para lectura).
        """
        self.opcion = opcion
    
    @property
    def get_huella(self):
        """
        Obtiene la huella capturada.
        
        Retorna la huella actual almacenada como un objeto bytearray.
        """
        return self.Huella

    def get_inicializado(self):
        """
        Verifica si el escáner de huellas está inicializado y listo para usar.
        
        Retorna el estado de inicialización del escáner.
        """
        return self.fingerprint_scanner.getInicializado()
    
    def setRBD(self,rbd):
        """
        Establece el RBD (registro de establecimiento) para el escáner.
        
        Parámetros:
        rbd (str): El RBD asociado al escáner.
        """
        self.fingerprint_scanner.setRBD(rbd)

    def setMarcacion(self,tipo):
        """
        Establece el tipo de marcación para el escáner.
        
        Parámetros:
        tipo (str): El tipo de marcación (por ejemplo, asistencia, verificación).
        """
        self.fingerprint_scanner.setMarcacion(tipo)    
    def shutdown(self):
        """
            Cierra todos los recursos y detiene el escaneo de huellas.
            
            Llama al método stop_fingerprint_scanning para detener el escaneo y cierra el escáner.
        """
        self.stop_fingerprint_scanning()
        self.fingerprint_scanner.shutdown()