import os

from extractors.image_extractor import AgenteOCR
from extractors.markitdown_extractor import AgenteDocumentos

class DocumentOrchestrator:
    def __init__(self):
        self.agente_doc = AgenteDocumentos()
        self.agente_ocr = AgenteOCR()   
        self.formatos_doc = ('.pdf', '.xlsx', '.xls', '.docx', '.pptx', '.csv')
        self.formatos_img = ('.png', '.jpg', '.jpeg')



    def enrutar_y_procesar(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return f"Error: El archivo '{ruta_archivo}' no existe."

        # Identificar la extensión del archivo
        _, ext = os.path.splitext(ruta_archivo.lower())
        print(f"\n[Orquestador] Evaluando archivo: {ruta_archivo} (Ext: {ext})")

        #Agregar al README En una versión productiva estos mensajes serían gestionados mediante el módulo logging."
        # Decisiones del Orquestador
        if ext in self.formatos_doc:
            print("[Orquestador] -> Enviando al módulo: mod_documentos")
            return self.agente_doc.extraer_texto(ruta_archivo)
        elif ext in self.formatos_img:
            print("[Orquestador] -> Enviando al módulo: mod_imagenes")
            return self.agente_ocr.extraer_texto(ruta_archivo)
        else:
            return f"[Orquestador] -> Error: Formato '{ext}' no soportado."


