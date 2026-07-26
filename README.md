# 🚚 DataVoice Project - Asistente Inteligente para Procesamiento de Documentos

## Descripción

Aplicación desarrollada en Python para automatizar el análisis de documentos mediante Inteligencia Artificial.

El sistema recibe documentos en distintos formatos, extrae su contenido utilizando la estrategia adecuada (MarkItDown u OCR), genera un análisis con Google Gemini y almacena el resultado estructurado para su consulta desde una interfaz web.

---

## Tecnologías utilizadas

- Python
- Google Gemini API
- MarkItDown
- SQLite
- Streamlit

---

## Funcionalidades

- Procesamiento de documentos PDF, imágenes y archivos de Office.
- Extracción automática de texto.
- Clasificación inteligente mediante IA.
- Generación de resumen ejecutivo.
- Identificación de prioridad y riesgo.
- Almacenamiento de resultados en SQLite.
- Visualización mediante Dashboard desarrollado con Streamlit.

---

## Arquitectura

El proyecto fue desarrollado siguiendo una arquitectura modular basada en responsabilidades únicas.

```
Documento
      │
      ▼
DocumentOrchestrator
      │
 ┌────┴────┐
 ▼         ▼
MarkItDown Markitdown + gemini
      │
      ▼
PromptManager
      │
      ▼
AIClient (Google Gemini)
      │
      ▼
SQLite
      │
      ▼
Dashboard (Streamlit)
```

Cada módulo es independiente, facilitando el mantenimiento y la escalabilidad del proyecto.

---

## Ejecución

1. Clonar el repositorio.

```bash
git clone https://github.com/AlanUG98/DataVoiceProyect.git
```

2. Instalar dependencias.

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env`.

```env
GOOGLE_API_KEY=TU_API_KEY
```

4. Ejecutar la aplicación.

```bash
streamlit run app.py
```

---

## Objetivo

El propósito del proyecto es demostrar el desarrollo de una solución completa para el procesamiento inteligente de documentos utilizando modelos de Inteligencia Artificial, manteniendo una arquitectura desacoplada y fácilmente extensible.