class Tipo_user:
    """
    Clase que representa un tipo de usuario en el sistema, con un identificador y una descripción.
    Esta clase permite acceder y modificar el id del tipo de usuario y su descripción.
    """
    def __init__(self, id, descripcion):
        """
        Inicializa un tipo de usuario con un identificador y una descripción.
        
        :param id: Identificador único del tipo de usuario.
        :param descripcion: Descripción detallada del tipo de usuario.
        """
        self.id_tipo_usuario = id
        self.descripcion = descripcion

    def get_id_tipo(self):
        """ Devuelve el id del tipo de usuario. """
        return self.id_tipo_usuario

    def set_id_tipo(self,id):
        """ Establece el id del tipo de usuario. """
        self.id_tipo_usuario = id

    def set_descripcion(self,desc):
        """ Establece la descripción del tipo de usuario. """
        self.descripcion = desc

    def get_descripcion(self):
        """ Devuelve la descripción del tipo de usuario. """
        return self.descripcion