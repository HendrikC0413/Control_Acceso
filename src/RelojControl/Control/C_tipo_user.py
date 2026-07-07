from  Modelo.DatabaseConnection import ConexionMySQL
from Modelo.tipo_usuario import Tipo_user

class C_tipo_usuario:
    """
    Clase que gestiona el acceso y manipulación de los tipos de usuarios en el sistema.
    Carga los tipos de usuarios desde la base de datos y proporciona los datos necesarios.
    """
    def __init__(self):
        """
        Inicializa la clase sin valores específicos.
        """
        self.id = None
        self.Desc = None
    
    def cargar_lista(self):
        """
        Carga la lista de tipos de usuario desde la base de datos.
        
        Realiza una consulta a la vista 'vista_tipo_usuario' en la base de datos y
        retorna una lista de objetos Tipo_user, que contienen el ID y la descripción de cada tipo de usuario.
        
        Retorna:
            list: Lista de objetos Tipo_user.
        """
        db = ConexionMySQL()
        tipos_empleado = []
        tipo_user = db.ejecutar_vista("controlacceso.vista_tipo_usuario")
        tipos_empleado = [Tipo_user(TU["idtipo_usuario"], TU["descripción_tipo"]) for TU in tipo_user]
        db.cerrar()
        return tipos_empleado
    