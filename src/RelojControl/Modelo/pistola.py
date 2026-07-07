import threading
from pynput import keyboard
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal

from Control.C_Registro import C_Registro

class Lectora_codigo_barras(QObject):

    """
    Clase que maneja la lectura de códigos de barras a través de un lector y emite señales 
    cuando la lectura se ha completado. También gestiona el tipo de marcación y el temporizador 
    para finalizar la lectura después de un tiempo de inactividad.
    """

    lectura_completada = Signal(str, int)
    def __init__(self, timeout=2):
        """
        Constructor de la clase Lectora_codigo_barras.
        Inicializa las variables necesarias para manejar la lectura del código de barras.
        """
        super().__init__()
        self.codigo_leido = ""
        self.timeout = timeout
        self.timer = None
        self.listener = None  # Para poder detener el listener
        self.leer_activo = False  # Para saber si la lectura está activa
        self.tipo_marcacion = 1

    def reset_timer(self):
        """ 
        Resetea el temporizador cada vez que se recibe un nuevo carácter.
        Cancela el temporizador anterior y crea uno nuevo que finalizará la lectura si no se recibe
        un nuevo carácter en el tiempo establecido.
        """
        if self.timer:
            self.timer.cancel()  # Cancela el temporizador anterior si lo hay
        self.timer = threading.Timer(self.timeout, self.finalizar_lectura)
        self.timer.start()  # Inicia el temporizador de nuevo

    def set_tipo_marcacion(self, tipo):
        """ 
        Permite actualizar el tipo de marcación desde la UI.
        Este método establece el tipo de marcación que se utilizará al finalizar la lectura del código.
        """
        self.tipo_marcacion = tipo

    def finalizar_lectura(self):
        """ 
        Método que se llama cuando el tiempo de espera se agota, es decir, cuando no se recibe un nuevo
        carácter en el tiempo configurado por el temporizador.
        Se emite una señal con el código leído y el tipo de marcación.
        """
        print(f"Registro: {self.codigo_leido} | Tipo de Marcación: {self.tipo_marcacion}")
        
        self.lectura_completada.emit(self.codigo_leido, self.tipo_marcacion)
        self.codigo_leido = ""
        
        self.codigo_leido = ""  # Resetea el código leído
        print("Lectura finalizada, esperando nuevo código...")

    def detener_lectura(self):
        """ 
        Detiene el listener de teclado manualmente, lo que interrumpe el proceso de lectura.
        """
        if self.listener:
            self.listener.stop()  # Detiene el listener
            print("Lectura detenida.")
        self.leer_activo = False  # Marca que la lectura ha sido detenida

    def on_press(self, tecla):
        """ 
        Captura la tecla presionada y agrega el carácter al código leído.
        Si se presiona la tecla Enter, finaliza la lectura.
        """
        try:
            if tecla == keyboard.Key.enter:
                # Si se presiona Enter, se finaliza la lectura
                self.finalizar_lectura()
                return False  # Detiene el listener de teclas
            else:
                # Si la tecla es un carácter normal, lo añadimos al código leído
                self.codigo_leido += tecla.char
                self.reset_timer()  # Resetea el temporizador al recibir un nuevo carácter
        except AttributeError:
            pass  # Ignora teclas especiales que no tengan 'char'

    def leer_codigo_barras(self):
        """ 
        Lee el dato ingresado por la pistola de códigos de barras y lo muestra en pantalla.
        Inicia el listener de teclado para capturar las teclas presionadas.
        """
        print("\nEscanea el código de barras con la pistola:")
        self.leer_activo = True  # Marca que la lectura está activa
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener  # Guarda el listener para poder detenerlo más tarde
            listener.join()  # Bloquea hasta que el código de barras se lea completamente
