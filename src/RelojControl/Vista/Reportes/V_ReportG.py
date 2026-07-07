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
    Reemplaza '/' y '-' por '_' en una fecha dada.
    
    Parámetros:
    - fecha: La fecha en formato de cadena (str) que se desea limpiar.
    
    Retorna:
    - Una cadena con los delimitadores '/' y '-' reemplazados por '_'.
    """
    return fecha.replace("/", "_").replace("-", "_") if fecha else ""

def generar_excel(rbd,tipo_reporte, desde=None, hasta=None, mes=None, anio=None):
    """
    Genera un archivo Excel con datos de ejemplo según el tipo de reporte especificado.
    
    Parámetros:
    - rbd: El RBD del establecimiento.
    - tipo_reporte: El tipo de reporte a generar (1: semanal, 2: mensual, 3: anual).
    - desde: La fecha de inicio (solo para tipo_reporte 1).
    - hasta: La fecha de fin (solo para tipo_reporte 1).
    - mes: El mes (solo para tipo_reporte 2).
    - anio: El año (solo para tipo_reporte 3).
    
    Retorna:
    - El nombre del archivo Excel generado.
    """
   
    Control_r = C_Registro()
    datos = Control_r.Reporte_General(rbd,desde,hasta,mes,anio,tipo_reporte)


    columnas = ["RUN", "Nombre", "Apellido", "Dias_Asistidos", "Dias_Completos"]
    df = pd.DataFrame(datos, columns=columnas)
    
    directorio = "Reportes/Reportes Generales"
    os.makedirs(directorio, exist_ok=True)
    
    detalles = ""
    if tipo_reporte == 1:
        detalles = f"_{limpiar_fecha(desde)}_al_{limpiar_fecha(hasta)}"
    elif tipo_reporte == 2:
        detalles = f"_{mes}"
    elif tipo_reporte == 3:
        detalles = f"_{limpiar_fecha(anio)}"
    
    nombre_archivo = f"{directorio}/ReporteGeneral_{tipo_reporte}{detalles}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    
    return nombre_archivo

class ReporteApp(QDialog):
    """
    Clase encargada de gestionar la interfaz para generar reportes generales.
    Permite al usuario seleccionar el tipo de reporte (semanal, mensual o anual) y generar un archivo Excel.
    """
    def __init__(self,rbd):
        """
        Constructor de la clase.
        Inicializa la interfaz para seleccionar el tipo de reporte y los campos necesarios según la opción seleccionada.
        
        Parámetros:
        - rbd: El RBD del establecimiento.
        """
        super().__init__()
        self.RBD = rbd
        self.setWindowTitle("Generar Reporte General")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Seleccione el tipo de reporte:")
        layout.addWidget(self.label)
        
        self.reporte_group = QButtonGroup(self)
        
        self.radio_semanal = QRadioButton("Reporte Semanal")
        self.radio_mensual = QRadioButton("Reporte Mensual")
        self.radio_anual = QRadioButton("Reporte Anual")
        
        self.reporte_group.addButton(self.radio_semanal)
        self.reporte_group.addButton(self.radio_mensual)
        self.reporte_group.addButton(self.radio_anual)
        
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
        
        layout.addWidget(self.radio_anual)
        
        self.hbox_anual = QHBoxLayout()
        self.label_anio_anual = QLabel("Año:")
        self.input_anio_anual = QLineEdit()
        self.hbox_anual.addWidget(self.label_anio_anual)
        self.hbox_anual.addWidget(self.input_anio_anual)
        layout.addLayout(self.hbox_anual)
        
        self.boton_generar = QPushButton("Generar")
        self.boton_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(self.boton_generar)
        
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.close)
        layout.addWidget(self.boton_cancelar)
        
        self.setLayout(layout)
    
    def generar_reporte(self):
        """
        Maneja la generación del reporte según la selección realizada por el usuario.
        Dependiendo del tipo de reporte seleccionado (semanal, mensual, anual),
        llama a la función correspondiente para generar el archivo Excel.
        """

        if self.radio_semanal.isChecked():
            tipo_reporte = 1
            desde = self.input_desde.text()
            hasta = self.input_hasta.text()
            archivo = generar_excel(self.RBD,tipo_reporte, desde=desde, hasta=hasta)
        elif self.radio_mensual.isChecked():
            tipo_reporte = 2
            mes = self.combo_mes.currentIndex()
            archivo = generar_excel(self.RBD,tipo_reporte, mes=mes)
        elif self.radio_anual.isChecked():
            tipo_reporte = 3
            anio = self.input_anio_anual.text()
            archivo = generar_excel(self.RBD,tipo_reporte, anio=anio)
        else:
            QMessageBox.warning(self, "Error", "Seleccione un tipo de reporte.")
            return
        
        QMessageBox.information(self, "Éxito", f"Reporte generado: {archivo}")
