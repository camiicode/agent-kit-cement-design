# Backend Agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Modelo latest recomendado por OpenAI
MODEL = "gpt-4.1-mini"

def process_message_with_agent(message: str):
  """
    Enviar el mensaje del usuario a OpenAI para que:
    - Entienda intención (crear lead, consultar ticket, FAQ, etc.)
    - Extraiga datos clave (nombre, email, ticket_id, etc.)
    - Devuelva la acción que debe realizar el backend
  """

  prompt = f"""
    Eres un agente para Cement Design. 
    Tu objetivo es clasificar el mensaje del usuario y devolver una intención clara.

    Si el usuario quiere crear un lead:
    - intención = "crear_lead"
    - extraer nombre, email y mensaje si están presentes.

    Si quiere consultar un ticket:
    - intención = "consultar_ticket"
    - extraer ticket_id si lo menciona.

    Si solo hace una pregunta general:
    - intención = "faq"

    Formato de respuesta SIEMPRE en JSON:

    {{
      "intencion": "...",
      "datos": {{
          "nombre": "...",
          "email": "...",
          "mensaje": "...",
          "ticket_id": "..."
      }},
      "respuesta_usuario": "Texto que enviaremos al usuario"
    }}

    Usuario dice: "{message}"
  """

  completion = client.response.create(
    model=MODEL,
    input=prompt,
    response_format={"type", "json_object"}
  )

  respuesta = completion.output_text
  return respuesta

