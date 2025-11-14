# Odoo connector/read_leads.py
import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variable del archivo .env
load_dotenv()

# Conexion a Odoo
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD") 

# 1 Autenticacion
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
ui = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
print(f"Autentiticado con UID: {ui}")

# 2 Conexion al endpoint de operaciones
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# 1.0 Buscar los leads mas recientes (Ultimos 5)
leads = models.execute_kw(
  ODOO_DB, ui, ODOO_PASSWORD,
  "crm.lead", "search_read",

  # 1.1 Filtros para obtener todos los leads  
  [[]],  # Filtros vacíos para obtener todos los leads

  # 1.2 Parámetros adicionales
  {
    "fields": ["id", "name", "email_from", "priority", "user_id"], 
    "limit": 5,
    "order": "create_date desc"
  }
)

# 1.3 Mostrar los resultados en Consola
print(f"name: {leads}")
for lead in leads:
    print(f"- ID: {lead['id']} | {lead['name']} | {lead['email_from']} | Prioridad: {lead['priority']} | Comercial: {lead['user_id'][1] if lead['user_id'] else 'Sin asignar'}")