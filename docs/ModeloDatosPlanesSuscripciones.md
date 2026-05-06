# Modelo De Datos De Planes Y Suscripciones

## 1. Objetivo

Definir un modelo de datos exacto, coherente con Domain.md y ejecutable en Django para resolver:

- planes free y premium;
- suspension por impago sin perdida de datos;
- reactivacion de privilegios;
- downgrade de premium a free sin borrado;
- control de limites;
- estado excedido.

La recomendacion es mantener el modelo simple pero serio. No conviene empezar con demasiadas tablas si la regla puede resolverse mejor con una entidad clara y un servicio de dominio bien definido.

## 2. Recomendacion de entidades principales

Entidades recomendadas:

1. Plan
2. Subscription
3. BillingEvent opcional en primera iteracion
4. AuditLog

Entidades que no recomiendo persistir desde el dia 1 salvo necesidad real:

1. OverLimitState como tabla independiente
2. EntitlementSnapshot como tabla independiente
3. FeatureFlag por usuario salvo caso comercial real

La razon es simple: el estado efectivo del usuario puede calcularse correctamente a partir de su plan, su suscripcion y su uso real.

## 3. Modelo exacto recomendado

### 3.1 Plan

Responsabilidad:

Representa la oferta comercial y funcional aplicable a un usuario.

Campos recomendados:

- id
- code
- name
- tier
- is_active
- sort_order
- max_collections
- max_items_total
- max_storage_bytes
- can_upload_custom_images
- can_use_public_collections
- can_use_groups (boolean: permite crear grupos/subcolecciones dentro de colecciones)
- can_use_advanced_features
- created_at
- updated_at

Notas de diseño:

- code debe ser unico.
- tier puede ser free o premium al inicio, pero debe permitir crecer.
- los limites numericos deben admitir null solo si null significa ilimitado y esa regla queda muy clara.
- can_use_groups es false en free y true en premium. Si un usuario baja a free, sus grupos existentes se conservan pero no puede crear nuevos.

Constraints recomendados:

- unique code
- sort_order index
- check de limites no negativos

Ejemplo conceptual:

- FREE: 5 colecciones, 200 items totales, 200 MB, sin grupos, sin funciones avanzadas.
- PREMIUM: 100 colecciones, 5000 items totales, 5 GB, con grupos ilimitados por coleccion, con funciones avanzadas.

### 3.2 Subscription

Responsabilidad:

Representa la relacion temporal y economica entre un usuario y un plan con cobro o sin cobro.

Campos recomendados:

- id
- user
- plan
- status
- started_at
- current_period_start
- current_period_end
- grace_until opcional
- canceled_at opcional
- suspended_at opcional
- ended_at opcional
- auto_renew
- provider
- provider_customer_id opcional
- provider_subscription_id opcional
- external_reference opcional
- created_at
- updated_at

Estados recomendados:

- active
- suspended
- overdue o past_due si quieres distinguir impago pendiente de suspension efectiva
- canceled
- expired

Notas de diseño:

- un usuario debe tener una sola suscripcion efectiva activa o vigente a la vez para este producto.
- si usas historial completo, puedes tener varias filas historicas, pero solo una efectiva.
- el plan free puede resolverse sin fila de suscripcion o con una suscripcion free tecnica. Mi recomendacion inicial es esta:
  - free efectivo por ausencia de suscripcion premium activa;
  - plan free definido explicitamente en la tabla Plan.

Constraints recomendados:

- indice por user y status
- indice por provider_subscription_id
- validacion para no permitir multiples suscripciones activas simultaneas incompatibles

### 3.3 BillingEvent opcional

Responsabilidad:

Registrar eventos economicos o tecnicos de cobro sin mezclarlo con la logica de negocio principal.

Campos recomendados:

- id
- subscription
- user
- event_type
- amount
- currency
- provider
- provider_event_id
- status
- payload_reference o metadata minima
- occurred_at
- created_at

Usarlo cuando:

- integres pasarela real;
- necesites trazar pagos, reintentos, reembolsos o webhooks.

No usarlo todavia si:

- aun no existe cobro real;
- solo estas modelando premium de forma interna.

## 4. Estado efectivo del usuario

No recomiendo guardar un campo suelto como user.is_premium como verdad principal. Puede existir un cache o denormalizacion secundaria, pero la fuente de verdad debe ser una regla de dominio.

La regla recomendada es:

1. si existe suscripcion premium activa, el plan efectivo es el plan de esa suscripcion;
2. si la suscripcion premium esta suspendida, vencida o cancelada, el plan efectivo pasa a free;
3. los datos del usuario no cambian de propietario ni se borran;
4. solo cambian sus privilegios y sus limites efectivos.

## 5. Estado excedido

### Recomendacion principal

No crear tabla propia al inicio.

Calcular estado excedido mediante servicio de dominio usando:

- plan efectivo;
- numero actual de colecciones;
- numero actual de items;
- almacenamiento consumido;
- otras capacidades si las hubiera.

Salida esperada del servicio:

- is_over_limit
- exceeded_limits
- allowed_actions
- recommended_actions

Ejemplo conceptual:

- exceeded_limits = collections, storage
- allowed_actions = view_existing, edit_existing
- blocked_actions = create_collection, upload_image
- recommended_actions = reduce_usage, reactivate_premium

### Cuando si crear persistencia adicional

Solo si luego necesitas:

- paneles operativos complejos;
- alertas programadas;
- caches de rendimiento por volumen muy alto.

En esa situacion recomendaria una tabla materializada o cache, no la verdad principal del dominio.

## 6. Reglas exactas de negocio traducidas a modelo

### 6.1 Suspension por impago

Regla:

- la suscripcion cambia a suspended;
- el plan efectivo pasa a free o a un estado equivalente sin privilegios premium;
- los datos no se borran;
- las capacidades premium se bloquean;
- el evento se audita.

Efecto tecnico:

- no borrar colecciones;
- no borrar items;
- no borrar imagenes;
- no tocar ownership;
- bloquear altas incompatibles con el plan efectivo.

### 6.2 Reactivacion tras pago

Regla:

- la suscripcion vuelve a active;
- el plan efectivo vuelve a premium;
- el usuario recupera privilegios compatibles con el plan;
- no hace falta reconstruir datos.

Efecto tecnico:

- reabrir acciones premium;
- recalcular limites efectivos;
- auditar la reactivacion.

### 6.3 Downgrade de premium a free

Regla:

- el usuario pierde privilegios premium;
- conserva contenido existente;
- si supera limites free, entra en estado excedido;
- no puede seguir ampliando aquello que supera el plan free.

Efecto tecnico:

- bloquear nuevas colecciones si ya supera max_collections;
- bloquear nuevos items si ya supera max_items_total;
- bloquear nuevas subidas si supera max_storage_bytes;
- permitir consulta y gestion compatible de datos existentes.

## 7. Servicios de dominio recomendados

No toda esta logica debe vivir en modelos o vistas. Recomiendo como minimo estos servicios:

1. get_effective_plan_for_user(user)
2. get_current_subscription_for_user(user)
3. calculate_usage_for_user(user)
4. calculate_limit_state_for_user(user)
5. can_user_perform_action(user, action)
6. suspend_subscription_for_non_payment(subscription)
7. reactivate_subscription(subscription)
8. downgrade_user_to_free(user)

## 8. Acciones que deben bloquearse por estado

### Usuario premium activo

Permitido:

- usar limites premium;
- usar capacidades premium;
- crear contenido dentro del plan.

### Usuario suspendido por impago

Permitido:

- iniciar sesion;
- consultar contenido existente;
- editar lo que no viole politicas del producto si esa es la decision final.

Bloqueado:

- acciones premium;
- ampliaciones incompatibles con free o con el estado suspendido.

### Usuario free excedido

Permitido:

- consultar datos existentes;
- reducir contenido;
- reactivar premium.

Bloqueado:

- crear nuevas entidades que empeoren el exceso;
- subir nuevas imagenes si ya supera almacenamiento;
- usar funciones premium.

## 9. Auditoria minima obligatoria

Registrar como minimo:

- activacion de suscripcion;
- suspension por impago;
- reactivacion;
- cancelacion;
- downgrade a free;
- deteccion de estado excedido si impacta acciones del usuario;
- denegaciones relevantes por limite o plan.

## 10. Indices y rendimiento recomendados

### Plan

- unique index en code
- index en is_active y sort_order

### Subscription

- index en user
- index compuesto en user y status
- index en plan y status
- unique parcial para suscripcion activa por usuario si tu base y estrategia lo permiten
- index en provider_subscription_id

## 11. Decision recomendada final

La solucion mas limpia para empezar es esta:

1. tabla Plan como fuente de limites y capacidades;
2. tabla Subscription para historial y estado premium;
3. plan efectivo calculado por servicio;
4. estado excedido calculado por servicio, no por tabla propia al inicio;
5. auditoria obligatoria de todos los cambios de estado relevantes.

Con esto cubres bien el dominio, mantienes el modelo simple y evitas meter complejidad prematura sin renunciar a una base profesional.
