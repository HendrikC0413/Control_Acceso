from Modelo.registro import Registro

class R_Grupal(Registro):
    """
    Clase que representa un registro grupal. Hereda de la clase `Registro` y añade
    propiedades adicionales para gestionar los datos de los usuarios.
    """
    def __init__(self, run, completo,nombre,apellido,asistidos):
        """
        Constructor que inicializa un registro grupal con los detalles del grupo, incluyendo 
        el RUN, estado de completado, nombre, apellido y cantidad de asistidos.
        
        :param run: RUN del registro (identificador único).
        :param completo: Indica si el registro está completo o no.
        :param nombre: Nombre de la persona registrada.
        :param apellido: Apellido de la persona registrada.
        :param asistidos: Numero de dias asistidos
        """
        super().__init__(run, completo)
        self.NOMBRE = nombre
        self.APELLIDO = apellido
        self.ASISTIDOS = asistidos

    # Getters y Setters

    @property
    def NOMBRE(self):
        """ Devuelve el nombre registrado del usuario. """
        return self._NOMBRE

    @NOMBRE.setter
    def RBD(self, nombre):
        """ Establece el nombre del usuario """
        self._NOMBRE = nombre

    @property
    def APELLIDO(self):
        """ Devuelve el apellido registrado del usuario """
        return self._APELLIDO

    @APELLIDO.setter
    def APELLIDO(self, apelido):
        """ Establece el apellido del usuario """
        self._APELLIDO = apelido

    @property
    def ASISTIDOS(self):
        """ Devuelve el número dedias asistidos """
        return self._ASISTIDOS

    @ASISTIDOS.setter
    def ASISTIDOS(self, asistidos):
        """ Devuelve el número de dias asistidos """
        self._ASISTIDOS = asistidos
