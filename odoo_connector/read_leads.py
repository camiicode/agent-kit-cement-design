# Odoo connector/read_leads.py
import xmlrpc.client
import os
from dotenv import load_dotenv

# Cargar variable del archivo .env
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD") 

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
ui = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
print(f"Autentiticado con UID: {ui}")

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# # 1.0 Buscar los leads mas recientes (Ultimos 5)
# leads = models.execute_kw(
#   ODOO_DB, ui, ODOO_PASSWORD,
#   "crm.lead", "search_read",

#   # 1.1 Filtros para obtener todos los leads  
#   [[]],  # Filtros vacíos para obtener todos los leads

#   # 1.2 Parámetros adicionales
#   {
#     "fields": ["id", "name", "email_from", "priority", "user_id"], 
#     "limit": 5,
#     "order": "create_date desc"
#   }
# )

# # 1.3 Mostrar los resultados en Consola
# print(f"name: {leads}")
# for lead in leads:
#     print(f"- ID: {lead['id']} | {lead['name']} | {lead['email_from']} | Prioridad: {lead['priority']} | Comercial: {lead['user_id'][1] if lead['user_id'] else 'Sin asignar'}")

# 2.0 Busqueda de un contacto en especifico
partners = models.execute_kw(
  ODOO_DB, ui, ODOO_PASSWORD,

  # 2.1 Si quiero hacer la consulta de un cliente especifico ---
  "res.partner", "search_read",
  [
    [["email", "=", "cliente.prueba@example.com"]]
  ],

  # 2.2 Campos a retornar de este cliente en especifico
  {"fields": ["id", "name", "email"]}
)

# 2.3 Imprimimos el partner en cuestion
print(partners)