from pyzkfp import ZKFP2
import time
from PIL import Image, ImageEnhance
import os
from datetime import datetime
from threading import Thread
import sys    
from PySide6.QtWidgets import QMessageBox
from Modelo.DatabaseConnection import ConexionMySQL
from Control.C_Registro import C_Registro

class FingerprintScanner:

    """
    Clase que maneja el registro y la lectura de huellas dactilares a través de un lector biométrico.
    Proporciona métodos para capturar, verificar y almacenar huellas.
    """
    
    def __init__(self):
        """
        Constructor de la clase FingerprintScanner. Inicializa el lector de huellas 
        y establece los valores predeterminados de la clase.
        """
        self.zkfp2 = ZKFP2()
        self.templates = []
        self.register = False
        self.rute = ""
        self.Bit = bytearray()
        self.inicializado = False
        self.initialize_zkfp2()
        self.RBD = ""
        self.tipo_marcacion = 1
       


    def initialize_zkfp2(self):
        """
        Inicializa el lector de huellas.
        """
        try:
            self.zkfp2.Init()
            device_count = self.zkfp2.GetDeviceCount()
            self.zkfp2.Light("green",1.0)
            if device_count == 0:
                raise RuntimeError("No se encontraron dispositivos de huellas.")
            self.zkfp2.OpenDevice(0)
            print("Lector de huellas inicializado correctamente.")
            self.inicializado = True
        except Exception as e:
            print(f"Error al inicializar el lector de huellas: {e}")
            self.inicializado = False
            #exit(1)
    
    """
        Guarda una imagen de huella dactilar utilizando la biblioteca Pillow.
        
        :param image_data: Los datos de la imagen en formato bytes.
        :param width: El ancho de la imagen (por defecto, 256).
        :param height: La altura de la imagen (por defecto, 288).
        :param directory: La ruta donde se guardarán las imágenes (por defecto, 'fingerprint_images').
        :return: La ruta completa del archivo guardado.
    """
    def save_fingerprint_image_locally(self, image_data, width=275, height=375, directory="fingerprint_images"):
            """
            Guarda una imagen de huella localmente para inspección (opcional).
            """
            if not os.path.exists(directory):
                os.makedirs(directory)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"fingerprint_{timestamp}.png"
            file_path = os.path.join(directory, file_name)

            try:
                image = Image.frombytes('L', (width, height), image_data)

                # Mejorar el contraste y la nitidez de la imagen
                enhancer = ImageEnhance.Contrast(image)
                contrast = enhancer.enhance(2.0)
                enhancer = ImageEnhance.Sharpness(contrast)
                enhanced_image = enhancer.enhance(1.5)

                enhanced_image.save(file_path, format="PNG")
                print(f"Imagen de la huella almacenada localmente en: {file_path}")
                self.rute = file_path
            except Exception as e:
                print(f"Error al guardar la imagen localmente: {e}") 


    def capture_handler(self, capture):
        """
        Procesa la captura de huellas para registro.
        """
        try:
            tmp, img = capture
            if self.register:
                self.process_fingerprint(tmp, img)
        except Exception as e:
            print(f"Error durante la captura: {e}")

    def read_handler(self, capture):
        """
        Procesa la captura de huellas para lectura.
        """
        try:
            tmp, img = capture
            print("Huella detectada. Procesando...")
            run = self.verify_fingerprint (capture)
            C_regis = C_Registro()
            idTarjeta = C_regis.Obtener_tarjeta(run,self.RBD)
            logrado = C_regis.Registrar_Asistencia(idTarjeta,self.tipo_marcacion)
            if logrado==1:
                print("logrado")
                self.mostrar_mensaje_info("PERFECTO, ASISTENCIA MARCADA... ¡BIENVENIDO¡")
            elif logrado==2:
                print("NO logrado")
                self.mostrar_mensaje_info("Advertencia, Se ha marcado ya esa opción con anterioridad")
            else:
                QMessageBox.warning(None, "Error", "No se pudo registrar su asistencia")
            # Aquí puedes agregar lógica para comparar la huella con una base de datos, etc.
        except Exception as e:
            print(f"Error durante la lectura: {e}")

    def process_fingerprint(self, tmp, img):
        """
        Procesa una huella dactilar y la guarda si es necesario.
        """
        error_count =0
        if len(self.templates) < 3:
            if not self.templates or self.zkfp2.DBMatch(self.templates[-1], tmp) > 0:
                self.templates.append(tmp)
                error_count = 0  # Reiniciar el contador de errores al detectar la misma huella
                print(f"Huella {len(self.templates)} capturada correctamente.")
                self.save_fingerprint_image_locally(img)

                if len(self.templates) < 3:
                    self.mostrar_mensaje_info("Ponga su dedo nuevamente.")

                if len(self.templates) == 3:
                    self.mostrar_mensaje_info("Procesando...")
                    self.save_combined_fingerprint()
            else:
                error_count += 1
                self.mostrar_mensaje_info(f"Dedo diferente detectado. Intento {error_count}/5. Usa el mismo dedo para continuar.")

                if error_count >= 5:
                    print("Se detectaron 5 intentos fallidos. Reiniciando proceso...")
                    self.templates.clear()
                    error_count = 0
                    self.mostrar_mensaje_info("Dedo incorrecto detectado demasiadas veces. Vuelva a comenzar.")
    
    def save_combined_fingerprint(self):
        """
        Combina las huellas capturadas y las guarda en la base de datos.
        """
        try:
            if len(self.templates) == 3:
                regTemp, regTempLen = self.zkfp2.DBMerge(*self.templates)
                huella_bytearray2 = bytearray(regTemp)
                print(f"Modelo biométrico capturado: {huella_bytearray2}")
                #if self.db_handler:
                #    self.db_handler.insert_huella(huella_bytearray2)
                print("Modelo biométrico combinado almacenado en la base de datos.")
                self.mostrar_mensaje_info("Huella capturada correctamente")
                self.Bit = huella_bytearray2
                self.templates.clear()
                self.register = False
        except Exception as e:
             self.mostrar_mensaje_info("A ocurrido un error al reunir sus huellas."+str(e))

    def start_registration(self):
        """
        Inicia el proceso de registro de huellas.
        """
        self.register = True
        self.mostrar_mensaje_info("Ahora por favor ponga su dedo en el lector")
        

    def start_reading(self):
        """
        Inicia el proceso de lectura de huellas.
        """
        self.register = False
        self.mostrar_mensaje_info("Modo de lectura activado. Coloca tu dedo en el lector...")

    def listen_to_fingerprints(self):
        """
        Inicia la escucha para capturar huellas.
        """
        try:
            while True:
                capture = self.zkfp2.AcquireFingerprint()
                if capture:
                    if self.register:
                        Thread(target=self.capture_handler, args=(capture,), daemon=True).start()
                    else:
                        Thread(target=self.read_handler, args=(capture,), daemon=True).start()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        """
        Cierra todos los recursos.
        """
        print("Cerrando el sistema...")
        self.zkfp2.CloseDevice()


    def mostrar_mensaje_info(self, mensaje):
        """
        Muestra un mensaje de información en la interfaz gráfica.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Información")
        msg.exec()
    
    def GetRute (self):
        """
        Obtiene la ruta de la imagen de huella capturada.
        """
        return self.rute
    
    def getHuella(self):
        """
        Obtiene el modelo biométrico de la huella capturada.
        """
        return self.Bit

    def getInicializado(self):
        """
        Verifica si el lector de huellas ha sido inicializado correctamente.
        """
        return self.inicializado
    
    def setRBD(self,rbd):
        """
        Establece el RBD para la verificación.
        """
        self.RBD = rbd
    
    def setMarcacion(self,tipo):
        """
        Establece el tipo de marcación para el registro de asistencia.
        """
        self.tipo_marcacion = tipo
    
    def verify_fingerprint(self, capture):
        """
        Compara una huella tomada en el momento con las almacenadas en la base de datos y devuelve el nombre de la persona.
        """
        #print("Coloca tu dedo en el lector para verificar...")
        RUT = None
        try:
            db = ConexionMySQL()
            if capture:
                tmp, _ = capture

                # Convertir el modelo biométrico a bytearray
                huella_bytearray = bytearray(tmp)
                print(f"Modelo biométrico capturado: {huella_bytearray}")

                # Configuración para la consulta incremental
                batch_size = 10
                offset = 0

                while True:
                    # Recuperar un lote de modelos biométricos junto con nombres
                    results = db.fetch_biometric_models_batch(batch_size, offset)

                    if not results:
                        # Si no hay más resultados, terminar la búsqueda
                        print("Huella no reconocida. Acceso denegado.")
                        break

                    for row in results:
                        stored_template, run = row  # Ahora se obtiene también el nombre
                        if stored_template != None:
                            if self.zkfp2.DBMatch(stored_template, huella_bytearray) > 0:
                                print(f"Huella detectada. Acceso concedido a {run}.")
                                RUT = run
                                return RUT

                    # Incrementar el desplazamiento para el siguiente lote
                    offset += batch_size
            else:
                print("No se pudo capturar la huella. Inténtalo de nuevo.")
            db.cerrar()
        except Exception as e:
            print(f"Error durante la verificación: {e}")
