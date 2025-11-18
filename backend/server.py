from backend.odoo_service import create_lead
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Modelo para recibir mensajes del Frontend
class chatMessage(BaseModel):
    message: str

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
async def chat_endpoint(data: chatMessage):
    user_message = data.message
    print("Mensaje recibido:", user_message)
    
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
        bot_reply = f"Bot recibio: {user_message}"

    return {"response": bot_reply}
