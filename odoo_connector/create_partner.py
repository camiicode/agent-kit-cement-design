# Odoo Connector / create_partner.py
import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variable del archivo .env
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# 1. Autenticación
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
print(f"Autenticado con UID: {uid}")

# 2. Conexion al  endpoint del nuevo partner
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

partner_data = {
  "name": "Cliente de prueba creado con un Agente AI de OpenAI",
  "email": "cliente.de.prueba@example.com",
  "phone": "+34600123456",
  "company_type": "person", # Marcacion como "Individuo" no "Compañia"
  "comment": "Contacto creado desde un ambiente de pruebs de Python usando XML-RPC",
}

# 4. Crear el partner en Odoo
partner_id = models.execute_kw(
  ODOO_DB, uid, ODOO_PASSWORD,
  "res.partner", "create",
  [partner_data]
)

print(f"Nuevo partner creado con ID: {partner_id}")