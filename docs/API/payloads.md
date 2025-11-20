#  Payloads

Este docuemnto define la estructura estandar de comunicacion entre:

* Widget Frontend
* Backend
* Agente KIT OpenAI
* (Opcional) Sistemas externo de Odoo

## Payload de entrada

```json
{
  "session_id": "string",
  "message": "string",
  "metadata": {
    "site": "string",
    "page": "string",
    "language": "string",
  },
  "context": {
    "last_intent": "string",
    "memory": "",
  },
}
```

### Descripcion de los campos

| Campo               | Tipo   | Obligatorio | Descripción                                    |
| ------------------- | ------ | ----------- | ---------------------------------------------- |
| session_id          | string | Sí          | Identificador único de la sesión del usuario   |
| message             | string | Sí          | Mensaje escrito por el usuario                 |
| metadata            | object | No          | Información sobre donde ocurre la conversación |
| metadata.site       | string | No          | Dominio del sitio                              |
| metadata.page       | string | No          | URL o ruta de la página actual                 |
| metadata.language   | string | No          | Idioma detectado                               |
| context             | object | No          | Memoria conversacional de la sesión            |
| context.last_intent | string | No          | Última intención detectada                     |
| context.memory      | object | No          | Datos transitorios de la conversación          |

## Payload de Salida (Backend → Frontend)

```json
{
  "reply": "string",
  "status": "success",
  "metadata": {
    "lead_id": 123456,
    "ticket_id": null,
  },
}
```
