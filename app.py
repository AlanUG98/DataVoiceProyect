import os
import json
import streamlit as st
from dotenv import load_dotenv

# Importamos tu orquestador y la BD
from orchestrator.orchestrator import DocumentOrchestrator
from database.sqlite_manager import SQLiteManager

load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="Control de Incidencias Logísticas",
    page_icon="🚚",
    layout="wide"
)

# --- INICIALIZACIÓN DE COMPONENTES ---
@st.cache_resource
def obtener_orquestador():
    api_key = os.getenv("GOOGLE_API_KEY")
    return DocumentOrchestrator(api_key=api_key)

@st.cache_resource
def obtener_db():
    return SQLiteManager("database/base_datos.db")

orquestador = obtener_orquestador()
db = obtener_db()

# --- TÍTULO PRINCIPAL ---
st.title("🚚 Dashboard Operativo - Asistente Logístico Multimodal")
st.markdown("---")

# --- MAQUETA EN 2 COLUMNAS ---
col_izquierda, col_derecha = st.columns([1, 2])

# ==========================================
# COLUMNA IZQUIERDA: Carga de Archivos e Historial
# ==========================================
with col_izquierda:
    st.subheader("📄 Cargar Documento")
    
    # Uploader de archivos de Streamlit
    archivo_subido = st.file_uploader(
        "Selecciona un archivo (PDF, Imagen, Excel, Word):",
        type=['pdf', 'png', 'jpg', 'jpeg', 'xlsx', 'docx', 'csv']
    )
    
    if st.button("🚀 Procesar Documento", use_container_width=True):
        if archivo_subido is not None:
            with st.spinner("Procesando con MarkItDown..."):
                # 1. Guardamos temporalmente el archivo recibido en disk para el orquestador
                os.makedirs("data/input", exist_ok=True)
                temp_path = os.path.join("data/input", archivo_subido.name)
                
                with open(temp_path, "wb") as f:
                    f.write(archivo_subido.getbuffer())
                
                # 2. El Orquestador procesa y guarda en BD automáticamente
                resultado = orquestador.enrutar_y_procesar(temp_path)
                
                st.success("¡Documento procesado y registrado con éxito!")
                st.rerun() # Recarga la interfaz para actualizar el historial
        else:
            st.warning("Por favor selecciona un archivo primero.")

    st.markdown("---")
    st.subheader("📋 Historial de Registros")
    
    # Consulta a la base de datos
    registros = db.obtener_documentos()
    
    if registros:
        # Mostramos una tabla seleccionable
        import pandas as pd
        df = pd.DataFrame(registros)
        
        # Selección del documento a inspeccionar
        opciones = [f"ID {r['id']} - {r['tipo_documento']} ({r['prioridad']})" for r in registros]
        seleccion = st.selectbox("Selecciona un registro para ver el detalle:", opciones)
        
        # Extraemos el ID seleccionado
        id_seleccionado = int(seleccion.split(" ")[1])
    else:
        st.info("No hay documentos procesados aún en la base de datos.")
        id_seleccionado = None

# ==========================================
# COLUMNA DERECHA: Detalle e Inspección del Documento
# ==========================================
with col_derecha:
    st.subheader("🔍 Detalle del Análisis")
    
    if id_seleccionado:
        # Obtenemos el registro completo con su JSON parseado desde SQLite
        detalle_registro = db.obtener_documento(id_seleccionado)
        data_json = detalle_registro["json_resultado"]
        
        # 1. TARJETAS DE MÉTRICAS RÁPIDAS
        c1, c2, c3 = st.columns(3)
        c1.metric("Tipo de Solicitud", data_json.get("classification", {}).get("request_type", "N/A"))
        
        prio = data_json.get("risk_and_priority", {}).get("priority", "Media")
        c2.metric("Prioridad", prio)
        
        riesgo = data_json.get("risk_and_priority", {}).get("risk_category", "Sin Riesgo")
        c3.metric("Riesgo Detectado", riesgo)
        
        st.markdown("---")
        
        # 2. RESUMEN EJECUTIVO
        st.markdown("### 📝 Resumen Ejecutivo")
        st.info(data_json.get("executive_summary", "Sin resumen disponible."))
        
        # 3. ACCIONES RECOMENDADAS Y RESPUESTA PROPUESTA
        col_acc, col_resp = st.columns(2)
        
        with col_acc:
            st.markdown("### 🛠️ Acciones Recomendadas")
            acciones = data_json.get("recommended_action", {}).get("action_details", [])
            for paso in acciones:
                st.write(f"- {paso}")
                
        with col_resp:
            st.markdown("### 💬 Respuesta Propuesta al Cliente")
            st.success(data_json.get("proposed_response", "Sin propuesta de respuesta."))
            
        # 4. INSPECTOR JSON COMPLETO (Plegable)
        with st.expander("🛠️ Ver Contrato JSON Completo (Payload Raw)"):
            st.json(data_json)
            
    else:
        st.info("👈 Selecciona o procesa un documento a la izquierda para desplegar sus detalles aquí.")