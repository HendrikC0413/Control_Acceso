import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog, QLabel, QVBoxLayout,QToolBar,QWidget,QPushButton,QLineEdit,QHBoxLayout,QRadioButton,QGridLayout,QButtonGroup
from PySide6.QtGui import QAction  # Corregida la importación
from PySide6.QtCore import Qt, QTimer, QTime, QThread, Signal
import pickle

from Control.ControlHuella import FingerprintManager
from Control.control_pistola import ControladorLector
from Vista.sesionini import IniciarSesion
from Vista.user.registro import Formulario
from Vista.actualizarH import ActualizadorHora 
from Vista.login import LoginForm
from Vista.school.v_school import EstablecimientoForm
from Vista.Reportes.V_ReportG import ReporteApp 
from Vista.Reportes.V_ReportI import ReporteUsuarioApp
from Vista.user.v_U_user import UpdateUsuario
from Vista.user.v_D_user import DeleteUsuario
from Vista.user.v_UA_user import Up_AsistenciaForm
from Vista.school.v_S_school import EstablecerEstablecimiento

class MainWindow(QMainWindow):
    """
    Clase principal que gestiona la interfaz del sistema de control de acceso.
    Proporciona funcionalidades como autenticación de usuario, selección de tipo de marcación,
    y administración de usuarios y establecimientos.
    """
    def __init__(self):
        """
        Inicializa la ventana principal con la configuración de la interfaz y la hora.
        """
        super().__init__()
        self.cHuella = 0
        self.Tipo_entrada = 0
        self.tipo_marcacion = 1
        self.OPCION = 0
        self.RBD = str(self.leer_Establecimiento())
        titulo = "Bienvenido: "+ self.RBD
        # Configuración básica de la ventana
        self.setWindowTitle(titulo)
        self.setGeometry(100, 100, 800, 600)

        # Crear la barra de menú
        self.crear_menu()

        self.init_ui()
        # Hilo para actualizar la hora
        self.hilo_hora = ActualizadorHora()
        self.hilo_hora.hora_actualizada.connect(self.update_hora)
        self.hilo_hora.fecha_actualizada.connect(self.update_fecha)
        self.hilo_hora.start()
    

    def init_ui(self):
        """
        Configura la interfaz de usuario, incluyendo etiquetas de hora y fecha,
        botones de autenticación y selección de tipo de marcación.
        """
        # Contenedor principal
        widget = QWidget()
        layout = QVBoxLayout()

        # Etiqueta para la hora
        self.label_hora = QLabel()
        self.label_hora.setAlignment(Qt.AlignCenter)
        self.label_hora.setStyleSheet("font-size: 64px; font-weight: bold;")  # Ajusta el tamaño aquí
        layout.addWidget(self.label_hora)

        # Etiqueta para la fecha
        self.label_fecha = QLabel()
        self.label_fecha.setAlignment(Qt.AlignCenter)
        self.label_fecha.setStyleSheet("font-size: 24px; font-weight: bold;")  # Ajusta el tamaño aquí
        layout.addWidget(self.label_fecha)

        # Radio buttons para seleccionar el método de identificación
        #self.radio_clave = QRadioButton("Clave")
        self.radio_tarjeta = QRadioButton("Tarjeta")

        self.radio_clave = QPushButton("Ingresar")
        self.radio_clave.setStyleSheet("background-color: #6A8CE0; color: white; font-size: 14.4px; padding: 6px;")
        
        #self.radio_clave.setChecked(True)

        # Layout horizontal para los radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_clave)
        radio_layout.addWidget(self.radio_tarjeta)

        # Conectar las señales de los radio buttons a sus respectivas funciones
        self.radio_clave.clicked.connect(self.open_Login_window)
        self.radio_tarjeta.toggled.connect(self.on_method_changed)
        
        self.grupo_Identificación = QButtonGroup(self)
        #self.grupo_Identificación.addButton(self.radio_clave)
        self.grupo_Identificación.addButton(self.radio_tarjeta)   

        #Inicializa la pistola
        self.Lectora = ControladorLector()

        # Inicializar el FingerprintManager
        self.fingerprint_manager = FingerprintManager()
        if(self.fingerprint_manager.get_inicializado()==True):
            self.cHuella = 1
            self.fingerprint_manager.set_option(2)
            self.fingerprint_manager.setRBD(self.RBD)
            self.radio_huella = QRadioButton("Huella")
            radio_layout.addWidget(self.radio_huella)
            self.radio_huella.toggled.connect(self.on_method_changed)
            self.grupo_Identificación.addButton(self.radio_huella)
        else:
              QMessageBox.information(self, "Importante", "NO SE HA DETECTADO LECTOR DE HUELLA ")
        

        # ------------------ GRUPO DE RADIO BUTTOMS ------------------

        self.grupo_Entrada = QButtonGroup(self)

        radio_opciones_layout = QGridLayout()

        self.radio_entrada = QRadioButton("Entrada")
        self.radio_salida = QRadioButton("Salida")
        self.radio_entrada_colacion = QRadioButton("Entrada Colación")
        self.radio_salida_colacion = QRadioButton("Salida Colación")

        self.grupo_Entrada.addButton(self.radio_entrada)
        self.grupo_Entrada.addButton(self.radio_salida)
        self.grupo_Entrada.addButton(self.radio_entrada_colacion)
        self.grupo_Entrada.addButton(self.radio_salida_colacion)

        self.radio_entrada.toggled.connect(self.on_marcacion_changed)
        self.radio_salida.toggled.connect(self.on_marcacion_changed)
        self.radio_entrada_colacion.toggled.connect(self.on_marcacion_changed)
        self.radio_salida_colacion.toggled.connect(self.on_marcacion_changed)

        # Estilo para hacer los botones más grandes
        estilo_radio = "font-size: 24px; font-weight: bold; padding: 10px;"

        self.radio_entrada.setStyleSheet(estilo_radio)
        self.radio_entrada.setChecked(True)
        self.radio_salida.setStyleSheet(estilo_radio)
        self.radio_entrada_colacion.setStyleSheet(estilo_radio)
        self.radio_salida_colacion.setStyleSheet(estilo_radio)

        # Añadir los botones al layout
        radio_opciones_layout.addWidget(self.radio_entrada, 0, 0)
        radio_opciones_layout.addWidget(self.radio_salida, 0, 1)
        radio_opciones_layout.addWidget(self.radio_entrada_colacion, 1, 0)
        radio_opciones_layout.addWidget(self.radio_salida_colacion, 1, 1)

        layout.addLayout(radio_opciones_layout)

        # Asignar layout al widget central
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        layout.addLayout(radio_layout)

        # Asignar layout al widget central
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def crear_menu(self):     
        """
        Crea y configura la barra de menú con las opciones principales.
        """                         
        # Crear la barra de menú
        menu_bar = self.menuBar()

        #Crear las secciones del menú
        self.menu_inicio(menu_bar)

    def iniciar_sesion(self):
        QMessageBox.information(self, "Iniciar sesión", "Has seleccionado 'Iniciar sesión'.")

    def menu_inicio(self, menu_bar):
        """
        Configura el menú de inicio con opciones de sesión y establecimiento.
        """
        # Agregar el menú "Inicio"
        inicio_menu = menu_bar.addMenu("Inicio")
         # Crear las acciones
        iniciar_sesion_action = QAction("Iniciar sesión", self)
        establecer_escuela_action = QAction("Establecer Establecimiento", self)
        salir_action = QAction("Salir", self)

        # Conectar las acciones a funciones
        iniciar_sesion_action.triggered.connect(self.open_child_window)
        establecer_escuela_action.triggered.connect(self.Set_Establecimiento)
        salir_action.triggered.connect(self.salir)

        # Agregar las acciones al menú
        inicio_menu.addAction(iniciar_sesion_action)
        inicio_menu.addSeparator()  # Línea separadora opcional
        inicio_menu.addAction(establecer_escuela_action)
        inicio_menu.addSeparator()  # Línea separadora opcional
        inicio_menu.addAction(salir_action)

        #Ocultamos las que solo el Admin tiene acceso.
        establecer_escuela_action.setVisible(True)

    def menu_Usuarios(self, menu_bar):
        """
        Configura el menú de Usuario con opciones CRUD del personal Visible: Admin, Director y encargados.
        """
        # Agregar el menú "Personal"
        usuarios_menu = menu_bar.addMenu("Personal")

        # Crear las acciones
        C_users = QAction("Ingresar personal", self)
        U_users = QAction("Modificar personal", self)
        D_users = QAction("Dar de baja personal", self)
        R_users = QAction("Modificar asistencia", self)

        # Conectar las acciones a funciones
        C_users.triggered.connect(lambda: self.usersControl(1))
        U_users.triggered.connect(lambda: self.usersControl(2))
        D_users.triggered.connect(lambda: self.usersControl(3))
        R_users.triggered.connect(lambda: self.usersControl(4))

        # Agregar las acciones al menú
        usuarios_menu.addAction(C_users)
        usuarios_menu.addAction(U_users)
        usuarios_menu.addSeparator()  # Línea separadora opcional
        usuarios_menu.addAction(R_users)
        usuarios_menu.addSeparator()  # Línea separadora opcional
        usuarios_menu.addAction(D_users)

    def menu_Establecimientos(self, menu_bar):
        """
            Configura el menú de establecimiento con opciones CRUD de estos mismos SOLO VISIBLE ADMIN.
        """
        # Agregar el menú "Escuelas"
        school_menu = menu_bar.addMenu("Escuelas")

        # Crear las acciones
        C_school = QAction("Ingresar escuela", self)
        U_school = QAction("Modificar escuela", self)
        D_school = QAction("Dar de baja escuela", self)

        # Conectar las acciones a funciones
        C_school.triggered.connect(lambda: self.schoolControl(1))
        U_school.triggered.connect(lambda: self.schoolControl(2))
        D_school.triggered.connect(lambda: self.schoolControl(3))

        # Agregar las acciones al menú
        school_menu.addAction(C_school)
        school_menu.addAction(U_school)
        school_menu.addSeparator()  # Línea separadora opcional
        school_menu.addAction(D_school)

    def menu_Report(self, menu_bar):
        """
        Configura el menú de reportes con opciones de visualicion de reportes. Visiblidad Admin, director y encargados
        """
        # Agregar el menú "Reportes"
        school_menu = menu_bar.addMenu("Reportes")

        # Crear las acciones
        R_Grupal = QAction("Reporte de asistencia grupal", self)
        R_individual = QAction("Reporte de asistencia individual", self)

        # Conectar las acciones a funciones
        R_Grupal.triggered.connect(lambda: self.reportControl(1))
        R_individual.triggered.connect(lambda: self.reportControl(2))
    
        # Agregar las acciones al menú
        school_menu.addAction(R_Grupal)
        school_menu.addAction(R_individual)

    def salir(self):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            sys.exit()

    def open_child_window(self):
        '''
            Abre el inicio de sesion para administrador, director y encargados
        '''
        self.child_window = IniciarSesion()
        self.child_window.login_exitoso.connect(self.mostrarOcultos)
        self.child_window.exec()
    
    def Set_Establecimiento(self):
        '''
            Metodo que establece que institución esta usando esta interfaz
        '''
        if(self.OPCION == 1):
            self.child_window =EstablecerEstablecimiento()
            self.child_window.establecido.connect(self.Cambiar_Title)
            self.child_window.exec()
        else:
             QMessageBox.warning(self, "Atención", "Usted no posee acceso a esta funcionalidad")


    def open_Login_window(self):
        '''
            Abre el inicio de sesion para todo usuario
        '''
        print("Modo de identificación: Clave")
        if(self.cHuella == 1):
            self.fingerprint_manager.stop_fingerprint_scanning()
            #self.fingerprint_manager.shutdown()

        self.Lectora.detener_lectura()
        login = LoginForm(self.RBD,self.tipo_marcacion)
        #login(self.mostrarOcultos)
        login.exec()    
    

    def usersControl(self, option):
        '''
            Segun el menu que seleccione será reenviado
        '''
        if option == 1:
            Ventana = Formulario(self.fingerprint_manager,self.RBD)
        elif option == 2:
            Ventana = UpdateUsuario(self.RBD)
        elif option == 3:
            Ventana = DeleteUsuario(self.RBD)
        elif option == 4:
            Ventana = Up_AsistenciaForm(self.RBD)
           
        Ventana.exec()


    def schoolControl(self, option):
        '''
            Segun el menu que seleccione será reenviado a una u otra vista del CRUD del establecimiento
        '''
        Escuelas = EstablecimientoForm(option)
        Escuelas.exec()

    def reportControl(self, option):
        '''
            Segun el menu que seleccione será reenviado a una u otra vista de los reportes
        '''
        if option == 1:
            R_Ejec = ReporteApp(self.RBD)
        elif option == 2:
            R_Ejec = ReporteUsuarioApp(self.RBD)
        R_Ejec.exec()
        

    def mostrarOcultos(self,option):
        '''
            Segun el tipo de usuario, se mostrará y ocultarán elementos del menu.
        '''
        self.OPCION = option
        print(option)
        if option == 1:
            self.menu_Usuarios(self.menuBar())
            self.menu_Establecimientos(self.menuBar())
            self.menu_Report(self.menuBar())
        elif option == 2 or option == 3:
            self.menu_Usuarios(self.menuBar())
            self.menu_Report(self.menuBar())

    def update_hora(self, hora):
        """Actualizar la hora en el QLabel"""
        self.label_hora.setText(hora)

    def update_fecha(self, fecha):
        """Actualizar la fecha en el QLabel"""
        self.label_fecha.setText(fecha)

    def on_method_changed(self):
        """
        Método que se ejecuta cuando se cambia el método de identificación.
        """
        if self.radio_clave.isChecked():
            self.open_Login_window()

        elif self.radio_tarjeta.isChecked():
            print("Modo de identificación:Tarjeta")
            if(self.cHuella == 1):
                self.fingerprint_manager.stop_fingerprint_scanning()
                #self.fingerprint_manager.shutdown()
            self.Lectora.iniciar_lectura()
            
        else:
            if(self.cHuella == 1):
                print("Modo de identificación: Huella")
                self.fingerprint_manager.set_option(2)
                self.fingerprint_manager.start_fingerprint_scanning()
                self.Lectora.detener_lectura()


    def on_marcacion_changed(self):
        """ Se ejecuta cuando cambia el tipo de marcación """
        if self.radio_entrada.isChecked():
            self.tipo_marcacion = 1
        elif self.radio_salida.isChecked():
            self.tipo_marcacion = 4
        elif self.radio_entrada_colacion.isChecked():
            self.tipo_marcacion = 3
        elif self.radio_salida_colacion.isChecked():
            self.tipo_marcacion = 2
        print(f"Tipo de marcación seleccionada: {self.tipo_marcacion}")
        self.Lectora.set_tipo_marcacion(self.tipo_marcacion)
        
        if(self.cHuella == 1):
           self.fingerprint_manager.setMarcacion(self.tipo_marcacion)
    
    def closeEvent(self, event):
        """
        Método que se ejecuta al cerrar la ventana para detener la detección de huellas.
        """
        self.fingerprint_manager.stop_fingerprint_scanning()
        event.accept()

    def leer_Establecimiento(self):
        """
        Lee el establecimiento desde un archivo binario y lo devuelve.
        """
        RBD = ""
        # Leer datos desde un archivo binario
        try:
            with open("data.dat", "rb") as bin_file:
                data_loaded = pickle.load(bin_file)
            print(f"Datos cargados: {data_loaded['RBD']}")
            RBD = data_loaded['RBD']
            #self.RBD
        except IOError as e:
            print(f"Error al leer los datos: {e}")
        except pickle.UnpicklingError as e:
            print(f"Error al deserializar los datos binarios: {e}")
        
        return RBD

    def Cambiar_Title(self,RBD):
        ''' Modifica el titulo de la ventana principal'''
        self.setWindowTitle("Bienvenido: "+ str(RBD))