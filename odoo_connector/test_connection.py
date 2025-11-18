import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if uid:
  print(f"Conectado a Odoo. UID del usuario: {uid}")
else:
  print("¡Conexión fallida!")