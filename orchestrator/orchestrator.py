import os
import json
from dotenv import load_dotenv
load_dotenv()


from extractors.image_extractor import AgenteOCR
from extractors.markitdown_extractor import AgenteDocumentos
from ai.prompt_manager import PromptManager
from ai.client import AIClient
from database.sqlite_manager import SQLiteManager

class DocumentOrchestrator:
    def __init__(self, api_key: str, db_path: str = "database/base_datos.db"):
        
        self.agente_doc = AgenteDocumentos()
        self.agente_ocr = AgenteOCR(api_key=api_key)  
        self.prompt_manager = PromptManager()
        self.ai_client = AIClient(api_key=api_key)
        self.db_manager = SQLiteManager(db_path=db_path)


        self.formatos_doc = ('.pdf', '.xlsx', '.xls', '.docx', '.pptx', '.csv')
        self.formatos_img = ('.png', '.jpg', '.jpeg')



    def enrutar_y_procesar(self, ruta_archivo, guardar_en_bd: bool = True):
        if not os.path.exists(ruta_archivo):
            return f"Error: El archivo '{ruta_archivo}' no existe."

        # Identificar la extensión del archivo
        _, ext = os.path.splitext(ruta_archivo.lower())
        print(f"\n[Orquestador] Evaluando archivo: {ruta_archivo} (Ext: {ext})")

        
        if ext in self.formatos_doc:
            print("Enviando al módulo: mod_documentos")
            texto_extraido = self.agente_doc.extraer_texto(ruta_archivo)
        elif ext in self.formatos_img:
            print("Enviando al módulo: mod_imagenes")
            texto_extraido = self.agente_ocr.extraer_texto(ruta_archivo)
        else:
            return f"Error: Formato '{ext}' no soportado."

        prompt = self.prompt_manager.construir_prompt(texto_extraido)
        respuesta = self.ai_client.analizar(prompt)

        if guardar_en_bd:
            print("[Orquestador] -> Guardando resultado en SQLite...")
            record_id = self.db_manager.guardar_documento(respuesta)
            print(f"[Orquestador] -> Exito! Registro guardado con ID: {record_id}")

        return respuesta

#main para pruebas
if __name__ == "__main__":
    API_KEY = os.getenv("GOOGLE_API_KEY")
    orquestador = DocumentOrchestrator(api_key=API_KEY)

    #archivo = r"data/input/archivoprueba1.pdf"
    archivo =  r"data/input/imagenprueba1.png"

    resultado = orquestador.enrutar_y_procesar(archivo, True)
    outputfile = "data/output/"
    with open(outputfile + "RespuestaIA.json", "w", encoding="utf-8") as save:
        json.dump(resultado, save, indent=4, ensure_ascii=False)