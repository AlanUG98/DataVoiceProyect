import os

class PromptManager:
    def __init__(self, path_system_prompt: str = "prompts/system_prompt.md", path_schema: str = "prompts/schema.json"):
        # Guardamos las rutas de las plantillas base
        self.path_system_prompt = path_system_prompt
        self.path_schema = path_schema

    def _leer_archivo(self, ruta: str) -> str:
        """Método helper (privado) para leer archivos de texto plano evitando duplicar código."""
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Error en PromptManager: No se encontró el archivo en '{ruta}'")
            
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()

    def construir_prompt(self, document_content: str) -> str:
        """
        Ensambla el System Prompt, el JSON Schema y el contenido a analizar.
        
        :param document_content: Texto extraído por los extractores/OCR
        :return: Prompt final completo listo para enviar a Gemini
        """
        # 1. Leemos los templates base
        system_prompt = self._leer_archivo(self.path_system_prompt)
        schema_json = self._leer_archivo(self.path_schema)

        # 2. Inyectamos el esquema en el placeholder
        prompt_ensamblado = system_prompt.replace("{JSON_SCHEMA_PLACEHOLDER}", schema_json)

        # 3. Concatenamos el contenido a analizar al final
        prompt_final = f"""{prompt_ensamblado}

---

# DOCUMENTO A ANALIZAR

{document_content}
"""
        return prompt_final