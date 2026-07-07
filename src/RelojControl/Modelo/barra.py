import hashlib
import os
import re
import barcode
from barcode.writer import ImageWriter


class Lectora_codigo_barras:

    """
    Clase que se encarga de homogeneizar códigos relacionados con RUNs y otros datos 
    para generar códigos únicos.
    """
    # Función para homogeneizar el RUN
    def homogenizar_run(self, run: str) -> str:  # Agregar 'self'
        """
        Función para homogeneizar el RUN. 
        Si el RUN termina en "K" precedido de un guion, reemplaza el guion por "0" 
        y elimina puntos y guiones del RUN.

        Args:
            run (str): RUN chileno a homogeneizar.
        
        Returns:
            str: RUN limpio sin puntos, guiones y con "K" reemplazado por "0" si es necesario.
        """
        # Si el RUN termina en "K" precedido de un guion, reemplazar el guion por "0"
        if run.endswith('-K'):
            run_limpio = run[:-2] + '0'  # Eliminar el guion y la K, y poner 0 en su lugar
            run_limpio = run_limpio.replace('.', '')
        else:
            # Si no termina con "K", solo quitar puntos y guión
            run_limpio = re.sub(r'[.-]', '',run)
        
        return run_limpio
    
    # Función para homogeneizar la cadena de texto de entre 4 y 7 caracteres con guion
    def homogenizar_cadena(self, cadena: str) -> str:  # Agregar 'self'
        """
        Función para homogeneizar la cadena de texto de entre 4 y 7 caracteres con guion.
        Asegura que la cadena tenga entre 4 y 7 caracteres y no tenga guiones ni puntos.

        Args:
            cadena (str): Cadena de texto a homogeneizar.
        
        Returns:
            str: Cadena limpia sin guiones ni puntos.
        
        Raises:
            ValueError: Si la cadena no tiene entre 4 y 7 caracteres.
        """
        # Asegurarse de que la cadena tenga entre 4 y 7 caracteres y tenga un guion
        if len(cadena) >= 4 and len(cadena) <= 7:
            # Reemplazar los puntos y guiones por "0"
            cadena_limpia = re.sub('-', '', cadena)
            return cadena_limpia
        else:
            raise ValueError("La cadena debe tener entre 4 y 7 caracteres.")
        
    def generar_codigo_unico(self, codigo_escuela, codigo_persona):
        """
        Función para generar un código único a partir de los códigos de escuela y persona.
        La entrada se concatena, se genera un hash SHA-256 y se reduce a 12 dígitos únicos.

        Args:
            codigo_escuela (str): Código de la escuela.
            codigo_persona (str): Código de la persona (RUN).

        Returns:
            str: Un código único de 12 dígitos.
        """
        # Paso 1: Concatenar los códigos

        codigo_escuela = self.homogenizar_cadena(codigo_escuela)  # Usar self
        codigo_persona = self.homogenizar_run(codigo_persona)  # Usar self
        entrada = f"{codigo_escuela}{codigo_persona}"
        
        # Paso 2: Generar un hash SHA-256 de la entrada
        hash_obj = hashlib.sha256(entrada.encode())
        hash_decimal = int(hash_obj.hexdigest(), 16)  # Convertir hash a entero
        
        # Paso 3: Reducir a 12 dígitos únicos
        codigo_unico = hash_decimal % (10**12)  # Asegurar que sea de 12 dígitos
        return str(codigo_unico).zfill(12)  # Rellenar con ceros si es necesario

    def generar_codigo_barras(self,contenido, archivo_salida):
        """
        Genera un código de barras EAN-13 y lo guarda como imagen en la carpeta 'Cod_Barras'.

        Args:
            contenido (str): Número que deseas codificar (debe tener 12 dígitos para EAN-13).
            archivo_salida (str): Nombre del archivo de salida sin extensión.

        Returns:
            str: Código EAN-13 completo (incluye el dígito verificador) si tiene éxito.
            None: Si ocurre un error.
        """
        try:
            # Verifica que el contenido sea válido para EAN-13
            if len(contenido) != 12 or not contenido.isdigit():
                raise ValueError("El contenido debe ser un número de 12 dígitos para EAN-13.")
            
            # Directorio donde se guardarán las imágenes
            directorio = "Cod_Barras"
            os.makedirs(directorio, exist_ok=True)

            # Ruta completa del archivo
            ruta_archivo = os.path.join(directorio, archivo_salida)

            # Crea el código de barras EAN-13
            codigo_barras = barcode.get('ean13', contenido, writer=ImageWriter())

            # Obtener el código EAN13 completo (incluye el dígito verificador)
            codigo_completo = codigo_barras.get_fullcode()

            # Guarda el código de barras como imagen en la carpeta Cod_Barras
            ruta_archivo_completa = codigo_barras.save(ruta_archivo)

            print(f"Código de barras generado y guardado en: {ruta_archivo_completa}")

            return codigo_completo
        except Exception as e:
            print(f"Error: {e}")
            return None
