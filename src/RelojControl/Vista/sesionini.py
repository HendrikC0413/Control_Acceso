# sesionini.py
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal

from Control.C_usuario import C_user

class IniciarSesion(QDialog):
    """
    Clase encargada de gestionar la ventana de inicio de sesión.
    Permite al usuario ingresar su RUT y clave para autenticar su acceso.
    Emite una señal cuando el inicio de sesión es exitoso, pasando el rol del usuario.
    """

    """
    Señal que se emite cuando el inicio de sesión es exitoso.
    Envía el rol del usuario (Administrador o Usuario).
    """
    login_exitoso = Signal(int)  
    def __init__(self):
        """
        Constructor de la clase.
        Inicializa los elementos de la interfaz gráfica, como los campos de RUT y clave,
        y el botón de entrada.
        """
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        layout = QVBoxLayout()
        
        # Campo de entrada para RUT
        self.rut_label = QLabel("RUT:")
        self.rut_input = QLineEdit()
        layout.addWidget(self.rut_label)
        layout.addWidget(self.rut_input)
        
        # Campo de entrada para Clave
        self.clave_label = QLabel("Clave:")
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)  # Ocultar la clave con asteriscos
        layout.addWidget(self.clave_label)
        layout.addWidget(self.clave_input)
        
        # Botón de Entrar
        self.entrar_button = QPushButton("Entrar")
        self.entrar_button.clicked.connect(self.show_alert)
        layout.addWidget(self.entrar_button)
        
        self.setLayout(layout)
    
    def show_alert(self):
        """
        Método que valida el RUT y la clave ingresados por el usuario.
        Si son correctos, emite la señal de inicio de sesión exitoso con el rol del usuario.
        Si son incorrectos, muestra un mensaje de alerta indicando el error.
    
        """
        control_usuario = C_user()
        run = self.rut_input.text()
        if control_usuario.verificar_formato_run(run) == False:
            run = control_usuario.formatear_run(run)
        clave = self.clave_input.text()

        valor = control_usuario.verificar_usuario(run,clave)
        print(valor)
        if valor:
            self.login_exitoso.emit(int(valor))  # Solo convierte si tiene datos válidos
        else:
           self.mostrar_mensaje("RUN o CLAVE INCORRECTOS INTENTE DENUEVO")
        self.accept()  # Cierra la ventana y retorna resultado a la principal

    def mostrar_mensaje(self,mensaje):
        """
        Muestra un cuadro de diálogo con un mensaje de información.

        Parámetros:
        mensaje (str): El mensaje que se mostrará en la ventana emergente.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Mensaje")
        msg.exec()