from Modelo.barra import Lectora_codigo_barras  # Importamos la clase

class ControladorLector:
    """
    Controlador para la gestión de la lectura y generación de códigos de barras y datos relacionados.
    Proporciona métodos para homogenizar datos y generar códigos únicos o de barras a través de la lectora.
    """
    def __init__(self):
        """
        Inicializa el controlador del lector de códigos de barras.
        Crea una instancia de la clase Lectora_codigo_barras.
        """
        self.lector = Lectora_codigo_barras()

    def homogenizar_run(self, run):
        """
        Homogeniza el RUN (Rol Único Nacional) proporcionado, ajustando el formato.
        
        Parámetros:
            run (str): El RUN a ser homogenizado.
        
        Retorna:
            str: El RUN homogenizado.

        Excepciones:
            ValueError: Si ocurre un error al intentar homogenizar el RUN.
        """
        try:
            run_homogenizado = self.lector.homogenizar_run(run)
            return run_homogenizado
        except ValueError as e:
            print(f"Error al homogeneizar RUN: {e}")

    def homogenizar_cadena(self, cadena):
        """
        Homogeniza la cadena de texto proporcionada.
        
        Parámetros:
            cadena (str): La cadena a ser homogenizada.
        
        Retorna:
            str: La cadena homogenizada.

        Excepciones:
            ValueError: Si ocurre un error al intentar homogenizar la cadena.
        """
        try:
            cadena_homogenizada = self.lector.homogenizar_cadena(cadena)
            return cadena_homogenizada
        except ValueError as e:
            print(f"Error al homogeneizar cadena: {e}")

    def generar_codigo_unico(self, codigo_escuela, codigo_persona):
        """
        Genera un código único utilizando los códigos de la escuela y de la persona.
        
        Parámetros:
            codigo_escuela (str): El código de la escuela.
            codigo_persona (str): El código de la persona.
        
        Retorna:
            str: El código único generado.

        Excepciones:
            ValueError: Si ocurre un error al generar el código único.
        """
        try:
            codigo_unico = self.lector.generar_codigo_unico(codigo_escuela, codigo_persona)
            return codigo_unico
        except ValueError as e:
            print(f"Error al generar código único: {e}")

    def generar_codigo_barras(self, contenido, archivo_salida):
        """
        Genera un código de barras a partir del contenido proporcionado y guarda el archivo generado.
        
        Parámetros:
            contenido (str): El contenido para el código de barras.
            archivo_salida (str): La ruta donde se guardará el archivo del código de barras.
        
        Retorna:
            str: El código completo generado.

        Excepciones:
            ValueError: Si ocurre un error al generar el código de barras.
        """
        try:
            codigo_completo = self.lector.generar_codigo_barras(contenido, archivo_salida)
            return codigo_completo
        except ValueError as e:
            print(f"Error al generar código de barras: {e}")