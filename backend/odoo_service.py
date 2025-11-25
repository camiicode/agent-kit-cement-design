# backend/odoo_service.py
import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================================
#   Cargar credenciales de Odoo desde variables de entorno
# =========================================================
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME") # svc_Agentkit
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD") # Contraseña segura del usuario tecnico

# =========================================================
#                   Conexion inicial a Odoo
# =========================================================
def get_uid():
  """Autentica y devuelve el UID del usuario tecnico."""
  try:
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    return uid
  except Exception as e:
    print(f"[ERROR] Error autenticaando en Odoo: {e}")
    return None
  
# =========================================================
#     Obtener el objeto "models" para hacer llamada RPC
# =========================================================
def get_models():
  return xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# =========================================================
#                   Crear LEAD en el CRM
# =========================================================
def create_lead(name, email, phone=None):
  """Crea un lead en Odoo. usado por el agente."""
  uid = get_uid()
  models = get_models()

  if not uid:
    return None
  
  try:
    lead_id = models.execute_kw(
      ODOO_DB, uid, ODOO_PASSWORD,
      'crm.lead', 'create',
      [{
        'name': name,
        'email_from': email,
        'phone': phone or '',
        "description": f"Lead creado por AgentKIT"
      }]
    )
    return lead_id
  
  except Exception as e:
    print(f"[ERROR] Error no se pudo crear el lead: {e}")
    return None

# =========================================================
#         Consultar estado de ticket de Helpdesk
# =========================================================
def check_ticket_status(ticket_id):
  """Consulte estado de ticket y comentarios"""
  uid = get_uid()
  models = get_models()

  try:
    data = models.execute_kw(
      ODOO_DB, uid, ODOO_PASSWORD,
      'helpdesk.ticket', 'search_read',
      [[["id", "=", ticket_id]]],
      {"fields": ["id", "name", "stage_id", "user_id", "description"]}
    )

    if not data:
      return None
    
    return data[0]
  
  except Exception as e:
    print(f"[ERROR] Error no se pudo consultar ticket: {e}")
    return None

# def get_odoo_models():
#   common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
#   uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {} )
#   models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object") 
#   return uid, models

# def create_lead(name, email_from):
#   uid, models, = get_odoo_models()
#   lead_id = models.execute_kw(
#     ODOO_DB, uid, ODOO_PASSWORD,
#     'crm.lead', 'create',
#     [{
#       'name': name,
#       'email_from': email_from,
#     }]
#   )
#   return lead_id
