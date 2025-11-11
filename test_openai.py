#test?openai.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variable from file .env
load_dotenv()

# Read the API Key from .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
  print("API Key not found. Please set the OPENAI_API_KEY environment variable.")
  exit()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Submit a request of test to the model
try:
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hola esto es una prueba desde Python"},
    ]
  )
  print("Conexion exitosa. Respuesta del modelo:")
  print(response.choices[0].message.content)

except Exception as e:
  print("Error al conectar con la API de OpenAI:")
  print(e)