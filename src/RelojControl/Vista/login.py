from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame
)
from PySide6.QtCore import Qt

from Control.C_Registro import C_Registro
from Control.C_usuario import C_user

class LoginForm(QDialog):

    """
    Clase encargada de gestionar el formulario de inicio de sesión.
    Permite al usuario ingresar su RUN y clave para autenticarse.
    Los datos ingresados se validan y si son correctos, la ventana se cierra.
    """

    def __init__(self,rbd,tipo_entrada):

        """
        Constructor de la clase.
        Inicializa la interfaz de inicio de sesión con los campos para ingresar RUN y clave,
        y el botón para intentar ingresar.
        
        Parámetros:
        - rbd: Identificador único de la institución o usuario.
        - tipo_entrada: Tipo de acceso que se va a realizar.
        
        """

        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.setFixedSize(400, 250)
        
        self.RBD = rbd
        self.TIPO_ENTRADA = tipo_entrada

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Título
        title_label = QLabel("Bienvenido")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28.8px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Formulario con borde
        form_container = QFrame()
        #form_container.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 20px;")
        form_layout = QVBoxLayout()
        
        form_fields = QFormLayout()
        
        # Campos del formulario
        self.run_input = QLineEdit()
        self.run_input.setPlaceholderText("Ingrese su RUN")
        self.run_input.setStyleSheet("font-size: 14.4px; padding: 6px;")
        
        self.clave_input = QLineEdit()
        self.clave_input.setPlaceholderText("Ingrese su clave")
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_input.setStyleSheet("font-size: 14.4px; padding: 6px;")
        
        form_fields.addRow(QLabel("RUN:", self), self.run_input)
        form_fields.addRow(QLabel("Clave:", self), self.clave_input)
        
        form_layout.addLayout(form_fields)
        
        # Botón de ingreso
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.ingresar_btn = QPushButton("Ingresar")
        self.ingresar_btn.setStyleSheet("background-color: #6A8CE0; color: white; font-size: 14.4px; padding: 6px;")
        self.ingresar_btn.clicked.connect(self.Marcaje)

        btn_layout.addWidget(self.ingresar_btn)
        
        form_layout.addSpacing(10)
        form_layout.addLayout(btn_layout)
        
        form_container.setLayout(form_layout)
        main_layout.addWidget(form_container)
        
        self.setLayout(main_layout)

    def Marcaje(self):
        """
        Obtiene los datos de los inputs del formulario y los valida.
        Si el usuario y clave son correctos, cierra la ventana de inicio de sesión..
        """
        # Obtener los valores de los campos de entrada
        run = self.run_input.text()
        clave = self.clave_input.text()
        Registro = C_Registro()
        Revisar = C_user()
        if Revisar.verificar_formato_run(run) == False:
                run = Revisar.formatear_run(run)

        if Registro.Verificar_usuario_clave(run,clave,self.RBD,self.TIPO_ENTRADA)==True:
            self.close()  # Cierra la ventana