# Odoo_connector/odoo_client.py
import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variable del archivo .env
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# 1 Autenticacion
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
print(f"Autenticado con UID: {uid}")

# 2 Conexion al endpoint de operaciones
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# 3 Crear un lead en el CRM
lead_data = {
    "name": "Prueba de integracion con AgentKit",
    "contact_name": "Juan Perez",
    "email_from": "juan.perez@example.com",
    "description": "Lead creado desde el conector Odoo-AgentKit",
    "priority": "2",
}

lead_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    "crm.lead", "create", [lead_data]
)

print(f"Lead creado con ID: {lead_id}")

