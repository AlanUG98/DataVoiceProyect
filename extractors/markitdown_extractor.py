from markitdown import MarkItDown

class AgenteDocumentos:
    def __init__(self):
        self.md = MarkItDown()

    def extraer_texto(self, ruta_archivo):
        try:
            # markitdown procesa el archivo y retorna un objeto de respuesta
            resultado = self.md.convert(ruta_archivo)
            
            # Devolvemos la propiedad text_content que contiene el string final
            return resultado.text_content
            
        except Exception as e:
            # Manejo básico de excepciones como en un try-catch de Java
            return f"Error al procesar el archivo con MarkItDown: {str(e)}"