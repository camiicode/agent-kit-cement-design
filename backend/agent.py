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
    Envía el mensaje del usuario a OpenAI para:
    - Detectar intención
    - Extraer datos
    - Devolver JSON con instrucciones
    """

    prompt = f"""
    
        Eres un agente conversacional para la empresa Cement Design.
        Tu responsabilidad es identificar lo que el usuario necesita y devolver una intención clara.

        ### Reglas de clasificación:

        1) CREAR LEAD (intencion = "crear_lead")
        Solo si el usuario muestra interés comercial:
        - cotización, precios, contacto de ventas, etc.

        2) CONSULTAR TICKET (intencion = "consultar_ticket")
        Si menciona ticket, soporte o número de caso.

        3) FAQ / GENERAL (intencion = "faq")
        Si no es comercial ni ticket.

        4) CONTEXTO Y MENSAJES DE SEGUIMIENTO
        Si el usuario previamente expresó intención de cotizar o interés comercial,
        y ahora envía datos (nombre, correo, teléfono, etc.), NO cambies la intención a "faq".

        Debes asumir que el usuario continúa el flujo de creación de lead.

        Ejemplos:
        - "Me llamo Juan Perez"
        - "Mi correo es juan@correo.com"
        - "Mi número es 310 xxx xxxx"

        En todos estos casos:
        → La intención debe permanecer "crear_lead".
        → Debes rellenar los campos faltantes.


        ### Formato de salida (JSON válido)
        {{
        "intencion": "...",
        "datos": {{
            "nombre": "...",
            "email": "...",
            "mensaje": "...",
            "ticket_id": "..."
        }},
        "respuesta_usuario": "Texto final para enviar al usuario."
        }}

        Mensaje: "{message}"
    """

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Debes responder SIEMPRE en JSON válido. "
                    "❗Prohibido usar bloques de código, backticks o etiquetas como ```json. "
                    "Responde SOLO con JSON puro sin formato adicional."
                )
            },
            {
                "role": "user",
                "content": prompt
            },
        ],

        temperature=0,
    )

    respuesta = completion.choices[0].message.content
    return respuesta
