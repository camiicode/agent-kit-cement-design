# odoo_connector/create_ticket.py
import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variable del archivo .env
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# Autenticación con Odoo
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
ui = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
print(f"Autentiticado con UID: {ui}")

# Conexión al modelo de objetos
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# Preparar los datos del ticket a crear
ticket_data = {
    "name": "Ticket de soporte de prueba con un AgentKit de OpenAI",
    "description": "Este es un ticket creado automáticamente para pruebas usando XML-RPC.",
    "partner_id": False, # ID del cliente (False si no aplica)
    "team_id": 1,  # ID del equipo de soporte
}

# Crear ticket en Odoo
ticket_id = models.execute_kw(
    ODOO_DB, ui, ODOO_PASSWORD,
    "helpdesk.ticket", "create",
    [ticket_data]
)

# Mostrar el ID del ticket creado
print(f"Ticket creado con ID: {ticket_id}")