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


        respuesta = response.choices[0].message.content
        respuesta_json = json.loads(respuesta)
        respuesta_json["processing"] = {
            "model_used": response.model,
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return respuesta_json