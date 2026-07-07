class User:
    """
    Clase que representa un usuario en el sistema con su información personal, tipo de usuario, clave y huella dactilar.
    Esta clase permite acceder y modificar los detalles de un usuario, incluyendo su huella.
    """
    def __init__(self,run,nombre,apellido_1,apellido_2,id_tipo_usuario,clave,huella=None):
        """
        Inicializa un objeto User con los detalles personales del usuario, el tipo de usuario y la clave.
        
        :param run: Identificador único del usuario (generalmente RUT en algunos países).
        :param nombre: Nombre del usuario.
        :param apellido_1: Primer apellido del usuario.
        :param apellido_2: Segundo apellido del usuario.
        :param id_tipo_usuario: Identificador que define el tipo de usuario.
        :param clave: Clave de acceso del usuario.
        :param huella: Huella digital del usuario, se define como un bytearray vacío si no se proporciona.
        """
        self.RUN = run
        self.NOMBRE = nombre
        self.APELLIDO_1 = apellido_1
        self.APELLIDO_2 = apellido_2
        self.TIPO_USER = id_tipo_usuario
        self.CLAVE = clave
        if huella is None:
            self.HUELLA = bytearray()
        else:
            self.HUELLA = huella
    
    @property
    def RUN(self):
        """ Obtiene el RUN del usuario. """
        return self._RUN

    @RUN.setter
    def RUN(self, value):
        """ Establece el RUN del usuario. """
        self._RUN = value

    @property
    def NOMBRE(self):
        """ Obtiene el nombre del usuario. """
        return self._NOMBRE

    @NOMBRE.setter
    def NOMBRE(self, value):
        """ Establece el nombre del usuario. """
        self._NOMBRE = value

    @property
    def APELLIDO_1(self):
        """ Obtiene el primer apellido del usuario. """
        return self._APELLIDO_1

    @APELLIDO_1.setter
    def APELLIDO_1(self, value):
        """ Establece el primer apellido del usuario. """
        self._APELLIDO_1 = value

    @property
    def APELLIDO_2(self):
        """ Obtiene el segundo apellido del usuario. """
        return self._APELLIDO_2

    @APELLIDO_2.setter
    def APELLIDO_2(self, value):
        """ Establece el segundo apellido del usuario. """
        self._APELLIDO_2 = value

    @property
    def TIPO_USER(self):
        """ Obtiene el tipo de usuario. """
        return self._TIPO_USER

    @TIPO_USER.setter
    def TIPO_USER(self, value):
        """ Establece el tipo de usuario. """
        self._TIPO_USER = value

    @property
    def CLAVE(self):
        """ Obtiene la clave del usuario. """
        return self._CLAVE

    @CLAVE.setter
    def CLAVE(self, value):
        """ Establece la clave del usuario. """
        self._CLAVE = value

    @property
    def HUELLA(self):
        """ Obtiene la huella dactilar del usuario. """
        return self._HUELLA

    @HUELLA.setter
    def HUELLA(self, value):
        """ Establece la huella dactilar del usuario. """
        self._HUELLA = value