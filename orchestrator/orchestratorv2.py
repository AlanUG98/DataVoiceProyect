import os

from extractors.image_extractor import AgenteOCR
from extractors.markitdown_extractor import AgenteDocumentos

class DocumentOrchestrator:
    def __init__(self):
        self.agente_doc = AgenteDocumentos()
        self.agente_ocr = AgenteOCR()   
        self.formatos_doc = ('.pdf', '.xlsx', '.xls', '.docx', '.pptx', '.csv','.png', '.jpg', '.jpeg')

    def enrutar_y_procesar(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return f"Error: El archivo '{ruta_archivo}' no existe."

        # Identificar la extensión del archivo
        _, ext = os.path.splitext(ruta_archivo.lower())
        print(f"\n[Orquestador] Evaluando archivo: {ruta_archivo} (Ext: {ext})")

        print("[Orquestador] -> Enviando al módulo: mod_documentos")
        return self.agente_doc.extraer_texto(ruta_archivo)

# --- Simulación de ejecución ---
if __name__ == "__main__":
    orquestador = DocumentOrchestrator()

    archivo = r"data/input/archivoprueba1.pdf"
    #archivo =  r"data/input/imagenprueba1.png"

    resultado = orquestador.enrutar_y_procesar(archivo)

    #guardar el resultado
    outputfile = "data/output/"
    with open(outputfile + "salida.md", "w", encoding="utf-8") as save:
        save.write(resultado)
    #print(resultado)
