# POST `/chat`

**Porposito:**
Canaliza un mensaje del usaurio hacia el agente
Retorna la respuesta que luego el Frotned mostrara en el widget

### Request Json

```json
{
  "session_id": "abc123",
  "message": "Crear lead carlos@example.com",
  "metadata": {
    "page": "/contact",
    "site": "cementdesign.shop"
  }
}
```

### Response Json

```json
{
  "reply": "Lead  creado con ID 'abc123'",
  "status": "success"
}
```
# POST `/admin/logs` (Opcional)

**Proposito:**
Guardar interacciones para analisis posterior, metricas opanelinterno

### Request Json

```json
{
  "session_id": "abc123",
  "user_message": "Hola",
  "Bot_response": "Hola te habla desi, ¿como puedo ayudarte?",
  "timestamp": 123456789
}
```
### Response Json

```json
{
  "status": "stored"
}
```
# POST `/webhook/odoo`

**Porposito:**
Futuro: recibir notificacionesde odoo cuando un ticket cambie de estado

### Request json

```json
{
  "ticket_id": "abc123",
  "new_status": "En progreso",
  "updated_by": "Nombre de agente soporte",
  "timestamp": 1732041210
}
```

### Repsonse Json

```json
{ "status": "received" }
```

