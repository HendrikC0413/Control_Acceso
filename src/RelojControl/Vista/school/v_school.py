from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame,QMessageBox
)
from PySide6.QtCore import Qt
import sys

from Control.C_School import C_Escuela

class EstablecimientoForm(QDialog):
    """
    Clase encargada de gestionar la ventana para realizar operaciones con un establecimiento.
    Permite agregar, modificar o eliminar un establecimiento según la opción seleccionada.
    """
    def __init__(self, opcion):
        """
        Constructor de la clase.
        Inicializa la interfaz con el formulario y los botones según la opción seleccionada.
        
        Parámetros:
        - opcion: Define la operación que se va a realizar (1: Agregar, 2: Modificar, 3: Eliminar).
        """
        super().__init__()
        
        self.OPCION = opcion

        # Configurar título según opción
        if opcion == 1:
            self.setWindowTitle("Ingrese Establecimiento")
        elif opcion == 2:
            self.setWindowTitle("Modificar Establecimiento")
        elif opcion == 3:
            self.setWindowTitle("Eliminar Establecimiento")
        
        self.setFixedSize(500, 300)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Título
        title_label = QLabel(self.windowTitle())
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Formulario con borde
        form_container = QFrame()
        #form_container.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 20px;")
        form_layout = QVBoxLayout()
        
        form_fields = QFormLayout()
        
        # Campo RBD
        self.rbd_input = QLineEdit()
        self.rbd_input.setPlaceholderText("Ingrese RBD")
        
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setVisible(opcion in [2, 3])
        
        # Bloquear RBD después de buscar en opciones 2 y 3
    
        self.buscar_btn.clicked.connect(self.BuscarEstablecimiento)
        
        rbd_layout = QHBoxLayout()
        rbd_layout.addWidget(self.rbd_input)
        rbd_layout.addWidget(self.buscar_btn)
        form_fields.addRow(QLabel("RBD:"), rbd_layout)
        
        # Campo Nombre del establecimiento
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese el nombre del establecimiento")
        form_fields.addRow("Nombre del establecimiento:", self.nombre_input)
        
        form_layout.addLayout(form_fields)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.clicked.connect(self.reset_fields)
        
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.CRUD_Establecimiento)
        
        self.guardar_btn.setStyleSheet("background-color: green; color: white;")
        self.cancelar_btn.setStyleSheet("background-color: lightblue; color: black;")

        if opcion == 3:
            self.guardar_btn.setStyleSheet("background-color: red; color: white;")
            self.cancelar_btn.setStyleSheet("background-color: lightblue; color: black;")
            self.guardar_btn.setText("Eliminar")
        
        btn_layout.addWidget(self.cancelar_btn)
        btn_layout.addWidget(self.guardar_btn)
        
        form_layout.addSpacing(10)
        form_layout.addLayout(btn_layout)
        
        form_container.setLayout(form_layout)
        main_layout.addWidget(form_container)
        
        self.setLayout(main_layout)
    
    def BuscarEstablecimiento(self):
        """
        Realiza una búsqueda del establecimiento usando el RBD ingresado.
        Si se encuentra, llena el campo de nombre con el resultado. 
        Si no, muestra un mensaje informando que no se encontró el establecimiento.
        """
        rbd = self.rbd_input.text()
        Control_Escuela = C_Escuela()
        Nombre = Control_Escuela.buscar_escuela(rbd)
        if Nombre != "":
            self.nombre_input.setText(Nombre)
        else:
                self.mostrar_mensaje_info(self,"No encontrado")
        self.rbd_input.setDisabled(True)

    def CRUD_Establecimiento(self):
        """
        Realiza la operación correspondiente (Agregar, Modificar o Eliminar) según la opción seleccionada.
        Muestra un mensaje indicando si la operación fue exitosa o si hubo un error.
        """
        rbd = self.rbd_input.text()
        Control_Escuela = C_Escuela()
        correcto = False
        texto = ""
        if self.OPCION== 1:
            nombre = self.nombre_input.text()
            correcto = Control_Escuela.agregar_escuela(rbd=rbd,nombre=nombre)
            texto = "Agregado correctamente"
        elif self.OPCION==2:
            nombre = self.nombre_input.text()
            correcto = Control_Escuela.modificar_escuela(rbd=rbd,nombre=nombre)
            texto = "Modificado correctamente"
        else:
            correcto = Control_Escuela.eliminar_escuela(rbd=rbd)
            texto = "Dado de baja correctamente"

        if correcto:
            self.mostrar_mensaje_info(texto)
        else:
            self.mostrar_mensaje_info("No se pudo realizar la operación")
    
    def reset_fields(self):
        """Restablecer los campos y desbloquear el input de RBD."""
        self.rbd_input.setDisabled(False)
        self.rbd_input.clear()
        self.nombre_input.clear()

    def mostrar_mensaje_info(self, mensaje):
        """
        Muestra un mensaje de información en la interfaz gráfica.
        
        Parámetros:
        - mensaje: El texto que se mostrará en el mensaje de información.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Información")
        msg.exec()