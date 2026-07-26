import sqlite3
import json
from datetime import datetime

class SQLiteManager:
    def __init__(self, db_path: str = "data/base_datos.db"):
        self.db_path = db_path
        # Aseguramos que la tabla exista en cuanto se instancie la clase
        self.crear_bd()

    def _conectar(self):
        """Método helper (privado) para abrir conexión. Equivale a DriverManager.getConnection() en Java."""
        return sqlite3.connect(self.db_path)

    def crear_bd(self):
        """Crea la tabla si no existe."""
        query = """
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_procesado TEXT NOT NULL,
            tipo_documento TEXT,
            prioridad TEXT,
            resumen TEXT,
            json_resultado TEXT NOT NULL
        );
        """
        # Usamos 'with' para abrir/cerrar la conexión automáticamente (como try-with-resources en Java)
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def guardar_documento(self, resultado_json: dict) -> int:   
        
        json_str = json.dumps(resultado_json, ensure_ascii=False)

        # Extraemos los campos para las columnas directas (o asignamos None/null si fallan)
        fecha_actual = datetime.now()
        tipo_doc = resultado_json.get("classification", {}).get("request_type")
        prioridad = resultado_json.get("risk_and_priority", {}).get("priority")
        resumen = resultado_json.get("executive_summary")

        query = """
        INSERT INTO documentos (fecha_procesado, tipo_documento, prioridad, resumen, json_resultado)
        VALUES (?, ?, ?, ?, ?)
        """
        
        with self._conectar() as conn:
            cursor = conn.cursor()
            # En Python se usan '?' para los PreparedStatements en SQL (prevención de SQL Injection)
            cursor.execute(query, (fecha_actual, tipo_doc, prioridad, resumen, json_str))
            conn.commit()
            return cursor.lastrowid  # Retorna el ID generado para este registro

    def obtener_documentos(self) -> list:
        """Obtiene la lista completa de documentos para el Dashboard."""
        query = "SELECT id, fecha_procesado, tipo_documento, prioridad, resumen FROM documentos ORDER BY id DESC"
        
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            # cursor.fetchall() equivale a recorrer un ResultSet en Java y pasarlo a una List<Map>
            columnas = [column[0] for column in cursor.description]
            resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return resultados

    def obtener_documento(self, doc_id: int) -> dict:
        """Obtiene un documento específico con su JSON completo por ID."""
        query = "SELECT * FROM documentos WHERE id = ?"
        
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (doc_id,))
            row = cursor.fetchone()
            
            if row:
                columnas = [column[0] for column in cursor.description]
                registro = dict(zip(columnas, row))
                # Convertimos el String JSON almacenado de vuelta a Objeto/Diccionario
                registro["json_resultado"] = json.loads(registro["json_resultado"])
                return registro
            return None