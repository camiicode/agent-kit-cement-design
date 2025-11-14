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
    bot_reply = f"Bot recibio: {user_message}"

    return {"response": bot_reply}