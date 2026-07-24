1. metadata
Información técnica sobre el origen del archivo y el procesamiento realizado.
    source_channel
        Tipo: string
        Descripción: Canal por el cual ingresó la solicitud a la plataforma.
        Ejemplo: "WhatsApp"

    source_original_filename
        Tipo: String
        Descripción: Nombre original del documento.
        Ejemplo: "incidencia24.pdf"

    source_file_type
        Tipo: string
        Descripción: Formato original del contenido o documento analizado.
        Ejemplo: "image/jpeg"

    received_at
        Tipo: string (Formato ISO 8601 UTC)
        Descripción: Marca temporal de cuando el sistema de IA terminó de procesar el documento.
        Ejemplo: "2026-07-24T14:30:00Z"

    processed_at
        Tipo: string (Formato ISO 8601 UTC)
        Descripción: Marca temporal de cuando el sistema de IA terminó de procesar el documento.
        Ejemplo: "2026-07-24T14:30:00Z"

2. classification
Categorización automática de la solicitud para enrutamiento interno.

    request_type
        Tipo: string
        Descripción: Tipo principal de la solicitud identificada en la entrada.
        Ejemplo: "Incidencia de Tránsito"

    confidence_score
        Tipo: float (Rango de 0.0 a 1.0)
        Descripción: Nivel de certeza con el que el modelo clasificó la solicitud.
        Ejemplo: 0.95   

3. extracted_data
Información clave obtenida mediante markitdown/OCR estructurado.

    reference_id
        Tipo: string (o null si no se detecta)
        Descripción: Identificador único de guía, rastreo o número de pedido.
        Ejemplo: "MX-98234-LOG"

    customer
        Objeto que agrupa la información del remitente o cliente final.
        name
            Tipo: string (o null si no se detecta)
            Descripción: Nombre de la persona física que envía el mensaje, correo o reporte.
            Ejemplo: "Alan urbina"

        company
            Tipo: string (o null si no se detecta)
            Descripción: Razon social, marca o nombre comercial de la empresa cliente.
            Ejemplo: "Distribuidora del Norte S.A. de C.V."

    affected_units
        Tipo: list de string
        Descripción: Lista de placas, identificadores de contenedores o tractocamiones involucrados.
        Ejemplo: ["T-502", "REM-12"]

    key_entities
        Tipo: dictionary
        Descripción: Par clave-valor dinámico para almacenar datos adicionales relevantes no estandarizados (fechas, montos, ubicaciones).
        Ejemplo: {"origen": "Querétaro", "destino": "Laredo", "retraso_estimado": "3 horas"}

4. risk_and_priority
    Evaluación operativa para alertas tempranas y tiempos de respuesta.

    priority
        Tipo: string (Valores permitidos: "Alta", "Media", "Baja")
        Descripción: Nivel de prioridad asignado automáticamente según el impacto operativo o comercial.
        Ejemplo: "Alta"

    risk_category
        Tipo: string (o null si risk_detected es false. Valores permitidos: "Retraso Crítico", "Daño de Mercancía", "Seguridad/Robo", "Documentación Faltante", "Sin Riesgo")
        Descripción: Clasificación específica del riesgo identificado.
        Ejemplo: "Retraso Crítico"

5. executive_summary
    Síntesis clara para consumo rápido del equipo operativo.

    executive_summary
        Tipo: string
        Descripción: Resumen de 2 a 3 oraciones que describe la situación actual sin necesidad de leer todo el correo/documento original.
        Ejemplo: "El transporte T-502 con destino a Laredo reporta un bloqueo carretero en la carretera Mex-Qro. Presenta un retraso estimado de 3 horas, lo que pone en riesgo la ventana de entrega pactada para las 17:00 hrs."

6. recommended_action
    Guía paso a paso sobre lo que el operador debe realizar.

    action_type
        Tipo: string
        Descripción: Acción principal recomendada a ejecutar.
        Ejemplo: "Notificar_Cliente_y_Reprogramar"

    action_details
        Tipo: list de string
        Descripción: Pasos secuenciales sugeridos para resolver la incidencia o procesar la solicitud.
        Ejemplo:
            JSON
            [
            "Informar a la bodega receptora sobre la nueva hora estimada de llegada (20:00 hrs).",
            "Verificar con la aseguradora la activación del protocolo de monitoreo nocturno.",
            "Ajustar la ventana de cita en el portal de entregas."
            ]

7. proposed_response
    Respuesta redactada para el cliente final lista para aprobación/edición del humano (Human-in-the-loop).

    proposed_response
        Tipo: string
        Descripción: Borrador de mensaje comercial y empático listo para enviarse por correo o WhatsApp.
        Ejemplo: "Estimado cliente, confirmamos la recepción de su reporte respecto al embarque MX-98234-LOG. Nuestro equipo de monitoreo ya está dando seguimiento a la incidencia en la ruta Querétaro-Laredo. Le mantendremos informado sobre el nuevo horario estimado de arribo tan pronto la unidad reanude su trayecto. Saludos cordiales."
        
8. processing
    Métricas técnicas de telemetría y desempeño del modelo para monitoreo, auditoría y control de costos.

    model_used
        Tipo: string
        Descripción: Identificador específico del modelo de IA generativa que procesó la solicitud.
        Ejemplo: "gemini-1.5-flash"

    processing_time_ms
        Tipo: integer
        Descripción: Tiempo total invertido por la IA para analizar el archivo/texto y estructurar la respuesta, medido en milisegundos.
        Ejemplo: 1240

    tokens_input
        Tipo: integer
        Descripción: Cantidad total de tokens consumidos en el prompt de entrada (incluyendo texto, imágenes o documentos procesados).
        Ejemplo: 850

    tokens_output
        Tipo: integer
        Descripción: Cantidad total de tokens generados por el modelo en la respuesta JSON estructurada.
        Ejemplo: 310


EJEMPLO:
{
  "metadata": {
    "source_channel": "WhatsApp",
    "source_original_filename": "incidencia24.pdf"
    "source_file_type": "image/jpeg",
    "received_at": "2026-07-42T114:20:000"
    "processed_at": "2026-07-24T14:30:002"
  },
  "processing": {
    "model_used": "gemini-1.5-flash",
    "processing_time_ms": 1240,
    "tokens_input": 850,
    "tokens_output": 310
  },
  "classification": {
    "request_type": "Incidencia de Tránsito",
    "confidence_score": 0.95
  },
  "extracted_data": {
    "reference_id": "MX-98234-LOG",
    "customer": {
      "name": "Alan Urbina",
      "company": "Distribuidora del Norte S.A. de C.V."
    },
    "affected_units": ["T-502", "REM-12"],
    "key_entities": {
      "origen": "Querétaro",
      "destino": "Laredo",
      "retraso_estimado": "3 horas"
    }
  },
  "risk_and_priority": {
    "priority": "Alta",
    "risk_category": "Retraso Crítico"
  },
  "executive_summary": "El transporte T-502 con destino a Laredo reporta un bloqueo carretero en la carretera Mex-Qro. Presenta un retraso estimado de 3 horas, lo que pone en riesgo la ventana de entrega pactada para las 17:00 hrs.",
  "recommended_action": {
    "action_type": "Notificar_Cliente_y_Reprogramar",
    "action_details": [
      "Informar a la bodega receptora sobre la nueva hora estimada de llegada (20:00 hrs).",
      "Verificar con la aseguradora la activación del protocolo de monitoreo nocturno.",
      "Ajustar la ventana de cita en el portal de entregas."
    ]
  },
  "proposed_response": "Estimado cliente, confirmamos la recepción de su reporte respecto al embarque MX-98234-LOG. Nuestro equipo de monitoreo ya está dando seguimiento a la incidencia en la ruta Querétaro-Laredo. Le mantendremos informado sobre el nuevo horario estimado de arribo tan pronto la unidad reanude su trayecto. Saludos cordiales.",
}
