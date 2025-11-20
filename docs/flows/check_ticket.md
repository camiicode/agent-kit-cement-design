# Flujo Conversacional — Consultar Estado de Ticket de Soporte

## 1. Introduccion del usuario

El usuario quiere conocer ele estado actualizado de un ticket de soporte previamente creado.
Puede expresar esta intencion de varias formas

* "¿Como va mi ticket?"
* "Quiero saber el estado de mi caso"
* "Ya hay avances en el ticket {ticket_id}"
* "Que han respondido en el ticket que abri?"

## 2. Objetivo del bot
Comprender el numero, referenica o ticket ID del ticket y consultar en Odoo su estado actual, comentarios recientes, actualziaciones de estados, y responsable/s asignado/s
Luego entregar un resumen claro y si aplica, notificar si el ticket esta bloqueado, resuelto o necesita procesos adicionales por parte del cliente o de la empresa

## 3. Informacion necesaria
Para poder consultar correctamente un ticket en Odoo, el bot debe de recopilar:

### 3.1 Numero o identificador del ticket
* Puede ser el ID interno, por ejemplo (12345)
* O el nombre/numero asignado, por ejemplo (54321)
* El bot debe de validar que el formato sea numerico o coincida con un nombre de ticket valido

### 3.2 Email del cliente (Si no se proporcina ID del ticket)
* Util para identificar los ultimos tickets asociados a un cliente
* Solo se pide si el usuario no tiene o no recuerda el numero del ticket

### 3.3  Confirmacion del usuario
* Si existen varios tickets asociados al cliente, pedir confirmacion:
  "Encontre estos tickets. ¿CUal desea consultar?

## 4. Mapa de dialogo (Estado → Mensaje → Accion en Odoo)
Este es el flujo conversacional paso a paso que seguira el bot

### Estado 0 - Inicio

**Usuario:** Quiero saber el estado de mi ticket
**Bot:** Claro, puedo ayudarte, ¿tienes el numero del ticket?

*Accion Odoo: Ninguna*

### Estado 1 - Usuario si tiene numero de ticket

**Usuario:** "Si, es el {tiket_id}"
**Bot:** 
  * Valida formato (Solo  numeros)
  * Busca en Odoo `helpdesk.ticket search_read.py`

**Si existe:** 
**Bot:** "El ticket {ticket_id} esta en estado {ticket_id_stage_id}. Ultima actualziacion: '{ticket_id_last_update}, ¿desea agregar un comentario?'"

**Si no existe:**
**Bot:** "No encuentro un ticket con ese numero. ¿Quieres verificar nuevamente, o prefieres hacer la consulta por medio de correo electronico?"

### Estado 2 - Usuario no tiene numero de ticket

**Usuario:** "No lo recuerdo"
**Bot:** "No hay problema ¿Podrias darme el correo con el que registraste el ticket?"

**Validacion:**
* Pedir correo valido (Regex simple)
* Si el usuario falla 2 veces → (Fallback)

**Accion Odoo:**
* Buscar tickets por el email del partner

**Si encuentra uno solo:**
**Bot:** "Encontre tu ticket con ID {ticket_id} -- {ticket_id_title} ¿Desea ver su estado?"

**Si encuentra varios (mas de 1):**
**Bot:** "Encontre estos tickets, ¿cual deseas consultar?"

{ticket_id_# - ticket_id_title}
{ticket_id_# - ticket_id_title}
{ticket_id_# - ticket_id_title}

**→ Pasa al estado 1, cuando usuario elige 1**

**Si no encuentraningun ticket asociado:**
**Bot:** "No encuentro ticket asociados a ese correo, ¿quiere crear uno?

### Estado 3 - Mostrar estado del ticket

**Bot consulta a Odoo:** campos `stage_id`, `description`, `last_update`, `user_id`

**Bot responde:**
"Tu ticket esta en estado {stage_id}, ultima actualizacion: {description}, responsable {user_id} ¿Deseas agregar un comentario?

### Estado 4 - usuario quiere ingresar comentario
**Usuario:** "Si, quiero decir que sigo esperando respuesta"
**Bot:** → `/helpdesk.ticket.message_post`

**Bot:**
"Listo he agregado el comentario a tu ticket, y se pondran en contacto tan pronto como sea posible"

### Fallbacks

**F1** -- Email Invalido 2 veces
**Bot:** "Parece que hay un problema con el correo. Te dejo este enlace para consultarlo manualmente. https://cementdesign.shop/my/tickets. ¿Te puedo colaborar en algo mas?"

**F2** -- Ticket no encontrado
**Bot:** -- "No puedo encontrar ese ticket. ¿desea crear uno nuevo?"


