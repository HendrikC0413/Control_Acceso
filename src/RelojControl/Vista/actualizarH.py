import sys
from PySide6.QtCore import Qt, QTimer, QTime, QThread, Signal,QDate,QLocale

class ActualizadorHora(QThread):
    """
    Clase encargada de actualizar la hora y la fecha actual de manera continua.
    Emite señales con la hora y la fecha actualizadas cada segundo.
    """
    """
    Señal que emite la hora actualizada en formato HH:mm:ss.
    """
    hora_actualizada = Signal(str)
    """
    Señal que emite la fecha actualizada en formato 'día de mes de año'.
    """
    fecha_actualizada = Signal(str)
    """
    Método principal que ejecuta un bucle infinito para actualizar la hora y la fecha cada segundo.
    Emite las señales correspondientes para la hora y la fecha actualizadas.
        
    """
    def run(self):
        """
        Método principal que ejecuta un bucle infinito para actualizar la hora y la fecha cada segundo.
        Emite las señales correspondientes para la hora y la fecha actualizadas.
        
        """
        locale = QLocale(QLocale.Spanish)
        while True:
            current_time = QTime.currentTime().toString("HH:mm:ss")
            current_date = locale.toString(QDate.currentDate(), "dddd dd 'de' MMMM yyyy")
            self.fecha_actualizada.emit(current_date.capitalize())  # Capitaliza la primera letra del día
            self.hora_actualizada.emit(current_time)
            self.msleep(1000)  # Esperar 1 segundo antes de actualizar