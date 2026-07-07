from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QDialog, 
    QHBoxLayout, QFormLayout, QComboBox, QFrame, QSpacerItem, QSizePolicy, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from Control.ControlHuella import FingerprintManager
from Control.control_lectora import ControladorLector
from Control.C_tipo_user import C_tipo_usuario
from Control.C_usuario import C_user

class Formulario(QDialog):
    """
        Formulario para el registro de usuarios.
        Permite ingresar RUN, RBD, nombre, apellidos, tipo de usuario, clave, 
        huella digital y tarjeta, gestionando su almacenamiento y validación.
    """
    def __init__(self, FM:FingerprintManager, RBD):
        super().__init__()
        self.setWindowTitle("Formulario Registro Usuario")
        self.setFixedSize(600, 500)
        self.fingerprint_manager = FM
        self.Cod_RBD = RBD
        self.cHuella = 0
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Formulario con borde
        form_container = QFrame()
        #form_container.setStyleSheet("border: 1px solid #ccc;")
        form_layout = QVBoxLayout()
        
        form_fields = QFormLayout()
        
        # Campos del formulario
        self.run_input = QLineEdit()
        self.rbd_input = QLineEdit()
        self.rbd_input.setText(self.Cod_RBD)
        self.rbd_input.setReadOnly(True)
        self.nombre_input = QLineEdit()
        self.apellido_paterno_input = QLineEdit()
        self.apellido_materno_input = QLineEdit()
        
        form_fields.addRow("RUN:", self.run_input)
        form_fields.addRow("RBD:", self.rbd_input)
        form_fields.addRow("Nombre:", self.nombre_input)
        form_fields.addRow("Apellido Paterno:", self.apellido_paterno_input)
        form_fields.addRow("Apellido Materno:", self.apellido_materno_input)
        
        # ComboBox
        CTipoUsuario = C_tipo_usuario()
        lista_tipo_usuarios = CTipoUsuario.cargar_lista()
        self.combo_box = QComboBox()
        
        # Agregar elementos con nombre visible y ID oculto
        for tipo_usuario in lista_tipo_usuarios:
            self.combo_box.addItem(tipo_usuario.descripcion, tipo_usuario.id_tipo_usuario)

        form_fields.addRow("Seleccione una opción:", self.combo_box)
        
        # Clave
        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)  # Ocultar la clave con asteriscos
        form_fields.addRow("Clave:", self.clave_input)
        
        form_layout.addLayout(form_fields)
        
        # Imagen y tarjeta
        img_layout = QVBoxLayout()
        self.image_label = QLabel()
        pixmap = QPixmap("Vista\Recursos\huella.jpg")  # Asegúrate de usar una ruta válida
        self.image_label.setPixmap(pixmap.scaled(100, 137, Qt.KeepAspectRatio))
        self.image_label.setFixedSize(100, 137)
        

        # Botón "Capturar" debajo de la imagen
        self.capturar_btn = QPushButton("Capturar")
        self.capturar_btn.setStyleSheet("background-color: #A9C9D9; color: black;")
        self.capturar_btn.clicked.connect(self.Capturar_Huella)


        tarjeta_layout = QVBoxLayout()
        codigo_layout= QHBoxLayout()
        self.tarjeta_input = QLineEdit()
        self.tarjeta_input.setReadOnly(True)
        self.generar_btn = QPushButton("Generar")
        self.generar_btn.setStyleSheet("background-color: #A9C9D9; color: black;")  # Tono azul pálido
        
        # Conectar el botón "Generar" con su función
        self.generar_btn.clicked.connect(self.generar_tarjeta)
        
        codigo_layout.addWidget(QLabel("Tarjeta:"))
        codigo_layout.addWidget(self.tarjeta_input)
        tarjeta_layout.addLayout(codigo_layout)
        tarjeta_layout.addWidget(self.generar_btn)
        Completo_layout = QHBoxLayout()
        if self.fingerprint_manager.get_inicializado() == True:
            img_layout.addWidget(self.image_label)
            img_layout.addWidget(self.capturar_btn)
            #img_layout.addLayout(tarjeta_layout)   
            Completo_layout.addLayout(img_layout)
            
        else:
            QMessageBox.information(self, "Importante", "NO SE HA DETECTADO LECTOR DE HUELLA ")
            self.cHuella = 1 
        
        Completo_layout.addLayout(tarjeta_layout)
        form_layout.addLayout(Completo_layout)
        
        # Botones de Registrar y Cancelar
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.registrar_btn = QPushButton("Registrar")
        self.registrar_btn.setStyleSheet("background-color: green; color: white;")
        self.registrar_btn.clicked.connect(lambda: self.guardar_datos(self.cHuella))
        
        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.setStyleSheet("background-color: red; color: white;")
        self.cancelar_btn.clicked.connect(self.close_window)
        
        btn_layout.addWidget(self.registrar_btn)
        btn_layout.addWidget(self.cancelar_btn)
        
        form_layout.addSpacing(10)
        form_layout.addLayout(btn_layout)
        
        form_container.setLayout(form_layout)
        main_layout.addWidget(form_container)
        
        self.setLayout(main_layout)
    
    def mostrar_mensaje(self,mensaje):
        """
        Muestra un mensaje emergente con información relevante al usuario.
        
        Parámetros:
        mensaje (str): Texto que se mostrará en la ventana emergente.
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Mensaje")
        msg.exec()

    def guardar_datos(self, option):
        """
        Obtiene los datos ingresados en el formulario, valida el RUN,
        los transforma a mayúsculas y los guarda en la base de datos.
        También asocia la tarjeta generada al usuario registrado.
        
        Parámetros:
        option (int): Indica si se capturó o no una huella digital.
        """
        # Obtener los valores de los campos de entrada
        run = self.run_input.text()
        rbd = self.rbd_input.text()
        nombre = self.nombre_input.text()
        apellido_paterno = self.apellido_paterno_input.text()
        apellido_materno = self.apellido_materno_input.text()
        clave = self.clave_input.text()
        tarjeta = self.tarjeta_input.text()
        opcion = self.combo_box.currentData()  # Obtener la opción seleccionada en el QComboBox
        if option != 1:
            huella = self.fingerprint_manager.get_huella
        else:
            huella = None

        # Guardar los datos en un archivo de texto
        try:
            usuario = C_user()
            if usuario.verificar_formato_run(run) == False:
                run = usuario.formatear_run(run)
            print(run)
            if usuario.validar_run(run) == True:
                usuario.Ingresar_Usuario(run,usuario.text_mayuscula(nombre),usuario.text_mayuscula(apellido_paterno),usuario.text_mayuscula(apellido_materno),opcion,clave,huella)
                usuario.Ingresar_Tarjeta(run,rbd,tarjeta)
                # Mostrar mensaje de éxito
                self.mostrar_mensaje("Datos guardados correctamente")
            else:
                 self.mostrar_mensaje("RUN ingresado no es valido")
        
        except Exception as e:
            # Mostrar mensaje de error si hay un problema al guardar
            print(f"Error al guardar los datos: {str(e)}")
            self.mostrar_mensaje("Ha ocurrido un error en el registro")
            #self.mostrar_mensaje("A ocurrido un error al realizar el registro")
    

    def generar_tarjeta(self):
        """
        Genera un código único de tarjeta utilizando el RUN y el RBD del usuario.
        Luego, crea un código de barras a partir del código generado y lo asigna 
        al campo correspondiente en la interfaz.
        """
       
        run = self.run_input.text()
        rbd = self.rbd_input.text()
        C_Lectora = ControladorLector()
        codigo = C_Lectora.generar_codigo_unico(rbd,run)
        salida = "CB_"+ str(self.limpiar_run(run))
        completo = C_Lectora.generar_codigo_barras(codigo,salida)
        self.tarjeta_input.setText(completo)  # Ejemplo de tarjeta generada


    def Capturar_Huella(self):
        """
        Inicia el proceso de captura de huella digital utilizando el lector biométrico.
        Cambia el estado del lector para que comience el escaneo y almacena la huella.
        """
        
        self.fingerprint_manager.set_option(1)
        self.fingerprint_manager.start_fingerprint_scanning()

    def closeEvent(self, event):
            """
            Se ejecuta cuando la ventana del formulario es cerrada.
            Desactiva el lector de huellas y muestra un mensaje informativo al usuario.
            
            Parámetros:
            event (QCloseEvent): Evento de cierre de la ventana.
            """
            self.fingerprint_manager.set_option(2)
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText("La ventana ha sido cerrada.")
            mensaje.setWindowTitle("Información")
            mensaje.exec()

            event.accept()  # Asegura que la ventana se cierre correctamente

    def limpiar_run(self,run):
        """
        Elimina los caracteres especiales (puntos y guion) del RUN para su procesamiento.
        Asegura que el RUN esté en un formato limpio antes de ser almacenado.
        
        Parámetros:
        run (str): RUN ingresado por el usuario.
        
        Retorna:
        str: RUN sin puntos ni guion.
        """
        return run.replace('.', '').replace('-', '') if run else ''
    
    def close_window(self):
        """
        Cierra la ventana del formulario sin guardar cambios.
        """
        self.close()
