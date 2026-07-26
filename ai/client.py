from openai import OpenAI
import json

class AIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def analizar(self, prompt : str) -> str:
        response = self.client.chat.completions.create(
            model="gemini-flash-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # --- LOG PARA VER EL OBJETO COMPLETO ---
        print("\n=== [DEBUG] RESPUESTA COMPLETA DEL LLM ===")
        # .model_dump_json() convierte el objeto de la API en un texto JSON limpio
        print(json.dumps(json.loads(response.model_dump_json()), indent=4, ensure_ascii=False))
        print("==========================================\n")
        # ----------------------------------------

        respuesta = response.choices[0].message.content
        respuesta_json = json.loads(respuesta)
        return respuesta_json