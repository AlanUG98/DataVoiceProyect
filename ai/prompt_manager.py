import os

class PromptManager:
    def __init__(self, path_system_prompt: str = "prompts/system_prompt.md", path_schema: str = "prompts/schema.json"):
        self.path_system_prompt = path_system_prompt
        self.path_schema = path_schema

    def _leer_archivo(self, ruta: str) -> str:
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Error en PromptManager: No se encontró el archivo en '{ruta}'")
            
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()

    def construir_prompt(self, document_content: str) -> str:
        system_prompt = self._leer_archivo(self.path_system_prompt)
        schema_json = self._leer_archivo(self.path_schema)

        prompt_ensamblado = system_prompt.replace("{JSON_SCHEMA_PLACEHOLDER}", schema_json)

        prompt_final = f"""{prompt_ensamblado}

---

# DOCUMENTO A ANALIZAR

{document_content}
"""
        return prompt_final