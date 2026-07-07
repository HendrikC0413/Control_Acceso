import sys
import os
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QMessageBox,
    QHBoxLayout, QLineEdit, QComboBox
)
from Control.C_Registro  import C_Registro

def limpiar_fecha(fecha):
    """
    Reemplaza '/' y '-' por '_' en las fechas ingresadas.
    
    Parámetros:
    - fecha: La fecha en formato de cadena (str) que se desea limpiar.
    
    Retorna:
    - Una cadena con los delimitadores '/' y '-' reemplazados por '_'.
    """
    return fecha.replace('/', '_').replace('-', '_') if fecha else ''

def limpiar_run(run):
    """
    Elimina los puntos y el guion de un RUN chileno.
    
    Parámetros:
    - run: El RUN del usuario a limpiar.
    
    Retorna:
    - El RUN limpio, sin puntos ni guion.
    """
    return run.replace('.', '').replace('-', '') if run else ''


def generar_excel(run,rbd, tipo_reporte, desde=None, hasta=None, mes=None):
    """
    Genera un archivo Excel con datos de ejemplo según el tipo de reporte.
    
    Parámetros:
    - run: El RUN del usuario.
    - rbd: El RBD del establecimiento.
    - tipo_reporte: El tipo de reporte a generar (1: semanal, 2: mensual).
    - desde: La fecha de inicio (solo para tipo_reporte 1).
    - hasta: La fecha de fin (solo para tipo_reporte 1).
    - mes: El mes (solo para tipo_reporte 2).
    
    Retorna:
    - El nombre del archivo Excel generado.
    """
    
    Control_r = C_Registro()
    datos = Control_r.Reporte_Usuario(rbd,run,desde,hasta,mes,tipo_reporte)

    
    columnas = ["RUN", "RBD", "Fecha", "Hora_entrada", "Hora_salida", "Hora_salida_colacion", "Hora_entrada_colacion", "Completo"]
    df = pd.DataFrame(datos, columns=columnas)
    
    directorio = "Reportes/Reportes Usuarios"
    os.makedirs(directorio, exist_ok=True)
    
    detalles = ""
    if tipo_reporte == 1:
        detalles = f"_{limpiar_fecha(desde)}_al_{limpiar_fecha(hasta)}"
    elif tipo_reporte == 2:
        detalles = f"_{mes}"
    
    nombre_archivo = f"{directorio}/Reporte_{limpiar_run(run)}_{tipo_reporte}{detalles}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    
    return nombre_archivo

class ReporteUsuarioApp(QDialog):
    """
    Clase encargada de gestionar la interfaz para generar reportes de usuario.
    Permite al usuario ingresar el RUN y seleccionar el tipo de reporte (semanal o mensual).
    """
    def __init__(self,rbd):
        """
        Constructor de la clase.
        Inicializa la interfaz para ingresar el RUN y seleccionar el tipo de reporte.

        Parámetros:
        - rbd: El RBD del establecimiento.
        """
        super().__init__()
        self.setWindowTitle("Generar Reporte de Usuario")
        self.setFixedSize(400, 300)
        self.RBD = rbd

        layout = QVBoxLayout()
        
        self.label = QLabel("Ingrese el RUN:")
        self.input_run = QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.input_run)
        
        self.reporte_group = QButtonGroup(self)
        
        self.radio_semanal = QRadioButton("Reporte Semanal")
        self.radio_mensual = QRadioButton("Reporte Mensual")
        
        self.reporte_group.addButton(self.radio_semanal)
        self.reporte_group.addButton(self.radio_mensual)
        
        layout.addWidget(self.radio_semanal)
        
        self.hbox_semanal = QHBoxLayout()
        self.label_desde = QLabel("Desde:")
        self.input_desde = QLineEdit()
        self.label_hasta = QLabel("Hasta:")
        self.input_hasta = QLineEdit()
        self.hbox_semanal.addWidget(self.label_desde)
        self.hbox_semanal.addWidget(self.input_desde)
        self.hbox_semanal.addWidget(self.label_hasta)
        self.hbox_semanal.addWidget(self.input_hasta)
        layout.addLayout(self.hbox_semanal)
        
        layout.addWidget(self.radio_mensual)
        
        self.hbox_mensual = QHBoxLayout()
        self.combo_mes = QComboBox()
        self.combo_mes.addItems(["Seleccione mes", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
        self.hbox_mensual.addWidget(self.combo_mes)
        layout.addLayout(self.hbox_mensual)
        
        self.boton_generar = QPushButton("Generar")
        self.boton_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(self.boton_generar)
        
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.close)
        layout.addWidget(self.boton_cancelar)
        
        self.setLayout(layout)

        # Establecer "Reporte Semanal" como seleccionado por defecto
        self.radio_semanal.setChecked(True)

        # Conectar eventos
        self.radio_semanal.toggled.connect(self.actualizar_interfaz)
        self.radio_mensual.toggled.connect(self.actualizar_interfaz)

        # Llamar a la función para aplicar restricciones iniciales
        self.actualizar_interfaz()
    
    def generar_reporte(self):
        """
        Maneja la generación del reporte según la selección del tipo de reporte.
        Verifica que el RUN esté ingresado y llama a la función para generar el reporte correspondiente.
        """
        run = self.input_run.text()
        if not run:
            QMessageBox.warning(self, "Error", "Ingrese el RUN del usuario.")
            return
        
        if self.radio_semanal.isChecked():
            tipo_reporte = 1
            desde = self.input_desde.text()
            hasta = self.input_hasta.text()
            archivo = generar_excel(run,self.RBD, tipo_reporte, desde=desde, hasta=hasta)
        elif self.radio_mensual.isChecked():
            tipo_reporte = 2
            mes = self.combo_mes.currentIndex()
            archivo = generar_excel(run,self.RBD, tipo_reporte, mes=mes)
        else:
            QMessageBox.warning(self, "Error", "Seleccione un tipo de reporte.")
            return
        
        QMessageBox.information(self, "Éxito", f"Reporte generado: {archivo}")

    def actualizar_interfaz(self):
        """
        Habilita o deshabilita los campos de fecha o mes según el tipo de reporte seleccionado.
        """
        if self.radio_semanal.isChecked():
            # Habilitar inputs de fecha y deshabilitar combo de mes
            self.input_desde.setEnabled(True)
            self.input_hasta.setEnabled(True)
            self.combo_mes.setEnabled(False)

            # Resetear el combo de mes a "Seleccione mes"
            self.combo_mes.setCurrentIndex(0)

        elif self.radio_mensual.isChecked():
            # Deshabilitar inputs de fecha y habilitar combo de mes
            self.input_desde.setEnabled(False)
            self.input_hasta.setEnabled(False)
            self.combo_mes.setEnabled(True)

            # Limpiar los campos de fecha
            self.input_desde.clear()
            self.input_hasta.clear()