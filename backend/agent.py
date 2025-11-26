# backend/agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4.1-mini"

def process_message_with_agent(message: str):
    """
    Enviar el mensaje del usuario a OpenAI para que:
    - Detecte intención (lead, ticket, FAQ)
    - Extraiga datos relevantes
    - Devuelva instrucciones en JSON
    """

    prompt = f"""
Eres un agente conversacional para la empresa Cement Design.
Tu responsabilidad es identificar lo que el usuario necesita y devolver una intención clara.

### Reglas de clasificación:

1) CREAR LEAD (intencion = "crear_lead")
Solo aplica si el usuario expresa un interés comercial explícito:
- solicitar cotización
- pedir precios
- mostrar interés en un producto/servicio
- pedir contacto con ventas
- solicitar información comercial

No crees leads si el usuario solo hace preguntas generales o no comerciales.

Debe extraer si es posible:
- nombre
- email
- mensaje proporcionado

2) CONSULTAR TICKET (intencion = "consultar_ticket")
Aplica cuando el usuario menciona:
- número de ticket
- quiere saber el estado del soporte
- pregunta por un caso en Helpdesk

Extraer:
- ticket_id si lo menciona

3) FAQ / GENERAL (intencion = "faq")
Cualquier otra pregunta general, informativa o de conversación.

### Formato de salida (IMPORTANTE)
Siempre devolver JSON válido:
{{
  "intencion": "...",
  "datos": {{
      "nombre": "...",
      "email": "...",
      "mensaje": "...",
      "ticket_id": "..."
  }},
  "respuesta_usuario": "Texto final que enviaremos al usuario."
}}

Mensaje del usuario: "{message}"
"""

    completion = client.responses.create(
        model=MODEL,
        input=prompt,
        response_format={"type": "json_object"}
    )

    respuesta = completion.output[0].content[0].text
    return respuesta
