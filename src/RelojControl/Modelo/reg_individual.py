from Modelo.registro import Registro

class R_individual(Registro):
    """
    Clase que representa un registro individual de asistencia. Hereda de la clase `Registro` 
    y contiene atributos específicos para gestionar la entrada y salida de una persona, 
    incluyendo las horas de entrada, salida y colación, así como el identificador de tarjeta.
    """
    def __init__(self, run, completo,rbd,fecha,h_entrada,h_salida,hc_salida,hc_entrada,idTarjeta=None):
        """
        Constructor que inicializa un registro individual con los detalles de la persona registrada,
        incluyendo su hora de entrada, salida, y las horas de colación.
        
        :param run: RUN del registro (identificador único).
        :param completo: Indica si el registro está completo o no.
        :param rbd: Identificador del establecimiento o curso.
        :param fecha: Fecha del registro.
        :param h_entrada: Hora de entrada.
        :param h_salida: Hora de salida.
        :param hc_salida: Hora de salida para colación.
        :param hc_entrada: Hora de entrada de colación.
        :param idTarjeta: (Opcional) Identificador de la tarjeta asociada. Si no se proporciona, se asigna vacío.
        """
        super().__init__(run, completo)
        self.RBD = rbd
        self.FECHA = fecha
        self.HORA_ENTRADA = h_entrada
        self.HORA_SALIDA = h_salida
        self.HORA_SALIDA_COLACION = hc_salida
        self.HORA_ENTRADA_COLACION = hc_entrada
        if idTarjeta is None:
            self.TARJETA = ""
        else:
            self.TARJETA = idTarjeta

    # Getters y Setters

    @property
    def RBD(self):
        """ Devuelve el RBD registrado (identificador del establecimiento o curso). """
        return self._RBD

    @RBD.setter
    def RBD(self, rbd):
        """ Establece el RBD del registro individual. """
        self._RBD = rbd

    @property
    def FECHA(self):
        """ Devuelve la fecha del registro. """ 
        return self._FECHA

    @FECHA.setter
    def FECHA(self, fecha):
        """ Establece la fecha del registro. """
        self._FECHA = fecha

    @property
    def HORA_ENTRADA(self):
        """ Devuelve la hora de entrada registrada. """
        return self._HORA_ENTRADA

    @HORA_ENTRADA.setter
    def HORA_ENTRADA(self, h_entrada):
        """ Establece la hora de entrada del registro. """
        self._HORA_ENTRADA = h_entrada

    @property
    def HORA_SALIDA(self):
        """ Devuelve la hora de salida registrada. """
        return self._HORA_SALIDA

    @HORA_SALIDA.setter
    def HORA_SALIDA(self, h_salida):
        """ Establece la hora de salida del registro. """
        self._HORA_SALIDA = h_salida

    @property
    def HORA_SALIDA_COLACION(self):
        """ Devuelve la hora de salida para colación registrada. """
        return self._HORA_SALIDA_COLACION

    @HORA_SALIDA_COLACION.setter
    def HORA_SALIDA_COLACION(self, hc_salida):
        """ Establece la hora de salida para colación. """
        self._HORA_SALIDA_COLACION = hc_salida

    @property
    def HORA_ENTRADA_COLACION(self):
        """ Devuelve la hora de entrada de colación registrada. """
        return self._HORA_ENTRADA_COLACION

    @HORA_ENTRADA_COLACION.setter
    def HORA_ENTRADA_COLACION(self, hc_entrada):
        """ Establece la hora de entrada de colación. """
        self._HORA_ENTRADA_COLACION = hc_entrada
    
    @property
    def TARJETA(self):
        """ Devuelve el identificador de la tarjeta registrada. """ 
        return self._TARJETA  # Devuelve el atributo correcto

    @TARJETA.setter
    def TARJETA(self, idt):
        """ Establece el identificador de la tarjeta del registro. """
        self._TARJETA = idt  # Asigna al atributo privado