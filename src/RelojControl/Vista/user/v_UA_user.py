import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox,QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout
from PySide6.QtWidgets import QMessageBox

from Control.C_usuario import C_user

class Up_AsistenciaForm(QDialog):
    """
    Ventana de diálogo para revisar y modificar la asistencia de un usuario.
    Permite buscar registros de asistencia por RUN y fecha, y modificar la hora de entrada o salida.
    """
    def __init__(self,rbd):
        """
        Inicializa la ventana de revisión de asistencia.

        Parámetros:
        - rbd (str): Identificador único de la institución o entidad relacionada.
        """
        super().__init__()
        self.RBD = rbd
        self.Idregistro = ""
        self.Insertar = 0
        self.setWindowTitle("Revisión asistencia")

        # Crear el título visible en la pantalla
        self.titulo_label = QLabel("Revisión de Asistencia")
        self.titulo_label.setAlignment(Qt.AlignCenter)
        self.titulo_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Crear los widgets
        self.run_input = QLineEdit()
        self.fecha_input = QLineEdit()
        self.hora_input = QLineEdit()

        self.opcion_combobox = QComboBox()
        self.opcion_combobox.addItem("Seleccione Opción")
        self.opcion_combobox.addItem("ENTRADA")
        self.opcion_combobox.addItem("SALIDA COLACIÓN")
        self.opcion_combobox.addItem("ENTRADA COLACIÓN")
        self.opcion_combobox.addItem("SALIDA")

        self.buscar_button = QPushButton("Buscar")
        self.cambiar_button = QPushButton("Modificar")
        self.cancelar_button = QPushButton("Cancelar")

        self.buscar_button.setStyleSheet("background-color: #14E3CD; color: black;")
        self.cambiar_button.setStyleSheet("background-color: #08E532; color: black;")

        # Layouts
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Hora:"), self.hora_input)

        # Configurar el layout de los campos RUN, Fecha y Buscar en la misma línea
        run_fecha_layout = QHBoxLayout()
        run_fecha_layout.addWidget(QLabel("RUN:"))
        run_fecha_layout.addWidget(self.run_input)
        run_fecha_layout.addWidget(QLabel("Fecha:"))
        run_fecha_layout.addWidget(self.fecha_input)
        run_fecha_layout.addWidget(self.opcion_combobox)
        run_fecha_layout.addWidget(self.buscar_button)

        # Configurar los botones de Cambiar y Cancelar
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cambiar_button)
        button_layout.addWidget(self.cancelar_button)

        # Configurar el layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.titulo_label)  # Agregar el título visible
        main_layout.addLayout(run_fecha_layout)  # Layout RUN, Fecha y Buscar
        main_layout.addLayout(form_layout)  # Layout de las horas
        main_layout.addLayout(button_layout)  # Layout de los botones

        self.setLayout(main_layout)

        # Bloquear campos por defecto (solo RUN y Fecha habilitados)
        self.bloquear_campos(True)

        # Conectar los botones con las funciones
        self.buscar_button.clicked.connect(self.buscar_asistencia)
        self.cambiar_button.clicked.connect(self.cambiar_asistencia)
        self.cancelar_button.clicked.connect(self.cancelar_asistencia)

    def bloquear_campos(self, bloquear):
        """
        Bloquea o desbloquea los campos del formulario según el parámetro 'bloquear'.

        Parámetros:
        - bloquear (bool): Si es True, bloquea los campos RUN, Fecha y Combobox. Si es False, habilita el campo Hora.
        """
        self.run_input.setEnabled(bloquear)
        self.fecha_input.setEnabled(bloquear)
        self.hora_input.setEnabled(not bloquear)
        self.opcion_combobox.setEnabled(bloquear)
        self.buscar_button.setEnabled(bloquear)

    def buscar_asistencia(self):
        """
        Busca un registro de asistencia en la base de datos utilizando el RUN, la fecha y el tipo de marcación.
        Si se encuentra el registro, carga la hora correspondiente en el campo Hora.
        Si no se encuentra, habilita la inserción de un nuevo registro.
        """
        print("Buscando asistencia...")
        run = self.run_input.text()
        fecha = self.fecha_input.text()
        tipo_marcacion = self.opcion_combobox.currentIndex()
        
        Control_usuario = C_user()
        
        if Control_usuario.verificar_formato_run(run) == False:
            run = Control_usuario.formatear_run(run)

        fecha = self.convertir_fecha(fecha)

        idTarjeta = Control_usuario.Obtener_tarjeta(run,self.RBD)

        id_registro, hora = Control_usuario.Ver_Eventos_Individual(fecha, idTarjeta, tipo_marcacion)

        self.Idregistro = id_registro

        if hora == "": 
            self.Insertar = 1
            self.hora_input.setText("")
        else:
            self.Insertar = 0
            self.hora_input.setText(hora)

        self.bloquear_campos(False)  # Desbloquear campos después de buscar

    def cambiar_asistencia(self):
        """
        Modifica o inserta un registro de asistencia en la base de datos.
        Dependiendo del valor de 'Insertar', realiza una inserción o una modificación.
        Muestra un mensaje de éxito o error según el resultado de la operación.
        """
        tipo_marcacion = self.opcion_combobox.currentIndex()
        hora = self.hora_input.text()
        correcto = False
        Control_usuario = C_user()

        if self.Insertar == 1:
            correcto = Control_usuario.InsertarEvento(self.Idregistro,tipo_marcacion,hora)
        else:
           correcto = Control_usuario.ModificarEvento(self.Idregistro,tipo_marcacion,hora)
        
        if correcto:
            self.mostrar_mensaje_info("Se a realizado la modificación correctamente")
            self.limpiar_campos()
            self.bloquear_campos(True)
        else:
            self.mostrar_mensaje_info("Ah ocurrido un error al realizar la modificación")

        # Aquí se podrían agregar acciones adicionales para cambiar la asistencia

    def limpiar_campos(self):
        """
        Limpia todos los campos del formulario y restablece el Combobox a su valor predeterminado.
        """
        self.run_input.clear()
        self.fecha_input.clear()
        self.hora_input.clear()
        self.opcion_combobox.setCurrentIndex(0)

    def cancelar_asistencia(self):
        """
        Cancela la operación actual, bloquea los campos y limpia el formulario.
        """
        print("Operación cancelada.")
        self.bloquear_campos(True)  # Bloquear los campos nuevamente
        self.limpiar_campos()

    def convertir_fecha(self,fecha):
        """
        Convierte una fecha en formato dd-mm-aaaa o dd/mm/aaaa al formato aaaa-mm-dd.

        Parámetros:
        - fecha (str): Fecha en formato dd-mm-aaaa o dd/mm/aaaa.

        Retorna:
        - str: Fecha en formato aaaa-mm-dd, o una cadena vacía si el formato es inválido.
        """
        import re
        fecha_convertida = ""
        # Verificar si la fecha es en formato dd-mm-aaaa o dd/mm/aaaa
        if re.match(r"\d{2}-\d{2}-\d{4}", fecha) or re.match(r"\d{2}/\d{2}/\d{4}", fecha):
            # Reemplazar '/' con '-'
            fecha = fecha.replace("/", "-")
            # Convertir la fecha al formato aaaa-mm-dd
            dia, mes, anio = fecha.split("-")
            fecha_convertida = f"{anio}-{mes}-{dia}"
        else:
            self.mostrar_mensaje_info("Formato invalido, debe ser xx-xx-xxxx o xx/xx/xxxx")

        return fecha_convertida

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
           