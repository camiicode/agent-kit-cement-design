from odoo_service import create_lead
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import process_message_with_agent
import json

# Memoria temporal por sesión
session_store = {}

# Modelo para recibir mensajes del Frontend
class ChatMessage(BaseModel):
    session_id: str | None = None
    message: str
    metadata: dict | None = None

app = FastAPI()

@app.get("/chat/raw_test")
async def raw_test():
    return {
        "status": "ok",
        "message": "El backend está respondiendo correctamente."
    }

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

    # Validaciones minimas (Sanity - Checks)

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

    # Inicializar sesión si no existe
    if session_id not in session_store:
        session_store[session_id] = {
            "nombre": None,
            "email": None,
            "telefono": None,
            "ultimo_mensaje": None
        }

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

    session_store[session_id]["ultimo_mensaje"] = user_message
    
    # --------------------------------------------------------
    #   Llamar al agente inteligente (OpenAI, via agent.py)
    # --------------------------------------------------------
    
    try:
        raw_result = process_message_with_agent(user_message)

        # Limpieza de seguridad: remover backticks y etiquetas de código
        clean_json = raw_result.replace("```json", "").replace("```", "").strip()

        print("=== JSON LIMPIO DEL AGENTE ===")
        print(clean_json)
        print("================================")

        agent_data = json.loads(clean_json)
    except Exception as e:
        print("[ERROR] No se pudo procesar la respuesta del agente:", str(e))
        return {"response": "Error interno procesando tu mensaje."}
    
    # Actualizar la memoria con los datos nuevos recibidos
    if "datos" in agent_data:
        datos = agent_data["datos"]

        if datos.get("nombre"):
            session_store[session_id]["nombre"] = datos["nombre"]

        if datos.get("email"):
            session_store[session_id]["email"] = datos["email"]

        if datos.get("telefono"):
            session_store[session_id]["telefono"] = datos["telefono"]


    # Extraer campos del JSON generado por el agente
    intencion = agent_data.get("intencion")
    datos = agent_data.get("datos", {})
    respuesta_usuario = agent_data.get("respuesta_usuario", "Entendido.")

    # --------------------------------------------------------
    #   Accion 1 - Crear lead
    # --------------------------------------------------------

    if intencion == "crear_lead":
        nombre = session_store[session_id]["nombre"]
        email = session_store[session_id]["email"]
        telefono = session_store[session_id]["telefono"]


        # Validacion Cement Design: Nombre obligatorio
        if not nombre or nombre.strip() == "":
            return{"response": "Para continuar, necesito tu nombre completo, como te llamas?"}
        
        # Al menos un dato de contacto, ya sea un email o un numero de telefono
        email = session_store[session_id]["email"]
        telefono = session_store[session_id]["telefono"]

        email_ok = email and isinstance(email, str) and email.strip() != ""
        telefono_ok = telefono and str(telefono).strip() != ""

        if not email_ok and not telefono_ok:
            return {
                "response": "Para que un asesor pueda contactarte, es necesario al menos un dato de contacto. ¿Podrías darme tu correo o tu número de teléfono?"
            }
        
        lead_id = create_lead(
            name=nombre,
            email=email,
            message=datos.get("mensaje", user_message),
            phone=telefono
        )



        if not lead_id:
            return {"response": "Hubo un error creando tu registro. Por favor intenta más tarde."}

        return {"response": f"{respuesta_usuario}\n✔ Lead creado con ID: {lead_id}"}
    
    # --------------------------------------------------------
    #   Accion 2 - Consultar Ticket
    # --------------------------------------------------------

    if intencion == "consultar_ticket":
        ticket_id = datos.get("ticket_id")

        if not ticket_id:
            return {"response": "Necesito tu numero de ticket para revisarlo"}
        
        from odoo_service import check_ticket_status
        ticket_info = check_ticket_status(ticket_id)

        if not ticket_info:
            return{"response": f"no encontre informacion del ticket {ticket_id}"}
        
        return{"response": f"{respuesta_usuario}\n Estado del ticket {ticket_id}: {ticket_info}"}
    
    # --------------------------------------------------------
    #   Accion 2 - FAQ / Pregunta general
    # --------------------------------------------------------

    return{"response": respuesta_usuario}
