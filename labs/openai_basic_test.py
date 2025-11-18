import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Inicializar cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# 3. Prompt simple para verificar funcionamiento
prompt = "Cuales son tus limitaciones actuales como modelo de lenguaje? y que puedo o no puedo testear contigo?"

# 4. Realizar la solicitud a la API de OpenAI
response = client.responses.create(
  model="gpt-4.1-mini",
  input=prompt
)

# 5. Imprimir la respuesta
print("\n Respuesta de OpenAI:")
print(response.output_text)

