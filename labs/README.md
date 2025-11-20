# Fase 1.2 -- Tutoriales practicos (Resumen de entregables completados)

Esta fase tuvo como objetivo construir las bases tecnicas minimas para validar la integracion entre OpenAi, Odoo v17 y un Frontned Basico, mediante ejercicios practicos y de bajo riesgo, todo los isguiente ya fue completado exitosamente

## Ejercicio 1 -- Conexion basica a OpenAI

**Archivo:** [openai_basic_test.py](./openai_basic_test.py)
**Estado:** COmpletado

Logros tecnicos.

* Configuracion correcta de `openai` y `python.dotenv`
* Lectura de clave API desde `.env`
* Solicitud simple de texto `(client.response.create)`
* Recepcion e impresion de la respuesta en consola

**Resultado validado:**
OpenAI responde correctamente a PROMPTS simples → API Funcional

## Ejercicio 2 -- Crear lead en Odoo V17 via XML-RPC

**Archivo:** [odoo_service.py](../backend/odoo_service.py)
**Estado:** Compeltado

Logros tecnicos.

* Autenticacion correcta contra Odoo v17 usando XML-RPC
* Funcion `create_ead()` funcionando y probada
* Lead creada desde el Backend en Python
* Validacion con un ID real generado en la base de datos de Odoo

**Resultado Validado:**
Conexion estable y permisos correctos para crear registros desde Python

## Ejercicio 3 -- Widegt Web + Backend FastAPI / Chat local 

**Archivos:** 
1. [`index.html`](../web_client/index.html)
2. [`app.js`](../web_client/app.js)
3. [`server.py`](../backend/server.py)

**Estado:** Completado
**Logros tecnicos:** 

* Comunicacion full-stack validada:
  - Frontend → FastAPI → Odoo → FastAPI → Frontend
* Manejo correcto del body `JSON` y respuesta `JSON`
* Widget funcionando con mensajes y acciones reales
* Creacion de Leads desde el chatbot local en [index.html](../web_client/index.html) corriendo con Live Server o servicio basico de base de datos local

**Resultado validado:**
Integracion end-to-end funcional, sin errores

# Conclusion:

Las fase 1.2 queda completaemnte finalizada, con las tres pruebas tecnicas funcionando correctamente y validadas desde consola, navegador, terminal y Odoo

Todo el Stack necesario para avanzar al diseño de agentes esta probado

* OpenAI → *OK*
* Backend Python → *OK*
* XML-RPC Odoo → *OK*
* Frontend local → *OK*
* Flujo end-to-end → *OK*

# Fase 2 — Diseño funcional y técnico

## 2.1 Arquitectura Propuesta

- **2.1.1** Para visualizar la arquitectura propuesta, puede ingresar al [PDF](../assets/Diagrama%20de%20Arquitectura%20minima%20(Texto%20estructurado).pdf)

## 2.2 Entregable diagrama y justificacion de decisiones

1. **Widget frontend (HTML + CSS + JS)**
El chatbot se integra directamente en el sitio web de Odoo, mediante un Widget liviano en Javascript

Las razones principales son:

* Evita desarrollar un modulo Odoo completo, mas lento y costoso
* Permite despliegue rapido y pruebas en tiempo real
* El widget funciona de forma independiente del backend de Odoo, evitando bloquear el CMS o afectar la experiencia del visitante
* Facilita mantener el widget como elemento desechable o escalable segun avance del proyecto

**Decision:** Mantener la interfaz minima, sin UI compleja, para validad la funcionalidad real del agente

2. **Backend API (FastAPI + Python)**
Se utiliza un microservicio externo a Odoo por razones criticas

* Aisla y protege la API keys de OpenAi y Odoo
  Ninguna clave debe de existir en el Frontend o en codigo visible del navegador
* Permite logica avanzada
  - Sanitizacion de inputs
  - Envio del mensaje a OPenAI
  - Interpretacion de intencion
  - Llamadas controladas a Odoo
* Permite escalar o reemplazar componentes sin afectar a Odoo
* Evita sobrecargar la base de datos o Threads del servidor Odoo

**Decision:** FastAPI por su velocidad de procesamiento, asincronia nativa y facilidad de uso y de integracion con Python

3. **OpenAI Agent KIT (Modelo + Funciones)**
El agente gestiona la comprension del mensaje del usuario y decide cuando ejecutar acciones externas 

**Ventajas Claras**

* Permite entender intencion, incluso si el usuario escribe de forma ambigua
* Reduce la logica manual en el Backend
* Permite implementar funciones como:
  - [create_lead.py](../odoo_connector/create_lead.py)
  - [create_ticket.py](../odoo_connector/create_ticket.py)
  - [create_partner.py](../odoo_connector/create_partner.py)
  - [reade_leads.py](../odoo_connector/read_leads.py)
  - [read_partners.py](../odoo_connector/read_partners.py)
  - [test_connection.py](../odoo_connector/test_connection.py)
* Delegamos la "inteligencia conversacional" al modulo, manteninendo el Backend Simple

**Decision:** Usar AgentKIT para centralizar la comprension del lenguaje y la invocacion de mensajes

4. **Conexion a Odoo (CRM, Helpdesk, Contactos, etc, via XML-RPC)**
El backend se conecta  a la base de datos de Odoo Cement Design usando XML-RPC por que:

* Es la API oficial y soportada para el CRM
* Permite crear y leer Leads, Partners, Tickets para hacer busqueda de registros
* No requiere modificar el codigo de Odoo
* Funciona con accesos tecnicos de acceso limitado, garantizando seguridad

**Decision:** Exposicion minima de Odoo, con permisos reducidos y conexion exclusivamente desde el Backend

5. **Logs (Base de datos ligera - Opcional en esta version)**
La arquitectura contempla un registro de interacciones, pero no se implementa en la version *MVP* por motivos estrategicos

* **Prioridad:** Entregar resultados visibles y rapidos a gerencia
* No se desea mantener una base de datos adicional hasta validar el proyecto
* Menos infraestructura, permite detectar errores y corregir mas rapido

La base de losgs, solo se implementara cuando gerencia valide el compromiso con el proyecto

**Decision:** Mantener *Placholders* para logs, pero no implementarlos en la fase inicial

6. **Panel de Administracion (Opcional)**
Se considera opcional por estas razones

- Requiere diseño UI, autenticacion y mantenimiento adicional
- No genera valor inmediato para la validacion del proyecto
- Gerencia debe primeor vber el agente funcionando en Cement Design

Si mas adelante la empresa requiere metricas o data de visualziacion, se implementara como modulo adicional

**Decision:** No incluir panel en el MVP para evitar retrasos

7. **Flujo resultante**
La arquitectura final permite

  1. Cliente Escribe →
  2. Widget envia mensjae al Backend →
  3. Backendzanitiza, crea sessionID y envia a OpenAI
  4. Agente interpreta intencion
  5. Si aplica llama funciones a Odoo
  6. Backend responde al Widget
  7. Cliente recibe mensaje final

**Garantiza:**

* Seguridad
* Escalabilidad
* Simplicidad
* Aisalmiento entre frontend y la base de datos real
* Control total sobre las funciones que puede ejecutar la IA
