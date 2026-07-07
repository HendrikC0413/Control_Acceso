class Registro:
    """
    Clase base que representa un registro con un identificador único (RUN) y un estado de completitud.
    Se utiliza para representar los registros básicos de una persona o entidad, y su estado de completitud.
    """
    def __init__(self,run,completo):
        """
        Inicializa un registro con un RUN (identificador único) y un estado de completitud.
        
        :param run: Identificador único del registro.
        :param completo: Estado del registro, indica si está completo o no.
        """
        self.RUN = run
        self.COMPLETO = completo

    # Getters y Setters
    
    @property
    def RUN(self):
        """ Devuelve el RUN del registro. """
        return self._RUN

    @RUN.setter
    def RUN(self, run):
        """ Establece el RUN del registro. """
        self._RUN = run

    @property
    def COMPLETO(self):
        """ Devuelve el estado de completitud del registro. """
        return self._COMPLETO

    @COMPLETO.setter
    def COMPLETO(self, completo):
        """ Establece el estado de completitud del registro. """
        self._COMPLETO = completo