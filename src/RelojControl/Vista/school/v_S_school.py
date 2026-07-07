import sys
import pickle
from PySide6.QtWidgets import QApplication, QDialog,QMessageBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal

class EstablecerEstablecimiento(QDialog):
    """
    Clase encargada de gestionar la ventana para establecer el RBD de un establecimiento.
    Permite ingresar un RBD y almacenarlo en un archivo binario.
    Emite una señal con el RBD establecido cuando se guarda correctamente.
    """
    establecido = Signal(str)
    """
    Señal que se emite cuando el RBD ha sido establecido correctamente.
    Envía el RBD ingresado.
    """
    def __init__(self):
        """
        Constructor de la clase.
        Inicializa la interfaz con un campo para ingresar el RBD y un botón para establecerlo.
        """
        super().__init__()
        
        self.setWindowTitle("Establecer Establecimiento")
        self.setGeometry(100, 100, 400, 200)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título
        self.title_label = QLabel("Establecer Establecimiento")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Formulario
        form_layout = QFormLayout()

        # Campo RBD
        self.rbd_input = QLineEdit()
        self.rbd_input.setPlaceholderText("Ingrese el RBD")
        form_layout.addRow("RBD:", self.rbd_input)
        
        # Botón Establecer
        self.btn_establecer = QPushButton("Establecer")
        self.btn_establecer.clicked.connect(self.mostrar_mensaje)
        
        # Layout para el botón
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_establecer, alignment=Qt.AlignRight)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        # Establecer el layout principal
        self.setLayout(layout)
    
    def mostrar_mensaje(self):
        """
        Valida el RBD ingresado, lo guarda en un archivo binario y muestra un mensaje de éxito o error.
        Emite una señal con el RBD establecido si la operación es exitosa.
        """
        rbd = self.rbd_input.text()
        mensaje = ""
        if rbd:
            # Datos a guardar (la RBD de la escuela)
            data_to_save = {"RBD": rbd}
            # Guardar datos en un archivo binario
            try:
                with open("data.dat", "wb") as bin_file:
                    pickle.dump(data_to_save, bin_file)
                print("Establecido exitosamente.")
                mensaje = "Se ha establecido exitosamente"
                self.establecido.emit(rbd)
            except IOError as e:
                print(f"Error al guardar los datos: {e}")
                mensaje = "A ocurrido un error"
        else:
            mensaje = "Por favor ingresa un RBD"
        
        reply = QMessageBox.information(self, "Mensaje", mensaje , QMessageBox.Ok)
        
        # Si se presiona el botón "Aceptar", cerrar la ventana
        if reply == QMessageBox.Ok:
            self.close()
