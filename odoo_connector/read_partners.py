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