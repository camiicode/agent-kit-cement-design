import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

def get_odoo_models():
  common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
  uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {} )
  models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object") 
  return uid, models

def create_lead(name, email_from):
  uid, models, = get_odoo_models()
  lead_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'crm.lead', 'create',
    [{
      'name': name,
      'email_from': email_from,
    }]
  )
  return lead_id
