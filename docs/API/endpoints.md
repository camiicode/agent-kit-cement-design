# POST `/chat`

**Porposito:**
Canaliza un mensaje del usaurio hacia el agente
Retorna la respuesta que luego el Frotned mostrara en el widget

### Request Json

```json
{
  "session_id": "sess_abc123",
  "message": "Quiero saber el estado de mi ticket",
  "metadata": {
    "site": "cementdesign.shop",
    "page": "/helpdesk",
    "language": "es",
  },
  "context": {
    "last_intent": "check_ticket_status",
    "memory": {},
  },
}
```

### Response Json

```json
{
  "reply": "Tu ticket 123456 esta actualmente en progreso. Ultima actualziacion: El equipo de soporte, añadio un comentario hace dos horas",
  "status": "success",
  "metadata": {
    "ticket_id": 123456
  }
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

