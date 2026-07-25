
from openai import OpenAI
from markitdown import MarkItDown

class AgenteOCR:
    def __init__(self, api_key: str):
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.md = MarkItDown(
            llm_client=client,
            llm_model="gemini-flash-latest"
        )

    def extraer_texto(self, ruta_archivo: str) -> str:
        try:
            resultado = self.md.convert(ruta_archivo)
            return resultado.text_content
        except Exception as e:
            return f"Error en AgenteOCR (MarkItDown + Gemini): {str(e)}"