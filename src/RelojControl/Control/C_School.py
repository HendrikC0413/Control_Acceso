from Modelo.DatabaseConnection import ConexionMySQL


class C_Escuela:
    """
    Clase encargada de gestionar las operaciones relacionadas con las escuelas.
    Permite agregar, modificar, eliminar y buscar escuelas en la base de datos.
    """

    def __init__(self):
        pass

    def agregar_escuela(self,rbd,nombre):
        """
        Agrega una nueva escuela a la base de datos utilizando el RBD y el nombre proporcionados.
        
        Parámetros:
        rbd (int): El RBD de la escuela a agregar.
        nombre (str): El nombre de la escuela a agregar.
        
        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
        realizado = False
        db = ConexionMySQL()
        db.ejecutar_procedimiento_insert("InsertarEscuela",(rbd,self.text_mayuscula(nombre)))
        realizado = True
        db.cerrar()
        return realizado

    def modificar_escuela(self,rbd,nombre):
        """
        Modifica los datos de una escuela en la base de datos utilizando el RBD y el nuevo nombre proporcionados.
        
        Parámetros:
        rbd (int): El RBD de la escuela a modificar.
        nombre (str): El nuevo nombre de la escuela.
        
        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
        realizado = False
        db = ConexionMySQL()
        db.ejecutar_procedimiento_update("ModificarEscuela",(1,rbd,self.text_mayuscula(nombre)))
        realizado = True
        db.cerrar()
        return realizado

    def eliminar_escuela(self,rbd):
        """
        Elimina una escuela de la base de datos utilizando el RBD proporcionado.
        
        Parámetros:
        rbd (int): El RBD de la escuela a eliminar.
        
        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
        realizado = False
        db = ConexionMySQL()
        db.ejecutar_procedimiento_update("ModificarEscuela",(2,rbd,None))
        realizado = True
        db.cerrar()
        return realizado

    def buscar_escuela(self,rbd):
        """
        Busca una escuela en la base de datos utilizando el RBD proporcionado.
        
        Parámetros:
        rbd (int): El RBD de la escuela a buscar.
        
        Retorna:
        str: El nombre de la escuela si se encuentra, una cadena vacía si no.
        """
        nombre = ""
        db = ConexionMySQL()
        resultado_proc = db.ejecutar_procedimiento("BuscarEscuelaPorRBD",(rbd,))

        if resultado_proc:   
            fila = resultado_proc[0][0]
            nombre =  str(fila.get("nombre_establecimiento")) if fila.get("nombre_establecimiento") else ""
        else:
            print("No se encontró el usuario.")
            nombre = ""

        db.cerrar()
        return nombre
    def text_mayuscula(self, Texto):
        """
        Convierte el texto proporcionado a mayúsculas.
        
        Parámetros:
        Texto (str): El texto que se desea convertir a mayúsculas.
        
        Retorna:
        str: El texto en mayúsculas.
        """
        return Texto.upper()