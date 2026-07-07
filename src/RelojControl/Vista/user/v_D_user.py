from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout,QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from Control.C_usuario import C_user
from Control.C_tipo_user import C_tipo_usuario

import sys

class DeleteUsuario(QDialog):
    """
    Ventana de diálogo para dar de baja a un usuario.
    Permite buscar un usuario por RUN y eliminarlo del sistema.
    """
    def __init__(self, RBD):
        super().__init__()
        self.RBD = RBD
        self.setWindowTitle("Dar de baja")
        self.setFixedSize(400, 450)

        layout = QVBoxLayout()

        # Título
        self.label_titulo = QLabel("Dar de baja a un usuario")
        self.label_titulo.setFont(QFont("Arial", 14, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_titulo)

        # RUN + Botón Buscar
        self.hbox_run = QHBoxLayout()
        self.label_run = QLabel("RUN:")
        self.input_run = QLineEdit()
        self.input_run.setPlaceholderText("Ingrese el RUN")
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_run)
        self.hbox_run.addWidget(self.label_run)
        self.hbox_run.addWidget(self.input_run)
        self.hbox_run.addWidget(self.boton_buscar)
        layout.addLayout(self.hbox_run)

        # RBD (Inicialmente deshabilitado)
        self.label_rbd = QLabel("RBD:")
        self.input_rbd = QLineEdit()
        self.input_rbd.setPlaceholderText("Ingrese el RBD")
        self.input_rbd.setEnabled(False)
        self.input_rbd.setText(self.RBD)
        layout.addWidget(self.label_rbd)
        layout.addWidget(self.input_rbd)

        # Nombre
        self.label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre")
        self.input_nombre.setEnabled(False)
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)

        # Apellido Paterno
        self.label_apellido_p = QLabel("Apellido Paterno:")
        self.input_apellido_p = QLineEdit()
        self.input_apellido_p.setPlaceholderText("Ingrese el apellido paterno")
        self.input_apellido_p.setEnabled(False)
        layout.addWidget(self.label_apellido_p)
        layout.addWidget(self.input_apellido_p)

        # Apellido Materno
        self.label_apellido_m = QLabel("Apellido Materno:")
        self.input_apellido_m = QLineEdit()
        self.input_apellido_m.setPlaceholderText("Ingrese el apellido materno")
        self.input_apellido_m.setEnabled(False)
        layout.addWidget(self.label_apellido_m)
        layout.addWidget(self.input_apellido_m)

        # ComboBox
        CTipoUsuario = C_tipo_usuario()
        lista_tipo_usuarios = CTipoUsuario.cargar_lista()
        self.label_combo = QLabel("Seleccione una opción:")
        self.combo_box = QComboBox()
        
        for tipo_usuario in lista_tipo_usuarios:
            self.combo_box.addItem(tipo_usuario.descripcion, tipo_usuario.id_tipo_usuario)

        self.combo_box.setEnabled(False)
        layout.addWidget(self.label_combo)
        layout.addWidget(self.combo_box)

        # Clave
        self.label_clave = QLabel("Clave:")
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Ingrese la clave")
        self.input_clave.setEchoMode(QLineEdit.Password)
        self.input_clave.setEnabled(False)
        layout.addWidget(self.label_clave)
        layout.addWidget(self.input_clave)

        # Botones
        self.hbox_botones = QHBoxLayout()
        self.boton_Delete = QPushButton("Dar de baja")
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.cancelar)
        self.boton_Delete.clicked.connect(self.Eliminar)
        self.hbox_botones.addWidget(self.boton_Delete)
        self.hbox_botones.addWidget(self.boton_cancelar)
        self.boton_Delete.setStyleSheet("background-color: #F23633; color: black;")
        layout.addLayout(self.hbox_botones)

        self.setLayout(layout)

    def buscar_run(self):
        """
        Busca un usuario en la base de datos a partir del RUN ingresado.
        Si el usuario existe, carga sus datos en los campos correspondientes y 
        deshabilita la edición del RUN y RBD.
        """
        self.input_run.setEnabled(False)  # Bloquear RUN
        self.input_rbd.setEnabled(False)  # Bloquear RBD después de buscar

        Control_User = C_user()
        run = self.input_run.text()
        if Control_User.verificar_formato_run(run) == False:
            run = Control_User.formatear_run(run)

        usuario = Control_User.Ver_Usuario(run)
        
        self.input_nombre.setText(usuario.NOMBRE)
        self.input_apellido_p.setText(usuario.APELLIDO_1)
        self.input_apellido_m.setText(usuario.APELLIDO_2)
        self.combo_box.setCurrentIndex(usuario.TIPO_USER-1)
        self.input_clave.setText(usuario.CLAVE)

        self.input_nombre.setText(usuario.NOMBRE)
        self.input_apellido_p.setText(usuario.APELLIDO_1)
        self.input_apellido_m.setText(usuario.APELLIDO_2)
        self.combo_box.setCurrentIndex(usuario.TIPO_USER-1)
        self.input_clave.setText(usuario.CLAVE)
       
    def Eliminar(self):
        """
        Elimina (logica) un usuario de la base de datos utilizando el RUN ingresado.
        Si la eliminación es exitosa, muestra un mensaje de confirmación; 
        en caso de error, muestra un mensaje con la descripción del problema.
        """

        Control_User = C_user()
        run = self.input_run.text()
        if Control_User.verificar_formato_run(run) == False:
            run = Control_User.formatear_run(run)
        try:
            Control_User.Eliminar_Usuario(run)
            self.mostrar_mensaje_info("Se ha dado de baja Correctamente")
        except Exception as e:
            self.mostrar_mensaje_info("A ocurrido un error al dar de baja"+ str(e))
    
    def cancelar(self):
        """
        Restablece el formulario a su estado inicial, permitiendo la edición del RUN.
        Limpia todos los campos excepto el RBD, que permanece inmutable.
        """
        self.input_run.setEnabled(True)  # Desbloquear RUN
        self.input_run.clear()
        self.input_rbd.setEnabled(False)  # Mantener RBD bloqueado
        self.input_nombre.clear()
        self.input_apellido_p.clear()
        self.input_apellido_m.clear()
        self.combo_box.setCurrentIndex(0)
        self.input_clave.clear()

    def mostrar_mensaje_info(self, mensaje):
        """
        Muestra un cuadro de diálogo con un mensaje de información.

        Parámetros:
        mensaje (str): El mensaje que se mostrará en la ventana emergente.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Información")
        msg.exec()