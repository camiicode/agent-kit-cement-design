from backend.odoo_service import create_lead
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Modelo para recibir mensajes del Frontend
class ChatMessage(BaseModel):
    session_id: str | None = None
    message: str
    metadata: dict | None = None

app = FastAPI()

# Permitir solicitudes desde nuestro widget web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(data: ChatMessage):
    user_message = data.message
    
    print("=== Nueva interaccion recibida ===")
    print(f"Session ID: {data.session_id}")
    print(f"Mensaje del usuario: {data.message}")
    print(f"Metadata: {data.metadata}")
    print("===================================")

    # Validaciones minimas (Sanity - Checks)---------------------------------------------------------

    # Validacion de mensaje
    if not data.message or not isinstance(data.message, str):
        print("[WARN] El campo 'message' llego vacio o no es texto. Asignando mensaje generico.")
        user_message = "Mensaje no valido."
    else:
        user_message = data.message.strip()

    # Validacion de session id
    if data.session_id is not None and not isinstance(data.session_id, str):
        print("[WARN] 'session_id' llego en un formato no valido. Se ignorara")
        session_id = None
    else:
        session_id = data.session_id

    # Validacion de metadata
    if data.metadata is not None and not isinstance(data.metadata, dict):
        print("[WARN] 'metadata' debe de ser un diccionario. Ignorando metadata.")
        metadata = {}
    else:
        metadata = data.metadata or {}

    # Limpieza de metadata esperada
    allowed_metadata_keys = ["site", "page"]
    clean_metadata = {}

    for key in allowed_metadata_keys:
        value = metadata.get(key)
        if value and isinstance(value, str):
            clean_metadata[key] = value
        elif key in metadata:
            print(f"[WARN] metadata ['{key}'] no es texto. Se ignora.")

    print(f"Mensaje validado: {user_message}")
    print(f"Session id final: {session_id}")
    print(f"Metadata final: {clean_metadata}")
    #-------------------------------------------------------------------------------------------------
    
    
    # Respuesta simulada (aquí iría la lógica del chatbot)
    bot_reply = ""
    
    # 1. Detectar si el usuario quiere crear un lead
    if user_message.lower().startswith("crear lead"):
        # Formato Esperado
        # Crear lead: Nombre, Apellido | correo@example.com
        try:
            parts = user_message.split("|")
            client_name = parts[0].replace("Crear lead:", "").strip()
            client_email = parts[1].strip()

            lead_id = create_lead(client_name, client_email)
            bot_reply = f"Lead creado con ID: {lead_id}"
            
        except Exception as e:
            bot_reply = f"Error al crear el lead: {str(e)}"

    else:
        #  Respuesta por defecto del chatbot
        bot_reply = f"{user_message}"

    return {"response": bot_reply}
