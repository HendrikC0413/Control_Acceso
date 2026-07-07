from Vista.inicio import MainWindow


'''Inicio, abre la interfaz de la aplicación'''
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())